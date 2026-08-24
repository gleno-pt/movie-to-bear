# Tutorial

## Setup
### Make the application directory and change to it
```bash
mkdir movie-to-bear
cd movie-to-bear
```

### Initialise the app with `uv`
```bash
uv init
```

### Create a virtual Python 3.12 environment
```bash
uv python install 3.12
uv python pin 3.12

```

#### Issue
When I ran `uv python pin 3.12` i recevied the following error: 
```bash
error: The requested Python version `3.12` is incompatible with the project `requires-python` value of `>=3.13`.
```

I changed the `pyproject.toml` file:
```yaml
requires-python = ">=3.13"
```
to:
```yaml
requires-python = ">=3.12"
```
Rerunning the command worked:
```bash
Pinned `.python-version` to `3.12`
```

Then run the following: 
```bash
uv sync

```

I changed the `pyproject.toml` file:
```yaml
requires-python = ">=3.12"
```
to:
```yaml
requires-python = ">=3.12,<3.13"
```
### Add dependencies
```bash
uv add fastapi uvicorn httpx pydantic-settings logstruct
```

### Add dev dependencies
```bash
uv add --dev pytest pytest-asyncio coverage ruff
```
### Confirm Python and `uv` versions:
```bash
uv run python --version
uv --version
```

They should be something like:
```bash
Python 3.12.8
uv 0.11.14 (3fdfdc7d4 2026-05-12 x86_64-pc-windows-msvc)
```


## Lesson 1 — Set up the project structure

### 1. Create the diretories
```text
movie-to-bear/
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
│
├── src/
│   └── movie_to_bear/
│       ├── __init__.py
│       └── main.py
│
└── tests/
    ├── __init__.py
    └── test_health.py
```

Run in the project folder: 
```bash
mkdir src\movie_to_bear
mkdir tests
```
Create package files:
```powershell
New-Item src\movie_to_bear\__init__.py
New-Item src\movie_to_bear\main.py
New-Item tests\__init__.py
New-Item tests\test_health.py

```

### 2. Install our dependencies
```bash
uv add fastapi uvicorn httpx pydantic-settings logstruct
uv add --dev pytest pytest-asyncio coverage ruff
```

Runtime dependencies
: These are needed when the application runs
Development Dependancies
: These are needed when we are developing/testing

> This was done in the setup already?!

### 3. Configure the `src` layout
The python package is here:
```text
src/
└── movie_to_bear/
```
Our tests are here:
```text
tests/
```

When we run the following:
```bash
uv run pytest

```
We want Python to be able to do:
```python
from movie_to_bear.main import app
```
without manually modifying `PYTHONPATH`.

Configure the package in `pyproject.toml`:

```yaml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/movie_to_bear"]
```

Run: 
```bash
uv sync
```

### 4. Create the first FastAPI application
The `src/movie_to_bear/main.py` should contain the below code:
```python
from fastapi import FastAPI


app = FastAPI(
    title="Movie to Bear",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

### 5. Run the application
From the `terminal`, run:
```bash
uv run uvicorn movie_to_bear.main:app --reload
```

Open in a browser:
```text
http://127.0.0.1:8000/health
```
You should get:
```json
{
  "status": "ok"
}
```
FastAPI will also automatically provide interactive API documentation at:
```text
http://127.0.0.1:8000/docs
```
and the alternative OpenAPI UI at:
```text
http://127.0.0.1:8000/redoc
```

### 6. Now write the test
The `tests/test_health.py` should contain:
```python
from fastapi.testclient import TestClient

from movie_to_bear.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Run the test:
```bash
uv run pytest
```

### 7. Run `coverage`
In the `terminal`, run:
```bash
uv run coverage run -m pytest
```

Then run:
```bash
uv run coverage report
```

## Lesson 2 — Configuration and environment variables
### 1. The problem we're solving
The goal is to make the application able to read configuration such as the TMDB API token without putting secrets into Python source code.

Use `pydantic-settings` to store secrets, etc.

### 2. Create `config.py`
Create `src/movie_to_bear/core/config.py`   
As well as src/movie_to_bear/core/\_\_init\_\_.py`

The `config.py` file should contain the following:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    tmdb_api_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
```

> Understand the following:
- `BaseSettings`    
    It is designed to populate fields from configuration sources, e.g. environment variables.
- `env_file=".env"`   
    This tells Pydantic Settings to look for a `.env` file.
- `case_sensitive=False`   
    This tells Pydantic Settings to ignore case. 


### 3. Create `.env` file

At the project root, create the `.env` file with the following:
```text
TMDB_API_TOKEN=test-token
```

### 4. Create `.env.example` file
At the project root, create the `.env.example` file:
```text
TMDB_API_TOKEN=
```
This files documents what configuration a developer needs.
The `.env.example` file can be committed to Git.   
The `.env` file should not be.

### 5. Update `.gitignore` file
Check your `.gitignore` file.

If `.env` isn't already there, add:
```text
.env
```

