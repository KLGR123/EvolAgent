import os
import uuid
from typing import List, Dict, Optional, Literal
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

from .utils import DenseEmbedModel, SparseEmbedModel, SearchResult


class Retriever:
    """
    Retriever is a class that retrieves the memories from the qdrant collection.
    It uses the dense and sparse models to retrieve the memories.
    """

    def __init__(self, 
        client: QdrantClient,
        name: Literal["plan", "dev", "test", "critic"], 
        type: Literal["semantic", "episodic"],
        model: str = "text-embedding-3-large", 
        embed_dim: int = 3072
    ):
        self.name = name
        self.model = model
        self.embed_dim = embed_dim

        self.client = client
        self.dense_model = DenseEmbedModel(model_name="text-embedding-3-large")
        self.sparse_model = SparseEmbedModel()

        self.collection_name = f"{name}_{type}"
        self._create_collection()

    def _create_collection(self, hybrid: bool = True) -> None:
        """
        Create the collection.
        """

        if self.client.collection_exists(collection_name=self.collection_name):
            pass
            # print(f"Collection {self.collection_name} already exists")
        else:
            vectors_config = {
                "dense": VectorParams(
                    size=self.embed_dim,
                    distance=Distance.COSINE
                ),
            }
            if hybrid:
                sparse_vectors_config = {"sparse": SparseVectorParams()}
            else:
                sparse_vectors_config = None
            
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=vectors_config,
                    sparse_vectors_config=sparse_vectors_config
                )
            except Exception as e:
                print(f"Collection {self.collection_name} creation failed: {e}")
        
    def add(self,  # TODO chunking corruption due to text length longer than 8192?
        texts: List[str], 
        metadatas: Optional[List[Dict]] = None, 
        ids: Optional[List[str]] = None, 
        hybrid: bool = True
    ) -> None:
        """
        Add the texts to the collection.
        """

        ids = [str(uuid.uuid4()) for _ in texts] if ids is None else ids
        if metadatas is None:
            metadatas = [{"text": text} for text in texts]
        else:
            for i, metadata in enumerate(metadatas):
                metadata["text"] = texts[i]
        
        dense_embeddings = self.dense_model.embed(texts)
        points_to_add = []

        if hybrid:
            sparse_embeddings = self.sparse_model.embed(texts)
            points_to_add = [
                PointStruct(
                    id=idx,
                    payload=meta,
                    vector={
                        "dense": dense_emb,
                        "sparse": SparseVector(
                            indices=sparse_emb.indices.tolist(),
                            values=sparse_emb.values.tolist(),
                        ),
                    },
                )
                for idx, meta, dense_emb, sparse_emb in zip(ids, metadatas, dense_embeddings, sparse_embeddings)
            ]
        else:
            points_to_add = [
                PointStruct(
                    id=idx,
                    payload=meta,
                    vector={"dense": dense_emb},
                )
                for idx, meta, dense_emb in zip(ids, metadatas, dense_embeddings)
            ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points_to_add,
            wait=True
        )

    def _delete(self, ids: List[str]): # TODO
        """
        Delete the vectors from the collection by their IDs.
        """

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids, # type: ignore
            wait=True,
        )
        print(f"Deleted {len(ids)} points from collection {self.collection_name}")

    def delete_all(self) -> None:
        """
        Delete the collection.
        """

        if self.client.collection_exists(collection_name=self.collection_name):
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Collection {self.collection_name} deleted")
        
    def _search_dense(self, 
        query: str, 
        limit: int = 10, 
        score_threshold: float = 0.5
    ) -> List[SearchResult]:
        """
        Search the dense model.
        """
        
        query_embedding = self.dense_model.embed(query)[0]
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True,
            score_threshold=score_threshold
        )
        results = []
        for hit in search_result:
            payload = hit.payload or {}
            result = SearchResult(
                id=str(hit.id),
                score=hit.score,
                payload=payload,
                text=payload.get("text", "")
            )
            results.append(result)     
        return results
        
    def _search_sparse(self, 
        query: str, 
        limit: int = 10
    ) -> List[SearchResult]:
        """
        Search the sparse model.
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
        results = []
        for hit in search_result.points:
            payload = hit.payload or {}
            result = SearchResult(
                id=str(hit.id),
                score=hit.score,
                payload=payload,
                text=payload.get("text", "")
            )
            results.append(result)
        return results
        
    def _search_hybrid(self, query: str, limit: int = 10, score_threshold: float = 0.5) -> List[SearchResult]:
        """
        Search the hybrid model.
        """

        dense_embedding = self.dense_model.embed(query)[0]
        sparse_embedding = list(self.sparse_model.embed(query))[0]
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(query=SparseVector(
                        indices=sparse_embedding.indices.tolist(),
                        values=sparse_embedding.values.tolist(),
                    ),
                    using="sparse",
                    limit=limit*2,
                ),
                Prefetch(
                    query=dense_embedding,
                    using="dense", 
                    limit=limit*2,
                ),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
            with_payload=True,
            score_threshold=score_threshold
        )
        results = []
        for hit in search_result.points:
            payload = hit.payload or {}
            result = SearchResult(
                id=str(hit.id),
                score=hit.score,
                payload=payload,
                text=payload.get("text", "")
            )
            results.append(result)
        return results
        
    def search(self, 
        query: str, 
        limit: int = 5, 
        method: Literal["dense", "sparse", "hybrid"] = "hybrid", 
        score_threshold: float = 0.6, # TODO: add score_threshold
        augment: bool = False # TODO: add augment
    ) -> List[SearchResult]:
        """
        Search for documents in the collection.

        Args:
            query: The query string to search for.
            limit: The topk  results to return.
            method: The method to use for searching. "dense", "sparse", "hybrid"
            score_threshold: The minimum confidence score for a result to be returned.
        """
        if method == "dense":
            return self._search_dense(query, limit, score_threshold)
        elif method == "sparse":
            return self._search_sparse(query, limit)
        else:
            return self._search_hybrid(query, limit, score_threshold)


if __name__ == "__main__":
    client = QdrantClient(path=os.getenv("QDRANT_PERSIST_PATH"))  
    retriever = Retriever(client=client, name="plan", type="semantic", model="text-embedding-3-large")
    texts = ["Hello, world!", "Another document", "This is a test."]
    retriever.add(texts=texts)

    results = retriever.search(query="test now", limit=5, method="hybrid")
    print(results)
    
    to_delete_ids = [results[2].id]
    retriever._delete(ids=to_delete_ids)
    results = retriever.search(query="test now", limit=1, method="hybrid")
    print(results)

    retriever.delete_all()
    print("Done.")