"""Data, plotting and independent checks for the real-mixture tutorials.

Model constructors and ReducedHELD calls remain visible in the notebooks.
No fitted parameters, EOS corrections or surrogate activity models live here.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

import numpy as np
from thermoweave.equilibrium.core import R_J_MOL_K
from thermoweave.equilibrium.reduced_held import HELDSettings

DATA = json.loads((Path(__file__).parent / "data/real_mixtures.json").read_text())
COMPONENTS = DATA["components"]


def solid_gibbs(T):
    """Benzene(s) G/(RT) per mole relative to pure liquid; delta Cp = 0."""
    d = COMPONENTS["benzene"]
    return -d["enthalpy_of_fusion_J_mol"] / R_J_MOL_K * (1./T - 1./d["melting_temperature_K"])


def held_settings(noisy=False):
    """Explicit precision for the real SAFT or float COSMO-RS backends."""
    return HELDSettings(stage1_starts=12, screen_points=96, max_starts=12,
                        verify_cap=10, verify_random=5, max_iterations=60,
                        cut_tol=1e-6 if noisy else 1e-10,
                        polish_tol=2e-5 if noisy else 2e-9,
                        fd_step=1e-3 if noisy else 1e-5,
                        inner_method="newton", inner_refine=0, polish_fused=True,
                        inner_ftol=1e-10 if noisy else 1e-13,
                        inner_gtol=1e-7 if noisy else 1e-10, seed=0)


def check_flash(model, T, feed, result, tol=5e-7):
    """Independent species balance, isoactivity, solid saturation and G check.

    Fractions beta here are phase *mole* fractions. HELD's mass_fractions are
    a separate result and must never be substituted into a molar lever rule.
    """
    assert result.converged and result.certified, (result.notes, result.residuals)
    feed = np.asarray(feed, dtype=float)
    amounts = np.asarray(result.phases)
    assert np.min(amounts) >= -tol
    balance = float(np.max(np.abs(amounts.sum(axis=0)-feed)))
    assert balance < tol, balance
    X = np.asarray(result.mole_fractions)
    beta = amounts.sum(axis=1)/feed.sum()
    np.testing.assert_allclose(beta @ X, feed/feed.sum(), atol=tol, rtol=0)
    liquids = [i for i,k in enumerate(result.phase_kinds) if k == "liquid"]
    mu = [np.log(np.maximum(X[i], 1e-300))+model.ln_activity_coefficients(T, X[i]) for i in liquids]
    present = feed > 0
    spread = max((float(np.max(np.abs((v-mu[0])[present]))) for v in mu[1:]), default=0.)
    assert spread < tol, spread
    saturation = (max((abs(v[0]-solid_gibbs(T)) for v in mu), default=0.)
                  if "benzene(s)" in result.phase_kinds else 0.)
    assert saturation < tol, saturation
    energy = 0.
    for n,x,kind in zip(amounts,X,result.phase_kinds):
        energy += n.sum()*(model.reduced_mixing_gibbs(T,x) if kind == "liquid" else solid_gibbs(T))
    assert abs(energy-result.gibbs) < tol*max(1.,feed.sum())
    assert result.gibbs <= result.gibbs_feed+tol*max(1.,feed.sum())
    return {"species_balance_error_mol":balance, "liquid_mu_error_over_RT":spread,
            "solid_saturation_error_over_RT":saturation,
            "gibbs_reconstruction_error_over_RT":abs(energy-result.gibbs),
            "phase_mole_fractions":beta.tolist(),
            "phase_mass_fractions":result.mass_fractions.tolist()}


def phase_table(result, names):
    total = sum(p.sum() for p in result.phases)
    return [{"phase":k, "mole_fraction_of_total":float(n.sum()/total),
             "mass_fraction_of_total":float(w),
             **{f"x_{name}":float(v) for name,v in zip(names,x)}}
            for k,n,w,x in zip(result.phase_kinds,result.phases,result.mass_fractions,result.mole_fractions)]


def phase_label(result):
    n = result.phase_kinds.count("liquid")
    s = "benzene(s)" in result.phase_kinds
    if n == 0:
        return "S" if s else "empty"
    return ("S+" if s else "") + ({1:"L",2:"L1+L2"}.get(n,f"{n}L"))


def cosmo_components(names):
    """Resolve actual user-owned conformers; never return stand-in data."""
    root = os.environ.get("THERMOWEAVE_COSMO_ROOT")
    if not root:
        raise RuntimeError("Set THERMOWEAVE_COSMO_ROOT to the COSMOconf25 NeutralSpecies directory. "
                           "Real COSMO inputs are required; there is no synthetic fallback.")
    build = os.environ.get("THERMOWEAVE_OPENCOSMORS_BUILD")
    if build and build not in sys.path:
        sys.path.insert(0, build)
    module = os.environ.get("THERMOWEAVE_OPENCOSMORS_MODULE", "openCOSMORS")
    importlib.import_module(module)
    definitions, manifest = [], []
    for name in names:
        base = Path(root)
        if (base / "NeutralSpecies").is_dir():
            base = base / "NeutralSpecies"
        folder = base/COMPONENTS[name]["cosmo_directory"]/"COSMO_TZVPD_FINE"
        paths = sorted(folder.glob("*.cosmo"))
        if not paths:
            raise FileNotFoundError(f"No Turbomole COSMO_TZVPD_FINE conformers for {name}")
        definitions.append({"name":name,"paths":[str(p) for p in paths]})
        manifest.append({"name":name,"basis":"COSMO_TZVPD_FINE","conformers":[
            {"file":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]})
    return definitions, manifest


def ternary_axes(ax):
    corners = np.array([[0.,0.],[1.,0.],[.5,np.sqrt(3)/2]])
    frame = np.vstack([corners,corners[0]])
    ax.plot(frame[:,0],frame[:,1],color="black",lw=1)
    for xy,name in zip(corners,["benzene","water","ethanol"]):
        ax.annotate(name,xy,xytext=(0,8 if name=="ethanol" else -16),textcoords="offset points",ha="center")
    ax.set_aspect("equal");ax.set_axis_off()
    return corners


def ternary_plot(result, feed, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7,5))
    corners = ternary_axes(ax)
    xy = np.asarray(result.mole_fractions) @ corners
    if result.n_phases==3:
        from matplotlib.patches import Polygon
        ax.add_patch(Polygon(xy,closed=True,facecolor="tab:orange",alpha=.35,label="S+L1+L2 tie triangle"))
    elif result.n_phases==2:
        ax.plot(xy[:,0],xy[:,1],"-",color="tab:orange",label="coexisting phases")
    ax.scatter(xy[:,0],xy[:,1],s=45,color="tab:blue",zorder=3)
    for j,(p,k,x) in enumerate(zip(xy,result.phase_kinds,result.mole_fractions)):
        label = k if k!="liquid" else f"L{j+1}"
        offset = (28, 3) if k=="liquid" and x[0]>.95 else (5, 16 if k!="liquid" else 7)
        ax.annotate(label,p,xytext=offset,textcoords="offset points")
    # A thin physical triangle should be magnified, never artificially widened.
    rich = [i for i,x in enumerate(result.mole_fractions)
            if result.phase_kinds[i]=="liquid" and x[0]>.95]
    if result.n_phases==3 and rich:
        X = np.asarray(result.mole_fractions)
        inset = ax.inset_axes([.03,.58,.35,.31])
        inset.add_patch(Polygon(X[:,1:3],closed=True,facecolor="tab:orange",alpha=.35))
        inset.scatter(X[:,1],X[:,2],color="tab:blue",s=18)
        j = rich[0]
        inset.set_xlim(-.0003, max(.003, X[j,1]*1.7))
        inset.set_ylim(-.002, max(.02, X[j,2]*1.6))
        inset.set(xlabel="x water",ylabel="x ethanol",title="Benzene-rich corner (zoom)")
        inset.tick_params(labelsize=7)
        inset.xaxis.label.set_size(8);inset.yaxis.label.set_size(8);inset.title.set_size(8)
        inset.annotate("S",(0,0),xytext=(5,5),textcoords="offset points",fontsize=8)
        inset.annotate("L organic",X[j,1:3],xytext=(5,2),textcoords="offset points",fontsize=8)
        inset.grid(alpha=.2)
    z = np.asarray(feed)/np.sum(feed) @ corners
    ax.scatter(*z,marker="x",s=70,color="black",label="feed",zorder=4)
    ax.set_title(title);ax.legend(loc="upper right");fig.tight_layout()
    return fig,ax
