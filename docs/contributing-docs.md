# Maintain the documentation

The documentation is written in Markdown and Jupyter notebooks and built with
MkDocs Material. Search, a navigation sidebar, code-copy buttons, equations and
readable notebook outputs are included. The library source remains in the
private ThermoWeave repository.

## Build locally

From the ThermoWeave repository root, install documentation dependencies in an
environment of your choice:

```text
python -m pip install -r requirements-docs.txt
python tools/prepare_docs.py --output ../thermoweave-docs
```

Then enter the generated documentation checkout and build or preview it:

```text
cd ../thermoweave-docs
python -m mkdocs build --strict
python -m mkdocs serve
```

Open the local URL printed by MkDocs. The preparation command copies only the
documentation, tutorial notebook sources and required companion files. It does
not copy the library implementation, molecular databases, external backends,
credentials or model weights. It leaves an existing target's `.git` directory
intact. The destination must be outside the library checkout.

## GitHub Pages

The publication target is a dedicated documentation repository. Its workflow
builds the site on pushes to `main`, validates links with `--strict`, uploads
the static artifact and deploys it through the official GitHub Pages actions.
The deployment does not install ThermoWeave or run any EOS/backend calculation.

To update the site, edit the documentation in the library checkout, rerun the
preparation command targeting the documentation checkout, review that checkout's
diff, and commit/push the reviewed documentation changes. Refresh saved notebook
outputs only after separately validating the actual calculations. Pages serves
the last successful deployed build.

The site's hosting visibility is separate from the library repository's
visibility. GitHub Free organizations can serve Pages from a public docs
repository; a private source repository requires an eligible paid plan. See
[GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Style and information architecture

The source theme is configured in `mkdocs.yml`; additional typography, colors,
responsive rules and notebook styling live in `docs/assets/stylesheets/thermoweave.css`.
IBM Plex fonts are self-hosted in `docs/assets/fonts/`, with their OFL license
and source hashes. The documentation build needs no external font service.
Both light and dark palettes must keep readable text, links, code and figures.

Theory is organized under `docs/theory.md` and `docs/theory/`. It explains the
models, assumptions and equations, with references and links to practical use.
The Practical guide starts at `docs/guide/index.md`, with installation, model
setup and calculation recipes. Runnable notebooks have their own Tutorials tab.
Keep the existing model/setup page URLs when reorganizing the navigation.

The common-tangent figure is an explicitly labelled analytic Margules example.
Regenerate it in an environment with the tutorial dependencies using
`python tools/render_theory_figures.py`. The site build only copies the saved
SVG and notebook outputs; it does not execute scientific calculations.
