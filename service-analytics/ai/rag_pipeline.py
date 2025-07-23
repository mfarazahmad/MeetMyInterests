from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from ai.utils import embedding_generator
from ai.prompt_engineer import prompt_engineer, TaskType
from config.bootstrap import vectorIndex
from config.logger import log


class RAGPipeline:
    """RAG pipeline with hybrid search, reranking, and structured prompting."""
    
    def __init__(self):
        self.embedding_model = embedding_generator
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.bm25_index = None
        self.documents = []
        log.info("RAG pipeline initialized")
    
    def initialize_bm25_index(self, documents: List[str]) -> None:
        """Initialize BM25 sparse search index."""
        try:
            # Tokenize documents for BM25
            tokenized_docs = [doc.split() for doc in documents]
            self.bm25_index = BM25Okapi(tokenized_docs)
            self.documents = documents
            log.info(f"BM25 index initialized with {len(documents)} documents")
        except Exception as e:
            log.error(f"Error initializing BM25 index: {e}")
            raise
    
    def dense_search(self, query: str, k: int = 20) -> List[Dict[str, Any]]:
        """Perform dense vector search."""
        try:
            query_embedding = self.embedding_model.generate_embedding(query)
            search_results = vectorIndex.query(query_embedding, k, 'general')
            
            results = []
            for match in search_results.get('matches', []):
                results.append({
                    'content': match.get('metadata', ''),
                    'score': match.get('score', 0.0),
                    'id': match.get('id', ''),
                    'search_type': 'dense'
                })
            
            return results
        except Exception as e:
            log.error(f"Error in dense search: {e}")
            return []
    
    def sparse_search(self, query: str, k: int = 20) -> List[Dict[str, Any]]:
        """Perform sparse BM25 search."""
        try:
            if self.bm25_index is None:
                log.warning("BM25 index not initialized, returning empty results")
                return []
            
            # Get BM25 scores
            tokenized_query = query.split()
            scores = self.bm25_index.get_scores(tokenized_query)
            
            # Get top k results
            top_indices = np.argsort(scores)[::-1][:k]
            
            results = []
            for idx in top_indices:
                if scores[idx] > 0:  # Only include relevant results
                    results.append({
                        'content': self.documents[idx],
                        'score': float(scores[idx]),
                        'id': f"bm25_{idx}",
                        'search_type': 'sparse'
                    })
            
            return results
        except Exception as e:
            log.error(f"Error in sparse search: {e}")
            return []
    
    def hybrid_search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Perform hybrid search combining dense and sparse results."""
        try:
            # Perform both searches
            dense_results = self.dense_search(query, k=k)
            sparse_results = self.sparse_search(query, k=k)
            
            # Combine and deduplicate results
            all_results = self._merge_results(dense_results, sparse_results)
            
            # Rerank combined results
            reranked_results = self._rerank_results(query, all_results)
            
            return reranked_results[:k]
            
        except Exception as e:
            log.error(f"Error in hybrid search: {e}")
            return []
    
    def _merge_results(self, dense_results: List[Dict], sparse_results: List[Dict]) -> List[Dict]:
        """Merge and deduplicate search results."""
        merged = {}
        
        # Add dense results
        for result in dense_results:
            content = result['content']
            if content not in merged:
                merged[content] = result
            else:
                # Keep the higher score
                if result['score'] > merged[content]['score']:
                    merged[content] = result
        
        # Add sparse results
        for result in sparse_results:
            content = result['content']
            if content not in merged:
                merged[content] = result
            else:
                # Keep the higher score
                if result['score'] > merged[content]['score']:
                    merged[content] = result
        
        return list(merged.values())
    
    def _rerank_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """Rerank results using cross-encoder."""
        try:
            if not results:
                return results
            
            # Prepare pairs for reranking
            pairs = [(query, result['content']) for result in results]
            
            # Get reranking scores
            scores = self.reranker.predict(pairs)
            
            # Update results with reranking scores
            for i, result in enumerate(results):
                result['rerank_score'] = float(scores[i])
            
            # Sort by reranking score
            reranked_results = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
            
            return reranked_results
            
        except Exception as e:
            log.error(f"Error in reranking: {e}")
            return results
    
    def process_query(self, query: str, task_type: TaskType = TaskType.GENERAL, 
                     additional_context: List[str] = None) -> str:
        """Process query using RAG pipeline."""
        try:
            # Perform hybrid search
            search_results = self.hybrid_search(query, k=10)
            
            # Extract context from search results
            contexts = [result['content'] for result in search_results if result['content']]
            
            # Add additional context if provided
            if additional_context:
                contexts.extend(additional_context)
            
            # Create structured prompt
            prompt = prompt_engineer.create_structured_prompt(query, contexts, task_type)
            
            # Generate response using the prompt
            from ai.utils import response_generator
            response = response_generator.generate_response(prompt)
            
            return response
            
        except Exception as e:
            log.error(f"Error processing query: {e}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def process_financial_query(self, query: str, financial_data: List[str] = None) -> str:
        """Process financial queries with specialized handling."""
        return self.process_query(query, TaskType.FINANCIAL, financial_data)
    
    def process_trip_query(self, query: str, travel_info: List[str] = None) -> str:
        """Process trip planning queries with specialized handling."""
        return self.process_query(query, TaskType.TRIP_PLANNING, travel_info)
    
    def process_pdf_query(self, query: str, document_content: List[str] = None) -> str:
        """Process PDF analysis queries with specialized handling."""
        return self.process_query(query, TaskType.PDF_ANALYSIS, document_content)
    
    def process_health_query(self, query: str, health_info: List[str] = None) -> str:
        """Process health advice queries with specialized handling."""
        return self.process_query(query, TaskType.HEALTH_ADVICE, health_info)
    
    def process_productivity_query(self, query: str, productivity_context: List[str] = None) -> str:
        """Process productivity queries with specialized handling."""
        return self.process_query(query, TaskType.PRODUCTIVITY, productivity_context)


# Initialize global RAG pipeline
rag_pipeline = RAGPipeline() 