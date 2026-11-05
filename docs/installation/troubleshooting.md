# Verify and troubleshoot

Run checks in the same Conda environment and interpreter that will perform the
calculations. Avoid testing only a terminal import when the error occurs in a
different notebook kernel.

## Python and package location

```text
conda activate thermoweave
python -c "import sys, thermoweave; print(sys.executable); print(thermoweave.__file__)"
python -m pip check
conda env config vars list
```

In a notebook, inspect `sys.executable`. Select **Python (ThermoWeave)** if it
points to another environment. With an editable installation,
`thermoweave.__file__` points into the source checkout; the Python executable
still belongs to the Conda environment.

## Common installation errors

| Symptom | What to check |
|---|---|
| `Repository not found` or authentication failure | The code repository is private. Confirm your GitHub account has access and Git is authenticated. The backend repository has separate access. |
| `conda` is not recognized | Reopen the initialized shell, or use Miniforge Prompt on Windows. |
| Environment named `thermoweave` already exists | Activate it. Use a new environment name when making a separate installation. |
| `environment.yml` is not found | Enter the ThermoWeave repository root before creating the environment. |
| `No module named thermoweave` | Activate the environment; check `sys.executable`. Reinstall if an editable source checkout was moved. |
| JAX or `jaxlib` fails to install/import | Check the OS/CPU table and JAX's current wheel support; on Windows check its redistributable requirement. |
| Notebook imports differ from terminal imports | Change the notebook kernel and restart it. |
| First SAFT calculation takes longer | JAX compiles the kernels on first use. Later calls reuse them. |
| `No module named openCOSMORS` | Confirm the backend was built for this environment's Python, set its build path, and restart Jupyter after environment changes. |
| Backend import reports a missing shared library | Build against the current environment and ensure its compiler/OpenMP runtime libraries are available. |
| `Illegal instruction` from the backend | Check that the binary's SIMD instructions match the CPU. Rebuild for that machine. |
| COSMO conformers not found | Check the root directory and the exact component/basis tree shown in the COSMO-RS guide. |
| Parametrization not found | Use an absolute path to a valid JSON file, or keep the backend's bundled parameter directory in place. |

## Verify the external model

Before running a full SLLE notebook, use the short
[COSMO-RS check](../models/opencosmors.md#verify-before-running-slle). It checks
the compiled module, three required component directories and parameter source,
then computes water/ethanol activities.

The tutorial configuration uses absolute local paths stored in the named
Conda environment. It does not require a particular username or home folder.
After changing variables, deactivate/reactivate the environment and restart
JupyterLab so new kernels inherit them.

## Scientific input errors

An unsupported SMILES or a missing SAFT interaction is separate from an
installation failure. Use manual group assignment or a compatible parameter
table and inspect the assignment report. A missing density root can also mean
the requested phase branch does not exist at that state. See the
[model assumptions](../capabilities.md) before changing solver settings.
