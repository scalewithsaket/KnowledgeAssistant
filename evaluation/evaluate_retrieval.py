"""
Evaluation of retrieval
"""
import json
from pathlib import Path

from app.ingestion.embedder import Embedder
from app.storage.vector_store import search_similar

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation_questions.json"

TOP_K = 3

def analyse_thresholds(evaluation_results):
    """
    Simulate retrieval-distance thresholds without changing RAG.
    """

    thresholds = [0.50, 0.60, 0.70, 0.80, 0.90]

    print("\n" + "=" * 60)
    print("RETRIEVAL THRESHOLD ANALYSIS")
    print("=" * 60)

    for threshold in thresholds:
        print(f"\nThreshold: {threshold:.2f}")

        for item in evaluation_results:
            best_distance = item["best_distance"]

            # Reject only when the best retrieved chunk
            # is farther away than the threshold.
            rejected = best_distance > threshold

            print(
                f"  {item['id']} ({item['category']}): "
                f"best={best_distance:.4f} | "
                f"{'REJECT' if rejected else 'KEEP'}"
            )


def main():
    """
    Evaluating retrieval
    """
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    embedder = Embedder()

    total_answerable = 0
    hit_count = 0
    recall_sum = 0.0

    evaluation_results = []

    for item in questions:
        question = item["question"]
        expected_sections = set(item["expected_sections"])

        embedding = embedder.embed(question)
        results = search_similar(
            query_embedding=embedding,
            top_k=TOP_K,
        )

        evaluation_results.append({
            "id": item["id"],
            "category": item["category"],
            "best_distance": results[0]["distance"],
        })

        retrieved_sections = [
            result["section"] for result in results
        ]
        retrieved_expected = (
            expected_sections & set(retrieved_sections)
        )

        print(f"\n[{item['id']}] {item['category']}")
        print(f"Question: {question}")

        for result in results:
            print(
                f"  Distance: {result['distance']:.4f}"
                f" | {result['section']}"
            )

        if not expected_sections:
            print("  Retrieval metric: N/A (unsupported question)")
            continue

        total_answerable += 1

        hit = bool(retrieved_expected)
        recall = (
            len(retrieved_expected) / len(expected_sections)
        )

        hit_count += int(hit)
        recall_sum += recall

        print(f"  Hit@{TOP_K}: {hit}")
        print(f"  Recall@{TOP_K}: {recall:.2f}")
        print(
            "  Expected sections missing: "
            f"{sorted(expected_sections - set(retrieved_sections))}"
        )

    analyse_thresholds(evaluation_results)

    if total_answerable:
        print("\n" + "=" * 50)
        print(f"Hit@{TOP_K}: {hit_count / total_answerable:.2f}")
        print(
            f"Recall@{TOP_K}: "
            f"{recall_sum / total_answerable:.2f}"
        )
        print(f"Evaluated answerable/partially answerable questions: "
              f"{total_answerable}")


if __name__ == "__main__":
    main()
