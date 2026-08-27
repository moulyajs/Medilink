#test_query_rewriter.py
import pandas as pd

from chatbot.rag.query_rewriter import rewrite_query


df = pd.read_csv("query_rewriting_dataset_200_diverse.csv")

results = []

for _, row in df.iterrows():

    context = row["conversation_context"]
    follow_up = row["follow_up_query"]

    if context.strip():
        chat_history = [
            {
                "role": "user",
                "content": context
            }
        ]
    else:
        chat_history = []

    predicted = rewrite_query(
        follow_up,
        chat_history
    )

    results.append({
        "query_id": row["query_id"],
        "category": row["category"],
        "follow_up_query": follow_up,
        "expected": row["expected_rewritten_query"],
        "predicted": predicted
    })


results_df = pd.DataFrame(results)

results_df.to_csv(
    "query_rewriting_results.csv",
    index=False
)