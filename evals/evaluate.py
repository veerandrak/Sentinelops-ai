from sentinelops.orchestrator import investigate

CASES = [
    {"service": "checkout-api", "question": "Why are 5xx errors rising?", "expected_approval": True},
    {"service": "unknown-service", "question": "Investigate the service", "expected_approval": False},
]


def main() -> None:
    passed = 0
    for case in CASES:
        result = investigate(case["service"], case["question"])
        ok = result.requires_approval == case["expected_approval"] and bool(result.evidence)
        passed += int(ok)
        print(f"{'PASS' if ok else 'FAIL'}: {case['service']}")
    print(f"score={passed}/{len(CASES)} ({passed / len(CASES):.0%})")


if __name__ == "__main__":
    main()
