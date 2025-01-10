from mt import ensure_venv
ensure_venv(__file__)

import os
processes: list[str] = os.popen(
    'wmic process get description').read().splitlines()
processes = [process.strip() for process in processes]

print(processes)
