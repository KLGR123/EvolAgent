#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量分布分析和聚类可视化工具

该脚本从Qdrant向量数据库中获取向量数据，执行聚类分析，
并生成交互式可视化报告。支持多种聚类算法和降维方法。

主要功能：
- 从Qdrant数据库获取向量数据
- 数据预处理和清洗
- 聚类分析（KMeans, DBSCAN）
- 降维可视化（UMAP, t-SNE, PCA）
- 生成交互式HTML报告

作者: Assistant
版本: 2.2 (修正版)
"""

# =============================================================================
# 导入依赖
# =============================================================================

import os
import sys
import json
import time
import logging
import warnings
import collections
import multiprocessing as mp
from typing import Optional, Tuple, List, Dict, Any, Union
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import numpy.typing as npt
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from qdrant_client.http.exceptions import UnexpectedResponse

# 机器学习和数据处理
from sklearn.cluster import KMeans, DBSCAN, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import TSNE

# 可视化
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# 可选依赖
try:
    import umap
    from umap import UMAP
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP not available. Install with: pip install umap-learn")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =============================================================================
# 日志配置
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 抑制警告
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)  # 抑制sklearn数值计算警告

# =============================================================================
# 配置类
# =============================================================================

class Config:
    """配置类，集中管理所有配置参数"""
    
    # Qdrant连接配置
    COLLECTION_NAME = "developer_episodic"
    
    # 数据采样配置
    ENABLE_SAMPLING = True
    SAMPLE_SIZE = None  # None表示使用MAX_POINTS_FOR_VISUALIZATION
    RANDOM_SEED = 42
    MAX_POINTS_FOR_VISUALIZATION = 100000
    
    # 数据清洗配置
    ENABLE_DATA_CLEANING = True
    CLEAN_NON_FINITE_VALUES = True
    CLEAN_ZERO_VECTORS = True
    CLEAN_LOW_VARIANCE_FEATURES = False
    CLEAN_DIMENSION_INCONSISTENCY = True
    VARIANCE_THRESHOLD = 1e-8
    
    # 聚类配置
    CLUSTERING_METHOD = "dbscan"  # "kmeans" 或 "dbscan"
    AUTO_CLUSTER_DETECTION = True
    MAX_CLUSTERS = 15
    MIN_CLUSTERS = 2
    N_CLUSTERS = 8
    CLUSTER_DETECTION_METHOD = "silhouette"  # "elbow" 或 "silhouette"
    OUTLIER_DETECTION_ENABLED = True
    OUTLIER_METHOD = "distance_percentile"
    OUTLIER_PERCENTILE = 25
    OUTLIER_CONTAMINATION = 0.1
    
    # DBSCAN特定配置
    DBSCAN_EPS = None
    DBSCAN_MIN_SAMPLES = None
    DBSCAN_AUTO_PARAMS = True
    
    # 预处理配置
    ENABLE_PCA_PREPROCESSING = True
    PRE_REDUCTION = True
    PRE_PCA_COMPONENTS = 512
    PCA_VARIANCE_THRESHOLD = 0.95
    MAX_PCA_COMPONENTS = 100
    ENABLE_STANDARDIZATION = True
    ENABLE_L2_NORMALIZATION = True
    
    # 降维配置
    DIMENSION_REDUCTION_METHOD = "TSNE"  # "UMAP", "TSNE", "PCA" (推荐UMAP或PCA以进行参考点对比)
    OUTPUT_DIMENSIONS = 3
    UMAP_N_NEIGHBORS = 15
    UMAP_MIN_DIST = 0.1
    UMAP_METRIC = "cosine"
    TSNE_PERPLEXITY = 30
    TSNE_LEARNING_RATE = 200
    
    # 可视化配置
    VISUAL_EMBEDDING_SCALE = 0.7
    COLOR_PALETTE = "viridis"
    FIG_WIDTH = 800
    FIG_HEIGHT = 600
    MARKER_SIZE_2D = 13.5
    MARKER_SIZE_3D = 3
    POINT_SIZE = 3
    MARKER_OPACITY = 0.7
    POINT_OPACITY = 0.7
    SHOW_CLUSTER_CENTERS = True
    SHOW_OUTLIERS = True
    AXIS_TITLE_FONT_SIZE = 18
    AXIS_TICK_FONT_SIZE = 13
    PLOTLY_TEMPLATE = 'plotly_white'
    
    # 性能配置
    MAX_WORKERS = 4
    BATCH_SIZE = 1000
    MEMORY_LIMIT_GB = 8
    ENABLE_PARALLEL_PROCESSING = True
    USE_MINIBATCH_KMEANS = True
    EARLY_SAMPLE_SIZE = 3000
    ENABLE_PARALLEL = True
    N_JOBS = min(4, mp.cpu_count())
    
    # Basic overlay配置
    BASIC_OVERLAY_ENABLED = True
    BASIC_OVERLAY_COLLECTION = "developer_semantic"
    BASIC_OVERLAY_LIMIT = 5000
    BASIC_OVERLAY_COLOR = "#000000"
    BASIC_OVERLAY_SIZE = 2
    BASIC_OVERLAY_OPACITY = 0.8
    BASIC_MARKER_SIZE_BOOST = 2

# 创建配置实例
config = Config()

# =============================================================================
# 工具函数模块
# =============================================================================

class Utils:
    """工具函数类"""
    
    @staticmethod
    def validate_config(config_obj):
        """验证配置参数的合理性"""
        if config_obj.MIN_CLUSTERS < 2:
            logger.warning("MIN_CLUSTERS should be at least 2, adjusting to 2")
            config_obj.MIN_CLUSTERS = 2
        
        if config_obj.MAX_CLUSTERS <= config_obj.MIN_CLUSTERS:
            logger.warning("MAX_CLUSTERS should be greater than MIN_CLUSTERS, adjusting")
            config_obj.MAX_CLUSTERS = config_obj.MIN_CLUSTERS + 5
        
        if config_obj.PRE_PCA_COMPONENTS < 2:
            logger.warning("PRE_PCA_COMPONENTS should be at least 2, adjusting to 10")
            config_obj.PRE_PCA_COMPONENTS = 10
        
        if config_obj.OUTPUT_DIMENSIONS not in [2, 3]:
            logger.warning("OUTPUT_DIMENSIONS should be 2 or 3, defaulting to 2")
            config_obj.OUTPUT_DIMENSIONS = 2
        
        # 验证数据清洗配置
        if not config_obj.ENABLE_DATA_CLEANING:
            logger.info("Data cleaning is DISABLED - all vectors will be preserved")
            if not config_obj.CLEAN_NON_FINITE_VALUES and not config_obj.CLEAN_ZERO_VECTORS and not config_obj.CLEAN_LOW_VARIANCE_FEATURES and not config_obj.CLEAN_DIMENSION_INCONSISTENCY:
                logger.warning("All cleaning options are disabled. This may cause processing errors with invalid data.")
        else:
            logger.info("Data cleaning is ENABLED with the following options:")
            logger.info(f"  - Clean non-finite values: {config_obj.CLEAN_NON_FINITE_VALUES}")
            logger.info(f"  - Clean zero vectors: {config_obj.CLEAN_ZERO_VECTORS}")
            logger.info(f"  - Clean low variance features: {config_obj.CLEAN_LOW_VARIANCE_FEATURES}")
            logger.info(f"  - Clean dimension inconsistency: {config_obj.CLEAN_DIMENSION_INCONSISTENCY}")
    
    @staticmethod
    def safe_array_conversion(data, dtype=np.float32):
        """安全的数组转换，处理异常值"""
        try:
            if isinstance(data, dict):
                if 'dense' in data:
                    data = data['dense']
                elif 'vector' in data:
                    data = data['vector']
                else:
                    data = list(data.values())
            
            if isinstance(data, (list, tuple)) and len(data) > 0:
                if isinstance(data[0], dict):
                    processed_data = []
                    for item in data:
                        if isinstance(item, dict):
                            if 'dense' in item:
                                processed_data.append(item['dense'])
                            elif 'vector' in item:
                                processed_data.append(item['vector'])
                            else:
                                processed_data.append(list(item.values()))
                        else:
                            processed_data.append(item)
                    data = processed_data
            
            arr = np.array(data, dtype=dtype)
            
            if arr.ndim == 0 or (arr.ndim == 1 and arr.size == 0):
                logger.warning("Empty or scalar array encountered")
                return None
            
            if np.any(np.isnan(arr)) or np.any(np.isinf(arr)):
                logger.warning(f"Found {np.sum(np.isnan(arr))} NaN and {np.sum(np.isinf(arr))} inf values, replacing them.")
                arr = np.nan_to_num(arr, nan=0.0, posinf=float(np.finfo(dtype).max), neginf=float(np.finfo(dtype).min))
            
            return arr
        except Exception as e:
            logger.error(f"Array conversion failed: {e}")
            return None
    
    @staticmethod
    def calculate_clustering_metrics(labels, vectors):
        """计算聚类指标"""
        metrics = {}
        unique_labels = np.unique(labels)
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        n_outliers = np.sum(labels == -1) if -1 in unique_labels else 0
        
        metrics['n_clusters'] = n_clusters
        metrics['n_outliers'] = n_outliers
        metrics['outlier_ratio'] = n_outliers / len(labels) if len(labels) > 0 else 0
        
        if n_clusters >= 2 and len(vectors) > 0:
            try:
                non_outlier_mask = labels != -1
                if np.sum(non_outlier_mask) > 1:
                    filtered_labels = labels[non_outlier_mask]
                    filtered_vectors = vectors[non_outlier_mask]
                    
                    if len(np.unique(filtered_labels)) >= 2:
                        metrics['silhouette_score'] = silhouette_score(filtered_vectors, filtered_labels)
                        metrics['calinski_harabasz_score'] = calinski_harabasz_score(filtered_vectors, filtered_labels)
                        metrics['davies_bouldin_score'] = davies_bouldin_score(filtered_vectors, filtered_labels)
            except Exception as e:
                logger.warning(f"Failed to calculate clustering metrics: {e}")
        
        return metrics

# =============================================================================
# 数据获取模块
# =============================================================================

class DataFetcher:
    """数据获取类"""
    
    @staticmethod
    def fetch_data_from_qdrant_optimized(client, collection_name, max_points=None):
        """优化的数据获取函数"""
        logger.info(f"Fetching data from collection '{collection_name}'...")
        start_time = time.time()
        
        try:
            collection_info = client.get_collection(collection_name)
            total_points = collection_info.points_count
            
            if total_points == 0:
                logger.warning("Collection is empty")
                return np.array([]), np.array([])
            
            fetch_limit = min(max_points, total_points) if max_points is not None else total_points
            logger.info(f"Fetching {fetch_limit} points from {total_points} total points")
            
            response = client.scroll(
                collection_name=collection_name,
                limit=fetch_limit,
                with_vectors=True
            )
            
            all_vectors = [p.vector for p in response[0] if p.vector is not None]
            all_ids = [p.id for p in response[0] if p.vector is not None]
            
            if not all_vectors:
                logger.error("No vectors retrieved")
                return np.array([]), np.array([])
            
            vectors = Utils.safe_array_conversion(all_vectors, dtype=np.float32)
            ids = np.array(all_ids, dtype=object)
            
            elapsed_time = time.time() - start_time
            logger.info(f"Successfully fetched {len(vectors)} vectors in {elapsed_time:.2f}s")
            
            return vectors, ids
            
        except Exception as e:
            logger.error(f"Failed to fetch data from Qdrant: {e}")
            return np.array([]), np.array([])

    @staticmethod
    def fetch_basic_vectors(client, expected_dim=None):
        """获取basic overlay向量"""
        if not config.BASIC_OVERLAY_ENABLED:
            return None
        
        try:
            logger.info(f"Fetching basic overlay vectors from '{config.BASIC_OVERLAY_COLLECTION}'...")
            vectors, _ = DataFetcher.fetch_data_from_qdrant_optimized(
                client,
                config.BASIC_OVERLAY_COLLECTION,
                max_points=config.BASIC_OVERLAY_LIMIT
            )
            
            if vectors.shape[0] == 0:
                logger.warning(f"No basic vectors found in collection '{config.BASIC_OVERLAY_COLLECTION}'")
                return None
            
            if expected_dim is not None and vectors.shape[1] != expected_dim:
                logger.warning(f"Basic vector dimension mismatch: expected {expected_dim}, got {vectors.shape[1]}. Ignoring basic vectors.")
                return None

            logger.info(f"Successfully fetched {len(vectors)} basic vectors")
            return vectors
            
        except Exception as e:
            logger.warning(f"Failed to fetch basic vectors: {e}")
            return None

# =============================================================================
# 数据预处理模块
# =============================================================================

class DataPreprocessor:
    """数据预处理类"""
    
    class PreprocessingModel:
        """预处理模型类"""
        
        def __init__(self):
            self.pca = None
            self.scaler = None
            self.normalizer = None
            self.fitted = False
        
        def fit_transform(self, vectors):
            """拟合并转换向量"""
            result = vectors.copy()
            
            if config.ENABLE_PCA_PREPROCESSING and config.PRE_REDUCTION:
                n_components = min(config.PRE_PCA_COMPONENTS, vectors.shape[1], vectors.shape[0] - 1)
                if n_components > 1:
                    self.pca = PCA(n_components=n_components, random_state=config.RANDOM_SEED)
                    result = self.pca.fit_transform(result)
                    logger.info(f"PCA reduced dimensions from {vectors.shape[1]} to {result.shape[1]}")
            
            if config.ENABLE_STANDARDIZATION:
                self.scaler = StandardScaler()
                result = self.scaler.fit_transform(result)
            
            if config.ENABLE_L2_NORMALIZATION:
                self.normalizer = Normalizer(norm='l2')
                result = self.normalizer.fit_transform(result)
            
            self.fitted = True
            return result
        
        def transform_new(self, vectors):
            """转换新向量"""
            if not self.fitted:
                raise ValueError("Model must be fitted before transforming new data")
            
            result = vectors.copy()
            if self.pca is not None:
                result = self.pca.transform(result)
            if self.scaler is not None:
                result = self.scaler.transform(result)
            if self.normalizer is not None:
                result = self.normalizer.transform(result)
            
            return result

    @staticmethod
    def preprocess_with_pca_and_normalize(vectors):
        """使用PCA和归一化预处理向量，并返回模型"""
        try:
            model = DataPreprocessor.PreprocessingModel()
            processed_vectors = model.fit_transform(vectors)
            return processed_vectors, model # 返回处理后的向量和模型
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return vectors, None

# =============================================================================
# 聚类分析模块
# =============================================================================

class ClusterAnalyzer:
    """聚类分析类"""
    
    # ... (find_optimal_clusters_elbow_optimized, find_optimal_clusters_silhouette_fast, etc. 不需要修改)
    @staticmethod
    def find_optimal_clusters_elbow_optimized(vectors, max_clusters=None, min_clusters=2, sample_size=None):
        if max_clusters is None: max_clusters = config.MAX_CLUSTERS
        max_clusters = min(max_clusters, len(vectors) // 2)
        if max_clusters < min_clusters: return min_clusters
        sample_vectors = vectors[np.random.choice(len(vectors), sample_size, replace=False)] if sample_size and len(vectors) > sample_size else vectors
        inertias = []
        k_range = range(min_clusters, max_clusters + 1)
        for k in k_range:
            kmeans = MiniBatchKMeans(n_clusters=k, random_state=config.RANDOM_SEED, n_init='auto') if config.USE_MINIBATCH_KMEANS and len(sample_vectors) > config.BATCH_SIZE else KMeans(n_clusters=k, random_state=config.RANDOM_SEED, n_init='auto')
            kmeans.fit(sample_vectors)
            inertias.append(kmeans.inertia_)
        if len(inertias) < 3: return min_clusters
        second_diff = np.diff(np.diff(inertias))
        return k_range[np.argmax(second_diff) + 1] if len(second_diff) > 0 else min_clusters

    @staticmethod
    def find_optimal_clusters_silhouette_fast(vectors, max_clusters=None, min_clusters=2, sample_size=None):
        if max_clusters is None: max_clusters = config.MAX_CLUSTERS
        max_clusters = min(max_clusters, len(vectors) // 2)
        if max_clusters < min_clusters: return min_clusters
        sample_vectors = vectors[np.random.choice(len(vectors), sample_size, replace=False)] if sample_size and len(vectors) > sample_size else vectors
        best_score, best_k = -1, min_clusters
        for k in range(min_clusters, max_clusters + 1):
            labels = KMeans(n_clusters=k, random_state=config.RANDOM_SEED, n_init='auto').fit_predict(sample_vectors)
            score = silhouette_score(sample_vectors, labels)
            if score > best_score: best_score, best_k = score, k
        return best_k
    
    @staticmethod
    def perform_dbscan_clustering(vectors, eps=None, min_samples=None):
        # ... (此函数无需修改)
        if eps is None or min_samples is None:
            min_samples = max(2, int(np.log(len(vectors)))) if min_samples is None else min_samples
            if eps is None:
                sample_vectors = vectors[np.random.choice(len(vectors), 1000, replace=False)] if config.ENABLE_SAMPLING and len(vectors) > 1000 else vectors
                distances, _ = NearestNeighbors(n_neighbors=min_samples).fit(sample_vectors).kneighbors(sample_vectors)
                k_distances = np.sort(distances[:, min_samples - 1])
                eps = np.percentile(k_distances, 90)
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=config.N_JOBS)
        labels = dbscan.fit_predict(vectors)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        return labels, n_clusters

    @staticmethod
    def cluster_vectors_optimized(vectors):
        """优化的向量聚类函数"""
        if len(vectors) == 0:
            logger.error("No vectors to cluster"); return (None,) * 5
        
        logger.info(f"Starting clustering analysis on {len(vectors)} vectors...")
        
        # ... 数据清洗逻辑 ...
        original_count = len(vectors)
        if config.ENABLE_DATA_CLEANING:
            finite_mask = np.all(np.isfinite(vectors), axis=1)
            vectors = vectors[finite_mask]
            non_zero_mask = np.linalg.norm(vectors, axis=1) > 1e-10
            vectors = vectors[non_zero_mask]
            logger.info(f"Removed {original_count - len(vectors)} invalid vectors")
        
        if len(vectors) == 0:
            logger.error("No valid vectors remaining after cleaning"); return (None,) * 5

        # 预处理
        try:
            ### 已修改 ###
            processed_vectors, preprocessing_model = DataPreprocessor.preprocess_with_pca_and_normalize(vectors)
            if preprocessing_model is None: raise ValueError("Preprocessing model failed to initialize.")
            logger.info(f"Preprocessing completed. Shape: {processed_vectors.shape}")
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}"); return (None,) * 5

        # 执行聚类
        if config.CLUSTERING_METHOD.lower() == "dbscan":
            labels, n_clusters = ClusterAnalyzer.perform_dbscan_clustering(processed_vectors, config.DBSCAN_EPS, config.DBSCAN_MIN_SAMPLES)
        else: # KMeans
            optimal_k = config.N_CLUSTERS
            if config.AUTO_CLUSTER_DETECTION:
                find_func = ClusterAnalyzer.find_optimal_clusters_silhouette_fast if config.CLUSTER_DETECTION_METHOD == "silhouette" else ClusterAnalyzer.find_optimal_clusters_elbow_optimized
                optimal_k = find_func(processed_vectors, config.MAX_CLUSTERS, config.MIN_CLUSTERS, config.EARLY_SAMPLE_SIZE)
            
            kmeans_cls = MiniBatchKMeans if config.USE_MINIBATCH_KMEANS and len(processed_vectors) > config.BATCH_SIZE else KMeans
            kmeans = kmeans_cls(n_clusters=optimal_k, random_state=config.RANDOM_SEED, n_init='auto')
            labels = kmeans.fit_predict(processed_vectors)
            n_clusters = optimal_k

        if labels is None:
            logger.error("Clustering failed"); return (None,) * 5

        # ... (离群点检测逻辑无需修改)
        if config.OUTLIER_DETECTION_ENABLED and config.CLUSTERING_METHOD.lower() == "kmeans":
            cluster_centers = np.array([processed_vectors[labels == i].mean(axis=0) for i in range(n_clusters)])
            distances = np.linalg.norm(processed_vectors - cluster_centers[labels], axis=1)
            threshold = np.percentile(distances, 100 - config.OUTLIER_PERCENTILE)
            labels[distances > threshold] = -1

        kept_indices = np.arange(len(labels))
        ### 已修改 ###
        return labels, n_clusters, processed_vectors, kept_indices, preprocessing_model


# =============================================================================
# 降维可视化模块
# =============================================================================

class DimensionReducer:
    """降维处理类"""
    
    @staticmethod
    def reduce_dimensions_optimized(vectors, method="UMAP", n_components=2, return_reducer=False): ### 已修改 ###
        """优化的降维函数"""
        if len(vectors) == 0:
            logger.error("No vectors to reduce"); return (None, None) if return_reducer else None
        
        logger.info(f"Reducing dimensions using {method} to {n_components}D...")
        reducer, reduced = None, None
        
        try:
            if method.upper() == "UMAP":
                if not UMAP_AVAILABLE:
                    logger.warning("UMAP not available, falling back to t-SNE"); method = "TSNE"
                else:
                    reducer = UMAP(n_components=n_components, n_neighbors=config.UMAP_N_NEIGHBORS, min_dist=config.UMAP_MIN_DIST, metric=config.UMAP_METRIC, random_state=config.RANDOM_SEED, n_jobs=1)
                    reduced = reducer.fit_transform(vectors)

            if method.upper() == "TSNE":
                if vectors.shape[1] > 50 and len(vectors) > 1000:
                    vectors = PCA(n_components=50, random_state=config.RANDOM_SEED).fit_transform(vectors)
                perplexity = min(config.TSNE_PERPLEXITY, (len(vectors) - 1) // 3)
                reducer = TSNE(n_components=n_components, perplexity=perplexity, learning_rate=config.TSNE_LEARNING_RATE, random_state=config.RANDOM_SEED, n_jobs=1)
                reduced = reducer.fit_transform(vectors)
                # t-SNE不支持独立的transform，所以返回的reducer为None
                if return_reducer: reducer = None

            if method.upper() == "PCA":
                reducer = PCA(n_components=n_components, random_state=config.RANDOM_SEED)
                reduced = reducer.fit_transform(vectors)
            
            if reduced is None:
                logger.error(f"Unknown dimension reduction method: {method}")
                return (None, None) if return_reducer else None
            
            reduced = reduced * config.VISUAL_EMBEDDING_SCALE
            logger.info(f"{method} reduction completed.")
            
            ### 已修改 ###
            return (reduced, reducer) if return_reducer else reduced

        except Exception as e:
            logger.error(f"Dimension reduction failed: {e}")
            return (None, None) if return_reducer else None


# =============================================================================
# 可视化模块
# =============================================================================

class Visualizer:
    """可视化类"""
    
    @staticmethod
    def create_visualization(reduced_vectors, cluster_labels, metrics, collection_name, basic_reduced=None):
        """创建可视化图表"""
        logger.info("Creating visualization...")
        
        df_data = {'x': reduced_vectors[:, 0], 'y': reduced_vectors[:, 1], 'cluster': cluster_labels.astype(str)}
        if reduced_vectors.shape[1] >= 3:
            df_data['z'] = reduced_vectors[:, 2]
        df = pd.DataFrame(df_data)

        is_3d = config.OUTPUT_DIMENSIONS == 3 and 'z' in df.columns
        scatter_func = px.scatter_3d if is_3d else px.scatter
        
        fig = scatter_func(
            df, x='x', y='y', z='z' if is_3d else None,
            color='cluster',
            title=f'Vector Distribution - {collection_name}',
            color_discrete_sequence=px.colors.qualitative.Set3,
            template=config.PLOTLY_TEMPLATE
        )
        
        marker_size = config.MARKER_SIZE_3D if is_3d else config.MARKER_SIZE_2D
        fig.update_traces(marker=dict(size=marker_size, opacity=config.MARKER_OPACITY))
        
        if basic_reduced is not None and len(basic_reduced) > 0:
            trace_func = go.Scatter3d if is_3d else go.Scatter
            trace_data = {
                'x': basic_reduced[:, 0],
                'y': basic_reduced[:, 1],
                'mode': 'markers',
                'marker': dict(
                    color=config.BASIC_OVERLAY_COLOR,
                    size=marker_size * config.BASIC_MARKER_SIZE_BOOST,
                    opacity=config.BASIC_OVERLAY_OPACITY
                ),
                'name': 'Basic Overlay'
            }
            if is_3d:
                trace_data['z'] = basic_reduced[:, 2] if basic_reduced.shape[1] >= 3 else np.zeros(len(basic_reduced))
            
            fig.add_trace(trace_func(**trace_data))
        
        title_text = f"Vector Distribution - {collection_name}<br>Clusters: {metrics.get('n_clusters', 0)}, Outliers: {metrics.get('n_outliers', 0)}"
        if metrics.get('silhouette_score') is not None:
            title_text += f", Silhouette: {metrics['silhouette_score']:.3f}"
        
        fig.update_layout(title_text=title_text, width=config.FIG_WIDTH, height=config.FIG_HEIGHT)
        return fig

    # generate_html_report 函数无需修改，它会接收并正确处理图表对象
    @staticmethod
    def generate_html_report(fig, metrics, original_count, analyzed_count, total_time, collection_name, vector_dim, **kwargs):
        """生成HTML报告"""
        fig_html = fig.to_html(include_plotlyjs='cdn', div_id='main-plot') if fig else "<p>Visualization failed.</p>"
        stats = {
            'collection': collection_name, 'total_vectors': f"{original_count:,}", 'analyzed_vectors': f"{analyzed_count:,}",
            'vector_dimension': vector_dim, 'clusters_found': metrics.get('n_clusters', 0),
            'outliers': f"{metrics.get('n_outliers', 0)} ({metrics.get('outlier_ratio', 0):.1%})",
            'processing_time': f"{total_time:.2f}s",
            'silhouette_score': f"{metrics.get('silhouette_score', 'N/A'):.3f}" if isinstance(metrics.get('silhouette_score'), float) else 'N/A'
        }
        
        stats_html = "".join([f'<div class="stat-card"><div class="stat-title">{title.replace("_", " ").title()}</div><div class="stat-value">{value}</div></div>' for title, value in stats.items()])
        
        return f"""
