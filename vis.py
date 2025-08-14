import os
import time
import logging
import warnings
import multiprocessing as mp
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient

from sklearn.cluster import KMeans, DBSCAN, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, silhouette_samples
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import TSNE

import plotly.express as px
import plotly.graph_objects as go

# Optional dependencies
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

class Config:
    """Configuration class to centrally manage all parameters"""
    
    # Qdrant connection config
    COLLECTION_NAME = "developer_episodic"
    
    # Data sampling config
    ENABLE_SAMPLING = True
    SAMPLE_SIZE = None  # None means use MAX_POINTS_FOR_VISUALIZATION
    RANDOM_SEED = 42
    MAX_POINTS_FOR_VISUALIZATION = 100000
    
    # Data cleaning config
    ENABLE_DATA_CLEANING = True
    CLEAN_NON_FINITE_VALUES = True
    CLEAN_ZERO_VECTORS = True
    CLEAN_LOW_VARIANCE_FEATURES = False
    CLEAN_DIMENSION_INCONSISTENCY = True
    VARIANCE_THRESHOLD = 1e-8
    
    # Clustering config
    CLUSTERING_METHOD = "kmeans"  # "kmeans" or "dbscan"
    AUTO_CLUSTER_DETECTION = False
    MAX_CLUSTERS = 7
    MIN_CLUSTERS = 3
    N_CLUSTERS = 5
    CLUSTER_DETECTION_METHOD = "silhouette"  # "elbow" or "silhouette"
    OUTLIER_DETECTION_ENABLED = False  # turn off outlier detection, avoid generating -1 label
    OUTLIER_METHOD = "distance_percentile"
    OUTLIER_PERCENTILE = 95
    OUTLIER_CONTAMINATION = 0.1
    
    # DBSCAN specific config
    DBSCAN_AUTO_PARAMS = True
    DBSCAN_EPS = 0.3
    DBSCAN_MIN_SAMPLES = 30
   
    # Preprocessing config
    ENABLE_PCA_PREPROCESSING = False
    PRE_REDUCTION = True
    PRE_PCA_COMPONENTS = 512
    PCA_VARIANCE_THRESHOLD = 0.95
    MAX_PCA_COMPONENTS = 512
    ENABLE_STANDARDIZATION = True
    ENABLE_L2_NORMALIZATION = True
    
    # Dimension reduction config
    DIMENSION_REDUCTION_METHOD = "UMAP"  # "UMAP", "TSNE", "PCA" (recommend UMAP or PCA for reference point comparison)
    UNIFIED_TSNE_IF_OVERLAY = True
    OUTPUT_DIMENSIONS = 2
    UMAP_N_NEIGHBORS = 40
    UMAP_MIN_DIST = 0.2
    UMAP_METRIC = "cosine"
    TSNE_PERPLEXITY = 30
    TSNE_LEARNING_RATE = 200
    
    # Visualization config
    VISUAL_EMBEDDING_SCALE = 0.6
    COLOR_PALETTE = "viridis"
    FIG_WIDTH = 1200
    FIG_HEIGHT = 900
    MARKER_SIZE_2D = 11
    MARKER_SIZE_3D = 3
    POINT_SIZE = 3
    MARKER_OPACITY = 0.7
    POINT_OPACITY = 0.7
    SHOW_CLUSTER_CENTERS = False  # disable cluster center display
    SHOW_OUTLIERS = True
    AXIS_TITLE_FONT_SIZE = 18
    AXIS_TICK_FONT_SIZE = 13
    PLOTLY_TEMPLATE = 'simple_white'
    
    # Performance config
    USE_MINIBATCH_KMEANS = True
    EARLY_SAMPLE_SIZE = 3000
    N_JOBS = min(4, mp.cpu_count())
    
    # Basic overlay config
    BASIC_OVERLAY_ENABLED = True  # Re-enable basic overlay X marks
    BASIC_OVERLAY_COLLECTION = "developer_semantic"
    BASIC_OVERLAY_LIMIT = 5000
    BASIC_OVERLAY_COLOR = "#000000"
    BASIC_OVERLAY_SIZE = 1
    BASIC_OVERLAY_OPACITY = 0.8
    BASIC_MARKER_SIZE_BOOST = 1
    
    # Export settings
    EXPORT_PNG_400DPI = True
    SHOW_DENSITY_CONTOURS = True  # Re-enable beautiful density contours
    DENSITY_CONTOUR_LEVELS = 20

# Create configuration instance
config = Config()

