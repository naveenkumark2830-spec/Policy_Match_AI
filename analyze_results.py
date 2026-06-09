import pandas as pd

df = pd.read_csv("rag_evaluation_results.csv")

print("\nWorst Queries")
print("=" * 80)

print(
    df.sort_values(
        by="ndcg"
    )[
        [
            "query",
            "ndcg",
            "mrr",
            "retrieved_relevant"
        ]
    ].head(10)
)