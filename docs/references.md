# Scientific references and implementation provenance

Cite the equations, parameter sets and external models used in your calculation.
ThermoWeave has no assigned software DOI; do not substitute a fictitious one.

| Topic | Primary source |
|---|---|
| SAFT-γ Mie formulation | Papaioannou et al. (2014), J. Chem. Phys. 140, 054107. [DOI](https://doi.org/10.1063/1.4851455) |
| Mie-chain monomer formulation | Lafitte et al. (2013), J. Chem. Phys. 139, 154504. [DOI](https://doi.org/10.1063/1.4819786) |
| Base group parameter collection | Haslam et al. (2020), J. Chem. Eng. Data 65, 5862. [DOI](https://doi.org/10.1021/acs.jced.0c00746) |
| Aromatic ester/amine extension | M. Wehbe, PhD thesis, Imperial College London (2023), Tables 4.2–4.4. [Thesis](https://doi.org/10.25560/103095) |
| Pyridine-type nitrogen extension | Tenberg et al., 2025 preprint. [DOI](https://doi.org/10.1101/2025.10.18.683252); values from the [Clapeyron.jl database](https://github.com/ClapeyronThermo/Clapeyron.jl) |
| NRTL formulation | Renon and Prausnitz (1968), AIChE Journal 14, 135–144. [DOI](https://doi.org/10.1002/aic.690140124) |
| NRTL convention and bundled data | Pinned [Clapeyron implementation](https://github.com/ClapeyronThermo/Clapeyron.jl/blob/cb620c1af72b7bcea8407e4f970dbae64a7f8c9d/src/models/Activity/NRTL/NRTL.jl) and [NRTL parameter CSV](https://github.com/ClapeyronThermo/Clapeyron.jl/blob/cb620c1af72b7bcea8407e4f970dbae64a7f8c9d/database/Activity/NRTL/NRTL_unlike.csv), including row source citations |
| COSMO-RS background | A. Klamt (1995), J. Phys. Chem. 99, 2224–2235. [DOI](https://doi.org/10.1021/j100007a062) |
| HANNA background | Hoffmann et al. (2024), Chemical Science. [DOI](https://doi.org/10.1039/D4SC05115G); [upstream implementation](https://github.com/marco-hoffmann/HANNA) |
| SAFT numerical comparison and source tables | [SGTPy source and references](https://github.com/gustavochm/sgtpy) |
| SMILES/SMARTS matching | [RDKit documentation](https://www.rdkit.org/docs/GettingStartedInPython.html) |
| Automatic differentiation | [JAX documentation](https://docs.jax.dev/en/latest/automatic-differentiation.html) |
| Kirkwood–Buff inversion | Smith, Matteoli and O'Connell (eds.), *Fluctuation Theory of Solutions*, CRC Press (2013), Chapter 4 |

The shipped base JSON is converted from SGTPy's spreadsheet by
`tools/convert_sgtpy_saft_database.py`. Later source-table additions retain
their own row-level references. The two extension files only add rows; they
do not silently overwrite the base table. Check each parameter row's
`reference` field for the model actually used.

The JAX kernels follow the published equations and the SGTPy numerical
organization, with documented differences and regression comparisons in
`tests/saft/`. The NumPy collocation shim is a test-only port. Upstream MIT
notices for the distributed table values and comparison code are reproduced
in [THIRD_PARTY_NOTICES.md](third-party-notices.md).
