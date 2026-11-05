# Windows

## ThermoWeave, SAFT and notebooks

Install the Windows x86_64 Miniforge installer and run the commands in the
[common installation guide](../installation.md) in **Miniforge Prompt**. Its
commands do not require Bash syntax. Quote any path containing spaces.

JAX documents Windows CPU wheels and notes a possible requirement for the
[Microsoft Visual C++ redistributable](https://docs.jax.dev/en/latest/installation.html#cpu).
ThermoWeave currently runs CI on Linux, so Windows results have not been checked
by this project's CI.

When using VS Code or Jupyter, explicitly select **Python (ThermoWeave)**.
A terminal's active environment and an already-running notebook kernel can be
different interpreters.

## openCOSMO-RS through WSL2

The documented backend route is an x86_64 Linux environment under
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install).
Install WSL2 and a Linux distribution, then open that distribution's terminal
and follow the [Linux instructions](linux.md).

Install Conda, clone ThermoWeave and compile the backend **inside WSL**. A native
Windows environment and a WSL environment are separate installations; a Linux
`.so` cannot be loaded by Windows Python, and a Windows `.pyd` cannot be loaded
by Linux Python. Access your conformer data from a path visible inside WSL.
Starting with files in the Linux filesystem avoids confusion between Linux
paths and Windows drive paths.

The backend also contains upstream native Visual Studio build instructions,
but native Windows builds of its current high-level API are not validated by
this project. The WSL route keeps the documented build consistent with Linux.

## Paths in the Windows prompt

Use absolute paths, for example `"C:/Users/you/Data/COSMOconf25"`, in configuration
commands. Run each `conda env config vars set ...` command on its own line; the
[configuration guide](../models/opencosmors.md#configure-the-tutorials) uses no
Unix line-continuation syntax. For a WSL installation, configure Linux paths
from the WSL Conda environment instead.
