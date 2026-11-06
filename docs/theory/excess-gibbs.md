# Excess Gibbs energy models

A gE model represents the nonideal part of liquid mixing at fixed temperature
and pressure. Its central quantity is a scalar excess Gibbs energy; activity
coefficients follow from derivatives of that same function. This energy-based
construction makes the properties mutually consistent.

## Ideal and nonideal mixing

Using pure-liquid references,

$$\frac{g_{\mathrm{mix}}}{RT}
=\sum_i x_i\ln x_i+\frac{g^E}{RT},\qquad
\frac{g^E}{RT}=\sum_i x_i\ln\gamma_i.$$

The ideal contribution is completely determined by composition. The excess
term can be empirical, based on molecular surface interactions, or learned
from data. It describes the energy difference from ideal liquid mixing, not
the full energy of a molecule or its gas-phase reference.

Positive gE means an energetic penalty relative to ideal mixing; negative gE
means a favourable departure. Liquid splitting is governed by the curvature
and global convexity of the **total** mixing energy, including ideal mixing.

## Obtain activities from an energy

Chemical potentials require differentiation of the total excess energy:

$$\ln\gamma_i=
\left[\frac{\partial\{n\,g^E(T,P,\mathbf n/n)/(RT)\}}
{\partial n_i}\right]_{T,P,n_{j\ne i}}.$$

Differentiating a molar energy with respect to unconstrained x entries would
miss the change of total amount and normalization. For a binary mixture with
$x=x_1$, define $f(x)=g^E/(RT)$. The expressions reduce to

$$\ln\gamma_1=f+(1-x)f',\qquad
\ln\gamma_2=f-xf'.$$

This relation explains why a single smooth function produces two consistent
activity curves. It also implies the fixed-T/P Gibbs–Duhem identity

$$\sum_i x_i\,\mathrm d\ln\gamma_i=0.$$

Pure-component reference consistency requires gE→0 and gamma→1 for the species
present as a pure liquid. The activity coefficient of an absent species at
infinite dilution need not equal one.

## A simple analytic illustration

For the symmetric two-suffix Margules model, $f(x)=\chi x(1-x)$, so

$$\ln\gamma_1=\chi(1-x)^2,\qquad
\ln\gamma_2=\chi x^2.$$

This is a useful teaching example of an energy-derived activity model. Its
illustrative parameters are synthetic; the main application notebooks use the
actual SAFT, NRTL and COSMO-RS models. The [phase-equilibrium chapter](phase-equilibria.md)
uses the analytic example to explain the common-tangent construction.

## Empirical and predictive model families

[NRTL](nrtl.md) describes local compositions using directed binary parameters.
Their calibration and applicable range must come from the parameter source.
COSMO-RS instead evaluates surface interactions from quantum-chemical inputs;
HANNA predicts a constrained excess-Gibbs function. SPT-NRTL predicts the
parameters of an NRTL function. These routes share a thermodynamic output,
while their input requirements and sources of uncertainty differ.
See [COSMO-RS and learned models](cosmors-and-learned-models.md).

## What a gE model supplies

An activity model supplies liquid chemical-potential differences, mixing/excess
Gibbs energy and—when temperature dependence is supported—excess caloric
properties. The pressure-independent forms implemented here do not provide
PVT density roots or the pure-component saturation pressures required for VLE.
An appropriate solid reference is also needed for SLE/SLLE.

The [phase-equilibrium chapter](phase-equilibria.md) explains how those
additional inputs connect to activities. For code, start with
[the practical model comparison](../guide/index.md#choose-a-model),
[the activity recipe](../guide/calculations.md#calculate-activities-and-excess-properties)
and [notebook 13](../notebooks/13_nrtl_and_parameter_fitting.ipynb).