class Utils:
    """Utility functions class"""
    
    @staticmethod
    def validate_config(config_obj):
        """Validate configuration parameters for reasonableness"""
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
        
        # Validate data cleaning configuration
        if not config_obj.ENABLE_DATA_CLEANING:
            logger.info("Data cleaning is DISABLED - all vectors will be preserved")
        else:
            cleaning_options = [
                f"  - Clean non-finite values: {config_obj.CLEAN_NON_FINITE_VALUES}",
                f"  - Clean zero vectors: {config_obj.CLEAN_ZERO_VECTORS}",
                f"  - Clean low variance features: {config_obj.CLEAN_LOW_VARIANCE_FEATURES}",
                f"  - Clean dimension inconsistency: {config_obj.CLEAN_DIMENSION_INCONSISTENCY}"
            ]
            logger.info("Data cleaning is ENABLED with the following options:")
            logger.info('\n'.join(cleaning_options))
    
    @staticmethod
    def safe_array_conversion(data, dtype=np.float32):
        """Safe array conversion with handling of invalid values"""
        try:
            # Handle dictionary data structures
            if isinstance(data, dict):
                data = data.get('dense') or data.get('vector') or list(data.values())
            
            # Handle nested dictionary structures
            if isinstance(data, (list, tuple)) and data and isinstance(data[0], dict):
                processed_data = []
                for item in data:
                    if isinstance(item, dict):
                        processed_data.append(item.get('dense') or item.get('vector') or list(item.values()))
                    else:
                        processed_data.append(item)
                data = processed_data
            
            arr = np.array(data, dtype=dtype)
            
            if arr.ndim == 0 or (arr.ndim == 1 and arr.size == 0):
                logger.warning("Empty or scalar array encountered")
                return None
            
            # Handle NaN and infinite values
            if np.any(np.isnan(arr)) or np.any(np.isinf(arr)):
                logger.warning(f"Found {np.sum(np.isnan(arr))} NaN and {np.sum(np.isinf(arr))} inf values, replacing them.")
                arr = np.nan_to_num(arr, nan=0.0, 
                                   posinf=float(np.finfo(dtype).max), 
                                   neginf=float(np.finfo(dtype).min))
            
            return arr
        except Exception as e:
            logger.error(f"Array conversion failed: {e}")
            return None
    
    @staticmethod
    def calculate_clustering_metrics(labels, vectors):
        """Calculate clustering metrics"""
        unique_labels = np.unique(labels)
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
        n_outliers = np.sum(labels == -1) if -1 in unique_labels else 0
        
        metrics = {
            'n_clusters': n_clusters,
            'n_outliers': n_outliers,
            'outlier_ratio': n_outliers / len(labels) if len(labels) > 0 else 0,
            'cluster_sizes': {int(lbl): int((labels == lbl).sum()) 
                             for lbl in unique_labels if lbl != -1}
        }
        
        if n_clusters >= 2 and len(vectors) > 0:
            try:
                non_outlier_mask = labels != -1
                if np.sum(non_outlier_mask) > 1:
                    filtered_labels = labels[non_outlier_mask]
                    filtered_vectors = vectors[non_outlier_mask]
                    
                    if len(np.unique(filtered_labels)) >= 2:
                        metrics.update({
                            'silhouette_score': silhouette_score(filtered_vectors, filtered_labels),
                            'calinski_harabasz_score': calinski_harabasz_score(filtered_vectors, filtered_labels),
                            'davies_bouldin_score': davies_bouldin_score(filtered_vectors, filtered_labels)
                        })
                        
                        try:
                            sil_samples = silhouette_samples(filtered_vectors, filtered_labels)
                            metrics['silhouette_per_cluster'] = {
                                int(lbl): float(np.mean(sil_samples[filtered_labels == lbl]))
                                for lbl in np.unique(filtered_labels)
                            }
                        except Exception:
                            pass
            except Exception as e:
                logger.warning(f"Failed to calculate clustering metrics: {e}")
        
        return metrics

class DataFetcher:
    """Data fetching class"""
    
    @staticmethod
    def fetch_data_from_qdrant_optimized(client, collection_name, max_points=None):
        """Optimized data fetching function"""
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
            
            valid_points = [(p.vector, p.id) for p in response[0] if p.vector is not None]
            
            if not valid_points:
                logger.error("No vectors retrieved")
                return np.array([]), np.array([])
            
            all_vectors, all_ids = zip(*valid_points)
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
        """Fetch basic overlay vectors"""
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

