import os
import requests
import time
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams, 
    PointStruct, 
    SparseVector, 
    Prefetch, 
    FusionQuery, 
    Fusion, 
    SparseVectorParams
)
from fastembed import SparseTextEmbedding, SparseEmbedding
import uuid

load_dotenv()


@dataclass
class SearchResult:
    id: str
    score: float
    payload: Dict[str, Any]
    text: str


class DenseEmbedModel:
    def __init__(self, model_name: str = "text-embedding-3-large"):
        self.base_url = os.getenv("OPENAI_BASE_URL")
        if self.base_url:
            self.base_url = self.base_url.rstrip('/')
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        self.dimension = None
        
    def embed(self, texts: Union[str, List[str]], max_retries: int = 3, retry_delay: float = 1.0) -> List[List[float]]:
        texts = [texts] if isinstance(texts, str) else texts
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": texts,
            "model": self.model_name
        }
        
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    f"{self.base_url}/embeddings",
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                embeddings = [item["embedding"] for item in result["data"]]

                if self.dimension is None and embeddings:
                    self.dimension = len(embeddings[0])
                    
                return embeddings
                
            except requests.RequestException as e:
                last_exception = e
                if attempt < max_retries:
                    print(f"Dense embedding API call failed on attempt {attempt + 1}/{max_retries + 1}: {e}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise Exception(f"Dense embedding API call failed after {max_retries + 1} attempts: {e}")
        
        # This line of code will not be executed, but for type checking
        raise Exception(f"Dense embedding API call failed after {max_retries + 1} attempts: {last_exception}")


class SparseEmbedModel:  
    def __init__(self, model_name: str = "prithivida/Splade_PP_en_v1"):
        try:
            self.model = SparseTextEmbedding(model_name=model_name)
        except Exception as e:
            raise Exception(f"Sparse embedding model {model_name} initialization failed: {e}")
        
    def embed(self, documents: Union[str, List[str]]) -> List[SparseEmbedding]:
        try:
            if isinstance(documents, str):
                documents = [documents]
            sparse_embeddings = list(self.model.embed(documents))
            return sparse_embeddings
        except Exception as e:
            print(f"Sparse embedding failed: {e}")
            raise e