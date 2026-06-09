from src.rag_engine import OptimizedRAGEngine
import pandas as pd
import numpy as np
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGEvaluator:

    def __init__(self):
        self.results = []
        logger.info("RAG Evaluator initialized")

    def evaluate_query(
        self,
        query: str,
        retrieved_schemes: List[Dict],
        relevant_scheme_ids: List[int],
        k: int = 5
    ) -> Dict:

        retrieved_ids = [
            scheme["id"]
            for scheme in retrieved_schemes[:k]
        ]

        relevant_set = set(relevant_scheme_ids)

        metrics = {
            "query": query,
            "ndcg": self._ndcg(
                retrieved_ids,
                relevant_set,
                k
            ),
            "mrr": self._mrr(
                retrieved_ids,
                relevant_set
            ),
            "precision_at_k": self._precision_at_k(
                retrieved_ids,
                relevant_set,
                k
            ),
            "recall": self._recall(
                retrieved_ids,
                relevant_set
            ),
            "hit_rate": int(
                any(
                    doc_id in relevant_set
                    for doc_id in retrieved_ids
                )
            ),
            "relevant_count": len(relevant_set),
            "retrieved_relevant": sum(
                1
                for doc_id in retrieved_ids
                if doc_id in relevant_set
            )
        }

        self.results.append(metrics)
        return metrics

    def _ndcg(
        self,
        retrieved_ids,
        relevant_set,
        k
    ):

        dcg = 0.0

        for rank, doc_id in enumerate(
            retrieved_ids[:k],
            start=1
        ):
            if doc_id in relevant_set:
                dcg += 1 / np.log2(rank + 1)

        idcg = 0.0

        for rank in range(
            1,
            min(len(relevant_set), k) + 1
        ):
            idcg += 1 / np.log2(rank + 1)

        if idcg == 0:
            return 0.0

        return dcg / idcg

    def _mrr(
        self,
        retrieved_ids,
        relevant_set
    ):

        for rank, doc_id in enumerate(
            retrieved_ids,
            start=1
        ):
            if doc_id in relevant_set:
                return 1.0 / rank

        return 0.0

    def _precision_at_k(
        self,
        retrieved_ids,
        relevant_set,
        k
    ):

        if len(retrieved_ids) == 0:
            return 0.0

        hits = sum(
            1
            for doc_id in retrieved_ids[:k]
            if doc_id in relevant_set
        )

        return hits / k

    def _recall(
        self,
        retrieved_ids,
        relevant_set
    ):

        if len(relevant_set) == 0:
            return 0.0

        hits = sum(
            1
            for doc_id in retrieved_ids
            if doc_id in relevant_set
        )

        return hits / len(relevant_set)

    def get_summary(self):

        if not self.results:
            return {}

        df = pd.DataFrame(self.results)

        return {
            "total_queries": len(df),
            "avg_ndcg": df["ndcg"].mean(),
            "avg_mrr": df["mrr"].mean(),
            "avg_precision_at_5": df["precision_at_k"].mean(),
            "avg_recall": df["recall"].mean(),
            "hit_rate": df["hit_rate"].mean(),
            "total_relevant_schemes": df["relevant_count"].sum(),
            "total_retrieved_relevant": df["retrieved_relevant"].sum()
        }

    def print_report(self):

        summary = self.get_summary()

        print("\n" + "=" * 80)
        print("RAG EVALUATION REPORT")
        print("=" * 80)

        print(f"\nOverall Metrics:")
        print(f"   Total Queries Evaluated: {summary['total_queries']}")

        print(f"\n   NDCG@5:           {summary['avg_ndcg']:.4f}")
        print(f"   MRR:              {summary['avg_mrr']:.4f}")
        print(f"   Precision@5:      {summary['avg_precision_at_5']:.4f}")
        print(f"   Recall:           {summary['avg_recall']:.4f}")
        print(f"   Hit Rate:         {summary['hit_rate']:.2%}")

        print(f"\nCoverage:")
        print(f"   Total Relevant:   {summary['total_relevant_schemes']}")
        print(f"   Found:            {summary['total_retrieved_relevant']}")

        print("\n" + "=" * 80)

    def export_results(self, filepath):

        pd.DataFrame(self.results).to_csv(
            filepath,
            index=False
        )

        logger.info(
            f"Results exported to {filepath}"
        )


def evaluate_rag_system():

    logger.info("Starting RAG Evaluation")

    evaluator = RAGEvaluator()

    rag = OptimizedRAGEngine(
        r"C:\GovSchemeAI\GovSchemeAI"
    )

    # Load labeled ground truth file
    ground_truth = pd.read_csv(
        r"C:\GovSchemeAI\GovSchemeAI\candidate_ground_truth.csv",
        encoding="utf-8-sig"
    )

    # Clean column names
    ground_truth.columns = [
        col.replace("ï»¿", "").strip()
        for col in ground_truth.columns
    ]

    print("\nColumns Found:")
    print(ground_truth.columns.tolist())

    queries = ground_truth["query"].unique()

    print("\nEvaluating RAG System...")
    print(f"   Testing {len(queries)} queries\n")

    for query in queries:

        query_rows = ground_truth[
            ground_truth["query"] == query
        ]

        relevant_ids = (
            query_rows[
                query_rows["Relevant"] == 1
            ]["scheme_id"]
            .astype(int)
            .tolist()
        )

        retrieved = rag.search(
            query,
            top_k=5
        )

        metrics = evaluator.evaluate_query(
            query=query,
            retrieved_schemes=retrieved,
            relevant_scheme_ids=relevant_ids,
            k=5
        )

        print(
            f"✓ {query[:50]}"
            f" | NDCG={metrics['ndcg']:.4f}"
            f" | MRR={metrics['mrr']:.4f}"
        )

    evaluator.print_report()

    evaluator.export_results(
        r"C:\GovSchemeAI\GovSchemeAI\rag_evaluation_results.csv"
    )

    return evaluator


if __name__ == "__main__":
    evaluate_rag_system()