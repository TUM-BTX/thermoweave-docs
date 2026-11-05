# Linux

Use the [common installation steps](../installation.md) in a terminal initialized
for Conda. The project is tested on Linux x86_64 with Python 3.10/3.12; the
provided environment selects Python 3.12 and CPU JAX.

## SAFT and notebooks

No C++ compiler or external molecular database is required for the bundled SAFT
model. The environment installs its Python dependencies. On a headless server,
start JupyterLab with `jupyter lab --no-browser tutorials/` and connect through
your institution's normal SSH/tunnel workflow.

## Build tools for openCOSMO-RS

The optional backend is compiled separately for the activated environment's
Python and the target CPU. On Ubuntu/Debian, install these system tools if they
are absent:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake git
```

On other Linux distributions use their package manager for a C++14 compiler,
CMake and Git, or ask your system administrator. You need a compatible compiler,
not a specific home-directory layout. See the
[openCOSMO-RS build and configuration guide](../models/opencosmors.md).

The current backend's default build enables AVX. Build on hardware supporting
AVX. For an x86 machine limited to SSE3, use the upstream compiler options to
build an SSE3 target; disabling AVX alone does not automatically add `-msse3`.
Do not copy an AVX binary onto a computer that cannot execute it. ARM is not a
native target of this backend version.
