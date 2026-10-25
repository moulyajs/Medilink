
from unittest.mock import Mock

import pytest

from chatbot.rag import pipeline
from chatbot.rag import orchestrator


@pytest.mark.parametrize(
    ("intent", "handler_name"),
    [
        ("LATEST_VALUE", "handle_latest"),
        ("TREND", "handle_trend"),
        ("GENERAL_RAG", "handle_rag"),
    ],
)
def test_intent_selects_correct_handler(
    monkeypatch, intent, handler_name
):
    expected = {"content": f"{intent} handled"}

    handler = Mock(return_value=expected)
    monkeypatch.setitem(
        orchestrator.TASK_HANDLERS, intent, handler
    )
    monkeypatch.setattr(
        orchestrator, "build_response",
        lambda responses: {
            "answer": "\n\n".join(
                response["content"] for response in responses
            ),
            "chunks": [],
        },
    )

    result = orchestrator.orchestrate(
        parsed={
            "greeting": False,
            "thanks": False,
            "bye": False,
            "tasks": [{"intent": intent, "entity": "HAEMOGLOBIN"}],
        },
        patient_id="synthetic-patient",
        query="test query",
    )

    handler.assert_called_once_with(
        task={"intent": intent, "entity": "HAEMOGLOBIN"},
        patient_id="synthetic-patient",
        query="test query",
    )
    assert result["answer"] == expected["content"]


def test_pipeline_connects_rewriter_parser_and_orchestrator(
    monkeypatch,
):
    calls = {}

    def fake_rewrite(query, history):
        calls["rewrite"] = (query, history)
        return "What is my haemoglobin trend?"

    def fake_parse(query):
        calls["parse"] = query
        return {
            "greeting": False,
            "thanks": False,
            "bye": False,
            "tasks": [{"intent": "TREND", "entity": "HAEMOGLOBIN"}],
        }

    def fake_orchestrate(parsed, patient_id, query):
        calls["orchestrate"] = (parsed, patient_id, query)
        return {"answer": "Trend response", "chunks": []}

    monkeypatch.setattr(pipeline, "rewrite_query", fake_rewrite)
    monkeypatch.setattr(pipeline, "parse_query", fake_parse)
    monkeypatch.setattr(pipeline, "orchestrate", fake_orchestrate)

    history = [{"role": "user", "content": "Show my haemoglobin"}]
    result = pipeline.rag_pipeline(
        query="What about its trend?",
        patient_id="synthetic-patient",
        chat_history=history,
    )

    assert calls["rewrite"] == ("What about its trend?", history)
    assert calls["parse"] == "What is my haemoglobin trend?"
    assert calls["orchestrate"][1:] == (
        "synthetic-patient",
        "What is my haemoglobin trend?",
    )
    assert result["answer"] == "Trend response"


def test_empty_query_parser_fallback(monkeypatch):
    from chatbot.rag import query_parser

    response = Mock()
    response.json.return_value = {"response": "not valid JSON"}
    monkeypatch.setattr(
        query_parser.requests, "post", Mock(return_value=response)
    )

    parsed = query_parser.parse_query("")

    assert parsed["tasks"] == [{"intent": "GENERAL_RAG"}]


def test_query_rewriter_skips_complete_question(monkeypatch):
    from chatbot.rag.query_rewriter import rewrite_query

    post = Mock()
    monkeypatch.setattr("chatbot.rag.query_rewriter.requests.post", post)

    query = "What is my latest haemoglobin value?"
    result = rewrite_query(
        query,
        [{"role": "user", "content": "Hello"}],
    )

    assert result == query
    post.assert_not_called()
