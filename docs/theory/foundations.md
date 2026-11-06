# Thermodynamic foundations

A thermodynamic model represents an energy. Its derivatives determine chemical
potentials and measurable properties; equilibrium follows by minimizing the
appropriate total energy under the system's constraints. This common structure
connects EoS, activity models and the solvers in ThermoWeave.

## Potentials and independent variables

For a homogeneous phase, Helmholtz and Gibbs energies satisfy

$$A=A(T,V,\mathbf n),\qquad G=G(T,P,\mathbf n)=A+PV,$$

$$\mathrm dA=-S\,\mathrm dT-P\,\mathrm dV+\sum_i\mu_i\,\mathrm dn_i,$$

$$\mathrm dG=-S\,\mathrm dT+V\,\mathrm dP+\sum_i\mu_i\,\mathrm dn_i.$$

Thus a Helmholtz model naturally gives pressure through a volume derivative,
while a Gibbs model naturally describes composition changes at fixed T/P.
For an extensive homogeneous phase, $G=\sum_i n_i\mu_i$. Here $n_i$ is a mole
amount, $n=\sum_i n_i$ and $x_i=n_i/n$.

| Symbol | Meaning | Units |
|---|---|---|
| A, G | Total Helmholtz and Gibbs energy | J |
| g=G/n | Molar Gibbs energy | J/mol |
| gᴱ | Molar excess Gibbs energy | J/mol |
| aʳᵉˢ=Aʳᵉˢ/(nRT) | Reduced residual Helmholtz energy | dimensionless |
| μᵢ | Chemical potential | J/mol |
| ρ=n/V | Molar density | mol/m³ |
| R | Molar gas constant | J/(mol K) |

ThermoWeave's `reduced_*` energy methods return dimensionless molar energies
divided by RT. Its EoS density is molar density. See the
[practical unit conventions](../api.md) before combining model outputs.

## Chemical potential and activity

A chemical potential measures the energy change when a component is added:

$$\mu_i=\left(\frac{\partial G}{\partial n_i}\right)_{T,P,n_{j\ne i}}.$$

For a molecular liquid with the pure liquid as standard state,

$$\mu_i=\mu_i^{\mathrm{pure,L}}(T,P)+RT\ln a_i,
\qquad a_i=x_i\gamma_i.$$

The mole fraction describes composition; the activity coefficient describes
its nonideal contribution. Activity is dimensionless and is not interchangeable
with concentration or with gamma alone. At fixed T/P, a species has a tendency
to transfer from higher to lower chemical potential.

The standard state matters. Pure-liquid, ideal-gas and infinite-dilution
conventions give different numerical chemical potentials and activity
coefficients. Reference offsets cancel in a nonreactive phase-equilibrium
comparison only when the same component reference is used consistently in all
phases. Reaction equilibria additionally require standard reaction energies or
equilibrium constants.

## Mixing and excess energy

For pure-liquid references, the molar mixing energy is

$$g_{\mathrm{mix}}=g-\sum_i x_i g_i^{\mathrm{pure,L}}
=RT\sum_i x_i\ln x_i+g^E.$$

The ideal mixing term follows from compositional entropy. The excess term is
the difference between the actual mixture and an ideal liquid mixture at the
same T/P and composition. Its sign alone does not determine whether a mixture
splits: stability depends on the shape of the full mixing energy.

A **residual** property instead compares a fluid with an ideal-gas reference.
For residual Helmholtz energy that reference has the same T, V and composition.
Residual and excess energies therefore describe different departures and
should not be substituted for one another.

## Model, state and equilibrium

An EoS state needs temperature, composition and either density or pressure.
A liquid activity model commonly needs temperature and composition, with
pressure dependence neglected in the implemented form. A flash additionally
needs a feed and all admissible phase models, including any solid references.

A successful evaluation gives the properties of that specified homogeneous
state. Establishing whether it is stable requires a separate minimization or
stability analysis. Continue with [equations of state](equations-of-state.md),
[excess Gibbs energy models](excess-gibbs.md) and
[phase equilibria](phase-equilibria.md).
