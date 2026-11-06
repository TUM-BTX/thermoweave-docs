# macOS

## Can I install openCOSMO-RS locally on my Mac?

**The C++ backend used by ThermoWeave currently has no validated local macOS
installation route.** Its status depends on the Mac's CPU:

| Mac | Native openCOSMO-RS installation |
|---|---|
| Apple Silicon (M-series, ARM) | **Unsupported by the current backend.** Its x86 SSE3/AVX instructions need an ARM-compatible implementation before it can build natively. |
| Intel (x86_64) | **Unvalidated.** The CPU architecture is compatible, so a local build may be possible, but this project has not tested it or provided verified macOS build instructions. |

To use the validated workflow **from a Mac**, run the backend and notebook
kernel on a compatible **x86_64 Linux machine** and connect to Jupyter from the
Mac's browser. The computation then runs on Linux. A Linux environment with an
ARM CPU does not satisfy the backend's x86 requirement.

This concerns `openCOSMO-RS_cpp_26`, the backend required by these tutorials.
The ThermoWeave Python library and the SAFT model have separate requirements,
explained below. Installing the Conda environment alone does not install or
port the COSMO-RS backend.

## Apple Silicon (M-series)

Install the **arm64** Miniforge installer and use a native ARM terminal. Then
follow the [common installation guide](../installation.md). JAX lists native
Apple ARM CPU wheels in its [installation guide](https://docs.jax.dev/en/latest/installation.html#cpu).
No GPU configuration is needed for the SAFT examples. This project has not run
macOS CI, so this is an upstream-supported dependency route rather than a
claim of local macOS validation.

Avoid mixing ARM and Intel Python packages in the same environment. Confirm
the architecture with:

```text
python -c "import platform; print(platform.machine())"
```

## Intel Macs

Current JAX wheel documentation does not list macOS x86_64. The standard SAFT
environment is therefore not a validated one-command route on an Intel Mac.
For the documented SAFT workflow, use a supported Linux environment on compatible
hardware. Installing an older JAX release or building from source requires its
own compatibility checks; the guide does not silently pin an untested version.

The Python core without SAFT can still be installed separately where its
NumPy/SciPy dependencies are available:

```text
conda create -n thermoweave-core python=3.12 pip
conda activate thermoweave-core
python -m pip install -e ".[tutorials]"
```

Run the installation command from the repository root. This core installation
does not provide SAFT EOS evaluations.

## openCOSMO-RS

The current C++ backend uses x86 SSE3/AVX intrinsics. It cannot be built natively
for Apple Silicon simply by changing a path or turning off AVX. Use a compatible
remote x86_64 Linux computer for the validated backend workflow, including the
COSMO-RS SLLE notebooks. An Intel macOS build is also outside this project's
validated build route; see the backend's documentation before attempting one.

You can still read the [saved notebook calculations](../tutorials.md) in the
documentation site without installing the backend.