class DataPreprocessor:
    """Data preprocessing class"""
    
    class PreprocessingModel:
        """Preprocessing model class"""
        
        def __init__(self):
            self.pca = None
            self.scaler = None
            self.normalizer = None
            self.fitted = False
        
        def fit_transform(self, vectors):
            """Fit and transform vectors"""
            result = vectors.copy()
            
            # Apply PCA preprocessing if enabled
            if config.ENABLE_PCA_PREPROCESSING and config.PRE_REDUCTION:
                n_components = min(config.PRE_PCA_COMPONENTS, vectors.shape[1], vectors.shape[0] - 1)
                if n_components > 1:
                    self.pca = PCA(n_components=n_components, random_state=config.RANDOM_SEED)
                    result = self.pca.fit_transform(result)
                    logger.info(f"PCA reduced dimensions from {vectors.shape[1]} to {result.shape[1]}")
            
            # Apply standardization if enabled
            if config.ENABLE_STANDARDIZATION:
                self.scaler = StandardScaler()
                result = self.scaler.fit_transform(result)
            
            # Apply L2 normalization if enabled
            if config.ENABLE_L2_NORMALIZATION:
                self.normalizer = Normalizer(norm='l2')
                result = self.normalizer.fit_transform(result)
            
            self.fitted = True
            return result
        
        def transform(self, vectors):
            """Transform new vectors using fitted model"""
            if not self.fitted:
                raise ValueError("Model must be fitted before transforming new data")
            
            result = vectors.copy()
            for transformer in [self.pca, self.scaler, self.normalizer]:
                if transformer is not None:
                    result = transformer.transform(result)
            
            return result
        
        # Alias for clarity
        transform_new = transform

    @staticmethod
    def preprocess_with_pca_and_normalize(vectors):
        """Preprocess vectors with PCA and normalization, return processed vectors and model"""
        try:
            model = DataPreprocessor.PreprocessingModel()
            processed_vectors = model.fit_transform(vectors)
            return processed_vectors, model
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return vectors, None