### 6. Test the configuraiton manually
From the `terminal`, run:
```bash
uv run python

```
In the REPL: 
```python
from movie_to_bear.core.config import settings

print(settings.tmdb_api_token)
```

The result should be: 
```text
test-token
```
Exit the REPL with:
```python
exit()
```

### 7. Why not just use `os.getenv()`?

```python
import os

token = os.getenv("TMDB_API_TOKEN")
```
Doing it this way spreads `os.getenv()` throughout the application as it grows. 

Using Pydantic Settings, allows a single configuration object: 

```python
settings.tmdb_api_token
```

### 8. Add a configuration test
Create `tests/test_config.py` with the following content:
```python
from movie_to_bear.core.config import settings


def test_tmdb_api_token_is_loaded() -> None:
    assert settings.tmdb_api_token == "test-token"
```

Run it:
```bash
uv run pytest
```


### 9. One problem with our test
Tests should control their own configuration.
This can be improved using pytest fixtures and environment-variable overrides.

### 10. Configuration precedence
In Pydantic Settings is that configuration can come from different sources.

An environment variable can override the `.env` variable.
For example, in `.env`:
```text
TMDB_API_TOKEN=test-token
``` 
but Powershell has:
```powershell
$env:TMDB_API_TOKEN="another-token"
```
then the environment variable takes precedence.

This is useful in production because `.env` files are not needed.

The Python application doesn't need to know where the value came from.

### 11. What we've achieved
The application as a configuration boundry:
```mermaid
flowchart TD
    .env --> settings["Settings
    tmdb_api_token"]
    settings --> FastAPI
    settings --> TMDBClient
    settings --> Logging

```

## Lesson 3 — Structured logging
### 1. The target architecture
### 2. Create the logging module
Create `src/movie_to_bear/core/logging.py` with the following content:
```python
import logging
import sys

import structlog


def configure_logging() -> None:
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
```

### 3. Refactor `main.py`
```python
import structlog
from fastapi import FastAPI

from movie_to_bear.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Movie to Bear",
        version="0.1.0",
    )

    logger = structlog.get_logger()

    @app.get("/health")
    async def health() -> dict[str, str]:
        logger.info(
            "health_check",
            status="ok",
        )

        return {"status": "ok"}

    return app


app = create_app()
```


> Understand the following concepts:
- **Application Factory**   
    ```python
    def create_app() -> FastAPI:
    ```
    This function is capable of constructing our application.
    
    ´´´python
    app = create_app()
    ```
    This creates the normal application instance that `Unicorn` uses.

### 4. Run the tests
```bash
uv run pytest
uv run uvicorn movie_to_bear.main:app --reload
curl http://127.0.0.1:8000/health
```

### 5. Understand what we did
The below code creates an event with two pieces of information, `event` and `status`:
```python
logger.info(
    "health_check",
    status="ok",
)
```
The processes add `logger`, `level` and `timestamp`.

`JSONRenderer` serialises the event.    
We don't construct the JSON ourselves.

Don't do this:
```python
logger.info('{"event": "health_check", "status": "ok"}')
```

### 6. Add a meaningful field

Change the following code in `src\movie_to_bear\main.py`:
```python
logger.info(
    "health_check",
    status="ok",
)
```
to:
```python
logger.info(
    "health_check",
    status="ok",
    component="api",
)
```


### 7. Don't test the JSON string
`structlog` provides testing utilities specifically for capturing log events.

Modify `tests/test_health.py` to contain:
```python
import structlog
from fastapi.testclient import TestClient

from movie_to_bear.main import create_app


def test_health() -> None:
    app = create_app()
    client = TestClient(app)

    with structlog.testing.capture_logs() as logs:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    health_logs = [log for log in logs if log["event"] == "health_check"]

    assert len(health_logs) == 1
    assert health_logs[0]["status"] == "ok"
    assert health_logs[0]["component"] == "api"
```

We're not asserting:
```python
assert some_json_string == "..."
```

We're inspecting the actual structured event.   
That makes the test much less brittle.


### 9. A subtle problem
There's something interesting about the code we've just written.

Our test calls:
```python
create_app()
```
and `create_app()` calls:
```python
configure_logging()
```
So every time we create an application, we're configuring global logging.

That's not ideal.

For example, imagine we eventually have:
```bash
test_search_movie
test_search_tv
test_tmdb_error
test_bear_export
test_health
...
```
and each test creates an application.

We don't want every application creation to repeatedly reconfigure global logging.

This is a good example of why application lifecycle and global configuration need to be considered separately.

We're not going to solve that yet.

Instead, I want you to see the problem first.

## Lesson 4 — Build the TMDB HTTP client
### 1. First, understand the TMDB authentication
TMDB's current API supports authentication using an **API Read Access Token**, sent as a Bearer token in the `Authorization` header.

Conceptually, the request looks like this:
```text
GET /3/search/movie?query=The%20Matrix
Authorization: Bearer YOUR_TOKEN
```

### 2. Add the TMDB base URL to configuration
In `src/movie_to_bear/core/config.py`, add: 
```python
class Settings(BaseSettings):
    tmdb_api_token: str
    tmdb_base_url: str = "https://api.themoviedb.org/3" <--
