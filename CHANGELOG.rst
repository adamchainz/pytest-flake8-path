=========
Changelog
=========

* Switch package build backend from setuptools to `uv_build <https://docs.astral.sh/uv/concepts/build-backend/>`__.
  This makes builds with uv about nine times faster, since uv runs the backend natively, without creating a build environment or spawning a Python process.
  Additionally, source distributions no longer include test files, which setuptools previously included incompletely, missing the files needed to actually run them.

* Drop Python 3.9 support.

1.7.0 (2025-09-09)
------------------

* Support Python 3.14.

1.6.0 (2024-10-25)
------------------

* Drop Python 3.8 support.

* Support Python 3.13.

1.5.0 (2023-07-10)
------------------

* Drop Python 3.7 support.

1.4.0 (2023-06-16)
------------------

* Support Python 3.12.

1.3.0 (2022-05-11)
------------------

* Support Python 3.11.

1.2.0 (2022-01-10)
------------------

* Drop Python 3.6 support.

1.1.0 (2021-08-11)
------------------

* Normalize file paths in output on Windows to Unix format. This allows test
  suites to run the same on all operating systems. Fixes `pytest-flake8dir
  Issue #103 <https://github.com/adamchainz/pytest-flake8dir/issues/103>`__.

1.0.0 (2021-08-10)
------------------

* Initial release, ported from `pytest-flake8dir
  <https://pypi.org/project/pytest-flake8dir/>`__.
