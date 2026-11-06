# Set up HANNA

The `HannaModel` adapter uses an external HANNA checkout and its model assets.
Follow the upstream [HANNA repository](https://github.com/marco-hoffmann/HANNA)
for the predictor and weight files. They are not bundled with ThermoWeave.

From the ThermoWeave repository root, in the active environment:

```text
python -m pip install -e ".[hanna]"
conda env config vars set HANNA_ROOT="/path/to/HANNA"
conda deactivate
conda activate thermoweave
```

Replace the example path with the absolute path to your upstream checkout and
obtain its required assets before running the HANNA block of notebook 09.
PyTorch's own platform requirements also apply. See the upstream instructions
when configuring a platform-specific accelerator; no GPU is required by the
ThermoWeave SAFT examples.

HANNA supplies liquid excess-Gibbs/activity predictions through the shared
interface. It does not supply a pressure–volume equation of state. The
[theory chapter](../theory/cosmors-and-learned-models.md#learned-excess-gibbs-functions) explains the distinction.
