# TONSearch API Documentation Draft

This repository issue board includes task **T08 — Write API Documentation** with the requirement to document three public APIs in **OpenAPI 3.0**:

- Search endpoint
- Brief generation endpoint
- Risk scoring endpoint

This contribution adds a first draft of that specification in `openapi.yaml`.

## Files

- `openapi.yaml` — OpenAPI 3.0.3 draft spec for the public TONSearch API

## What is covered

### 1. Search API
Documented as `POST /search`.

Includes:
- natural-language query input
- filter support
- pagination cursor
- ranked search results
- normalized intent/entity parsing

### 2. Brief Generation API
Documented as `POST /briefs`.

Includes:
- brief request payload
- supported output formats
- section selection
- structured response example

### 3. Risk Scoring API
Documented as `POST /risk-scores`.

Includes:
- entity-scoped risk scoring
- opportunity scoring
- explanation signals
- confidence score

### 4. Error Handling
Documented reusable responses for:
- `400 invalid_request`
- `401 unauthorized`
- `403 forbidden`
- `404 not_found`
- `429 rate_limited`
- `500 internal_error`

### 5. Authentication
Documented bearer-token auth under `components.securitySchemes.bearerAuth`.

### 6. Rate Limits
Added a documented rate-limit section via OpenAPI extensions:
- authenticated default: `120 rpm`
- anonymous default: `10 rpm`

## Assumptions
Because the repository currently exposes planning/tasks rather than a running implementation, the spec makes explicit draft assumptions:

- base URLs are placeholders
- exact field names may change once the backend exists
- examples are illustrative
- auth and rate limits are conservative defaults

These assumptions are intentionally called out in the `info.description` so the file is still useful without pretending implementation details already exist.

## Recommended next improvements
If the maintainers accept this direction, the next pass should:

1. align field names with the actual backend
2. add response schemas for export/PDF workflow
3. define shared entity models in more depth
4. document webhook/async generation if briefs become long-running jobs
5. publish a rendered docs site from this spec

## Validation
The YAML parses successfully as YAML locally. A next step would be linting it with an OpenAPI linter once one is added to the repo.
