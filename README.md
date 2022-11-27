# s3-cache-header-setter-python

## Linting

Linting commands to run from the devcontainer/pipeline.

Pylint

```bash
pylint header_setter
```

Mypy

```bash
mypy header_setter
```

Bandit

```bash
bandit -r header_setter
```

## Unit testing

```bash
pytest --cov-report html
```
