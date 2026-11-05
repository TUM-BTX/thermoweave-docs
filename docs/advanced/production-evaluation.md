# Production Corpus Evaluation

ThermoWeave resolves component metadata directly from a `DB_Component` directory
or `DB_Component.zip`, selects every available COSMO conformer, and runs neutral
corpora through the C++26 legacy bulk path. It does not create one `Model` per
record.

```python
from thermoweave.evaluation.component_archive import ComponentArchiveResolver
from thermoweave.evaluation.corpus_runner import CorpusRunner

resolver = ComponentArchiveResolver(
    "/path/to/data/DB_Component_old/DB_Component.zip",
    "/path/to/data/COSMOconf25",
    file_format="turbomole",
    basis="COSMO_TZVPD_FINE",
    required_keys=required_component_keys,
)
resolved = resolver.resolve()
resolved.write_manifest("component-manifest.json")

runner = CorpusRunner(
    resolved.database,
    "/path/to/openCOSMO-RS_cpp_26/parametrizations/"
    "cosmoconf25_tm_volfix_20260711_stageA_NM_plus_stageB_NM.json",
    volume_correction=False,  # LLE tie lines are mole-fraction basis.
)
report = runner.run("/path/to/data/DB_System/GeneralSystems/"
                    "DECHEMA-CDS_Vol5-Part3_LLE_Ternary-Quaternary-Systems_1980")
report.to_json("dechema-report.json")
```

`ComponentArchiveResolver` records source paths, selected conformers, SHA-256
hashes, resolved/skipped keys, and explicit skip reasons. `CorpusRunner` records
parsed/usable/scored entries, skipped records, predictions, grouped metrics, and
parse/preparation/C++/postprocessing/end-to-end timings. The C++ timings are
also decomposed into `cpp_initialize`, `cpp_load_molecules`,
`cpp_load_calculations`, and `cpp_calculate`; `cpp_molecule_volume_export` is
reported separately when the volume API is used. `cpp_bulk_evaluation` remains
the total wrapper wall time for backward-compatible aggregate reporting.

Supported neutral corpus categories are IDAC, AC, `logK`, LLE-NIST,
LLE-DECHEMA, and dGsolvation. MIAC and electrolyte/reactive records are reported
as unsupported rather than silently evaluated with a molecular model.

For ORCA use `file_format="orca"` and the default `COSMO_TZVPD` basis; for
COSMOconf25 use `file_format="turbomole"` and `COSMO_TZVPD_FINE`. All matching
`c000`, `c001`, and later conformers are included in sorted order.
