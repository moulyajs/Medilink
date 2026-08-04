from .query_rewriter import rewrite_query
from .query_parser import parse_query
from .orchestrator import orchestrate


def rag_pipeline(
    query: str,
    patient_id: str,
    chat_history: list,
):

    # ----------------------------------
    # STEP 1 : Rewrite Query
    # ----------------------------------

    rewritten_query = rewrite_query(
        query,
        chat_history,
    )

    print("\n" + "=" * 80)
    print("QUERY REWRITER")
    print("=" * 80)
    print("Original Query:")
    print(query)

    print("\nRewritten Query:")
    print(rewritten_query)

    # ----------------------------------
    # STEP 2 : Parse Query
    # ----------------------------------

    parsed = parse_query(rewritten_query)

    print("\n" + "=" * 80)
    print("PARSED QUERY")
    print("=" * 80)
    print(parsed)

    # ----------------------------------
    # STEP 3 : Execute
    # ----------------------------------

    response = orchestrate(
        parsed=parsed,
        patient_id=patient_id,
        query=rewritten_query,
    )

    print("\n" + "=" * 80)
    print("FINAL RESPONSE")
    print("=" * 80)
    print(response)

    return response