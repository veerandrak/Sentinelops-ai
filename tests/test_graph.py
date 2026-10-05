from sentinelops.graph import build_graph


def test_graph_requires_approval_for_correlated_checkout_incident():
    result = build_graph().invoke(
        {"service": "checkout-api", "question": "Why are 5xx errors rising?"}
    )
    assert result["requires_approval"] is True
    assert len(result["evidence"]) == 3
    assert result["context"]
