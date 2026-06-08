import pandas as pd
import numpy as np

print("=" * 70)
print("CLEANING DATA - STEP 1")
print("=" * 70)

# Load raw data
df = pd.read_csv(
    r"D:\GovSchemeAI\data\schemes_with_text.csv"
)

print(f"\n Original data:")
print(f"   Rows: {len(df)}")
print(f"   Columns: {df.columns.tolist()}")
print(f"   NaN in scheme_text: {df['scheme_text'].isna().sum()}")

# ============= AGGRESSIVE CLEANING =============

# 1. Remove rows with NaN scheme_text
df = df[df['scheme_text'].notna()]
print(f"\n After removing NaN: {len(df)} rows")

# 2. Convert to string
df['scheme_text'] = df['scheme_text'].astype(str)

# 3. Remove rows where scheme_text is the string 'nan'
df = df[df['scheme_text'] != 'nan']
print(f" After removing 'nan' strings: {len(df)} rows")

# 4. Strip whitespace
df['scheme_text'] = df['scheme_text'].str.strip()

# 5. Remove empty strings
df = df[df['scheme_text'] != '']
df = df[df['scheme_text'].str.len() > 0]
print(f" After removing empty: {len(df)} rows")

# 6. Remove None strings
df = df[df['scheme_text'] != 'None']
print(f" After removing None: {len(df)} rows")

# 7. Remove duplicates
before_dedup = len(df)
df = df.drop_duplicates(subset=['scheme_text'], keep='first')
print(f" After removing duplicates: {len(df)} rows (removed {before_dedup - len(df)})")

# 8. Final check - no NaN allowed
df = df.fillna('')
df = df[df['scheme_text'].str.len() > 0]
print(f" Final rows: {len(df)}")

# ============= VERIFICATION =============
print(f"\n🔍 VERIFICATION:")
print(f"   NaN values: {df['scheme_text'].isna().sum()}")
print(f"   Empty strings: {(df['scheme_text'] == '').sum()}")
print(f"   'nan' strings: {(df['scheme_text'] == 'nan').sum()}")
print(f"   Min text length: {df['scheme_text'].str.len().min()}")
print(f"   Max text length: {df['scheme_text'].str.len().max()}")

# Sample
print(f"\nSample texts:")
for i, text in enumerate(df['scheme_text'].head(3).tolist(), 1):
    print(f"   {i}. {text[:80]}...")

# Save cleaned
output_path = r"C:\Users\navee\OneDrive\Attachments\Desktop\GovSchemeAI\data\cleaned_schemes.csv"
df.to_csv(output_path, index=False)
print(f"\n Cleaned data saved: {output_path}")
print(f"   Total rows: {len(df)}")