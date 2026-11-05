# Capabilities and assumptions

| Area | Available | Limits |
|---|---|---|
| Model interface | Activities, dimensionless mixing/excess Gibbs energy; custom models | Composition is a full mole-fraction vector |
| SAFT-γ Mie | Native JAX Helmholtz EOS, liquid/vapour density roots, PVT, fugacities, activities, derivatives | Results depend on group coverage and parameter quality; charged groups do not add electrolyte EOS terms |
| SMILES assignment | Printed atom/group report, exact coverage, manual alternative | Conservative neutral-chemistry rules; unsupported/ambiguous inputs fail |
| VLE | Bubble/dew P/T using activity coefficients and supplied saturation pressures | Ideal vapour; no Poynting correction; these convenience solvers are not a general EOS φ–φ flash |
| LLE/stability | Binary and multicomponent candidates, multistart TPD, CEM grid/hull and polish | Local searches and grid resolution affect completeness |
| SLE | Pure-solid Schröder–van Laar solubility/dissolution temperature | Constant fusion enthalpy, ΔCp=0; no solid solutions or cocrystal free energies inferred |
| ReducedHELD | Coupled liquid/solid phase search and diagnostic certification | Numerical certification reflects configured searches/tolerances, not an unconditional mathematical global guarantee |
| COSMO-RS/HANNA | Optional adapters and batch activities | External engines/assets required; gE adapters do not supply a PVT EOS |
| Fitting/evaluation | SAFT group fits; neutral COSMO-RS corpus tools; explicit records/metrics | Data provenance, units, weighting and validation split are caller responsibilities |
| Reactive/electrolyte | Mass action, ME-PDH composition, reduced-coordinate and synthetic examples | Experimental advanced workflows; verify charge/reference-state and global-stability assumptions for each application |

Hydration-network and steric-hindrance switches are research extensions, not
adopted universal improvements over published SAFT parameters. The bundled
parameter rows retain their individual scientific provenance. The publication
checkout does not include unpublished thesis-specific fitted amide tables,
experimental mixture-equilibrium corpora, generated research runs or neural-network weights. A small cited set of pure-component properties is included for real-mixture tutorials.

Optional analytic examples and fitting-recovery data are labelled synthetic.
The main application course uses actual SAFT/COSMO-RS models and cited pure-component
inputs. A successful numerical round trip demonstrates consistency, not experimental validation.
