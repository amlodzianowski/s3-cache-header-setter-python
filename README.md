# s3-cache-header-setter-python

This project is a serverless helper for configuring [Cache-Control headers](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html#ExpirationAddingHeadersInS3) on objects uploaded to S3.

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

## Deployment

### Prerequisites

[Pipenv](https://pipenv.pypa.io/en/latest/) installed on the deployment machine
[Node](https://nodejs.org/en/download/) installed on the deployment machine

```bash
npx sls deploy -s dev
npx sls invoke -f setter -s dev -p tests/fixtures/s3_event.json
```

## TODO

Update the `serverless-python-requirements` dependency once the fix [for this](https://github.com/serverless/serverless-python-requirements/issues/716) is released
