# Chapter 30 control verification

Use Python 3.12.14, Django 6.1.3 and Hypothesis 6.170.17 from the root tested requirements. Run each command in its own process from the repository root:

```shell
python -m unittest -v examples.ch30.test_http
python -m unittest -v examples.ch30.test_local
python -m examples.ch30.shrink_demo
```

The HTTP/property suite passes four methods. The local suite passes six methods, including 93 bounded layouts. The shrinking demonstration prints and rechecks a foreign-note counterexample for a deliberately broken global reader. The supplied passive report remains authored input, not an executed scanner result. Browser-engine and deployed hosting behavior are outside these local checks.
