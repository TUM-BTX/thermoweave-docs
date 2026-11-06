# Third-party notices and parameter provenance

ThermoWeave includes SAFT parameter tables converted from SGTPy, extension values
from the Clapeyron.jl database, a pinned NRTL parameter CSV, and a NumPy port of SGTPy collocation routines
used only by comparison tests. Their upstream MIT notices are reproduced below.
SAFT kernels implement the cited thermodynamic equations in JAX; SGTPy is an
optional comparison oracle, not a runtime dependency. Each parameter row keeps
its scientific reference. See [references](references.md).

HANNA and OpenCOSMO-RS are external backends, installed separately; their source,
weights and COSMO datasets are not bundled here. Their own license terms apply.
NumPy, SciPy, JAX, RDKit, Matplotlib and Jupyter remain separately distributed
dependencies under their respective licenses.

## gustavochm/sgtpy

Source: https://github.com/gustavochm/sgtpy/blob/master/LICENSE.txt

```text
MIT License

Copyright (C) 2020, Andrés Mejía (amejia@udec.cl), Gustavo Chaparro (gustavochaparro@udec.cl),
Erich Muller (e.muller@imperial.ac.uk).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ClapeyronThermo/Clapeyron.jl

Bundled NRTL data:
[database/Activity/NRTL/NRTL_unlike.csv](https://github.com/ClapeyronThermo/Clapeyron.jl/blob/cb620c1af72b7bcea8407e4f970dbae64a7f8c9d/database/Activity/NRTL/NRTL_unlike.csv),
commit `cb620c1af72b7bcea8407e4f970dbae64a7f8c9d`, retrieved 2026-11-06.
The CSV retains its source column, which is empty for every pair. Original
per-pair experimental references and validity ranges are unknown. ThermoWeave's native JAX NRTL
implementation follows the same directed a+b/T convention; Julia is not a
runtime dependency. See [NRTL](models/nrtl.md).

Source: https://github.com/ClapeyronThermo/Clapeyron.jl/blob/master/LICENSE.md

```text
MIT License

Copyright (c) 2020 Hon Wa Yew and Pierre Walker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


## SPT-NRTL collection access

ThermoWeave bundles an index of 9,823 CSV tables from
[ClapeyronThermo/spt-nrtl-db](https://github.com/ClapeyronThermo/spt-nrtl-db),
revision `f8e903ad96ac1a6d9c3dbaaa53c1752e8106286e`, retrieved 2026-11-06.
It contains component SMILES, table paths, sizes and Git blob hashes; no SPT
coefficient tables are bundled. The loader fetches verified external tables
into a user cache or reads a user-provided local copy.

The scientific reference for these predictions is Winter, Winter, Esper,
Schilling and Bardow (2023), *SPT-NRTL: A physics-guided machine learning model
to predict thermodynamically consistent activity coefficients*, Fluid Phase
Equilibria 568, 113731, https://doi.org/10.1016/j.fluid.2023.113731.
The mirror's CITATION.bib refers to the earlier SPT paper; the SPT-NRTL paper
above is the method citation used by ThermoWeave. Neither per-pair experimental
citations nor validated temperature intervals are present in the CSVs.

The mirror has no separate data-license file in the pinned revision.
ThermoWeave's MIT code license does not relicense external downloaded tables;
consult the dataset provider's terms for redistribution of those tables.
