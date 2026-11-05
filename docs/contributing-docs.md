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
