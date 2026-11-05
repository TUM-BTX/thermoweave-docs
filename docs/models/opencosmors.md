# Set up openCOSMO-RS

ThermoWeave wraps a **separately installed C++ backend**. Three inputs are
needed: the compiled Python module, molecular COSMO conformer files, and a
compatible parametrization. Installing the ThermoWeave Conda environment does
not download the engine or the molecular database.

## Obtain a compatible backend

The tutorials use the high-level `Model` and `load_parametrization` API of
[jnotse/openCOSMO-RS_cpp_26](https://github.com/jnotse/openCOSMO-RS_cpp_26).
That repository is private and requires separate access from its maintainers.
Its [backend documentation](https://github.com/jnotse/openCOSMO-RS-docs) also
requires access. An arbitrary installation of a different openCOSMO-RS version
may not supply the API used here.

The validated route uses x86_64 Linux and Python 3.12. Windows users should
follow the [WSL2 route](../installation/windows.md#opencosmo-rs-through-wsl2).
The backend currently uses x86 SIMD, so native Apple Silicon/ARM builds are
not supported by this code. See the [platform overview](../installation.md#choose-your-platform).

## Build for your environment

Install the [Linux build tools](../installation/linux.md#build-tools-for-opencosmo-rs)
first. In a parent folder of your choice, activate ThermoWeave and clone the
backend with its submodules:

```bash
conda activate thermoweave
git clone --recurse-submodules https://github.com/jnotse/openCOSMO-RS_cpp_26.git
cd openCOSMO-RS_cpp_26
```

Configure CMake for the **active Python interpreter**, then build. The Python
command avoids embedding any user's installation path:

```bash
python -c "import subprocess, sys; subprocess.run(['cmake', '-S', '.', '-B', 'build', '-DCMAKE_BUILD_TYPE=Release', '-DOCRS_BUILD_TESTS=OFF', '-DPython_EXECUTABLE=' + sys.executable], check=True)"
cmake --build build --parallel 2
```

The default backend build targets AVX-capable x86 hardware. Its compiler flags
must match the computer that will run it. The extension is normally created
under `build/`; locate the actual directory containing `openCOSMORS*.so`
(or `.pyd` for a native Windows build) if your build uses another output layout.
A build for Python 3.12 cannot be reused as a Python 3.13 extension. Rebuild
when changing the interpreter ABI, OS or target architecture.

Keep the backend checkout in place: bundled parametrization names are resolved
against its `parametrizations/` directory. An explicit absolute JSON path also
works. The neutral tutorial configuration uses the engine's default precision;
a double-precision build is an optional advanced choice and exports a different
module name, `openCOSMORS_double`.

## Obtain the component files

Obtain compatible COSMOconf25 Turbomole conformers through your own database
access. The input files are not included in ThermoWeave and are not generated
from SMILES during these tutorials. Place them anywhere you can read.

The supplied water/ethanol and benzene/water/ethanol tutorials expect this tree:

```text
COSMOconf25/
└── NeutralSpecies/
    ├── H2O/
    │   └── COSMO_TZVPD_FINE/
    │       └── *.cosmo
    ├── C2H6O_001_ethanol/
    │   └── COSMO_TZVPD_FINE/
    │       └── *.cosmo
    └── C6H6_001_benzene/
        └── COSMO_TZVPD_FINE/
            └── *.cosmo
```

Set the root to `COSMOconf25` or directly to `NeutralSpecies`. The helper loads
all matching `.cosmo` conformers in sorted order and prints their filenames
and hashes. To use a different database layout in your own calculations, pass
explicit component file lists to `build_cosmors_model`; the layout above is a
tutorial convention, not an engine-wide requirement.

## Choose a parametrization

| Source | How to select it |
|---|---|
| Backend-bundled Turbomole set | `default_turbomole` |
| Another bundled set | Its supported name, for example `default_orca` with compatible ORCA inputs |
| Your own compatible backend JSON | An absolute file path, such as `/path/to/parameters/my_set.json` |

A parametrization must match the COSMO file format and quantum-chemical level.
The supplied tutorials use **Turbomole COSMO_TZVPD_FINE** data and
`default_turbomole`. Their data helper does not switch to ORCA just because you
change the parameter name. Use explicit `.orcacosmo` component definitions for
an ORCA workflow.

The setting selects a source; it does not copy or convert your JSON file.
Engine-supported Julia-schema JSON files can be loaded by name or file path.
Use `load_parametrization(source)` in Python to inspect the adapted values.

## Configure the tutorials

Replace each quoted example path with an **absolute path on your computer**.
The first path contains `NeutralSpecies`; the second contains the compiled
extension. The single-line commands work without shell-specific continuation
characters:

```text
conda activate thermoweave
conda env config vars set THERMOWEAVE_COSMO_ROOT="/path/to/COSMOconf25"
conda env config vars set THERMOWEAVE_OPENCOSMORS_BUILD="/path/to/openCOSMO-RS_cpp_26/build"
conda env config vars set THERMOWEAVE_COSMO_PARAMETERS="default_turbomole"
conda deactivate
conda activate thermoweave
conda env config vars list
```

For a parameter file, replace the third command with:

```text
conda env config vars set THERMOWEAVE_COSMO_PARAMETERS="/path/to/parameters/my_set.json"
```

On native Windows use paths such as `C:/Users/you/Data/COSMOconf25`; inside WSL
use Linux paths. Spaces are allowed inside the quoted values. Do not enter the
literal `/path/to/...` placeholders. Conda saves the values per environment;
see its [environment-variable guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables).
Reactivate after changes and restart JupyterLab so new kernels inherit them.

| Variable | Used for |
|---|---|
| `THERMOWEAVE_COSMO_ROOT` | Tutorial conformer root. No default machine-specific path is assumed. |
| `THERMOWEAVE_OPENCOSMORS_BUILD` | Tutorial helper inserts this directory into Python's import path. Optional if the module is already importable. |
| `THERMOWEAVE_COSMO_PARAMETERS` | Tutorial parameter source; defaults to `default_turbomole`. |
| `THERMOWEAVE_OPENCOSMORS_MODULE` | Optional extension name; defaults to `openCOSMORS`. |

These variables are consumed by the tutorial helper and notebook setup. For
your own scripts, make the backend importable and pass component paths and a
parameter source explicitly; an example follows below.

## Verify before running SLLE

From the **ThermoWeave repository root**, with the environment active:

```text
python tools/check_cosmors_setup.py
```

The command should find all three components, load the selected parameters
and print two finite water/ethanol log activity coefficients. It changes no
parameter or database files. Then open JupyterLab from the repository root:

```text
jupyter lab tutorials/
```

Run notebook 09 for liquid activities, then notebook 12 for binary/ternary
SLLE. To execute the external notebooks without the browser interface:

```text
python tools/execute_notebooks.py --group external
```

## Use explicit paths in your own Python code

```python
import os
import sys
from pathlib import Path

# Reuse the paths saved in the activated Conda environment.
sys.path.insert(0, os.environ["THERMOWEAVE_OPENCOSMORS_BUILD"])
from thermoweave import build_cosmors_model

root = Path(os.environ["THERMOWEAVE_COSMO_ROOT"])
if (root / "NeutralSpecies").is_dir():
    root = root / "NeutralSpecies"

components = []
for name, directory in [("water", "H2O"), ("ethanol", "C2H6O_001_ethanol")]:
    files = sorted((root / directory / "COSMO_TZVPD_FINE").glob("*.cosmo"))
    if not files:
        raise FileNotFoundError(f"No conformers for {name}")
    components.append({"name": name, "paths": [str(p) for p in files]})

source = os.environ.get("THERMOWEAVE_COSMO_PARAMETERS", "default_turbomole")
model = build_cosmors_model(source, components)
print(model.ln_activity_coefficients(298.15, [0.8, 0.2]))
```

## What about DB_Component?

The supplied tutorials load molecular conformer files directly. A separate
`DB_Component` metadata database is not required for them. For larger corpora,
`ComponentArchiveResolver` accepts either a `DB_Component` directory or ZIP,
plus the COSMO root; see [production evaluation](../advanced/production-evaluation.md).
The metadata and quantum-chemical conformers are distinct inputs.
