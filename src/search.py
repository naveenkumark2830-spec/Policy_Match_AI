import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

print("=" * 70)
print("SCHEME SEARCH ENGINE")
print("=" * 70)

class SchemeSearchEngine:
    def __init__(self):
        # Load model
        print("\n⏳ Loading model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Model loaded")
        
        # Load FAISS index
        index_path = r"D:\GovSchemeAI\models\scheme_index.faiss"
        if not os.path.exists(index_path):
            print(f"❌ ERROR: {index_path} not found!")
            exit()
        
        print(f"\n⏳ Loading FAISS index...")
        self.index = faiss.read_index(index_path)
        print(f"✅ Index loaded (total vectors: {self.index.ntotal})")
        
        # Load metadata
        metadata_path = r"D:\GovSchemeAI\data\cleaned_schemes.csv"
        if not os.path.exists(metadata_path):
            print(f"❌ ERROR: {metadata_path} not found!")
            exit()
        
        print(f"\n⏳ Loading metadata...")
        self.df = pd.read_csv(metadata_path)
        print(f"✅ Metadata loaded ({len(self.df)} schemes)")
    
    def search(self, query, top_k=5):
        """Search for similar schemes"""
        print(f"\n🔍 Searching for: '{query}'")
        
        # Encode query
        query_embedding = self.model.encode([query]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        print(f"\n✅ Found {len(indices[0])} results:")
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0]), 1):
            if idx < len(self.df):
                scheme = self.df.iloc[idx]
                result = {
                    'rank': i,
                    'scheme_text': scheme['scheme_text'],
                    'distance': float(distance),
                    'similarity': 1 / (1 + float(distance))  # Convert distance to similarity
                }
                results.append(result)
                
                print(f"\n{i}. {scheme['scheme_text'][:100]}...")
                print(f"   Distance: {float(distance):.4f}")
                print(f"   Similarity: {result['similarity']:.2%}")
        
        return results

# Test the search engine
if __name__ == "__main__":
    engine = SchemeSearchEngine()
    
    # Test queries
    test_queries = [
        "education loan for students",
        "government scheme for saving money",
        "investment with high returns",
        "senior citizen pension scheme",
        "business loan for entrepreneurs"
    ]
    
    print("\n" + "=" * 70)
    print("TESTING SEARCH ENGINE")
    print("=" * 70)
    
    for query in test_queries[:2]:  # Test first 2
        results = engine.search(query, top_k=3)
        print("\n" + "-" * 70)