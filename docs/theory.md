# Thermodynamic background

This guide connects the quantities returned by the APIs. The numbered
[notebooks](tutorials.md) turn the formulas into calculations.
All energies below are molar unless total amounts are written explicitly.

## Chemical potentials and gE models

For the liquid pure-component standard state,

$$\mu_i=\mu_i^{\mathrm{pure,L}}(T,P)+RT\ln(x_i\gamma_i).$$

A liquid excess-Gibbs model gives the departure from ideal mixing:

$$\frac{g_{mix}}{RT}=\sum_i x_i\ln x_i+\frac{g^E}{RT},\qquad
\frac{g^E}{RT}=\sum_i x_i\ln\gamma_i.$$

Thermodynamic consistency follows by differentiating the *total* excess
Gibbs energy with respect to mole numbers:

$$\ln\gamma_i=\left[\frac{\partial\{n g^E(T,P,\mathbf{n}/n)/(RT)\}}
{\partial n_i}\right]_{T,P,n_{j\ne i}}.$$

The optional [custom-model theory notebook](notebooks/theory/custom_activity_models.ipynb) illustrates this with a symmetric two-suffix Margules model,
$g^E/(RT)=A x_1x_2$, giving $\ln\gamma_1=A x_2^2$ and
$\ln\gamma_2=A x_1^2$. Its parameters are synthetic. NRTL and UNIQUAC are
other established gE model families; they are not bundled model classes here.

COSMO-RS and HANNA also provide liquid activities through adapters. COSMO-RS
uses quantum-chemical surface information and statistical thermodynamics;
HANNA predicts an excess-Gibbs function from molecular representations.
See [Klamt](https://doi.org/10.1021/j100007a062) and the
[HANNA paper](https://doi.org/10.1039/D4SC05115G). A gE model alone does not
supply a liquid/vapour PVT equation of state.

## SAFT-γ Mie: a Helmholtz equation of state

SAFT models a molecule through interacting segments, chain connectivity and
association sites. In SAFT-γ Mie, transferable groups supply segment and
interaction parameters. The residual dimensionless Helmholtz energy is split
into monomer, chain and association terms:

$$a^{res}\equiv\frac{A^{res}}{nRT}
=a^{monomer}+a^{chain}+a^{association}.$$

The monomer terms use a Mie pair potential,

$$u(r)=C\epsilon[(\sigma/r)^{\lambda_r}-(\sigma/r)^{\lambda_a}],\qquad
C=\frac{\lambda_r}{\lambda_r-\lambda_a}
\left(\frac{\lambda_r}{\lambda_a}\right)^{\lambda_a/(\lambda_r-\lambda_a)}.$$

Here $\sigma$ sets the size, $\epsilon$ the attraction scale, and the two
exponents control repulsion and attraction. Association represents specific
site bonding, such as hydrogen bonding. The core formulation follows
[Papaioannou et al.](https://doi.org/10.1063/1.4851455) with monomer terms from
[Lafitte et al.](https://doi.org/10.1063/1.4819786).

SMILES fragmentation supplies group counts, not a new interaction model.
The exact-cover report makes that structural choice inspectable. Missing
unlike pairs may use combining rules; inspect `missing_interactions` before
calling a mixture a prediction. Group-count representations can identify
positional isomers with the same groups: atom recognition does not remove
that limitation.

## Properties from Helmholtz derivatives

For molar density $\rho=n/V$,

$$Z=\frac{P}{\rho RT}=1+\rho\left(\frac{\partial a^{res}}{\partial\rho}\right)_{T,x},
\qquad v=1/\rho.$$

Density evaluation solves $P(T,\rho,x)=P_{target}$. A liquid or vapour root
selects a branch; coexistence requires an additional equilibrium calculation.
From the residual Helmholtz function,

$$\frac{h^{res}}{RT}=-T\left(\frac{\partial a^{res}}{\partial T}\right)_{\rho,x}+Z-1.$$

Absolute enthalpy, entropy and heat capacity additionally need ideal-gas
reference contributions. ThermoWeave does not infer them from group counts.
The SAFT parameter tables store $\epsilon/k_B$ in K and $\sigma$ in Å; the
assembled model parameters and core property calls use SI.

Fugacity coefficients connect the EOS to the liquid model interface:

$$\ln\gamma_i=\ln\phi_i^{mix,L}(T,P,x)-\ln\phi_i^{pure,L}(T,P).$$

JAX differentiates energies and implicitly differentiates converged density
and association roots. Notebook 04 checks Gibbs–Duhem identities and computes

$$h^E=-RT^2\sum_i x_i\left(\frac{\partial\ln\gamma_i}{\partial T}\right)_{P,x},
\qquad \bar v_i=\left(\frac{\partial V}{\partial n_i}\right)_{T,P,n_{j\ne i}},
\qquad\kappa_T=\frac{1}{\rho(\partial P/\partial\rho)_{T,x}}.$$

KB inversion combines chemical-potential derivatives, partial volumes and
compressibility to obtain concentration-fluctuation integrals. It is a
thermodynamic inversion, not a molecular simulation; avoid interpreting
homogeneous-branch results inside a miscibility gap as stable bulk data.

## Phase and reaction equilibrium

Coexisting phases have equal chemical potentials and satisfy material
balances. Stability asks whether another phase assemblage lowers total Gibbs
energy. TPD, multistart coexistence searches, CEM and ReducedHELD address
related parts of this problem with different numerical assumptions.

For a pure solid and constant fusion enthalpy ($\Delta C_p=0$), SLE uses

$$\ln(x_i\gamma_i)=-\frac{\Delta h_{fus,i}}{R}
\left(\frac{1}{T}-\frac{1}{T_{m,i}}\right).$$

A root of this equation alone does not decide competition with other solids
or a liquid–liquid split. Notebook 07 contrasts the root with a coupled flash.

The VLE convenience API uses $y_iP=x_i\gamma_iP_i^{sat}$, ideal vapour and
no Poynting correction. General EOS VLE instead requires
$x_i\phi_i^L=y_i\phi_i^V$; notebook 03 demonstrates both EOS branches, while
notebook 05 explicitly teaches the ideal-vapour convenience solver.

For reactions, $\nu^T\ln a=\ln K$. Charged species additionally require
charge-balanced feeds and consistent ionic reference states. The electrolyte
and reactive examples are labelled experimental; see [capabilities](capabilities.md).

## Binary versus ternary SLLE

At fixed pressure the Gibbs phase rule is F=C−P+1. Binary S+L1+L2 is an
invariant at a single temperature. Three phase amounts in a binary invariant
are not uniquely determined by the two component balances; a numerical flash
can return an equally stable two-phase representation. Ternary S+L1+L2 at
fixed T/P occupies a tie triangle: its three phase compositions stay fixed
while phase amounts vary with the feed. Tutorials 10–12 compute these cases
with the actual SAFT and COSMO-RS models and measured fusion properties.
