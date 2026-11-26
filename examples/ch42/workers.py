from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from examples.ch28.export_queue import run_with_retry
from examples.ch42.capstone import work


def two_workers(database, *, workspace_id, job_id, keyrings, clock):
    gate = Barrier(2,timeout=5)
    def worker():
        observations = []
        def arrive(missing):
            observations.append(missing)
            gate.wait()
        result = run_with_retry(lambda:work(database,workspace_id=workspace_id,job_id=job_id,
            keyrings=keyrings,clock=clock,after_probe=arrive if not observations else None))
        return observations[0],result
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(worker) for _ in range(2)]
        return [future.result(timeout=10) for future in futures]
