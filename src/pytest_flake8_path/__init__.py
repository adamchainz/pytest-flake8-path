from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Generator

import pytest
from _pytest.tmpdir import TempPathFactory


class Flake8Result:
    def __init__(self, out: str, err: str, exit_code: int) -> None:
        self.out = out
        self.out_lines: list[str] = []
        for line in out.strip().splitlines():
            if ":" in line:
                filename, rest = line.split(":", 1)
                norm_filename = filename.replace("\\", "/")
                self.out_lines.append(f"{norm_filename}:{rest}")
            else:
                self.out_lines.append(line)
        self.err = err
        self.err_lines = err.strip().splitlines()
        self.exit_code = exit_code


if TYPE_CHECKING:
    BasePathType = Path
else:
    # Have to extend concrete type, which is determined in Path.__new__
    BasePathType = type(Path())


class Flake8Path(BasePathType):
    def run_flake8(self, extra_args: list[str] | None = None) -> Flake8Result:
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

        process = subprocess.run(
            args=args,
            cwd=str(self),
            capture_output=True,
            text=True,
        )
        return Flake8Result(
            out=process.stdout,
            err=process.stderr,
            exit_code=process.returncode,
        )


@pytest.fixture
def flake8_path(tmp_path_factory: TempPathFactory) -> Generator[Flake8Path, None, None]:
    path = Flake8Path(tmp_path_factory.mktemp("flake8_path"))
    (path / "setup.cfg").write_text("[flake8]\n")
    yield path
