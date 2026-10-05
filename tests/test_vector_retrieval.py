from sentinelops.vector_retrieval import retrieve

def test_retrieval_returns_source_and_score():
    hits=retrieve("checkout API DB timeout deployment")
    assert hits
    assert hits[0]["source"].endswith("checkout-api.md")
    assert 0 <= hits[0]["score"] <= 1
