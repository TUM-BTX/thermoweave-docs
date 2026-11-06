# SPT-NRTL parameter collection

ThermoWeave can load the **SPT-NRTL v3 predictions** published with
[Winter et al. (2023)](https://doi.org/10.1016/j.fluid.2023.113731).
The paper describes approximately 100 million predicted mixture entries. The
pinned [Clapeyron mirror](https://github.com/ClapeyronThermo/spt-nrtl-db/tree/f8e903ad96ac1a6d9c3dbaaa53c1752e8106286e)
contains 9,823 component tables. The package includes their index, paths, sizes
and Git blob hashes. It fetches individual tables as needed; the large
collection is **not bundled into the library or cloned during installation**.

These coefficients are machine-learning predictions. Their citation is the
SPT-NRTL paper; they are not individually regressed experimental parameter
sets. The CSVs contain neither per-pair experimental references nor validated
temperature intervals. These fields remain explicitly unknown in the model
metadata. The training dataset's temperature span is not a validated interval
for every predicted pair. Validate predictions for your application, especially
LLE/SLLE: the study primarily evaluates activity coefficients and VLE.

## Install and load a mixture

The standard Conda environment includes the required JAX and RDKit packages.
For a separate environment, run from the ThermoWeave checkout:

```text
python -m pip install -e ".[nrtl-spt,tutorials]"
```

```python
from thermoweave import NRTL

model = NRTL.from_spt({"water": "O", "ethanol": "CCO"})
print(model.ln_activity_coefficients(298.15, [0.4, 0.6]))
print(model.reference)
print(model.metadata["source_kind"])             # prediction
print(model.metadata["temperature_range_K"])     # None: unknown
print(model.metadata["pairs"])
```

The mapping defines component order. RDKit canonicalizes SMILES before lookup;
for exact canonical SMILES already used by the collection, pass
`canonicalize=False` to work without RDKit. Invalid SMILES or missing coverage
raise an error. All parameters are loaded at construction; property evaluation
and equilibrium calculations perform no network or database access.

The first call needs internet access to `raw.githubusercontent.com`. Downloads
are pinned to commit `f8e903ad96ac1a6d9c3dbaaa53c1752e8106286e` and checked
against the index's file size and Git blob hash before atomic cache storage.
Pair metadata also records the table's SHA-256 digest. No GitHub login, Julia,
neural-network weights or COSMO files are needed to use these tabulated predictions.

## Temperature dependence

The imported coefficients retain the full equations from the paper:

$$\tau_{ij}=a_{ij}+b_{ij}/T+l_{ij}\ln(T/\mathrm{K})+d_{ij}T,$$
$$\alpha_{ij}(T)=\alpha_{ij}^{0}+e_{ij}T.$$

| CSV column | ThermoWeave coefficient | Units |
|---|---|---|
| `a_1` | `alpha[i,j]` and `alpha[j,i]` | dimensionless |
| `a_2` | `alpha_linear[i,j]` and `alpha_linear[j,i]` | 1/K |
| `t_12_1` | `a[i,j]` | dimensionless |
| `t_12_2` | `b[i,j]` | K |
| `t_12_3` | `tau_log[i,j]` | dimensionless |
| `t_12_4` | `tau_linear[i,j]` | 1/K |
| `t_21_1` … `t_21_4` | The corresponding four entries `[j,i]` | as above |

Here i/j follow the **source row's** `SMILES0`/`SMILES1`, which are mapped to
your component order. The loader does not approximate the imported function by
refitting a+b/T. Activities and caloric properties use the same differentiable
Gibbs function, including the derivative of alpha(T).

```python
tau_at_T, alpha_at_T = model.interaction_parameters(298.15)
HE = model.excess_enthalpy(298.15, [0.4, 0.6])        # J/mol
CpE = model.excess_heat_capacity(298.15, [0.4, 0.6])  # J/(mol K)
```

The effective alpha must remain nonnegative at evaluated temperatures. This
check does not establish a scientific validity range.

## Pair selection and multicomponent mixtures

The collection contains predictions for ordered molecular inputs. Reversing
the two SMILES can produce a different predicted parameter set. For each
unordered pair, the loader selects the lexicographically first indexed source
SMILES whose table contains a complete row for its partner. It uses **both
directed tau functions and the shared alpha function from that one row**.
It does not mix or average the two ordered predictions. The selected source
order is recorded in `model.metadata["pairs"]`. Permuting your component
mapping permutes the resulting matrices and preserves the model predictions.

```python
ternary = NRTL.from_spt({"benzene": "c1ccccc1", "water": "O", "ethanol": "CCO"})
print(ternary.ln_activity_coefficients(298.15, [0.2, 0.5, 0.3]))
```

Combining binary predictions in multicomponent NRTL is a modelling assumption.
Use independent ternary data and stability checks to assess it. The resulting
model supports ThermoWeave's common activity-model equilibrium interfaces.

## Cache locations and offline use

Default cache roots are:

| OS | Default root |
|---|---|
| Linux | `$XDG_CACHE_HOME/thermoweave/spt-nrtl`, or `~/.cache/thermoweave/spt-nrtl` |
| macOS | `~/Library/Caches/thermoweave/spt-nrtl` |
| Windows | `%LOCALAPPDATA%/thermoweave/spt-nrtl` |

Each root contains a revision-specific folder with hash-named CSV cache files.
Hash names avoid collisions between aromatic/aliphatic SMILES on case-insensitive
Windows and macOS filesystems. This cache is independent of
the checkout, active working directory and Conda environment. Override the root
with `cache_dir=` or the `THERMOWEAVE_SPT_CACHE` environment variable.

```python
from thermoweave.nrtl import SPTNRTLDatabase

# Inspect available component-table SMILES without downloading tables.
db = SPTNRTLDatabase(cache_dir="my-spt-cache")
print(len(db.available_smiles))
# Online: cache all tables needed for a later offline calculation.
db.prefetch(["O", "CCO"])
# Offline: a missing table raises an error without a network attempt.
offline = SPTNRTLDatabase(cache_dir="my-spt-cache", offline=True)
model = NRTL.from_spt({"water": "O", "ethanol": "CCO"}, database=offline)
```

A local copy of the pinned mirror can be selected with `data_dir=` or
`THERMOWEAVE_SPT_DATA`. Point it at the repository root or its `v3` directory;
files are verified against the same index. Most users only need the much
smaller per-component cache. A corrupt cached file can be replaced with
`db.fetch_component("CCO", refresh=True)` while online.

Save an assembled model to avoid requiring either RDKit or the collection when
reopening it (JAX remains necessary for evaluation):

```python
model.to_json("water-ethanol-spt-nrtl.json")
restored = NRTL.from_json("water-ethanol-spt-nrtl.json")
```

The v2 JSON includes every temperature coefficient and provenance field.
External SPT tables keep their upstream terms; ThermoWeave's MIT code license
does not relicense those data. No SPT coefficient tables are redistributed in
the package. See [notebook 14](../notebooks/14_spt_nrtl_parameters.ipynb) for an
executed example with actual downloaded predictions.
