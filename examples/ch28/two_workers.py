from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from examples.ch28.export_queue import process_request, run_with_retry


def coordinated_workers(database, *, request_id, keyring, now):
    gate = Barrier(2, timeout=5)
    def worker():
        observations = []  # Each worker owns this list.
        def arrive(missing):
            observations.append(missing)
            gate.wait()
        # Coordinate only the first attempt; retrying must not wait for a departed peer.
        def attempt():
            hook = arrive if not observations else None
            return process_request(database, request_id=request_id, keyring=keyring, now=now, after_probe=hook)
        outcome = run_with_retry(attempt)
        return observations[0], outcome
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(worker) for _ in range(2)]
        return [future.result(timeout=10) for future in futures]
