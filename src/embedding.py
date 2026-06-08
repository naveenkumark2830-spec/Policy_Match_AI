import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

print("=" * 70)
print("CREATING EMBEDDINGS - STEP 2")
print("=" * 70)

# Load CLEANED data
cleaned_path = r"D:\GovSchemeAI\data\cleaned_schemes.csv"

if not os.path.exists(cleaned_path):
    print(f" ERROR: {cleaned_path} not found!")
    print("Run cleaning.py first!")
    exit()

df = pd.read_csv(cleaned_path)

print(f"\n Loaded cleaned data:")
print(f"   Rows: {len(df)}")
print(f"   Columns: {df.columns.tolist()}")

# Get texts
texts = df["scheme_text"].tolist()

# Final verification before encoding
print(f"\n Pre-encoding verification:")
print(f"   Total texts: {len(texts)}")
print(f"   None values: {sum(1 for t in texts if t is None)}")
print(f"   NaN values: {sum(1 for t in texts if str(t) == 'nan')}")
print(f"   Empty strings: {sum(1 for t in texts if str(t).strip() == '')}")

# Remove any problematic values
texts = [str(t).strip() for t in texts if t and str(t).strip() and str(t) != 'nan']
print(f"   After final clean: {len(texts)} texts")

# Load model
print(f"\n Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"Model loaded")

# Encode with error handling
print(f"\nEncoding {len(texts)} texts...")
try:
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32
    )
    print(f" Encoding successful!")
except ValueError as e:
    print(f"Encoding error: {e}")
    print("\nDebugging info:")
    for i, text in enumerate(texts):
        if not isinstance(text, str):
            print(f"   Row {i}: Type={type(text)}, Value={text}")
    exit()

# Verify embeddings
print(f"\nEmbeddings created:")
print(f"   Shape: {embeddings.shape}")
print(f"   Data type: {embeddings.dtype}")

# Save embeddings
os.makedirs(r"C:\Users\navee\OneDrive\Attachments\Desktop\GovSchemeAI\models", exist_ok=True)

embeddings_path = r"C:\Users\navee\OneDrive\Attachments\Desktop\GovSchemeAI\models\embeddings.npy"
np.save(embeddings_path, embeddings)
print(f"Embeddings saved: {embeddings_path}")

# Save with metadata
df_clean = pd.DataFrame({
    'scheme_text': texts,
    'embedding_id': range(len(texts))
})

metadata_path = r"C:\Users\navee\OneDrive\Attachments\Desktop\GovSchemeAI\data\schemes_with_embeddings.csv"
df_clean.to_csv(metadata_path, index=False)
print(f"Metadata saved: {metadata_path}")

print("\n" + "=" * 70)
print("EMBEDDING COMPLETE!")
print("=" * 70)