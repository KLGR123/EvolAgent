"""
Memory retrieval system for EvolAgent.

This module provides the Retriever class for managing vector-based memory storage
and retrieval using Qdrant as the backend with hybrid search capabilities.
"""

import hashlib

from typing import List, Dict, Literal
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams, 
    PointStruct, 
    SparseVector, 
    Prefetch, 
    FusionQuery, 
    Fusion, 
    SparseVectorParams,
)

from .utils import (
    DenseEmbeddingModel, 
    SparseEmbeddingModel, 
    SearchResult, 
    validate_token_length, 
    truncate_text_to_tokens
)
from ..utils.config import config


class MemoryRetriever:
    """
    Vector-based memory retriever with hybrid search capabilities.
    
    Supports dense, sparse, and hybrid search methods for retrieving relevant
    memories from a Qdrant collection. Handles both semantic and episodic memory types.
    """

    def __init__(self, 
        client: QdrantClient,
        role: Literal["planner", "developer", "tester", "critic"], 
        memory_type: Literal["semantic", "episodic"],
    ):
        """
        Initialize the memory retriever.
        
        Args:
            client: Qdrant client instance
            role: Agent role for memory namespacing
            memory_type: Type of memory (semantic or episodic)
        """
        self.role = role
        self.memory_type = memory_type
        self.client = client
        
        # Initialize embedding models
        self.dense_model = DenseEmbeddingModel(
            model_name=config.get('models.default_embedding_model', 'text-embedding-3-large')
        )
        self.sparse_model = SparseEmbeddingModel()

        # Create unique collection name
        self.collection_name = f"{role}_{memory_type}"
        self._ensure_collection_exists()

    def _ensure_collection_exists(self, enable_hybrid: bool = True) -> None:
        """
        Ensure the Qdrant collection exists with proper configuration.
        
        Args:
            enable_hybrid: Whether to enable sparse vectors for hybrid search
        """
        if self.client.collection_exists(collection_name=self.collection_name):
            return
            
        try:
            # Dense vector configuration
            vectors_config = {
                "dense": VectorParams(
                    size=config.get('models.embedding_dimension', 1536),
                    distance=Distance.COSINE
                ),
            }
            
            # Sparse vector configuration for hybrid search
            sparse_vectors_config = {"sparse": SparseVectorParams()} if enable_hybrid else None
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=vectors_config,
                sparse_vectors_config=sparse_vectors_config
            )
            
        except Exception as e:
            print(f"Failed to create collection {self.collection_name}: {e}")
            raise
        
    def add_memories(self,  
        payloads: List[Dict], 
        enable_hybrid: bool = True,
        max_tokens: int = None
    ) -> None:
        """
        Add memory entries to the collection with deduplication and validation.
        
        Args:
            payloads: List of memory payloads with 'text' and optional 'code' fields
            enable_hybrid: Whether to generate sparse embeddings for hybrid search
            max_tokens: Maximum tokens per text chunk (uses config default if None)
        """
        if not payloads:
            return
            
        if max_tokens is None:
            max_tokens = config.get('memory.max_tokens_per_chunk', 8192)

        # Generate content hashes for deduplication
        content_ids = [self._generate_content_id(payload["text"]) for payload in payloads]
        existing_mask = self._check_existing_ids(content_ids)
        
        # Filter out existing entries
        new_payloads = [
            payload for payload, exists in zip(payloads, existing_mask) 
            if not exists
        ]
        new_ids = [
            content_id for content_id, exists in zip(content_ids, existing_mask) 
            if not exists
        ]
        
        if not new_ids:
            return

        # Validate and process text content
        processed_payloads = []
        for i, payload in enumerate(new_payloads):
            is_valid, token_count = validate_token_length(payload["text"], max_tokens)
            
            if not is_valid:
                print(f"Warning: Text chunk {i} has {token_count} tokens, exceeding limit of {max_tokens}")
                processed_text = truncate_text_to_tokens(payload["text"], max_tokens)
                print(f"Truncated text chunk {i} to {max_tokens} tokens")
            else:
                processed_text = payload["text"]
                
            processed_payloads.append({
                **payload,
                "text": processed_text
            })
        
        # Generate embeddings for text content only
        # dense_embeddings = self.dense_model.embed([p["text"] for p in processed_payloads])
        dense_embeddings = []
        batch_size = config.get('memory.batch_size', 16)
        for i in range(0, len(processed_payloads), batch_size):
            batch_texts = [payload["text"] for payload in processed_payloads[i:i + batch_size]]
            dense_embeddings.extend(self.dense_model.embed(batch_texts))
        
        # Create points for insertion
        points_to_add = []
        
        if enable_hybrid:
            sparse_embeddings = self.sparse_model.embed([p["text"] for p in processed_payloads])
            points_to_add = [
                PointStruct(
                    id=content_id,
                    payload=payload,
                    vector={
                        "dense": dense_emb,
                        "sparse": SparseVector(
                            indices=sparse_emb.indices.tolist(),
                            values=sparse_emb.values.tolist(),
                        ),
                    },
                )
                for content_id, payload, dense_emb, sparse_emb in zip(
                    new_ids, processed_payloads, dense_embeddings, sparse_embeddings
                )
            ]
        else:
            points_to_add = [
                PointStruct(
                    id=content_id,
                    payload=payload,
                    vector={"dense": dense_emb},
                )
                for content_id, payload, dense_emb in zip(
                    new_ids, processed_payloads, dense_embeddings
                )
            ]

        # Insert into collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=points_to_add,
            wait=True
        )
        
    def _generate_content_id(self, text: str) -> str:
        """Generate a unique ID based on text content."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
        
    def _check_existing_ids(self, ids: List[str]) -> List[bool]:
        """
        Check which IDs already exist in the collection.
        
        Args:
            ids: List of content IDs to check
            
        Returns:
            List of booleans indicating existence
        """
        try:
            points_count = self.client.count(collection_name=self.collection_name, exact=True)
            
            if points_count.count == 0:
                return [False] * len(ids)
                
            responses = self.client.scroll(
                collection_name=self.collection_name,
                limit=points_count.count,
                with_payload=False,
                with_vectors=False,
            )
            
            existing_ids = set(str(record.id) for record in responses[0])
            return [content_id in existing_ids for content_id in ids]
            
        except Exception as e:
            print(f"Error checking existing IDs: {e}")
            return [False] * len(ids)  # Assume none exist on error

    def delete_memories(self, ids: List[str]) -> None:
        """
        Delete specific memory entries by their IDs.
        
        Args:
            ids: List of content IDs to delete
        """
        if not ids:
            return
            
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=ids, 
                wait=True,
            )
            print(f"Deleted {len(ids)} memories from collection {self.collection_name}")
        except Exception as e:
            print(f"Error deleting memories: {e}")

    def clear_all_memories(self) -> None:
        """Delete the entire collection and recreate it."""
        try:
            if self.client.collection_exists(collection_name=self.collection_name):
                self.client.delete_collection(collection_name=self.collection_name)
                print(f"Collection {self.collection_name} cleared")
                
            # Recreate the collection
            self._ensure_collection_exists()
            
        except Exception as e:
            print(f"Error clearing collection {self.collection_name}: {e}")
        
    def _search_dense_only(self, 
        query: str, 
        limit: int = 10, 
        score_threshold: float = 0.35
    ) -> List[SearchResult]:
        """
        Perform dense vector search only.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            score_threshold: Minimum relevance score
            
        Returns:
            List of search results
        """
        query_embedding = self.dense_model.embed(query)[0]
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            using="dense",
            limit=limit,
            with_payload=True,
            score_threshold=score_threshold
        )
        
        return self._format_search_results(search_result.points)
        
    def _search_sparse_only(self, 
        query: str, 
        limit: int = 10
    ) -> List[SearchResult]:
        """
        Perform sparse vector search only.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        sparse_embedding = list(self.sparse_model.embed(query))[0]
        query_vector = SparseVector(
            indices=sparse_embedding.indices.tolist(),
            values=sparse_embedding.values.tolist(),
        )
        
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            using="sparse",
            limit=limit,
            with_payload=True,
        )
        
        return self._format_search_results(search_result.points)
        
    def _search_hybrid(self, 
        query: str, 
        limit: int = 10, 
        score_threshold: float = 0.35
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining dense and sparse vectors.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            score_threshold: Minimum relevance score
            
        Returns:
            List of search results
        """
        # Generate both embeddings
        dense_embedding = self.dense_model.embed(query)[0]
        sparse_embedding = list(self.sparse_model.embed(query))[0]
        
        # Perform hybrid search with RRF fusion
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(
                    query=SparseVector(
                        indices=sparse_embedding.indices.tolist(),
                        values=sparse_embedding.values.tolist(),
                    ),
                    using="sparse",
                    limit=limit * 2,  # Fetch more for better fusion
                ),
                Prefetch(
                    query=dense_embedding,
                    using="dense", 
                    limit=limit * 2,
                ),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
            with_payload=True,
            # score_threshold=score_threshold
        )
        
        return self._format_search_results(search_result.points)
    
    def _format_search_results(self, points) -> List[SearchResult]:
        """
        Format Qdrant points into SearchResult objects.
        
        Args:
            points: Qdrant search result points
            
        Returns:
            List of formatted search results
        """
        results = []
        for hit in points:
            payload = hit.payload or {}
            result = SearchResult(
                id=str(hit.id),
                score=hit.score,
                payload=payload,
                text=payload.get("text", ""),
                code=payload.get("code", None)
            )
            results.append(result)
        return results
        
    def search(self, 
        query: str, 
        limit: int = 5, 
        method: Literal["dense", "sparse", "hybrid"] = "dense", 
        score_threshold: float = 0.35,
    ) -> List[SearchResult]:
        """
        Search for relevant memories using the specified method.

        Args:
            query: The search query text
            limit: Maximum number of results to return
            method: Search method ("dense", "sparse", or "hybrid")
            score_threshold: Minimum relevance score for results
            
        Returns:
            List of relevant search results
            
        Raises:
            ValueError: If an invalid search method is specified
        """
        try:
            if method == "dense":
                return self._search_dense_only(query, limit, score_threshold)
            elif method == "sparse":
                return self._search_sparse_only(query, limit)
            elif method == "hybrid":
                return self._search_hybrid(query, limit, score_threshold)
            else:
                raise ValueError(f"Invalid search method: {method}")
                
        except Exception as e:
            print(f"Error during {method} search: {e}")
            return []