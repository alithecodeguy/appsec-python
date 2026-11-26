# Chapter 28 concurrency laboratory

Run from the repository root with Python 3.12 or later:

```shell
python -m pip install -r examples/ch28/requirements.txt
python -m examples.ch28.queue_demo
python -m examples.ch28.cancellation
python -m unittest -v examples.ch28.test_queue
```

Keep chapter 23's authorization module and chapter 27's export crypto module
unchanged. Each run uses temporary SQLite files and disposable AES keys.
Two threads use separate database connections. A barrier forces both diagnostic
reads to finish before either write. Database uniqueness, not the barrier,
enforces one result per request. No live broker or Django endpoint is supplied.
