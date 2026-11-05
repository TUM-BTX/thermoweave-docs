# ThermoWeave documentation

Documentation website: https://tum-btx.github.io/thermoweave-docs/

The ThermoWeave library is maintained separately in the private [TUM-BTX/ThermoWeave repository](https://github.com/TUM-BTX/ThermoWeave).

Build with Python 3.12:

```bash
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
python -m mkdocs serve
```

The site renders saved notebook outputs without running calculations. See docs/contributing-docs.md for the source synchronization workflow.
