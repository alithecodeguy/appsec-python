import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory


async def fixture_worker(queue, root, started, release):
    request_id = await queue.get()
    try:
        # The task owns its private directory and closes its file before the suspension point.
        with TemporaryDirectory(prefix="partial-", dir=root) as folder:
            with (Path(folder)/"part.bin").open("wb") as stream:
                stream.write(b"synthetic fixture only\n")
            started.set()
            await release.wait()  # Controlled long wait; no timing-based sleep.
            return request_id
    finally:
        queue.task_done()  # Accounting for this get, not a success acknowledgement.


async def cancellation_case():
    with TemporaryDirectory(prefix="casebook-cancel-") as root:
        queue = asyncio.Queue(maxsize=1)
        queue.put_nowait(1)  # Only a stored request ID belongs on the queue.
        try:
            queue.put_nowait(2)
        except asyncio.QueueFull:
            backpressure = True
        else:
            backpressure = False
        started, release = asyncio.Event(), asyncio.Event()
        task = asyncio.create_task(fixture_worker(queue, root, started, release))
        cancelled = False
        try:
            async with asyncio.timeout(2):
                await started.wait()
            partial_exists = any(Path(root).iterdir())
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                cancelled = True
            async with asyncio.timeout(2):
                await queue.join()
            return {"backpressure":backpressure, "partial_exists":partial_exists,
                    "cancelled":cancelled, "remaining_files":len(list(Path(root).iterdir())),
                    "queued_ids":queue.qsize()}
        finally:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass


if __name__ == "__main__":
    for name, value in asyncio.run(cancellation_case()).items():
        print(name + ":", value)
