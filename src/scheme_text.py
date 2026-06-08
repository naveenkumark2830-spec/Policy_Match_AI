import pandas as pd

df = pd.read_csv(r"D:\GovSchemeAI\data\cleaned_schemes.csv")

df["scheme_text"] = (
    df["scheme_name"].astype(str)
    + " "
    + df["details"].astype(str)
    + " "
    + df["benefits"].astype(str)
    + " "
    + df["eligibility"].astype(str)
    + " "
    + df["schemeCategory"].astype(str)
    + " "
    + df["tags"].astype(str)
)

df.to_csv(
    "schemes_with_text.csv",
    index=False
)

print(df[["scheme_name", "scheme_text"]].head())