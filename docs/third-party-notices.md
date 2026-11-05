# Third-party notices and parameter provenance

ThermoWeave includes SAFT parameter tables converted from SGTPy, extension values
from the Clapeyron.jl database, and a NumPy port of SGTPy collocation routines
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
