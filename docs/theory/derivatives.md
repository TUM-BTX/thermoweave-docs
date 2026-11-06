# Derivatives and consistency

A thermodynamic potential connects many properties through derivatives.
Consistency means these properties follow from the same potential and
reference convention. It does not by itself establish agreement with measured
data or global stability of the state.

## Excess caloric properties

Let $f(T,P,\mathbf x)=g^E/(RT)$. At fixed P and composition,

$$h^E=-RT^2\left(\frac{\partial f}{\partial T}\right)_{P,x},$$

$$C_p^E=-R\left[2T\left(\frac{\partial f}{\partial T}\right)_{P,x}
+T^2\left(\frac{\partial^2 f}{\partial T^2}\right)_{P,x}\right].$$

Because $f=\sum_i x_i\ln\gamma_i$,

$$h^E=-RT^2\sum_i x_i
\left(\frac{\partial\ln\gamma_i}{\partial T}\right)_{P,x}.$$

A temperature-dependent NRTL alpha therefore contributes to hE and CpE,
alongside all terms in tau(T). For an EoS-derived activity coefficient, the
constant-P derivative also includes changes in the converged density. Holding
density fixed would calculate a different derivative.

These are excess properties. Absolute caloric properties require appropriate
pure-component references; their units and energy zeros must remain consistent.

## Composition derivatives

Use mole amounts n as independent variables and normalize x=n/Σn inside the
energy. For a model derived from total excess Gibbs energy,

$$J_{ij}=\left(\frac{\partial\ln\gamma_i}{\partial n_j}\right)_{T,P,n_{k\ne j}}
=\frac{\partial^2\{n g^E/(RT)\}}{\partial n_i\partial n_j}.$$

For a smooth potential J is symmetric. Extensivity and Gibbs–Duhem consistency
also imply $\mathbf x^T J=0$ when evaluated at unit total amount. These are
useful numerical checks of normalization and implementation. The derivative
along a binary composition path is different: changing x₁ also changes x₂.

ThermoWeave's NRTL/SAFT `ln_activity_coefficients_jacobian(T, x)` uses the
unit-total-amount convention. Differentiating the total energy independently
and comparing with the closed-form activities checks more than reproducing
the implementation's own algebra.

## Density response functions

For a homogeneous EoS branch,

$$\kappa_T=-\frac1V\left(\frac{\partial V}{\partial P}\right)_{T,\mathbf n}
=\frac1{\rho(\partial P/\partial\rho)_{T,x}},$$

$$\overline v_i=\left(\frac{\partial V}{\partial n_i}\right)_{T,P,n_{j\ne i}}.$$

Compressibility measures the volume response to pressure, and partial molar
volumes describe the change when a component is added. Kirkwood–Buff inversion
combines these responses with chemical-potential derivatives to obtain
concentration-fluctuation integrals. It is a thermodynamic inversion of a
homogeneous state; interpreting a metastable or unstable branch as a stable
bulk phase would require a separate physical justification.

The [API guide](../api.md) documents the KB result's cm³/mol and 1/GPa units,
which differ from the SI units used by core EoS calls.

## Implicit solutions and automatic differentiation

Density and association-site fractions satisfy equations of the form
$F(\mathbf q,\boldsymbol\theta)=0$. At a locally isolated converged root with
nonsingular $F_q$,

$$\frac{\mathrm d\mathbf q}{\mathrm d\boldsymbol\theta}
=-F_q^{-1}F_{\theta}.$$

ThermoWeave's JAX EoS kernels use implicit differentiation for the density and
association roots. NRTL has an explicit energy/activity expression. Both model
families can supply exact AD parameter Jacobians for their fitting helpers.
Near singular roots or phase boundaries, derivative conditioning needs care.

JAX compilation and a float64 policy support efficient repeated evaluations;
they do not fix an unconverged root, a poorly identified fit or a wrong
parameter convention. Public model methods handle their documented precision
scope; pure-kernel users must configure precision before tracing.

**Use in Python:** [notebook 04](../notebooks/04_derivatives_and_response_functions.ipynb),
[NRTL fitting](../advanced/nrtl-fitting.md),
[the batch calculation recipe](../guide/calculations.md#evaluate-a-composition-grid)
and [API conventions](../api.md). Scientific background for KB inversion is
listed in [the references](../references.md).