```

Notice that `tmdb_api_token` is mandatory.   
`tmdb_base_url` is optional because it has a default.

> **Secrets/configuration that must be supplied**   
versus   
**configuration with a sensible application default.**   

### 3. Add the HTTP timeout
Also add:
```python
class Settings(BaseSettings):
    tmdb_api_token: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    tmdb_timeout: float = 10.0 <--
```

### 4. Create the TMDB client
Create:
```text
src/movie_to_bear/clients/__init__.py
src/movie_to_bear/clients/tmdb.py
```

The client's function is to communicate with TMDB.
It doesn't know anything else about the API - FastAPI, Bear, the HTTP routes, etc. 

### 5. Create TMDBClient
Update `src/movie_to_bear/clients/tmdb.py` with the follwoing content: 
```python
import httpx
import structlog

from movie_to_bear.core.config import Settings


logger = structlog.get_logger()


class TMDBClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.tmdb_base_url
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_token}",
                "Accept": "application/json",
            },
            timeout=settings.tmdb_timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()
```
### 6. Understand the constructor
This: 
```python
self._client = httpx.AsyncClient(...)
```
creates a reuseable async HTTP client.

We're configuring:
```python
base_url = self._base_url
```
so later we can write:
```python
await self._client.get("/search/movie")
```

### 7. Authentication
This:
```python
headers = {
    "Authorization": f"Bearer {settings.tmdb_api_token}",
    "Accept": "application/json",
}
```
means every request made by this client gets:
```text
Authorization: Bearer <token>
Accept: application/json
```
automatically.

That's another reason to encapsulate HTTP communication in a client.

### 8. Add the first API operation
Add:
```python
    async def search_movies(self, query: str) -> dict:
        response = await self._client.get(
            "/search/movie",
            params={
                "query": query,
            },
        )

        response.raise_for_status()

        return response.json()
```

TMDB documents /3/search/movie as the movie search endpoint.

So:
```python
await client.search_movies("The Matrix")
```
eventually results in:
```text
GET /search/movie?query=The+Matrix
```

### 9. Why `raise_for_status()`?
This is important!

If TMDB returns `200` everything continues.
`httpx`raises an exception for anything else. 


### 10. Add logging
```python
    async def search_movies(self, query: str) -> dict:
        logger.info(
            "tmdb_search",
            media_type="movie",
            query=query,
        )

        response = await self._client.get(
            "/search/movie",
            params={
                "query": query,
            },
        )

        response.raise_for_status()

        logger.info(
            "tmdb_response",
            media_type="movie",
            status_code=response.status_code,
        )

        return response.json()
```
> Don't log the API token.


11. But don't call TMDB from a test
We don't want:
```python
async def test_search_movies():
    client = TMDBClient(settings)

    result = await client.search_movies("The Matrix")
```
because it makes a real request.
Instead, our test will replace the HTTP layer with a fake response.
This makes our tests:

- fast
- deterministic
- independent of the Internet
- independent of TMDB availability
- independent of API rate limits

### 12. Before we write the test
Our current TMDBClient creates its own:
```python
httpx.AsyncClient(...)
```
inside:
```python
__init__
```
That makes testing harder.

We could mock the internal _client, but there's a cleaner approach: **dependency injection.**

We'll eventually allow:
```python
TMDBClient(
    settings=settings,
    http_client=mock_http_client,
)
```
during testing.

## Lesson 5 — Dependency injection and mocking httpx

### 1. Modify `TMDBClient`

Change the constructor in `src/movie_to_bear/clients/tmdb.py`:
```python
import httpx
import structlog

from movie_to_bear.core.config import Settings


logger = structlog.get_logger()


class TMDBClient:
    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._http_client = http_client or httpx.AsyncClient(
            base_url=settings.tmdb_base_url,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_token}",
                "Accept": "application/json",
            },
            timeout=settings.tmdb_timeout,
        )

    async def close(self) -> None:
        await self._http_client.aclose()

    async def search_movies(self, query: str) -> dict:
        logger.info(
            "tmdb_search",
            media_type="movie",
            query=query,
        )

        response = await self._http_client.get(
            "/search/movie",
            params={"query": query},
        )

        response.raise_for_status()

        logger.info(
            "tmdb_response",
            media_type="movie",
            status_code=response.status_code,
        )

        return response.json()
```

The important part is:
```python
http_client: httpx.AsyncClient | None = None
```
If we don't provide one:
```python
TMDBClient(settings)
```
the class creates a real HTTP client.

But in a test we can provide one:
```python
TMDBClient(
    settings,
    http_client=fake_client,
)
```
That's dependency injection.

### 2. Why this is useful
> A class should receive important external dependencies rather than making them impossible to replace.

### 3. Create the TMDB tests
Create `tests/test_tmdb.py` with the follwing content:
```python
from unittest.mock import AsyncMock

