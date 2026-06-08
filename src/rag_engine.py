from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizedRAGEngine:
    """RAG engine without sentence-transformers dependency"""
    
    QUERY_CACHE = {}
    CACHE_SIZE = 1000
    
    def __init__(self, base_path: str):
        logger.info("Initializing RAG Engine")
        
        try:
            logger.info("Loading embedding model")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.model.eval()
            self.use_embeddings = True
        except ImportError:
            logger.warning("SentenceTransformer not available, using text matching")
            self.model = None
            self.use_embeddings = False
        
        logger.info("Loading FAISS index")
        index_path = os.path.join(base_path, "models", "scheme_index.faiss")
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = None
            logger.warning("FAISS index not found")
        
        logger.info("Loading metadata")
        data_path = os.path.join(base_path, "data", "cleaned_schemes.csv")
        self.df = pd.read_csv(data_path)
        self.scheme_dict = {i: row['scheme_text'] for i, row in self.df.iterrows()}
        
        if self.index:
            logger.info(f"RAG ready with {self.index.ntotal} schemes")
        else:
            logger.info(f"RAG ready with {len(self.df)} schemes (no FAISS)")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search schemes"""
        
        cache_key = f"{query}:{top_k}"
        
        if cache_key in self.QUERY_CACHE:
            logger.info("Cache hit")
            return self.QUERY_CACHE[cache_key]
        
        logger.info(f"Searching: {query[:40]}")
        
        try:
            if self.use_embeddings and self.index:
                results = self._search_with_embeddings(query, top_k)
            else:
                results = self._search_with_text_matching(query, top_k)
            
            if len(self.QUERY_CACHE) > self.CACHE_SIZE:
                self.QUERY_CACHE.pop(next(iter(self.QUERY_CACHE)))
            
            self.QUERY_CACHE[cache_key] = results
            return results
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return self._search_with_text_matching(query, top_k)
    
    def _search_with_embeddings(self, query: str, top_k: int) -> List[Dict]:
        """Search using FAISS embeddings"""
        
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False
        ).astype('float32')
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for rank, (distance, idx) in enumerate(zip(distances[0], indices[0]), 1):
            if idx < len(self.df):
                scheme_text = self.scheme_dict.get(idx, "")
                results.append({
                    'rank': rank,
                    'scheme': scheme_text[:120] + "..." if len(scheme_text) > 120 else scheme_text,
                    'full_scheme': scheme_text,
                    'distance': float(distance),
                    'similarity': round(1 / (1 + float(distance)), 3)
                })
        
        return results
    
    def _search_with_text_matching(self, query: str, top_k: int) -> List[Dict]:
        """Fallback: Simple text matching"""
        
        logger.info("Using text matching (FAISS unavailable)")
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scores = []
        
        for idx, scheme_text in self.scheme_dict.items():
            scheme_lower = scheme_text.lower()
            scheme_words = set(scheme_lower.split())
            
            overlap = len(query_words.intersection(scheme_words))
            score = overlap / (len(query_words) + 1)
            
            scores.append((idx, scheme_text, score))
        
        scores.sort(key=lambda x: x[2], reverse=True)
        
        results = []
        for rank, (idx, scheme_text, score) in enumerate(scores[:top_k], 1):
            results.append({
                'rank': rank,
                'scheme': scheme_text[:120] + "..." if len(scheme_text) > 120 else scheme_text,
                'full_scheme': scheme_text,
                'distance': float(1 - score),
                'similarity': round(score, 3)
            })
        
        return results
    
    def search_by_profile(self, profile: Dict, top_k: int = 5) -> List[Dict]:
        """Search by profile"""
        
        logger.info("Profile search")
        
        query_parts = []
        
        if profile.get('age'):
            age = profile['age']
            if age < 18:
                query_parts.append("student youth scholarship")
            elif age > 60:
                query_parts.append("senior citizen pension retirement")
            else:
                query_parts.append("working professional employment")
        
        if profile.get('occupation'):
            occupation_keywords = {
                'student': 'education scholarship loan',
                'employed': 'salary employment provident fund savings',
                'self-employed': 'business loan entrepreneur MSME',
                'retired': 'pension retirement savings',
            }
            keyword = occupation_keywords.get(profile['occupation'], '')
            if keyword:
                query_parts.append(keyword)
        
        if profile.get('income'):
            income = profile['income']
            if income < 300000:
                query_parts.append("low income welfare assistance")
            elif income > 2000000:
                query_parts.append("investment wealth management")
        
        if profile.get('state'):
            query_parts.append(profile['state'])
        
        if profile.get('category'):
            query_parts.append(f"{profile['category']} category")
        
        query = " ".join(filter(None, query_parts)) or "government scheme"
        return self.search(query, top_k)