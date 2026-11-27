"""Check local evidence consistency. This does not authenticate reports or approve release."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile


def main():
    root=Path(__file__).resolve().parents[2]
    review=root/"examples/ch43"
    def read(name): return json.loads((review/name).read_text())
    def digest(data): return hashlib.sha256(data).hexdigest()
    candidate=read("evidence/candidate.json")
    archive=review/"evidence"/candidate["artifact"]
    assert digest(archive.read_bytes())==candidate["artifact_sha256"],"artifact changed"
    with zipfile.ZipFile(archive) as bundle:
        assert set(bundle.namelist())==set(candidate["files_sha256"]),"archive inventory differs"
        for name,expected in candidate["files_sha256"].items():
            committed=subprocess.check_output(["git","-C",str(root),"show",f'{candidate["source_commit"]}:{name}'])
            assert digest(bundle.read(name))==expected==digest(committed),name
            assert digest((root/name).read_bytes())==expected,("working example differs",name)
    assert digest((review/"build_candidate.py").read_bytes())==candidate["builder_sha256"],"builder changed"
    for name in ("evidence/candidate-run.json","manual-review.json","example-findings.json","release-decision.json"):
        record=read(name)
        for field in ("source_commit","artifact_sha256"):
            assert record[field]==candidate[field],(name,field)
    decision=read("release-decision.json")
    for name,expected in decision["evidence_sha256"].items():
        assert digest((review/name).read_bytes())==expected,name
    assert {row["id"] for row in decision["controls"]}=={f"EXP-{n:02}" for n in range(1,13)}
    print("candidate/evidence consistency: PASS")
    print("mandatory control rows:",len(decision["controls"]))
    print("production decision:",decision["decision"])
    print("scope: unsigned local records; not authenticated release approval")


if __name__=="__main__":
    main()
