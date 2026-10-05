from sentinelops.orchestrator import investigate


def test_checkout_incident_is_grounded_and_gated():
    result = investigate("checkout-api", "Why did failures start after deployment?")
    assert result.severity == "high"
    assert len(result.evidence) == 3
    assert result.requires_approval is True
    assert "v2.4.1" in result.hypothesis