import httpx

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.core.config import Settings


async def test_search_movies() -> None:
    response = httpx.Response(
        status_code=200,
        json={
            "page": 1,
            "results": [
                {
                    "id": 603,
                    "title": "The Matrix",
                }
            ],
            "total_pages": 1,
            "total_results": 1,
        },
    )

    http_client = AsyncMock(spec=httpx.AsyncClient)
    http_client.get.return_value = response

    settings = Settings(
        tmdb_api_token="test-token",
    )

    client = TMDBClient(
        settings=settings,
        http_client=http_client,
    )

    result = await client.search_movies("The Matrix")

    assert result["page"] == 1
    assert result["results"][0]["id"] == 603
    assert result["results"][0]["title"] == "The Matrix"

    http_client.get.assert_awaited_once_with(
        "/search/movie",
        params={"query": "The Matrix"},
    )
```

### 4. What's happening here?

#### Fake response
An actual `httpx.Response` is constructed:
```python
response = httpx.Response(
    status_code=200,
    json={...},
)
```
No actual request occurs.

#### Fake client
We are creating a mock that behaves like an `AsyncClient`:
```python
http_client = AsyncMock(spec=httpx.AsyncClient)
```

When we make a request to the mock client, no request is made.
The predefined response is returned.

### 5. We're testing more than the result
This assertion is particularly useful:
```python
http_client.get.assert_awaited_once_with(
    "/search/movie",
    params={"query": "The Matrix"},
)
```
We're checking that our client actually made the correct HTTP request.

### 6. Run it

#### Issue
1. Failed: async def functions are not natively supported.
    When running `uv run pytest`, I received the following error:
    ```bash
    tests/test_tmdb.py::test_search_movies - Failed: async def functions are not natively supported.
    ```

    I had to install `pytest-asyncio`:
    ```bash
    uv add --dev pytest-asyncio
    uv sync
    ```

    Configure `pytest` in `pyproject.toml`:
    ```yaml
    [tool.pytest.ini_options]
    asyncio_mode = "auto"
    ```


2. RuntimeError: Cannot call `raise_for_status` as the request instance has not been set on this response.
    In the test code, `httpx` expects the `Response` to be associated with a `Request`. A manually constructed response doesn't have one, so httpx raises this error.

    ```python
    request = httpx.Request(
        "GET",
        "https://api.themoviedb.org/3/search/movie",
    )

    response = httpx.Response(
        status_code=200,
        request=request, <--
        json={
            "page": 1,
            "results": [
                {
                    "id": 603,
                    "title": "The Matrix",
                }
            ],
            "total_pages": 1,
            "total_results": 1,
        },
    )
    ```


### 7. Test a TMDB error
Add the following code to `tests/test_tmdb.py`:
```python
import pytest


