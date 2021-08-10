import subprocess
import sys
from pathlib import Path
from typing import Generator, List, Optional

import pytest
from _pytest.tmpdir import TempPathFactory


class Flake8Result:
    def __init__(self, out: str, err: str, exit_code: int) -> None:
        self.out = out
        self.out_lines = out.strip().splitlines()
        self.err = err
        self.err_lines = err.strip().splitlines()
        self.exit_code = exit_code


BasePathType = type(Path())


class Flake8Path(BasePathType):
    def run_flake8(self, extra_args: Optional[List[str]] = None) -> Flake8Result:
        args = [
            sys.executable,
            "-m",
            "flake8",
            "--jobs",
            "1",
            "--config",
            "setup.cfg",
            ".",
        ]
        if extra_args:
            args.extend(extra_args)

        process = subprocess.Popen(
            args=args,
            cwd=str(self),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        process.wait()

        # type narrowing
        assert process.stdout is not None
        assert process.stderr is not None

        return Flake8Result(
            out=process.stdout.read(),
            err=process.stderr.read(),
            exit_code=process.returncode,
        )


@pytest.fixture
def flake8_path(tmp_path_factory: TempPathFactory) -> Generator[Flake8Path, None, None]:
    path = Flake8Path(tmp_path_factory.mktemp("flake8_path"))
    (path / "setup.cfg").write_text("[flake8]\n")
    yield path
