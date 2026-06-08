import pandas as pd

# Load dataset
df = pd.read_csv(r"D:\GovSchemeAI\data\updated_data.csv")

print("Before Cleaning")
print(df.shape)
print(df.columns)

# Remove unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove duplicates
df = df.drop_duplicates()

# Fill missing values
df = df.fillna("")

print("\nAfter Cleaning")
print(df.shape)

# Save cleaned dataset
df.to_csv(
    r"D:\GovSchemeAI\data\cleaned_schemes.csv",
    index=False
)

print("Dataset Cleaned Successfully")