<!DOCTYPE html><html><head><title>Vector Analysis - {collection_name}</title><meta charset="utf-8">
<style>
    body{{font-family:Arial,sans-serif;margin:20px;background-color:#f5f5f5}} .container{{max-width:1200px;margin:0 auto;background-color:white;padding:20px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}}
    .header{{text-align:center;margin-bottom:30px;padding-bottom:20px;border-bottom:2px solid #eee}} .stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-bottom:30px}}
    .stat-card{{background-color:#f8f9fa;padding:15px;border-radius:8px;border-left:4px solid #007bff}} .stat-title{{font-weight:bold;color:#333;margin-bottom:5px}} .stat-value{{font-size:1.2em;color:#007bff}}
    .visualization{{margin:20px 0;text-align:center}} .footer{{margin-top:30px;padding-top:20px;border-top:2px solid #eee;text-align:center;color:#666;font-size:0.9em}}
</style></head><body><div class="container"><div class="header"><h1>Vector Distribution Analysis</h1><h2>{collection_name}</h2><p>Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}</p></div>
<div class="stats-grid">{stats_html}</div><div class="visualization"><h3>Interactive Visualization</h3>{fig_html}</div>
<div class="footer"><p>Generated by Vector Distribution Analysis Tool v2.2</p><p>Configuration: {config.DIMENSION_REDUCTION_METHOD} + {config.CLUSTERING_METHOD.upper()}</p></div></div></body></html>
"""

# =============================================================================
# 主程序模块
# =============================================================================

def main():
    """主函数"""
    logger.info("Starting vector distribution analysis...")
    total_start_time = time.time()
    
    try:
        Utils.validate_config(config)
        client = QdrantClient(path="qdrant")
        logger.info("Connected to Qdrant successfully")
        
        vectors, ids = DataFetcher.fetch_data_from_qdrant_optimized(client, config.COLLECTION_NAME)
        if len(vectors) == 0:
            logger.error("No vectors retrieved. Exiting."); return
        
        original_vector_count = len(vectors)
        vector_dim = vectors.shape[1]
        
        analysis_vectors = vectors
        analysis_ids = np.asarray(ids)
        if config.ENABLE_SAMPLING and len(vectors) > config.MAX_POINTS_FOR_VISUALIZATION:
            logger.info(f"Sampling {config.MAX_POINTS_FOR_VISUALIZATION} vectors...")
            indices = np.random.choice(len(vectors), config.MAX_POINTS_FOR_VISUALIZATION, replace=False)
            analysis_vectors, analysis_ids = vectors[indices], ids[indices]
        
        logger.info(f"Analyzing {len(analysis_vectors)} vectors")
        
        ### 已修改: 捕获预处理模型 ###
        cluster_result = ClusterAnalyzer.cluster_vectors_optimized(analysis_vectors)
        if cluster_result[0] is None:
            logger.error("Clustering failed. Exiting."); return
            
        cluster_labels, final_n_clusters, normalized_vectors, kept_indices, preprocessing_model = cluster_result

        # ... (聚类样本导出逻辑无需修改)
        kept_ids = analysis_ids[kept_indices]
        export_samples = {int(label): [str(x) for x in kept_ids[cluster_labels == label][:5]] for label in np.unique(cluster_labels) if label != -1}
        with open(f"cluster_samples_{config.COLLECTION_NAME}.json", 'w') as f:
            json.dump({'collection': config.COLLECTION_NAME, 'per_cluster_ids': export_samples}, f, indent=2)

        metrics = Utils.calculate_clustering_metrics(cluster_labels, normalized_vectors)
        
        ### 已修改: 捕获降维器 ###
        reduced_vectors, reducer = DimensionReducer.reduce_dimensions_optimized(
            normalized_vectors,
            method=config.DIMENSION_REDUCTION_METHOD,
            n_components=config.OUTPUT_DIMENSIONS,
            return_reducer=True
        )
        if reduced_vectors is None:
            logger.error("Dimensionality reduction failed. Exiting."); return

        ### 已修改: 正确处理 basic 向量 ###
        basic_reduced = None
        if config.BASIC_OVERLAY_ENABLED:
            raw_basic_vectors = DataFetcher.fetch_basic_vectors(client, expected_dim=vector_dim)
            
            if raw_basic_vectors is not None and preprocessing_model is not None:
                try:
                    logger.info("Transforming basic vectors with the existing preprocessing model...")
                    basic_processed = preprocessing_model.transform_new(raw_basic_vectors)
                    
                    if reducer is not None:
                        logger.info(f"Transforming basic vectors with the existing '{config.DIMENSION_REDUCTION_METHOD}' reducer...")
                        # 使用已有的reducer进行transform，而不是fit_transform
                        basic_reduced = reducer.transform(basic_processed)
                        basic_reduced = basic_reduced * config.VISUAL_EMBEDDING_SCALE
                        logger.info("Successfully transformed basic vectors.")
                    else:
                        logger.warning(f"Reducer '{config.DIMENSION_REDUCTION_METHOD}' does not support transforming new data. Cannot plot basic overlay.")
                
                except Exception as e:
                    logger.warning(f"Failed to process basic vectors for overlay: {e}")
                    basic_reduced = None

        # 创建可视化
        fig = Visualizer.create_visualization(
            reduced_vectors, 
            cluster_labels, 
            metrics,
            config.COLLECTION_NAME,
            basic_reduced=basic_reduced
        )
        if fig is None:
            logger.error("Visualization creation failed. Exiting."); return

        # 生成并保存HTML报告
        total_time = time.time() - total_start_time
        html_content = Visualizer.generate_html_report(
            fig=fig, metrics=metrics, original_count=original_vector_count,
            analyzed_count=len(normalized_vectors), total_time=total_time,
            collection_name=config.COLLECTION_NAME, vector_dim=vector_dim
        )
        
        os.makedirs('output', exist_ok=True)
        output_path = f'output/distribution_{config.COLLECTION_NAME}.html'
        with open(output_path, 'w', encoding='utf-8') as f: f.write(html_content)
        
        logger.info(f"Analysis completed in {total_time:.2f}s. Report saved to {output_path}")
        
    except Exception as e:
        logger.error(f"An unexpected error occurred in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()