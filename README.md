# Student ML API

A Flask-based API developed to demonstrate a professional MLOps CI/CD workflow using Git, GitHub Pull Requests, GitHub Actions, Docker, semantic versioning, and GitHub Container Registry (GHCR).

## Project Overview

The project demonstrates the following workflow:

Feature Branch → Pull Request → Automated CI → Code Review → Merge into Main → Version Tag → Docker Build → Container Registry

Direct development on the `main` branch is avoided. Changes are introduced through feature branches and validated through GitHub Actions before merging.

## API Endpoints

### Health Endpoint

`GET /health`

The endpoint reports the health of the application together with application and model version information.

### Prediction Endpoint

`POST /predict`

Example request:

```json
{
  "value": 5
}
```

Example prediction:

```json
{
  "input": 5,
  "prediction": 10
}
```

The endpoint validates missing and invalid input and returns an appropriate error response.

## Unit Testing

The project uses `pytest`.

The test suite verifies:

- Health endpoint success
- Successful prediction
- Missing prediction input
- Invalid prediction input

Run the tests with:

```bash
pytest -v
```

## Continuous Integration

The CI workflow is defined in:

`.github/workflows/ci.yml`

CI runs for Pull Requests targeting `main` and performs:

1. Repository checkout
2. Python environment setup
3. Dependency installation
4. Unit tests
5. Docker build validation

A failed test or Docker build causes the CI check to fail and prevents unsafe changes from being merged.

## Docker

The application uses a version-specific Python base image and follows Docker layer-ordering practices.

Build an image:

```bash
docker build -t student-ml-api:1.0.0 .
```

Run the container:

```bash
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
```

Test the application:

```bash
curl http://localhost:5000/health
```

## Release Workflow

The release workflow is defined in:

`.github/workflows/release.yml`

It is triggered by semantic Git tags such as:

- `v1.0.0`
- `v1.1.0`

The release pipeline:

1. Checks out the repository
2. Runs tests
3. Authenticates with GHCR
4. Builds the Docker image
5. Applies versioned image tags
6. Publishes the image to the registry

Container images are published to:

`ghcr.io/zarnab123/student-ml-api`

Required released versions include:

- `1.0.0`
- `1.1.0`
- `latest`

## Versioning and Rollback

Semantic version tags are used to create reproducible releases.

Version `1.0.0` remains available in the registry after newer releases, allowing the application to be rolled back without rebuilding the source code.

A rollback can be performed by running the previously published image:

```bash
docker pull ghcr.io/zarnab123/student-ml-api:1.0.0
docker run -d -p 5003:5000 ghcr.io/zarnab123/student-ml-api:1.0.0
```

The `/health` endpoint can then be used to verify that version `1.0.0` is running.

## Release Traceability

Traceability for application version `1.1.0`:

- Pull Request: `#4`
- Merge Commit: `99af2bc`
- Git Tag: `v1.1.0`
- Docker Image: `ghcr.io/zarnab123/student-ml-api:1.1.0`
- Image Digest: `sha256:5c0c873e7be80f12248599f718104102bec949400458424b4c264196748eb55b`

This provides a traceable chain from the reviewed source change to the exact published container artifact.

## OCI Image Metadata

The Docker image includes OCI metadata labels for:

- Application version
- Git commit revision
- Source repository
- Build date

The release workflow also supports commit-SHA image tagging for commit-specific traceability.

## Docker Layer Caching

The Dockerfile copies `requirements.txt` before the application source code.

This allows Docker to reuse the dependency-installation layer when only `app.py` changes. If `requirements.txt` changes, the dependency layer must be rebuilt.

## Failure Analysis

### Failure 1 — Failed pytest / CI

**Symptom:**  
The GitHub Actions CI pipeline failed after an intentionally incorrect assertion was introduced in the health endpoint test.

**Root Cause:**  
The test expected an incorrect health status, causing the actual API response and expected test value to differ.

**Evidence:**  
The pytest step failed and GitHub Actions marked the CI check as failed.

**Correction:**  
The health endpoint test was corrected to expect the proper `healthy` status. The correction was committed with:

`fix: correct health endpoint test`

After the fix was pushed, the tests and CI pipeline passed successfully.

### Failure 2 — Wrong Container Port

**Symptom:**  
The application health endpoint could not be reached when an incorrect container-port mapping was used.

**Root Cause:**  
The Flask application listens on port `5000` inside the container, while the Docker mapping targeted an incorrect internal container port.

**Evidence:**  
The health request failed with the incorrect mapping. With the correct mapping, the application became reachable.

**Correction:**  
The container was mapped to its correct internal port `5000`, after which the `/health` endpoint returned the expected response.

## Technologies

- Python
- Flask
- pytest
- Git
- GitHub
- GitHub Actions
- Docker
- GitHub Container Registry (GHCR)
