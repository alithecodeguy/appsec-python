import json
from pathlib import Path


EXPECTED_CSP = {
    "default-src": frozenset({"'none'"}),
    "script-src": frozenset({"'none'"}),
    "object-src": frozenset({"'none'"}),
    "base-uri": frozenset({"'none'"}),
    "form-action": frozenset({"'self'"}),
    "frame-ancestors": frozenset({"'none'"}),
}
ENFORCED_CSP = "; ".join(name + " " + " ".join(sorted(values))
                         for name, values in EXPECTED_CSP.items())


def response_policy_failures(headers):
    # A strict contract for one normalized header mapping, not a general CSP parser.
    headers = {name.lower(): value for name, value in headers.items()}
    failures = []
    cache = {part.strip().lower() for part in headers.get("cache-control", "").split(",")}
    if "no-store" not in cache:
        failures.append("missing Cache-Control no-store")
    enforced = headers.get("content-security-policy")
    if not enforced:
        failures.append("missing enforced Content-Security-Policy")
        return failures
    directives = {}
    for part in enforced.split(";"):
        words = part.split()
        if not words:
            continue
        name = words[0].lower()
        if name in directives:
            failures.append("duplicate CSP directive")
            return failures
        directives[name] = frozenset(words[1:])
    if directives != EXPECTED_CSP:
        failures.append("enforced CSP differs from the fixture contract")
    return failures


def main():
    report = json.loads(Path(__file__).with_name("passive-report.json").read_text())
    assert report["provenance"] == "authored teaching fixture"
    failures = response_policy_failures(report["response"]["headers"])
    print("Observation:", report["capture_id"], report["response"]["status"])
    print("Header contract:", "PASS" if not failures else "FAIL")
    for failure in failures:
        print("-", failure)


if __name__ == "__main__":
    main()
