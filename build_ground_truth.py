from src.rag_engine import OptimizedRAGEngine
import pandas as pd

rag = OptimizedRAGEngine(r"C:\GovSchemeAI\GovSchemeAI")

QUERIES = [
    # Widow
    "widow pension",
    "widow financial assistance",
    "single woman pension",
    "widow welfare scheme",
    "widow benefits",

    # Student
    "student scholarship",
    "college scholarship",
    "higher education aid",
    "merit scholarship",
    "student financial assistance",

    # Farmer
    "farmer financial assistance",
    "agriculture subsidy",
    "crop support scheme",
    "organic farming support",
    "farm equipment subsidy",

    # Senior Citizen
    "old age pension",
    "senior citizen pension",
    "retirement support",
    "elderly welfare scheme",
    "old age financial assistance",

    # Employment
    "job training",
    "skill development",
    "unemployment assistance",
    "vocational training",
    "employment scheme",
]

rows = []

for query in QUERIES:

    print("\n" + "=" * 80)
    print("QUERY:", query)

    results = rag.search(query, top_k=10)

    for rank, result in enumerate(results, start=1):

        print(
            f"{rank}. "
            f"ID={result['id']} | "
            f"SIM={result['similarity']} | "
            f"{result['scheme'][:100]}"
        )

        rows.append({
            "query": query,
            "rank": rank,
            "scheme_id": result["id"],
            "similarity": result["similarity"],
            "scheme": result["scheme"]
        })

df = pd.DataFrame(rows)

df.to_csv(
    r"C:\GovSchemeAI\GovSchemeAI\candidate_ground_truth.csv",
    index=False
)

print("\nSaved to candidate_ground_truth.csv")