async def test_search_movies_raises_for_http_error() -> None:
    request = httpx.Request(
        "GET",
        "https://api.themoviedb.org/3/search/movie",
    )

    response = httpx.Response(
        status_code=500,
        request=request,
        json={"status_message": "Internal Server Error"},
    )

    http_client = AsyncMock(spec=httpx.AsyncClient)
    http_client.get.return_value = response

    settings = Settings(
        tmdb_api_token="test-token",
    )

    client = TMDBClient(
        settings=settings,
        http_client=http_client,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await client.search_movies("The Matrix")
```

### 8. Test that the token is actually used
The client is responsible for constructing the authenticated HTTP client when one isn't injected.

We can test the headers by injecting a fake client and checking that production construction is harder to test directly, but this points us toward a design improvement.

Rather than writing increasingly complicated tests around the constructor, we're going to make the HTTP configuration explicit.

That will lead us to a cleaner design where authentication configuration is isolated.

This will be implemented later.


### 9. Run Ruff

Run the following in the terminal:
```bash
uv run ruff check .
```

Also, run the following:
```bash
uv run ruff format --check .
```

If Ruff reports formatting issues, you can fix them with the following command:
```bash
uv run ruff format .
```

Then run the Ruff check again.


### 10. Run coverage

Finally:
```bash
uv run coverage run -m pytest
uv run coverage report
```

## Lesson 6 — The TMDB service layer
We have the following:
```mermaid
flowchart LR
    fastapi[fastAPI Endpoint]
    client[TMDB Client]
    tmdb[TMDB]

    fastapi-->client
    client-->httpx
    httpx-->tmdb
```
A service layer needs to be introduced: 
```mermaid
flowchart LR
    fastapi[fastAPI Endpoint]
    svc[TMDB Service]
    client[TMDB Client]
    tmdb[TMDB]
    fastapi-->svc
    svc-->client
    client-->tmdb
```

The distinction is important:
- Client = knows how to communicate with TMDB.
- Service = knows what our application wants to do with TMDB.
- FastAPI route = handles HTTP requests/responses.

### 1. Why do we need a service?

### 2. Create the service package
Create the following:
```bash
src/movie_to_bear/services/
├── __init__.py
└── tmdb.py
```

### 3. Create TMDBService

Put this into `src/movie_to_bear/services/tmdb.py`:

```python
from movie_to_bear.clients.tmdb import TMDBClient


class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(self, query: str) -> dict:
        return await self._client.search_movies(query)
```


### 4. Client vs service
Now the distinction becomes much more meaningful.

- The client returns **TMDB data**.
- The service returns **application data**.

### 5. Don't return dict forever
We don't want our application to become dependent on arbitrary TMDB JSON structures.   
If TMDB changes their structure, we don't want it to affect us too much.    
The application should eventually have its own model.   

### 6. Test the service

Create `tests/test_tmdb_service.py` with the following content:
```python
from unittest.mock import AsyncMock

from movie_to_bear.services.tmdb import TMDBService


async def test_search_movies() -> None:
    client = AsyncMock()

    client.search_movies.return_value = {
        "page": 1,
        "results": [
            {
                "id": 603,
                "title": "The Matrix",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_movies("The Matrix")

    assert result["page"] == 1
    assert result["results"][0]["id"] == 603
    assert result["results"][0]["title"] == "The Matrix"

    client.search_movies.assert_awaited_once_with("The Matrix")
```

We'll mock the **client**, not HTTP.   
Each layer has a focused test.   
The client mocked HTTP   
The service will mock the client.


### 7. Run the tests
Run the tests: 
```bash
uv run pytest
```

### 8. Introducing Pydantic models

Create:
```bash
src/movie_to_bear/models/
├── __init__.py
└── tmdb.py
```

Add the following to `src/movie_to_bear/models/tmdb.py`:
```python
from datetime import date

from pydantic import BaseModel


class MovieSearchResult(BaseModel):
    id: int
    title: str
    release_date: date | None = None
    overview: str | None = None
    poster_path: str | None = None
```

Also add:
```python
class MovieSearchResponse(BaseModel):
    page: int
    results: list[MovieSearchResult]
    total_pages: int
    total_results: int
```


### 9. Why Pydantic belongs here

Suppose TMDB returns:
```json
{
  "id": 603,
  "title": "The Matrix",
  "release_date": "1999-03-30"
}
```
Pydantic converts:
```text
"1999-03-30"
```
into:
```python
date(1999, 3, 30)
```
So our application isn't passing raw JSON strings around.

This becomes particularly valuable when we eventually create the Bear representation.

### 10. Modify the service

Change:
```python
async def search_movies(self, query: str) -> dict:
    return await self._client.search_movies(query)
```
to:
```python
from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.models.tmdb import MovieSearchResponse


class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(
        self,
        query: str,
    ) -> MovieSearchResponse:
        response = await self._client.search_movies(query)

        return MovieSearchResponse.model_validate(response)
```

This is the beginning of our **domain boundary**.


### 11. Update the service test

Change the `` to:
```python
from unittest.mock import AsyncMock

from movie_to_bear.models.tmdb import MovieSearchResponse
from movie_to_bear.services.tmdb import TMDBService


async def test_search_movies() -> None:
    client = AsyncMock()

    client.search_movies.return_value = {
        "page": 1,
        "results": [
            {
                "id": 603,
                "title": "The Matrix",
                "release_date": "1999-03-30",
                "overview": "A computer hacker learns...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_movies("The Matrix")

    assert isinstance(result, MovieSearchResponse)
    assert result.page == 1
    assert result.results[0].id == 603
    assert result.results[0].title == "The Matrix"
    assert result.results[0].release_date is not None
    assert result.results[0].release_date.year == 1999

    client.search_movies.assert_awaited_once_with("The Matrix")
```

### 12. One deliberate simplification

You might notice that we're calling:
```python
MovieSearchResponse.model_validate(response)
```
rather than having the HTTP client return a Pydantic model.

That's deliberate.

I'm keeping the responsibilities:

- TMDBClient = HTTP communication
- TMDBService = application interpretation
- Pydantic model = data contract

This separation gives us flexibility later.

## Lesson 7 — FastAPI dependency injection

### 1. Why dependency injection?
> Use FastAPI's dependency injection system to connect all the parts of the application together

We don't want the FastAPI route instantiating objects that it needs each time somebody calls the endpoint. 

FastAPI can construct the dependencies.

This also makes testing easier because the real dependencies can be replaced by mocks.



### 2. Create an API package

Create:
```bash
src/movie_to_bear/api/
├── __init__.py
└── dependencies.py
```

### 3. Create the TMDB client dependency
Add the following content to `src/movie_to_bear/api/dependencies.py`:
```python
from fastapi import Depends

from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.core.config import Settings, settings
from movie_to_bear.services.tmdb import TMDBService


def get_settings() -> Settings:
    return settings


def get_tmdb_client(
    app_settings: Settings = Depends(get_settings),
) -> TMDBClient:
    return TMDBClient(app_settings)


def get_tmdb_service(
    client: TMDBClient = Depends(get_tmdb_client),
) -> TMDBService:
    return TMDBService(client)
```

Three dependencies are created:
1. `get_settings()`
2. `get_tmdb_client()`
3. `get_tmdb_service()`

### 4. Why Depends()?

Consider:
```python
def get_tmdb_service(
    client: TMDBClient = Depends(get_tmdb_client),
) -> TMDBService:
```
We're telling FastAPI:

> Before calling get_tmdb_service, call get_tmdb_client and give me its result.

The chain does not have to be manually constructed each time.

### 5. Create the search router

Create `src/movie_to_bear/api/routes.py` with the following content:
```python
from fastapi import APIRouter, Depends, Query

from movie_to_bear.services.tmdb import TMDBService
from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.models.tmdb import MovieSearchResponse


router = APIRouter(
    prefix="/api/v1",
)


@router.get(
    "/search/movies",
    response_model=MovieSearchResponse,
)
async def search_movies(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MovieSearchResponse:
    return await service.search_movies(query)
```

### 6. Why `response_model`?

This:
```python
response_model = MovieSearchResponse
```
is important.

The service returns:
```python
MovieSearchResponse
```
and FastAPI uses the Pydantic model as the API contract.

The endpoint has a defined response structure.

### 7. `Query(min_length=1)`
The query string is validated:
```python
query: str = Query(min_length=1)
```
So:
```text
/api/v1/search/movies?query=The%20Matrix
```
is valid.

But:
```text
/api/v1/search/movies?query=
```
will be rejected by FastAPI with a validation error.

We're deliberately putting basic HTTP validation at the A


Basic HTTP validation is deliberately being put at the API boundary.


### 8. Connect the router to the application

Modify `src/movie_to_bear/main.py`.
Add:
```python
from movie_to_bear.api.routes import router
```
and inside `create_app()`:
```python
app.include_router(router)
```

### 9. Run the application

Start:
```bash
uv run uvicorn movie_to_bear.main:app --reload
```
Now open:
```text
http://127.0.0.1:8000/docs
```
You should see:
```text
GET /health
GET /api/v1/search/movies
```
FastAPI generated the interactive API documentation automatically from our route definitions and Pydantic models.

### 10. Don't test the real TMDB yet

We're going to test the endpoint without the Internet.   
This is one of the most important benefits of FastAPI dependency injection.

### 11. Override the dependency in the test

Create `tests/test_search.py` with the following content:
```python
from datetime import date

from fastapi.testclient import TestClient

from movie_to_bear.api.dependencies import get_tmdb_service
from movie_to_bear.main import app
from movie_to_bear.models.tmdb import MovieSearchResponse, MovieSearchResult


def test_search_movies() -> None:
    class FakeTMDBService:
        async def search_movies(self, query: str):
            assert query == "The Matrix"

            return MovieSearchResponse(
                page=1,
                results=[
                    MovieSearchResult(
                        id=603,
                        title="The Matrix",
                        release_date=date(1999, 3, 30),
                        overview="A computer hacker...",
                        poster_path="/poster.jpg",
                    )
                ],
                total_pages=1,
                total_results=1,
            )

    fake_service = FakeTMDBService()
    app.dependency_overrides[get_tmdb_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get(
            "/api/v1/search/movies",
            params={"query": "The Matrix"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["page"] == 1
        assert data["results"][0]["id"] == 603
        assert data["results"][0]["title"] == "The Matrix"

    finally:
        app.dependency_overrides.clear()
```
### 12. FastAPI dependency overrides
```python
app.dependency_overrides[get_tmdb_service] = FakeTMDBService()
```
This tells FastAPI:

> Whenever the application asks for get_tmdb_service, give it this fake service instead.

### 13. Why try/finally?

This is important:
```python
try:
    ...
finally:
    app.dependency_overrides.clear()
```
Dependency overrides are stored on the FastAPI application object.

If we forget to clear them, another test could accidentally inherit the override.

That creates extremely confusing test failures.

We'll improve this later with a pytest fixture so we don't have to repeat the cleanup manually.

For now, I want you to see what FastAPI is actually doing.

14. Run the tests

Now:
```bash
uv run pytest
```

#### Issue
1. When running: `uv run ruff check .`, the following error occurs:
    ```bash
    B008 Do not perform function call `Depends` in argument defaults; instead, perform the call within the function, or read the default from a module-level singleton variable
    --> src/movie_to_bear/api/dependencies.py:13:30
    |
    12 | def get_tmdb_client(
    13 |     app_settings: Settings = Depends(get_settings),
    |                              ^^^^^^^^^^^^^^^^^^^^^
    14 | ) -> TMDBClient:
    15 |     return TMDBClient(app_settings)
    ```

    This is a **Ruff/flake8-bugbear (B008)** issue, and in this case Ruff is flagging a pattern that is actually idiomatic FastAPI.

    To fix this, configure Ruff to allow `Depends` calls in defaults.   
    Add the following to `pyproject.toml`:

    ```yaml
    [tool.ruff.lint]
    extend-ignore = ["B008"]
    ```
2. FAILED tests/test_search.py::test_search_movies - TypeError: <tests.test_search.test_search_movies.<locals>.FakeTMDBService object at 0x75b3548ee7e0> is not a callable object

    FastAPI expects the override to be a callable — normally a function — but we're giving it an instance.

    Change `tests/test_search.py` from:
    ```python
    app.dependency_overrides[get_tmdb_service] = FakeTMDBService()
    ```
    to:
    ```python
    fake_service = FakeTMDBService()

    app.dependency_overrides[get_tmdb_service] = lambda: fake_service
    ```

## Lesson 8 — Introduce a media domain model

The key design decision is:

> TMDB is an external data source. Our application should not make its internal model depend completely on TMDB's JSON structure.

### 1. The problem with our current model

The current model `MovieSearchResult.py` works from movies. However, it will not work for TV series. We would have to translate TV series data somewhere.   
This is what the service layer is for.

### 2. Create a domain model

Create `src/movie_to_bear/models/media.py` with the following content:
```python
from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class MediaType(StrEnum):
    MOVIE = "movie"
    TV = "tv"


class Media(BaseModel):
    id: int
    media_type: MediaType
    title: str
    overview: str | None = None
    release_date: date | None = None
    poster_path: str | None = None
```


### 3. Why use `StrEnum`?

`StrEnum` gives us string-like enum values.   
This works nicely with JSON APIs and Pydantic.

### 4. Keep the TMDB models

We now have two different concepts:
```text
models/
├── media.py
└── tmdb.py
```

TMDB models are external representations 
Media model is internal representation.

### 5. Update the service

Change the service to translate the TMDB result into our domain model.   

Add the following content to `src/movie_to_bear/models/media.py`:
```python
class MediaSearchResponse(BaseModel):
    page: int
    results: list[Media]
    total_pages: int
    total_results: int
```
### 6. Translate TMDB → domain

Update `services/tmdb.py`:
```python
from movie_to_bear.clients.tmdb import TMDBClient
from movie_to_bear.models.media import (
    Media,
    MediaSearchResponse,
    MediaType,
)
from movie_to_bear.models.tmdb import MovieSearchResponse


class TMDBService:
    def __init__(self, client: TMDBClient) -> None:
        self._client = client

    async def search_movies(
        self,
        query: str,
    ) -> MediaSearchResponse:
        response = await self._client.search_movies(query)

        tmdb_response = MovieSearchResponse.model_validate(response)

        return MediaSearchResponse(
            page=tmdb_response.page,
            results=[
                Media(
                    id=movie.id,
                    media_type=MediaType.MOVIE,
                    title=movie.title,
                    overview=movie.overview,
                    release_date=movie.release_date,
                    poster_path=movie.poster_path,
                )
                for movie in tmdb_response.results
            ],
            total_pages=tmdb_response.total_pages,
            total_results=tmdb_response.total_results,
        )
```

### 7. Update the API response model

The route currently says:
```python
response_model = MovieSearchResponse
```
Change that to:
```python
response_model = MediaSearchResponse
```
and update the return type:
```python
async def search_movies(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MediaSearchResponse:
    return await service.search_movies(query)
``` 
Now the public API exposes our model, not TMDB's model.

### 8. Update the service test

Change `tests/test_tmdb_service.py` with the following: 
```python
from movie_to_bear.models.media import MediaSearchResponse, MediaType


result = await service.search_movies("The Matrix")

assert isinstance(result, MediaSearchResponse)
assert result.page == 1
assert result.results[0].id == 603
assert result.results[0].title == "The Matrix"
assert result.results[0].media_type == MediaType.MOVIE
assert result.results[0].release_date is not None
assert result.results[0].release_date.year == 1999
```

We're now testing something meaningful:

> Does the service correctly translate TMDB data into our application's media model?

### 9. Update the API test

Update the fake service with the following:
```python
from movie_to_bear.models.media import (
    Media,
    MediaSearchResponse,
    MediaType,
)

fake_response = MediaSearchResponse(
    page=1,
    results=[
        Media(
            id=603,
            media_type=MediaType.MOVIE,
            title="The Matrix",
            release_date="1999-03-30",
            overview="A computer hacker...",
            poster_path="/poster.jpg",
        )
    ],
    total_pages=1,
    total_results=1,
)
return fake_response
```
### 10. Run everything
```bash
uv run ruff check .
uv run ruff format --check .
uv run coverage run -m pytest
uv run coverage report
```
## Lesson 9 — TMDB TV search

### 1. Add a TV model

Add new models to `src/movie_to_bear/models/tmdb.py`:
```python
class TVSearchResult(BaseModel):
    id: int
    name: str
    first_air_date: date | None = None
    overview: str | None = None
    poster_path: str | None = None


class TVSearchResponse(BaseModel):
    page: int
    results: list[TVSearchResult]
    total_pages: int
    total_results: int
```

### 2. Add `search_tv()`to the client
Add the following content to `src/movie_to_bear/clients/tmdb.py`:
```python
async def search_tv(self, query: str) -> dict:
    logger.info(
        "tmdb_search",
        media_type="tv",
        query=query,
    )

    response = await self._http_client.get(
        "/search/tv",
        params={"query": query},
    )

    response.raise_for_status()

    logger.info(
        "tmdb_response",
        media_type="tv",
        status_code=response.status_code,
    )

    return response.json()
```

### 3. Add TV search to the service

Add the following to `src/movie_to_bear/services/tmdb.py`:
```python
from movie_to_bear.models.tmdb import (
    MovieSearchResponse,
    TVSearchResponse,
)


async def search_tv(
    self,
    query: str,
) -> MediaSearchResponse:
    response = await self._client.search_tv(query)

    tmdb_response = TVSearchResponse.model_validate(response)

    return MediaSearchResponse(
        page=tmdb_response.page,
        results=[
            Media(
                id=show.id,
                media_type=MediaType.TV,
                title=show.name,
                overview=show.overview,
                release_date=show.first_air_date,
                poster_path=show.poster_path,
            )
            for show in tmdb_response.results
        ],
        total_pages=tmdb_response.total_pages,
        total_results=tmdb_response.total_results,
    )
```

### 4. Add the TV route
Add the following content to `src/movie_to_bear/api/routes.py`:
```python
from movie_to_bear.models.media import MediaSearchResponse


@router.get(
    "/search/tv",
    response_model=MediaSearchResponse,
)
async def search_tv(
    query: str = Query(min_length=1),
    service: TMDBService = Depends(get_tmdb_service),
) -> MediaSearchResponse:
    return await service.search_tv(query)
```

### 5. Test the TMDB client
Add the following to `tests/test_tmdb.py`:
```python
async def test_search_tv() -> None:
    request = httpx.Request(
        "GET",
        "https://api.themoviedb.org/3/search/tv",
    )

    response = httpx.Response(
        status_code=200,
        request=request,
        json={
            "page": 1,
            "results": [
                {
                    "id": 1399,
                    "name": "Game of Thrones",
                    "first_air_date": "2011-04-17",
                    "overview": "Seven noble families...",
                    "poster_path": "/poster.jpg",
                }
            ],
            "total_pages": 1,
            "total_results": 1,
        },
    )

    http_client = AsyncMock(spec=httpx.AsyncClient)
    http_client.get.return_value = response

    settings = Settings(
        tmdb_api_token="test-token",
    )

    client = TMDBClient(
        settings=settings,
        http_client=http_client,
    )

    result = await client.search_tv("Game of Thrones")

    assert result["page"] == 1
    assert result["results"][0]["id"] == 1399
    assert result["results"][0]["name"] == "Game of Thrones"

    http_client.get.assert_awaited_once_with(
        "/search/tv",
        params={"query": "Game of Thrones"},
    )
```


### 6. Test the service translation

Add the following to `tests/test_tmdb_service.py`:

```python
async def test_search_tv() -> None:
    client = AsyncMock()

    client.search_tv.return_value = {
        "page": 1,
        "results": [
            {
                "id": 1399,
                "name": "Game of Thrones",
                "first_air_date": "2011-04-17",
                "overview": "Seven noble families...",
                "poster_path": "/poster.jpg",
            }
        ],
        "total_pages": 1,
        "total_results": 1,
    }

    service = TMDBService(client)

    result = await service.search_tv("Game of Thrones")

    assert isinstance(result, MediaSearchResponse)
    assert result.page == 1

    media = result.results[0]

    assert media.id == 1399
    assert media.title == "Game of Thrones"
    assert media.media_type == MediaType.TV
    assert media.release_date is not None
    assert media.release_date.year == 2011

    client.search_tv.assert_awaited_once_with("Game of Thrones")
```



### 7. Test the API
Add another test to `tests/test_search.py`:
```python
class FakeTMDBService:
    async def search_movies(self, query: str) -> MediaSearchResponse:
        return MediaSearchResponse(
            page=1,
            results=[
                Media(
                    id=603,
                    media_type=MediaType.MOVIE,
                    title="The Matrix",
                    release_date="1999-03-30",
                )
            ],
            total_pages=1,
            total_results=1,
        )

    async def search_tv(self, query: str) -> MediaSearchResponse:
        return MediaSearchResponse(
            page=1,
            results=[
                Media(
                    id=1399,
                    media_type=MediaType.TV,
                    title="Game of Thrones",
                    release_date="2011-04-17",
                )
            ],
            total_pages=1,
            total_results=1,
        )
```


### 8. Run the tests



### 9. We now have a useful abstraction
TMDB has two different APIs with two different response formats.   
The application only has one.   



### 10. One thing I want you to notice
We have two endpoints:
- movies
- tv

We want to allow the user to search for a title, and not be bothered with weather it is a movie or a tv series.
