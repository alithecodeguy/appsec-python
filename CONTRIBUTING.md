# Contributing

[Repository](README.md) · [Book contents](manuscript/README.md#contents) · [Examples](examples/README.md)

Corrections to explanations, examples, links and accessibility are welcome. Use the repository's [issue templates](https://github.com/alithecodeguy/appsec-python/issues/new/choose) to report a problem or suggest an improvement. Keep real credentials and private data out of issues, patches and test output.

## Make a focused change

1. Name the chapter and section, describe the problem and give a small reproduction when applicable.
2. Edit the manuscript in `manuscript/`. Keep chapter filenames `01.md` through `44.md` stable so existing links keep working.
3. Follow the [writing guide](book-context.md): short sentences, consistent terminology, copyable listings, explicit starting state and explained results.
4. When changing a shipped example, update the matching manuscript listing and test the relevant behavior. Keep deliberately incorrect examples clearly labeled.
5. Describe what you checked and any remaining verification gap in your pull request.

Casebook's recurring rule matters across chapters: the reader needs current active membership in the note's stored workspace. Lee manages Alpha only. Queued exports recheck current authority before releasing private data. Check permitted, refused and revoked cases when a change affects that rule.

## Check Markdown and navigation

Run from the repository root with Python 3.9 or later. This check needs only the standard library and Git; it does not install the example dependencies.

```shell
python3 scripts/check_book.py
```

It checks chapter coverage, generated navigation, code-fence closure and local Markdown file/heading links. It does not request external websites, parse Mermaid or execute chapter examples. The GitHub workflow runs the same check on pushes and pull requests.

Chapter navigation and section lists live between `<!-- book:header:start -->` / `<!-- book:header:end -->` and the equivalent footer markers. After changing a chapter's headings, regenerate them:

```shell
python3 scripts/check_book.py --write
git diff --check
```

Commit the refreshed Markdown along with the change. The generator is repeatable; edit chapter text outside its markers. Inspect diagrams and tables in GitHub's Markdown Preview after a rendering change. Keep diagrams in fenced `mermaid` blocks with captions and a prose explanation.

## Check runnable examples

Follow [tested-versions.md](tested-versions.md) for the exact interpreter, dependencies and commands. Run Django laboratories in separate processes because they configure different settings. A change to prose or navigation does not require rerunning every application test.

The JSON reports and source archives under `examples/` are retained evidence for specific runs. Do not overwrite them merely to make a check green. The full verifier accepts `--out` for a fresh report outside the reviewed ledger:

```shell
./.venv/bin/python examples/verify_book.py --out /tmp/casebook-book-verification.json
```

For changed executable sources, collect new results, identify their subject and update the associated narrative and evidence together. A changed capstone candidate also requires a corresponding review of its evidence hashes and decision ledger. Do not present local test results as browser, cloud or production evidence.