class ClusterAnalyzer:
    """Clustering analysis class"""
    
    @staticmethod
    def find_optimal_clusters_elbow_optimized(vectors, max_clusters=None, min_clusters=2, sample_size=None):
        """Find optimal number of clusters using elbow method"""
        max_clusters = min(max_clusters or config.MAX_CLUSTERS, len(vectors) // 2)
        if max_clusters < min_clusters:
            return min_clusters
            
        sample_vectors = (vectors[np.random.choice(len(vectors), sample_size, replace=False)] 
                         if sample_size and len(vectors) > sample_size else vectors)
        
        inertias = []
        k_range = range(min_clusters, max_clusters + 1)
        
        for k in k_range:
            kmeans_cls = MiniBatchKMeans if config.USE_MINIBATCH_KMEANS and len(sample_vectors) > 1000 else KMeans
            kmeans = kmeans_cls(n_clusters=k, random_state=config.RANDOM_SEED, n_init='auto')
            kmeans.fit(sample_vectors)
            inertias.append(kmeans.inertia_)
        
        if len(inertias) < 3:
            return min_clusters
            
        second_diff = np.diff(np.diff(inertias))
        return k_range[np.argmax(second_diff) + 1] if len(second_diff) > 0 else min_clusters

    @staticmethod
    def find_optimal_clusters_silhouette_fast(vectors, max_clusters=None, min_clusters=2, sample_size=None):
        """Find optimal number of clusters using silhouette method"""
        max_clusters = min(max_clusters or config.MAX_CLUSTERS, len(vectors) // 2)
        if max_clusters < min_clusters:
            return min_clusters
            
        sample_vectors = (vectors[np.random.choice(len(vectors), sample_size, replace=False)] 
                         if sample_size and len(vectors) > sample_size else vectors)
        
        best_score, best_k = -1, min_clusters
        for k in range(min_clusters, max_clusters + 1):
            labels = KMeans(n_clusters=k, random_state=config.RANDOM_SEED, n_init='auto').fit_predict(sample_vectors)
            score = silhouette_score(sample_vectors, labels)
            if score > best_score:
                best_score, best_k = score, k
        
        return best_k
    
    @staticmethod
    def perform_dbscan_clustering(vectors, eps=None, min_samples=None):
        """Perform DBSCAN clustering with improved parameter estimation"""
        if eps is None or min_samples is None:
            # more reasonable min_samples estimation: approximately 2 times the data dimension, but at least 5
            if min_samples is None:
                min_samples = max(5, min(int(vectors.shape[1] * 0.1), 50))
            
            if eps is None:
                sample_vectors = (vectors[np.random.choice(len(vectors), 1000, replace=False)] 
                                if config.ENABLE_SAMPLING and len(vectors) > 1000 else vectors)
                distances, _ = NearestNeighbors(n_neighbors=min_samples).fit(sample_vectors).kneighbors(sample_vectors)
                k_distances = np.sort(distances[:, min_samples - 1])
                
                # try multiple percentiles, select eps that produces reasonable number of clusters
                percentiles = [50, 60, 70, 80]
                best_eps = None
                best_n_clusters = 0
                
                for pct in percentiles:
                    test_eps = np.percentile(k_distances, pct)
                    test_dbscan = DBSCAN(eps=test_eps, min_samples=min_samples, n_jobs=1)
                    test_labels = test_dbscan.fit_predict(sample_vectors[:500])  # small sample fast test
                    test_n_clusters = len(set(test_labels)) - (1 if -1 in test_labels else 0)
                    
                    # find eps that produces 3-15 clusters
                    if 3 <= test_n_clusters <= 15 and test_n_clusters > best_n_clusters:
                        best_eps = test_eps
                        best_n_clusters = test_n_clusters
                
                eps = best_eps if best_eps is not None else np.percentile(k_distances, 70)
        
        logger.info(f"DBSCAN parameters: eps={eps:.4f}, min_samples={min_samples}")
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=config.N_JOBS)
        labels = dbscan.fit_predict(vectors)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_outliers = np.sum(labels == -1)
        
        logger.info(f"DBSCAN results: {n_clusters} clusters, {n_outliers} outliers ({n_outliers/len(labels):.1%})")
        return labels, n_clusters

    @staticmethod
    def cluster_vectors_optimized(vectors):
        """Optimized vector clustering function"""
        if len(vectors) == 0:
            logger.error("No vectors to cluster")
            return (None,) * 5
        
        logger.info(f"Starting clustering analysis on {len(vectors)} vectors...")
        
        # Data cleaning
        original_count = len(vectors)
        kept_indices = np.arange(original_count)
        
        if config.ENABLE_DATA_CLEANING:
            # Remove non-finite values
            finite_mask = np.all(np.isfinite(vectors), axis=1)
            vectors = vectors[finite_mask]
            kept_indices = kept_indices[finite_mask]
            
            # Remove zero vectors
            non_zero_mask = np.linalg.norm(vectors, axis=1) > 1e-10
            vectors = vectors[non_zero_mask]
            kept_indices = kept_indices[non_zero_mask]
            
            logger.info(f"Removed {original_count - len(vectors)} invalid vectors")
        
        if len(vectors) == 0:
            logger.error("No valid vectors remaining after cleaning")
            return (None,) * 5

        # Preprocessing
        try:
            processed_vectors, preprocessing_model = DataPreprocessor.preprocess_with_pca_and_normalize(vectors)
            if preprocessing_model is None:
                raise ValueError("Preprocessing model failed to initialize.")
            logger.info(f"Preprocessing completed. Shape: {processed_vectors.shape}")
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return (None,) * 5

        # Perform clustering
        if config.CLUSTERING_METHOD.lower() == "dbscan":
            eps = None if config.DBSCAN_AUTO_PARAMS else config.DBSCAN_EPS
            min_s = None if config.DBSCAN_AUTO_PARAMS else config.DBSCAN_MIN_SAMPLES
            labels, n_clusters = ClusterAnalyzer.perform_dbscan_clustering(processed_vectors, eps, min_s)
        else:  # KMeans
            optimal_k = config.N_CLUSTERS
            if config.AUTO_CLUSTER_DETECTION:
                find_func = (ClusterAnalyzer.find_optimal_clusters_silhouette_fast 
                           if config.CLUSTER_DETECTION_METHOD == "silhouette" 
                           else ClusterAnalyzer.find_optimal_clusters_elbow_optimized)
                optimal_k = find_func(processed_vectors, config.MAX_CLUSTERS, 
                                    config.MIN_CLUSTERS, config.EARLY_SAMPLE_SIZE)
                logger.info(f"Auto-detected optimal K: {optimal_k}")
            else:
                logger.info(f"Using fixed K: {optimal_k}")
            
            kmeans_cls = MiniBatchKMeans if config.USE_MINIBATCH_KMEANS and len(processed_vectors) > 1000 else KMeans
            kmeans = kmeans_cls(n_clusters=optimal_k, random_state=config.RANDOM_SEED, n_init='auto')
            labels = kmeans.fit_predict(processed_vectors)
            n_clusters = optimal_k
            
            logger.info(f"KMeans completed: {n_clusters} clusters")

        if labels is None:
            logger.error("Clustering failed")
            return (None,) * 5

        # Outlier detection (KMeans only) - fix logic problem
        original_n_clusters = n_clusters
        if config.OUTLIER_DETECTION_ENABLED and config.CLUSTERING_METHOD.lower() == "kmeans":
            logger.info(f"Applying outlier detection (threshold: {config.OUTLIER_PERCENTILE}%)")
            cluster_centers = np.array([processed_vectors[labels == i].mean(axis=0) for i in range(n_clusters)])
            distances = np.linalg.norm(processed_vectors - cluster_centers[labels], axis=1)
            threshold = np.percentile(distances, config.OUTLIER_PERCENTILE)
            outlier_mask = distances > threshold
            labels[outlier_mask] = -1
            n_outliers = np.sum(outlier_mask)
            logger.info(f"Marked {n_outliers} points as outliers ({n_outliers/len(labels):.1%})")
        else:
            logger.info("Outlier detection disabled or not applicable")

        return labels, n_clusters, processed_vectors, kept_indices, preprocessing_model

class DimensionReducer:
    """Dimensionality reduction class"""
    
    @staticmethod
    def reduce_dimensions_optimized(vectors, method="UMAP", n_components=2, return_reducer=False):
        """Optimized dimensionality reduction function with optional reducer return"""
        if len(vectors) == 0:
            logger.error("No vectors to reduce")
            return (None, None) if return_reducer else None
        
        logger.info(f"Reducing dimensions of {len(vectors)} vectors using {method} to {n_components}D...")
        reducer, reduced = None, None
        
        try:
            if method.upper() == "UMAP":
                if not UMAP_AVAILABLE:
                    logger.warning("UMAP not available, falling back to t-SNE")
                    method = "TSNE"
                else:
                    reducer = UMAP(
                        n_components=n_components,
                        n_neighbors=config.UMAP_N_NEIGHBORS,
                        min_dist=config.UMAP_MIN_DIST,
                        metric=config.UMAP_METRIC,
                        random_state=config.RANDOM_SEED,
                        n_jobs=1
                    )
                    reduced = reducer.fit_transform(vectors)

            if method.upper() == "TSNE":
                # Pre-reduction for high-dimensional data
                if vectors.shape[1] > 50 and len(vectors) > 1000:
                    pca_for_tsne = PCA(n_components=50, random_state=config.RANDOM_SEED)
                    vectors = pca_for_tsne.fit_transform(vectors)
                
                # Ensure perplexity is valid
                perplexity = max(1, min(config.TSNE_PERPLEXITY, len(vectors) - 1))
                
                tsne_reducer = TSNE(
                    n_components=n_components,
                    perplexity=perplexity,
                    learning_rate=config.TSNE_LEARNING_RATE,
                    random_state=config.RANDOM_SEED,
                    n_jobs=config.N_JOBS
                )
                reduced = tsne_reducer.fit_transform(vectors)
                
                if return_reducer:
                    logger.warning("t-SNE does not support transforming new data. Cannot return a reusable reducer.")
                    reducer = None

            if method.upper() == "PCA":
                reducer = PCA(n_components=n_components, random_state=config.RANDOM_SEED)
                reduced = reducer.fit_transform(vectors)
            
            if reduced is None:
                logger.error(f"Unknown dimension reduction method: {method}")
                return (None, None) if return_reducer else None
            
            # Apply visual scaling
            reduced = reduced * config.VISUAL_EMBEDDING_SCALE
            logger.info(f"{method} reduction completed.")
            
            return (reduced, reducer) if return_reducer else reduced

        except Exception as e:
            logger.error(f"Dimension reduction failed: {e}")
            import traceback
            traceback.print_exc()
            return (None, None) if return_reducer else None

class Visualizer:
    """Visualization class"""
    
    @staticmethod
    def create_visualization(reduced_vectors, cluster_labels, metrics, collection_name, basic_reduced=None):
        """Create visualization chart"""
        logger.info("Creating visualization...")
        logger.info(f"Reduced vectors shape: {reduced_vectors.shape}")
        logger.info(f"Cluster labels shape: {cluster_labels.shape}")
        logger.info(f"Unique clusters: {np.unique(cluster_labels)}")
        logger.info(f"Basic reduced shape: {basic_reduced.shape if basic_reduced is not None else 'None'}")
        
        # Prepare DataFrame with proper cluster label handling
        # Convert cluster labels to categorical strings, handle outliers (-1) specially
        cluster_str_labels = []
        for label in cluster_labels:
            if label == -1:
                cluster_str_labels.append('Outlier')
            else:
                cluster_str_labels.append(f'Cluster {label}')
        
        df_data = {
            'x': reduced_vectors[:, 0],
            'y': reduced_vectors[:, 1],
            'cluster': cluster_str_labels
        }
        
        if reduced_vectors.shape[1] >= 3:
            df_data['z'] = reduced_vectors[:, 2]
        
        df = pd.DataFrame(df_data)

        # Determine dimensionality and select appropriate plotting function
        is_3d = config.OUTPUT_DIMENSIONS == 3 and 'z' in df.columns
        # Force use of regular scatter instead of ScatterGL for debugging
        scatter_func = px.scatter_3d if is_3d else px.scatter
        
        # Use gradient red color scheme as originally intended
        # Create a gradient from dark red to light red/pink
        red_gradient_colors = [
            '#8B0000',  # Dark red
            '#B22222',  # Fire brick
            '#DC143C',  # Crimson  
            '#FF4500',  # Orange red
            '#FF6347',  # Tomato
            '#FF7F7F',  # Light coral
            '#FFB6C1',  # Light pink
            '#FFC0CB',  # Pink
            '#FFCCCB',  # Light pink
            '#FFE4E1',  # Misty rose
            '#FFF0F5',  # Lavender blush
            '#FFFFFF'   # White (for contrast if needed)
        ]
        
        # Dynamically build plotting function keyword arguments
        plot_kwargs = {
            'x': 'x',
            'y': 'y',
            'color': 'cluster',
            'color_discrete_sequence': red_gradient_colors,  # use red gradient colors
            'template': config.PLOTLY_TEMPLATE
        }
        
        # Debug: Print cluster information and color mapping
        unique_clusters = np.unique(cluster_labels)
        logger.info(f"Unique cluster labels: {unique_clusters}")
        logger.info(f"Number of unique clusters: {len(unique_clusters)}")
        logger.info(f"Red gradient colors being used: {red_gradient_colors[:len(unique_clusters)]}")
        
        # Add 'z' parameter only in 3D mode
        if is_3d:
            plot_kwargs['z'] = 'z'

        # Debug: Print DataFrame info
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
        logger.info(f"Sample data:\n{df.head()}")
        logger.info(f"Data ranges - X: [{df['x'].min():.3f}, {df['x'].max():.3f}], Y: [{df['y'].min():.3f}, {df['y'].max():.3f}]")
        logger.info(f"Cluster value counts:\n{df['cluster'].value_counts()}")
        
        # Prepare marker settings
        marker_size = config.MARKER_SIZE_3D if is_3d else config.MARKER_SIZE_2D
        debug_marker_size = max(marker_size, 8)
        debug_opacity = 1.0  # Full opacity
        
        # DEBUG: Create figure manually using go.Scatter instead of px.scatter
        if not is_3d:
            fig = go.Figure()
            
            # Create traces for each cluster manually with red gradient
            for cluster_name in df['cluster'].unique():
                cluster_data = df[df['cluster'] == cluster_name]
                cluster_index = int(cluster_name.split()[-1]) if 'Cluster' in cluster_name else 0
                color = red_gradient_colors[cluster_index % len(red_gradient_colors)]
                
                fig.add_trace(go.Scatter(
                    x=cluster_data['x'],
                    y=cluster_data['y'],
                    mode='markers',
                    marker=dict(
                        color=color,
                        size=debug_marker_size,
                        opacity=debug_opacity
                    ),
                    name=cluster_name
                ))
            
            logger.info(f"Manually created {len(fig.data)} traces")
        else:
            # Use parameter unpacking to call function for 3D
            fig = scatter_func(df, **plot_kwargs)
            fig.update_traces(marker=dict(size=debug_marker_size, opacity=debug_opacity))
            logger.info(f"Updated markers with size={debug_marker_size}, opacity={debug_opacity}")
        
        # Debug: Print trace information
        logger.info(f"Number of traces after scatter creation: {len(fig.data)}")
        for i, trace in enumerate(fig.data):
            logger.info(f"Trace {i}: {trace.name}, type: {type(trace).__name__}, points: {len(trace.x) if hasattr(trace, 'x') else 'N/A'}")

        # Add density contours in 2D mode only (background layer)
        if not is_3d:
            if config.SHOW_DENSITY_CONTOURS:
                try:
                    # Create custom light red colorscale for density contours
                    light_red_colorscale = [
                        [0.0, 'rgba(255, 255, 255, 0.3)'],      # Transparent white
                        [0.2, 'rgba(255, 228, 225, 0.6)'],   # Very light pink
                        [0.4, 'rgba(255, 192, 203, 0.7)'],   # Light pink
                        [0.6, 'rgba(255, 160, 160, 0.8)'],   # Light coral
                        [0.8, 'rgba(255, 120, 120, 0.9)'],   # Medium light red
                        [1.0, 'rgba(220, 20, 60, 1.0)']      # Crimson
                    ]
                    
                    contour = go.Histogram2dContour(
                        x=reduced_vectors[:, 0],
                        y=reduced_vectors[:, 1],
                        colorscale=light_red_colorscale,
                        reversescale=False,  # Don't reverse since we want darker at higher density
                        showscale=False,
                        ncontours=config.DENSITY_CONTOUR_LEVELS,
                        opacity=0.3,  # Slightly higher opacity for better visibility
                        contours=dict(showlines=False)
                    )
                    fig.add_trace(contour)
                    # Move contour to background
                    fig.data = fig.data[-1:] + fig.data[:-1]
                except Exception as e:
                    logger.warning(f"Failed to add density contours: {e}")
        
        # Add basic vector reference points (top layer - added after main scatter plot)
        if basic_reduced is not None and len(basic_reduced) > 0:
            trace_func = go.Scatter3d if is_3d else go.Scatter
            trace_data = {
                'x': basic_reduced[:, 0],
                'y': basic_reduced[:, 1],
                'mode': 'markers',
                'marker': dict(
                    color=config.BASIC_OVERLAY_COLOR,
                    size=marker_size * config.BASIC_MARKER_SIZE_BOOST * 2,  # make X symbols larger
                    opacity=1.0,  # full opacity to ensure visibility on top
                    symbol='x',
                    line=dict(width=2, color=config.BASIC_OVERLAY_COLOR)  # add outline for better visibility
                ),
                'name': 'Basic Overlay'
            }
            
            if is_3d:
                # Ensure basic vectors can be displayed in 3D even if they only have 2 dimensions
                trace_data['z'] = (basic_reduced[:, 2] if basic_reduced.shape[1] >= 3 
                                 else np.zeros(len(basic_reduced)))
            
            # Add basic overlay as the final trace to ensure it appears on top of scatter points
            fig.add_trace(trace_func(**trace_data))

        # Cluster centers display removed as per requirements
        
        # Update chart title and layout (remove main title as requested)
        title_components = [
            f"Clusters: {metrics.get('n_clusters', 0)}, Outliers: {metrics.get('n_outliers', 0)}"
        ]
        
        # if metrics.get('silhouette_score') is not None:
            # title_components.append(f"Silhouette: {metrics['silhouette_score']:.3f}")
        
        title_text = "<br>".join(title_components)
        
        fig.update_layout(
            title_text=title_text,
            title_y=0.95,  # move title higher to create more space
            title_x=0.5,   # center the title
            width=config.FIG_WIDTH,
            height=config.FIG_HEIGHT,
            legend_title_text='Cluster',
            font=dict(family='Times New Roman, serif', size=16),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(t=80, b=40, l=40, r=40),  # increase top margin for more space
            xaxis=dict(showline=True, linewidth=1, linecolor='black', mirror=True, 
                      zeroline=False, gridcolor='rgba(0,0,0,0.05)', 
                      showticklabels=False, title=''),  # hide x axis labels and title
            yaxis=dict(showline=True, linewidth=1, linecolor='black', mirror=True, 
                      zeroline=False, gridcolor='rgba(0,0,0,0.05)',
                      showticklabels=False, title='')   # hide y axis labels and title
        )
        return fig






def main():
    """Main function"""
    logger.info("Starting vector distribution analysis...")
    total_start_time = time.time()
    
    try:
        Utils.validate_config(config)
        
        client = QdrantClient(path="qdrant")
        logger.info("Connected to Qdrant successfully")
        
        # Data fetching
        vectors, ids = DataFetcher.fetch_data_from_qdrant_optimized(client, config.COLLECTION_NAME)
        if len(vectors) == 0:
            logger.error("No vectors retrieved. Exiting.")
            return
        
        original_vector_count = len(vectors)
        vector_dim = vectors.shape[1]
        
        # Apply sampling if enabled
        analysis_vectors = vectors
        analysis_ids = np.asarray(ids)
        if config.ENABLE_SAMPLING and len(vectors) > config.MAX_POINTS_FOR_VISUALIZATION:
            logger.info(f"Sampling {config.MAX_POINTS_FOR_VISUALIZATION} vectors...")
            indices = np.random.choice(len(vectors), config.MAX_POINTS_FOR_VISUALIZATION, replace=False)
            analysis_vectors, analysis_ids = vectors[indices], ids[indices]
        
        logger.info(f"Analyzing {len(analysis_vectors)} vectors")
        
        # Initialize variables that will be populated across all paths
        fig = None
        metrics = {}
        analyzed_count = 0
        reduced_vectors = None
        basic_reduced = None
        normalized_vectors = None
        cluster_labels = None
        kept_indices = None
        reducer = None
        basic_processed_for_analysis = None

        # Choose processing path based on dimensionality reduction method
        
        # Path 1: Unified t-SNE processing (when using t-SNE with basic vector overlay)
        if (config.DIMENSION_REDUCTION_METHOD.upper() == "TSNE" and 
            config.BASIC_OVERLAY_ENABLED and config.UNIFIED_TSNE_IF_OVERLAY):
            
            logger.info("--- Using Unified t-SNE Path for Overlay ---")
            
            # 1. Cluster main vectors first, get labels and preprocessing model
            cluster_result = ClusterAnalyzer.cluster_vectors_optimized(analysis_vectors)
            if cluster_result[0] is None:
                logger.error("Clustering failed. Exiting.")
                return
            cluster_labels, _, normalized_vectors, kept_indices, preprocessing_model = cluster_result
            analyzed_count = len(normalized_vectors)
            
            # 2. Fetch and process basic vectors
            raw_basic_vectors = DataFetcher.fetch_basic_vectors(client, expected_dim=vector_dim)
            if raw_basic_vectors is not None and preprocessing_model is not None:
                logger.info("Transforming basic vectors with the existing preprocessing model...")
                basic_processed = preprocessing_model.transform_new(raw_basic_vectors)
                
                # 3. Combine main and basic vectors
                num_main_vectors = len(normalized_vectors)
                combined_vectors = np.vstack((normalized_vectors, basic_processed))
                logger.info(f"Combined main ({num_main_vectors}) and basic ({len(basic_processed)}) vectors for unified t-SNE.")
                
                # 4. Apply dimensionality reduction to combined vectors
                combined_reduced = DimensionReducer.reduce_dimensions_optimized(
                    combined_vectors,
                    method="TSNE",
                    n_components=config.OUTPUT_DIMENSIONS,
                    return_reducer=False  # t-SNE doesn't need to return reducer
                )
                
                if combined_reduced is not None:
                    # 5. Split reduced results
                    reduced_vectors = combined_reduced[:num_main_vectors]
                    basic_reduced = combined_reduced[num_main_vectors:]
                    basic_processed_for_analysis = basic_processed
                    logger.info("Successfully split reduced vectors.")

                    metrics = Utils.calculate_clustering_metrics(cluster_labels, normalized_vectors)
                    fig = Visualizer.create_visualization(reduced_vectors, cluster_labels, metrics, 
                                                        config.COLLECTION_NAME, basic_reduced)
                else:
                    logger.error("Unified t-SNE dimensionality reduction failed.")

            else:
                logger.warning("Could not fetch or process basic vectors. Running t-SNE on main vectors only.")
                # Fallback to processing only main vectors
                reduced_vectors = DimensionReducer.reduce_dimensions_optimized(
                    normalized_vectors, "TSNE", config.OUTPUT_DIMENSIONS)
                if reduced_vectors is not None:
                    metrics = Utils.calculate_clustering_metrics(cluster_labels, normalized_vectors)
                    fig = Visualizer.create_visualization(reduced_vectors, cluster_labels, metrics, 
                                                        config.COLLECTION_NAME)

        # Path 2: Standard processing path (for UMAP, PCA, or t-SNE without overlay)
        else:
            logger.info("--- Using Standard Processing Path (UMAP/PCA or t-SNE without overlay) ---")
            
            # 1. Clustering and get preprocessing model
            cluster_result = ClusterAnalyzer.cluster_vectors_optimized(analysis_vectors)
            if cluster_result[0] is None:
                logger.error("Clustering failed. Exiting.")
                return
            cluster_labels, _, normalized_vectors, kept_indices, preprocessing_model = cluster_result
            analyzed_count = len(normalized_vectors)

            # 2. Dimensionality reduction and get reducer
            reduced_vectors, reducer = DimensionReducer.reduce_dimensions_optimized(
                normalized_vectors,
                method=config.DIMENSION_REDUCTION_METHOD,
                n_components=config.OUTPUT_DIMENSIONS,
                return_reducer=True
            )
            if reduced_vectors is None:
                logger.error("Dimensionality reduction failed. Exiting.")
                return

            # 3. Process and transform basic vectors for overlay display
            if config.BASIC_OVERLAY_ENABLED:
                raw_basic_vectors = DataFetcher.fetch_basic_vectors(client, expected_dim=vector_dim)
                
                if raw_basic_vectors is not None and preprocessing_model is not None:
                    try:
                        logger.info("Transforming basic vectors with the existing preprocessing model...")
                        basic_processed = preprocessing_model.transform_new(raw_basic_vectors)
                        basic_processed_for_analysis = basic_processed
                        
                        if reducer is not None:
                            logger.info(f"Transforming basic vectors with the existing '{config.DIMENSION_REDUCTION_METHOD}' reducer...")
                            basic_reduced = reducer.transform(basic_processed)
                            basic_reduced *= config.VISUAL_EMBEDDING_SCALE
                            logger.info("Successfully transformed basic vectors for overlay.")
                        else:
                            logger.warning(f"Reducer '{config.DIMENSION_REDUCTION_METHOD}' does not support transforming new data. Cannot plot basic overlay.")
                    
                    except Exception as e:
                        logger.warning(f"Failed to process basic vectors for overlay: {e}")
                        basic_reduced = None

            metrics = Utils.calculate_clustering_metrics(cluster_labels, normalized_vectors)
            fig = Visualizer.create_visualization(reduced_vectors, cluster_labels, metrics, 
                                                config.COLLECTION_NAME, basic_reduced)

        # Analysis and export (common to all paths)
        if fig is None:
            logger.error("Visualization creation failed. Exiting.")
            return
        
        total_time = time.time() - total_start_time
        logger.info(f"Analysis completed in {total_time:.2f}s")

        # Export 400DPI PNG only
        if config.EXPORT_PNG_400DPI and fig is not None:
            try:
                os.makedirs('output', exist_ok=True)
                png_path = f'output/visualization_{config.COLLECTION_NAME}.png'
                fig.write_image(png_path, scale=5, width=1200, height=900)  # ~400 DPI
                logger.info(f"400DPI PNG saved: {png_path}")
            except Exception as e:
                logger.warning(f"Failed to export PNG: {e}")
        
    except Exception as e:
        logger.error(f"An unexpected error occurred in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()