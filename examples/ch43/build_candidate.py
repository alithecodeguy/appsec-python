"""Build an allowlisted source candidate from a Git commit and test its extracted bytes."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import zipfile

SOURCE_COMMIT = "2c79fe0806a5a788e79afbd0adbc1c4a495a9a5d"
DEPENDENCIES = [
    "examples/ch23/authorization_service.py", "examples/ch27/export_crypto.py",
    "examples/ch28/export_queue.py", "examples/ch28/cancellation.py",
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


RUNNER = r'''
import hashlib, importlib, importlib.metadata as metadata, importlib.util
import io,json,os,platform,sqlite3,sys,unittest
from pathlib import Path
root=Path.cwd().resolve()
results={}
for name in ("test_capstone","test_web"):
    module=importlib.import_module("examples.ch42."+name)
    assert Path(module.__file__).resolve().is_relative_to(root)
    output=io.StringIO()
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
    results[name]={"run":result.testsRun,"passed":result.testsRun-len(result.skipped)-len(result.failures)-len(result.errors),
        "skipped":len(result.skipped),"failures":len(result.failures),"errors":len(result.errors),
        "successful":result.wasSuccessful(),"transcript":output.getvalue()}
origins={}
for name in ("examples.ch23.authorization_service","examples.ch27.export_crypto","examples.ch28.export_queue",
             "examples.ch28.cancellation","examples.ch42.capstone","examples.ch42.fixtures","examples.ch42.workers"):
    module=importlib.import_module(name)
    path=Path(module.__file__).resolve()
    assert path.is_relative_to(root), (name,path)
    origins[name]=str(path.relative_to(root))
packages={}
for name in ("cryptography","cffi","pycparser","Django"):
    try:
        dist=metadata.distribution(name)
    except metadata.PackageNotFoundError:
        packages[name]={"installed":False}
    else:
        info=dist.read_text("METADATA")
        packages[name]={"installed":True,"version":dist.version,"requires":dist.requires or [],
            "metadata_sha256":hashlib.sha256(info.encode()).hexdigest()}
import cryptography
from cryptography.hazmat.backends import default_backend
origin=Path(cryptography.__file__).resolve()
packages["cryptography"]["import_origin"]=str(origin)
packages["cryptography"]["import_file_sha256"]=hashlib.sha256(origin.read_bytes()).hexdigest()
print(json.dumps({"tests":results,"candidate_module_origins":origins,
    "runtime":{"python":platform.python_version(),"implementation":platform.python_implementation(),
               "sqlite":sqlite3.sqlite_version,"cryptography_openssl":default_backend().openssl_version_text()},
    "runtime_packages":packages,"tool_availability":{name:importlib.util.find_spec(name) is not None
        for name in ("bandit","pip_audit","django")}},indent=2))
'''


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--commit",default=SOURCE_COMMIT)
    parser.add_argument("--out",type=Path,default=Path("examples/ch43/evidence"))
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    def git(*parts):
        return subprocess.check_output(["git","-C",str(root),*parts])
    commit=git("rev-parse","--verify",args.commit+"^{commit}").decode().strip()
    tracked=git("ls-tree","-r","--name-only",commit,"examples/ch42").decode().splitlines()
    names=[name for name in tracked if name.endswith(".py") or Path(name).name.startswith("requirements")]+DEPENDENCIES
    assert names and all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in names)
    contents={name:git("show",f"{commit}:{name}") for name in sorted(set(names))}
    for name,data in contents.items():
        if name.endswith(".py"): ast.parse(data,filename=name)
    for name,data in contents.items():
        assert (root/name).read_bytes()==data, f"Working example differs from selected commit: {name}"
    args.out.mkdir(parents=True,exist_ok=True)
    archive=args.out/"candidate-source.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_STORED) as bundle:
        for name,data in contents.items():
            info=zipfile.ZipInfo(name,date_time=(2000,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644 << 16
            bundle.writestr(info,data)
    digest=sha(archive.read_bytes())
    subject={"source_commit":commit,"artifact":"candidate-source.zip","artifact_sha256":digest,
             "kind":"allowlisted source ZIP; runtime dependencies are NOT bundled"}
    (args.out/"candidate.json").write_text(json.dumps({**subject,"files_sha256":{name:sha(data) for name,data in contents.items()},
        "builder_sha256":sha(Path(__file__).read_bytes()),"provenance":"local unsigned build record; no SLSA level claim"},indent=2)+"\n")
    with TemporaryDirectory(prefix="casebook-ch43-candidate-") as folder:
        extracted=Path(folder)
        # Extract only the builder's own validated allowlist, not an arbitrary supplied archive.
        with zipfile.ZipFile(archive) as bundle:
            for name in contents:
                destination=extracted/name
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_bytes(bundle.read(name))
                assert sha(destination.read_bytes())==sha(contents[name])
        env={**os.environ,"PYTHONPATH":str(extracted),"PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1"}
        process=subprocess.run([sys.executable,"-c",RUNNER],cwd=extracted,env=env,capture_output=True,text=True,check=True)
        observed=json.loads(process.stdout)
        demos={}
        for stage in ("admission","worker","lifecycle"):
            process=subprocess.run([sys.executable,"-m","examples.ch42.demo","--stage",stage],
                cwd=extracted,env=env,capture_output=True,text=True,check=True)
            demos[stage]=process.stdout
    report={"evidence_kind":"actual local execution of extracted candidate source",**subject,
            "collected_at_utc":datetime.now(timezone.utc).isoformat(),**observed,"demonstrations":demos,
            "dependency_scope":"selected observed local runtime distributions; not a complete SBOM, lock or advisory scan",
            "working_tree_used":False,"baseline_python":"3.12.14",
            "baseline_python_tested":observed["runtime"]["python"]=="3.12.14"}
    (args.out/"candidate-run.json").write_text(json.dumps(report,indent=2)+"\n")
    print("commit:",commit)
    print("artifact SHA-256:",digest)
    for name,result in observed["tests"].items():
        print(name+":",result["passed"],"passed,",result["skipped"],"skipped")
    print("dependency/advisory scan: MISSING")
    print("production promotion: HOLD (mandatory integration/configuration/recovery evidence incomplete)")
    if not all(result["successful"] for result in observed["tests"].values()):
        raise SystemExit("Candidate tests failed; retained reports are failure evidence")


if __name__=="__main__":
    main()
