import os
import sys

test_env: bool = os.path.exists('.test_env')


def y_n(inp: str) -> bool:
    if inp is not None:
        print(inp)
    res: str = input().strip().lower()
    return res == 'y' or res == 'j'


def ensure_venv(file: str, args: list[str] = []) -> None:
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        pass
    else:
        print(f"Z: && cd Documents\\moritz_tools && .\\.\
              venv\\Scripts\\activate.bat && python {file} {' '.join(args)}")
        os.system(
            f"Z: && cd Documents\\moritz_tools && .\\.venv\\Scripts\\activate.bat && python {file} {' '.join(args)}")
        exit()
