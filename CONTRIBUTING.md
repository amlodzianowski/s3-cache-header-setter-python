# Welcome to the contributing guide <!-- omit in toc -->

Thank you for investing your time in contributing to our project!

## New contributor guide

To get an overview of the project, read the [README](README.md).

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

Megalinter

```bash
docker run -v `pwd`:/tmp/lint oxsecurity/megalinter:v6

## Testing

### Unit testing

```bash
pytest --cov-report html
```

### Integration testing

```bash
npx sls invoke -f setter -s dev -p tests/fixtures/s3_event.json
```

## Release

This project uses [Standard Version](https://www.npmjs.com/package/standard-version) for conducting releases. All commits should follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for accurately generating the CHANGELOG.md contents.

To perform a release

```bash
npm install
npm run release
```
