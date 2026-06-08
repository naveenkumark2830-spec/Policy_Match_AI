import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import sys
import torch

print("=" * 80)
print(" " * 20 + "FAISS INDEX BUILDER (OPTIMIZED)")
print("=" * 80)

# ============= CHECK SYSTEM =============
print(f"\n🔍 System Info:")
print(f"   GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

# ============= PATHS =============
BASE_PATH = r"D:\GovSchemeAI"
DATA_PATH = os.path.join(BASE_PATH, "data", "cleaned_schemes.csv")
MODELS_DIR = os.path.join(BASE_PATH, "models")
INDEX_PATH = os.path.join(MODELS_DIR, "scheme_index.faiss")

print(f"\n📁 Paths:")
print(f"   Data: {DATA_PATH}")
print(f"   Index: {INDEX_PATH}")

os.makedirs(MODELS_DIR, exist_ok=True)

# ============= LOAD DATA =============
print(f"\n📊 Loading data...")
df = pd.read_csv(DATA_PATH)
texts = df["scheme_text"].tolist()
print(f"✅ Loaded {len(texts)} schemes")

# ============= LOAD MODEL =============
print(f"\n⏳ Loading model...")
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.eval()  # Set to evaluation mode
    print(f"✅ Model loaded")
except Exception as e:
    print(f"❌ Model loading error: {e}")
    sys.exit(1)

# ============= ENCODE WITH OPTIMIZATIONS =============
print(f"\n🔄 Encoding {len(texts)} texts...")
print(f"   (Using small batch size to avoid memory issues)")

try:
    # Small batch size to avoid memory issues
    embeddings = model.encode(
        texts,
        batch_size=8,  # ✅ VERY SMALL batch size
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=False
    )
    print(f"\n✅ Encoding complete!")
    print(f"   Shape: {embeddings.shape}")
except torch.cuda.OutOfMemoryError:
    print(f"\n⚠️ GPU out of memory, switching to CPU...")
    model = model.to('cpu')
    torch.cuda.empty_cache()
    
    embeddings = model.encode(
        texts,
        batch_size=8,
        show_progress_bar=True,
        convert_to_numpy=True,
        device='cpu'
    )
    print(f"\n✅ Encoding complete on CPU!")
except Exception as e:
    print(f"❌ Encoding error: {e}")
    sys.exit(1)

# ============= CONVERT & VERIFY =============
print(f"\n🔍 Converting embeddings...")
embeddings = np.array(embeddings).astype("float32")
print(f"✅ Type: {embeddings.dtype}")
print(f"✅ Shape: {embeddings.shape}")
print(f"✅ Memory: {embeddings.nbytes / 1024 / 1024:.2f} MB")

# Verify no NaN
if np.any(np.isnan(embeddings)):
    print(f"⚠️ Found NaN values in embeddings!")
    embeddings = np.nan_to_num(embeddings)

# ============= CREATE & SAVE INDEX =============
print(f"\n🔨 Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add in chunks to avoid memory spike
chunk_size = 500
for i in range(0, len(embeddings), chunk_size):
    chunk = embeddings[i:i+chunk_size]
    index.add(chunk)
    print(f"   Added {min(i+chunk_size, len(embeddings))}/{len(embeddings)} vectors")

print(f"✅ Index created: {index.ntotal} vectors")

# Save
print(f"\n💾 Saving index...")
faiss.write_index(index, INDEX_PATH)
print(f"✅ Index saved")

# ============= VERIFY =============
print(f"\n✔️ Verifying...")
if os.path.exists(INDEX_PATH):
    size = os.path.getsize(INDEX_PATH)
    print(f"✅ File created!")
    print(f"   Path: {INDEX_PATH}")
    print(f"   Size: {size / 1024 / 1024:.2f} MB")
    
    # Test load
    test_index = faiss.read_index(INDEX_PATH)
    print(f"✅ Index loads correctly: {test_index.ntotal} vectors")
else:
    print(f"❌ File not created!")
    sys.exit(1)

print(f"\n" + "=" * 80)
print(f"{'✨ SUCCESS! FAISS INDEX CREATED':<80}")
print(f"=" * 80)
print(f"\n✅ Ready for search!")
print(f"   Next: python src/search.py")