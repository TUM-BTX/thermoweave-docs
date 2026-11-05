# Install ThermoWeave

This guide starts from a new computer. The recommended installation creates a
named Conda environment called `thermoweave`, with Python 3.12, the SAFT model,
automatic SMILES assignment, JupyterLab and development tools. No GPU is needed.

## 1. Install the prerequisites

1. Install [Miniforge](https://github.com/conda-forge/miniforge#download) for your
   operating system and CPU architecture. An existing Conda installation also
   works; you do not need a second one.
2. Install [Git](https://git-scm.com/downloads).
3. Obtain access to the private
   [TUM-BTX/ThermoWeave repository](https://github.com/TUM-BTX/ThermoWeave).
   Use an authenticated GitHub account when cloning over HTTPS. If GitHub asks
   for credentials, follow its [HTTPS authentication instructions](https://docs.github.com/en/get-started/git-basics/about-remote-repositories#cloning-with-https-urls).

Open a terminal on Linux/macOS, or the **Miniforge Prompt** on Windows. Check:

```text
conda --version
git --version
```

If `conda` is unavailable, finish the installer's shell initialization and open
a new terminal. On Windows, start with the Miniforge Prompt before configuring
PowerShell or another editor terminal.

## Choose your platform

| Platform | ThermoWeave + CPU SAFT | Optional C++ openCOSMO-RS |
|---|---|---|
| Linux x86_64 | This is the locally validated and CI-tested platform. | Supported build route; see the [Linux guide](installation/linux.md). |
| Windows x86_64 | Follow the [Windows guide](installation/windows.md); this project has not run Windows CI. | The documented route uses Linux through WSL2. |
| macOS Apple Silicon | JAX supplies ARM CPU wheels; this project has not run macOS CI. | The current backend uses x86 SIMD; use a compatible remote x86_64 Linux machine. |
| macOS Intel | Current JAX CPU wheel support does not include Intel macOS. | Use a compatible Linux machine for the documented workflow. |
| Linux ARM or other architectures | Consult JAX availability; not validated by this project. | The current backend's x86 SIMD code is a limitation. |

[JAX's installation guide](https://docs.jax.dev/en/latest/installation.html)
is the reference for current CPU/OS support. See the [macOS guide](installation/macos.md)
for the distinction between native SAFT and the optional COSMO-RS backend.
These instructions identify supported routes; they do not promise that every
external engine runs natively on every architecture.

## 2. Clone the library

Choose any parent folder where you want to keep the source and tutorial files:

```text
git clone https://github.com/TUM-BTX/ThermoWeave.git
cd ThermoWeave
```

All commands below that refer to `environment.yml`, `tutorials/` or `tools/`
are run from this **repository root**, the folder containing `pyproject.toml`.
No username-specific directory is required. If you already cloned it, enter
that checkout and run `git pull` instead of cloning again.

## 3. Create and activate the environment

```text
conda env create -f environment.yml
conda activate thermoweave
```

Create it once. In a new terminal, only `conda activate thermoweave` is needed.
The environment file installs Python and pip through Conda, then installs
ThermoWeave and its extras inside that environment through pip. The environment
is stored by Conda separately from your project folders.

If you already have an environment named `thermoweave`, activate it rather than
running the creation command again. See [updates](#updates-and-alternative-installations)
when updating an existing installation.

## 4. Check the installation

```text
python -m pip check
python -c "import sys, thermoweave, jax, rdkit; print(sys.executable); print(thermoweave.__file__); print(jax.devices())"
```

`pip check` should report no broken requirements. The interpreter should belong
to the Conda environment and JAX should list a device. Use a notebook or a
Python file to run the [first calculation](index.md#a-first-calculation).
A pressure close to 101325 Pa confirms the density/pressure round trip. The
first SAFT call compiles JAX kernels and takes longer than later calls.

## 5. Open the tutorials

```text
python -m ipykernel install --user --name thermoweave --display-name "Python (ThermoWeave)"
jupyter lab tutorials/
```

Select **Python (ThermoWeave)** as the notebook kernel and start with notebook
00. Register the kernel once; start JupyterLab again whenever you need it.
The [tutorial index](tutorials.md) identifies which examples need external data.
SAFT notebooks 00–08, 10 and 11 need no external COSMO files.

## 6. Add optional models

The standard installation is sufficient for SAFT and its binary/ternary SLLE
examples. Additional models have their own setup guides:

- [openCOSMO-RS](models/opencosmors.md): build/import the compatible backend,
  configure the conformer database location and choose a parametrization.
- [HANNA](models/hanna.md): install its Python dependencies and obtain its
  upstream model assets.

## Work from any folder

Activate the same environment in any project directory:

```text
conda activate thermoweave
python your_calculation.py
```

Your scripts and notebooks can live outside the ThermoWeave repository. In an
editor, select the environment's Python interpreter; in Jupyter, select
**Python (ThermoWeave)**. Starting Jupyter from another directory with
`jupyter lab .` opens that directory.

The environment file uses an **editable** install (`-e`): imports read the
library code from the source checkout. Keep that checkout in place. To copy
the library into the environment instead, run this from the repository root:

```text
python -m pip install ".[saft-smiles,tutorials,dev]"
```

A regular install stays available if the source folder is moved or removed.
Its code updates require reinstalling. The tutorial files remain in the source
checkout in either case.

## Updates and alternative installations

To update the library and requirements, run from the existing checkout:

```text
conda activate thermoweave
git pull
python -m pip install -e ".[saft-smiles,tutorials,dev]"
python -m pip check
```

If the environment file's Python/Conda requirements change, create a new named
environment from that file rather than treating a pip update as a Python upgrade:
`conda env create -n thermoweave-new -f environment.yml`.

For a manual environment setup, from the repository root:

```text
conda create -n thermoweave python=3.12 pip
conda activate thermoweave
python -m pip install -e ".[saft-smiles,tutorials,dev]"
```

| Extra | Adds |
|---|---|
| none | NumPy, SciPy and mpmath interval arithmetic |
| `saft` | JAX and export serialization |
| `saft-smiles` | SAFT plus RDKit for group assignment |
| `tutorials` | JupyterLab, notebook runner and Matplotlib |
| `hanna` | HANNA's Python dependencies; obtain model assets separately |
| `dev` | pytest and package-building tools; optional for calculations |

Use `python -m pip` after activating the intended environment. If something
fails, continue with [verification and troubleshooting](installation/troubleshooting.md).
