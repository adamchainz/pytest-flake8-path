from __future__ import annotations

import os
from textwrap import dedent

import flake8

from pytest_flake8_path import Flake8Result

# Prevent Flake8 from running in dev mode because it returns some problems
os.environ.pop("PYTHONDEVMODE", None)


def test_windows_path_normalization():
    result = Flake8Result(
        out=(
            ".\\example.py:1:2: E221 multiple spaces before operator\n"
            + "Flake8 is here!\n"
        ),
        err="",
        exit_code=0,
    )
    assert result.out_lines == [
        "./example.py:1:2: E221 multiple spaces before operator",
        "Flake8 is here!",
    ]


def test_simple_run(flake8_path):
    (flake8_path / "example.py").write_text("x  = 1\n")

    result = flake8_path.run_flake8()

    assert result.out_lines == [
        "./example.py:1:2: E221 multiple spaces before operator"
    ]
    assert result.err_lines == []
    assert result.exit_code == 1


def test_multi_line(flake8_path):
    (flake8_path / "example.py").write_text(
        dedent(
            """\
            x  = 1
            y  = 2
            """
        )
    )

    result = flake8_path.run_flake8()

    assert result.out_lines == [
        "./example.py:1:2: E221 multiple spaces before operator",
        "./example.py:2:2: E221 multiple spaces before operator",
    ]
    assert result.err_lines == []
    assert result.exit_code == 1


def test_with_setup_cfg(flake8_path):
    (flake8_path / "setup.cfg").write_text(
        dedent(
            """\
            [flake8]
            ignore = E221
            """
        )
    )
    (flake8_path / "example.py").write_text("x  = 1\n")

    result = flake8_path.run_flake8()

    assert result.out_lines == []
    assert result.err_lines == []
    assert result.exit_code == 0


def test_error_output(flake8_path):
    (flake8_path / "setup.cfg").write_text(
        dedent(
            """
            [flake8]
            extend-select = MC1

            [flake8:local-plugins]
            extension =
                MC1 = example:MyChecker1
            paths = .
            """
        )
    )
    (flake8_path / "example.py").write_text(
        dedent(
            """
            import warnings

            warnings.warn("This is a warning!", UserWarning)


            class MyChecker1:
                name = "MyChecker1"
                version = "1"

                def __init__(self, tree):
                    self.tree = tree

                def run(self):
                    if False:
                        yield
            """
        )
    )

    result = flake8_path.run_flake8()

    assert "This is a warning!" in result.err
    assert result.err_lines[0].endswith("UserWarning: This is a warning!")
    assert result.err_lines[1] == '  warnings.warn("This is a warning!", UserWarning)'


def test_extra_args(flake8_path):
    (flake8_path / "example.py").write_text("x  = 1\n")

    result = flake8_path.run_flake8(["--ignore", "E221"])

    assert result.out_lines == []
    assert result.err_lines == []
    assert result.exit_code == 0


def test_extra_args_version(flake8_path):
    result = flake8_path.run_flake8(extra_args=["--version"])
    assert result.out.startswith(flake8.__version__ + " ")


def test_separate_tmp_path(flake8_path, tmp_path):
    (flake8_path / "example.py").write_text("x  = 1\n")
    assert not (tmp_path / "example.py").exists()
