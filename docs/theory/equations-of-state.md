# Equations of state

An equation of state relates pressure, temperature, volume and composition.
A thermodynamically consistent energy formulation supplies that relation and
the derivatives needed for fugacity and caloric properties. ThermoWeave's
native molecular EoS is [SAFT-γ Mie](saft-gamma-mie.md).

## From Helmholtz energy to pressure

Write total Helmholtz energy as an ideal-gas term and a residual contribution:

$$A=A^{\mathrm{ig}}+A^{\mathrm{res}},\qquad
 a^{\mathrm{res}}=\frac{A^{\mathrm{res}}}{nRT}.$$

Because $P=-(\partial A/\partial V)_{T,\mathbf n}$ and $\rho=n/V$,

$$P=\rho RT\left[1+\rho\left(\frac{\partial a^{\mathrm{res}}}
{\partial\rho}\right)_{T,\mathbf x}\right],$$

$$Z\equiv\frac{P}{\rho RT}
=1+\rho\,a^{\mathrm{res}}_{\rho}.$$

The ideal-gas pressure is recovered when the residual term vanishes. An
interaction model changes the energy's density dependence and therefore the
pressure. The same potential must also be used for composition and temperature
derivatives if those properties are to remain consistent.

## Density roots and phase branches

At specified T, P and x, density is obtained from

$$F(\rho)=P_{\mathrm{model}}(T,\rho,\mathbf x)-P_{\mathrm{target}}=0.$$

Several roots can exist. A low-density root commonly represents a vapour
branch and a high-density root a liquid branch. Mechanical stability requires
positive isothermal compressibility, equivalently
$(\partial P/\partial\rho)_{T,x}>0$ for a homogeneous fluid.
This local criterion alone does not establish global stability against phase
separation.

Selecting `phase="liquid"` or `phase="vapor"` controls the density branch in
an EoS calculation. Equilibrium between branches additionally requires equal
component chemical potentials and material balances. Near a spinodal or
critical point the pressure slope can approach zero, making roots and their
derivatives ill conditioned.

## Fugacity and mixture equilibrium

Fugacity expresses chemical potential using an ideal-gas pressure convention:

$$f_i=x_i\phi_iP.$$

For a residual Helmholtz model,

$$\ln\phi_i=
\left[\frac{\partial(n a^{\mathrm{res}})}{\partial n_i}
\right]_{T,V,n_{j\ne i}}-\ln Z.$$

The derivative includes the change of density when a mole amount changes at
fixed total volume. The $-\ln Z$ term converts the ideal-gas reference from the
same T/V to the same T/P convention.

General EoS vapour–liquid coexistence requires

$$x_i^L\phi_i^L(T,P,\mathbf x^L)
=y_i^V\phi_i^V(T,P,\mathbf y^V).$$

The liquid and vapour compositions generally differ. A pair of density roots
at one imposed composition is not by itself a mixture flash.

## From an EoS to liquid activities

Using pure liquids at the same T/P as standard states gives

$$\ln\gamma_i=\ln\phi_i^{\mathrm{mix,L}}
-\ln\phi_i^{\mathrm{pure,L}}.$$

This is how SAFT supplies the liquid activity interface used by ThermoWeave's
model-independent equilibrium tools. A pure-liquid reference branch must be
available for that state and component. Liquid activity-based convenience
VLE routines make the additional assumptions described in
[phase-equilibrium theory](phase-equilibria.md#vapourliquid-equilibrium).

## Caloric properties and reference information

The residual enthalpy follows from a temperature derivative:

$$\frac{h^{\mathrm{res}}}{RT}
=-T\left(\frac{\partial a^{\mathrm{res}}}{\partial T}\right)_{\rho,x}+Z-1.$$

An absolute enthalpy or heat capacity additionally needs an ideal-gas reference
model. Segment parameters alone do not supply all ideal-gas caloric data.
The [derivative chapter](derivatives.md) explains the difference between
constant-density and constant-pressure differentiation.

**Use in Python:** [density/volume/pressure recipe](../guide/calculations.md#calculate-density-volume-and-pressure),
[SAFT setup](../models/saft-gamma-mie.md) and
[notebook 03](../notebooks/03_saft_eos_properties.ipynb).
The native molecular formulation follows
[Papaioannou et al.](https://doi.org/10.1063/1.4851455) and
[Lafitte et al.](https://doi.org/10.1063/1.4819786).
