# setting up development environment

## 1. ensure development dependencies are installed

Development and runtime dependencies are listed in the main [README.md](../README.md#install-from-source-code)

## 2. Make sure submodules are initialized and updated

```bash
$ git submodule update --init --remote --recursive
```

## 3. set up environment

Set up virtual environment:

```bash
$ python3 -m venv .venv
```

Activate Environment:

```bash
$ source .venv/bin/activate
```

Install project in editable mode:

```bash
# meson-python for --no-build-isolation, dev.txt for PyGObject special settings
(.venv) $ python3 -m pip install meson-python -r dev.txt
# '.' is the location of the project, '[test,dev]' installs development dependencies
(.venv) $ python3 -m pip install -Cbuild-dir=build/meson --no-build-isolation --editable .'[test,dev]'
# install pre-commit hooks
(.venv) $ pre-commit install
```
This installs the dependencies and typing stubs.  The resources can be found in `build/meson/data`.
The program should be launched with `bin/run-local.py`.

Remember to activate the virtual environment in your IDE or command line before launching

When changing resources or `*.in` files,
`python3 -m pip install -Cbuild-dir=build/meson --no-build-isolation --editable .'[test,dev]'`
needs to be re-run to update.

