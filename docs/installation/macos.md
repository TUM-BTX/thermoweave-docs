# macOS

## Can I install openCOSMO-RS locally on my Mac?

**Yes. The updated C++ backend builds and passes numerical/API regression
checks natively on both Apple Silicon and Intel Macs.**

| Mac | Native backend | ThermoWeave SAFT installation |
|---|---|---|
| Apple Silicon (M-series, ARM64) | Tested on macOS 15, Python 3.12; `OCRS_SIMD=AUTO` selects NEON. Float and double builds pass. | Use the standard Conda environment with native ARM Python; SAFT macOS CI is separate from the backend checks. |
| Intel (x86_64) | Tested on macOS 15, Python 3.12; `AUTO` selects AVX. | Use the COSMO-RS/core environment below if current JAX wheels are unavailable for Intel macOS. |

Use a backend checkout containing the [native portability change](https://github.com/jnotse/openCOSMO-RS_cpp_26/commit/b32d7b9377a7797bffede8e42792c2468c59e8a0).
Older versions of our fork lack the ARM path. The port brings in the upstream
NEON/scalar SIMD abstraction while retaining the established x86 calculation
paths. See the [passing native checks](https://github.com/jnotse/openCOSMO-RS_cpp_26/actions/runs/42194095644).
The backend and its test logs require access to that private repository.

## 1. Install native tools

Install [Miniforge](https://github.com/conda-forge/miniforge#download) for the
Mac's architecture and [Git](https://git-scm.com/downloads). On an M-series Mac,
choose ARM64; on an Intel Mac, choose x86_64. Install Apple's C++ command-line
tools if they are missing:

```bash
xcode-select --install
```

Complete the installer dialog before building. Avoid mixing an ARM Python
with Intel libraries or an Intel Python with ARM libraries. You can inspect
the active interpreter with:

```text
python -c "import platform, sys; print(platform.machine()); print(sys.executable)"
```

## 2. Set up ThermoWeave

### Apple Silicon: SAFT and COSMO-RS

Follow the [common installation guide](../installation.md) to create and
activate `thermoweave`. It installs SAFT/SMILES and notebook dependencies.
The C++ COSMO-RS engine is built separately in step 3 below.

### Intel: COSMO-RS without requiring JAX

Current JAX wheel documentation does not list Intel macOS. This does **not**
prevent installing ThermoWeave's COSMO-RS adapter, which does not require JAX.
From a ThermoWeave checkout, create an environment for COSMO-RS and notebooks:

```text
conda create -n thermoweave python=3.12 pip
conda activate thermoweave
python -m pip install -e ".[tutorials]"
python -m ipykernel install --user --name thermoweave --display-name "Python (ThermoWeave)"
```

If you already created a suitable environment, activate it instead of creating
it again. This core/COSMO-RS installation does not include SAFT EOS evaluations.

## 3. Build the C++ backend

Keep the intended Conda environment active. In a parent folder of your choice:

```bash
git clone --recurse-submodules https://github.com/jnotse/openCOSMO-RS_cpp_26.git
cd openCOSMO-RS_cpp_26
python -m pip install 'cmake>=3.15,<4' ninja numpy
python -c "import subprocess, sys; subprocess.run(['cmake', '-S', '.', '-B', 'build', '-G', 'Ninja', '-DCMAKE_BUILD_TYPE=Release', '-DOCRS_BUILD_TESTS=OFF', '-DOCRS_SIMD=AUTO', '-DPython_EXECUTABLE=' + sys.executable], check=True)"
cmake --build build --parallel 2
```

For an existing checkout, use `git pull` and update its submodules rather than
cloning again. Start with a fresh build directory if an old CMake cache points
to a different Python, architecture or source location.

`AUTO` selects NEON on Apple Silicon and AVX on Intel. `OCRS_SIMD=SCALAR` is an
explicit portable fallback. Keep the default `AUTO` choice for the documented
native route. The upstream option name `OPENCOMSORS_SIMD` is also accepted.

OpenMP is optional. Apple's Clang can build a working serial backend without
OpenMP; a missing OpenMP package alone is not a reason to stop the build.

## 4. Verify and configure the backend

Still inside the backend checkout:

```text
python -c "import sys; sys.path.insert(0, 'build'); import openCOSMORS; print(openCOSMORS.__file__); print(openCOSMORS.load_parametrization('default_turbomole')['metadata'])"
python -c "from pathlib import Path; print((Path.cwd() / 'build').resolve())"
```

Use the absolute build directory printed by the second command as
`THERMOWEAVE_OPENCOSMORS_BUILD`. Configure that location, your molecular COSMO
files and your parameter source using the
[database/parametrization instructions](../models/opencosmors.md#configure-the-tutorials).
Keep the backend checkout in place for bundled parameter names.

Then return to the **ThermoWeave repository root** and run:

```text
python tools/check_cosmors_setup.py
jupyter lab tutorials/
```

Select **Python (ThermoWeave)** and run notebook 09, followed by notebook 12
for binary and ternary SLLE. Your real conformer inputs are still required.

## What was validated?

The backend CI compiled and ran real-input Model/legacy API, conformer,
composition-derivative, solvation and electrolyte-diagnostic checks on native
macOS 15 Intel and ARM64 runners. Independent SIMD tests check float/double
products, sums, unaligned inputs and tail bounds. Linux AVX and scalar builds
passed the same checks. Full ThermoWeave SLLE notebooks were not executed on
the Mac runners; their saved calculations were validated separately on Linux.
