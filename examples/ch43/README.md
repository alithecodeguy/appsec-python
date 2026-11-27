# Chapter 43 candidate review

From the repository root, use Python 3.12+ with the chapter 42 core dependency:

```shell
python -m examples.ch43.build_candidate --out /tmp/casebook-ch43-new-review
```

The three named candidate artifacts are replaced in the selected output directory. The default commit is the actual chapter
42 revision, 2c79fe0806a5a788e79afbd0adbc1c4a495a9a5d. The builder reads only
allowlisted committed files, creates a deterministic uncompressed source ZIP,
checks that the runnable working examples match the committed bytes, extracts the candidate to a temporary
folder, and runs its tests/demos there. It does not edit the index, create a
commit, install packages, deploy or promote an artifact.

The retained evidence/ directory contains the actual candidate and test/runtime
records for the manuscript. This is a source archive; Python, native libraries
and distribution packages are supplied by the local runtime, not bundled.
The selected runtime inventory is not an SBOM or advisory scan. No SLSA level,
signature, authenticated approval or production release is claimed.

manual-review.json is authored source-inspection evidence. example-findings.json
contains explicitly fictional scanner/advisory records and no real CVE claim.
release-decision.json records the worked HOLD decision, proposed owners and
mandatory gaps. They do not authorize any external action.

The recorded result is 20 core passes and three web passes on Python 3.12.14 / Django 6.1.3. The missing
real dependency scan and actual production configuration,
key custody, backup/retention and rollback gaps keep production promotion on HOLD.

Check the retained manuscript evidence (not a newly selected output directory):

```shell
python -m examples.ch43.check_evidence
```
