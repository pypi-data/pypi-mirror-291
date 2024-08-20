<p align="center">
  <a href="https://chiloproject.io"><img src="https://raw.githubusercontent.com/dual/chilo-docs/main/img/logo-no-bg.png" alt="Chilo"></a>
</p>
<p align="center">
    <em>Chilo is a lightweight, form-meets-function, opinionated (yet highly configurable) api framework</em>
</p>

[![CircleCI](https://circleci.com/gh/dual/chilo.svg?style=shield)](https://circleci.com/gh/syngenta/acai-python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dual_chilo&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dual_chilo)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dual_chilo&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dual_chilo)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dual_chilo&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dual_chilo)
[![pypi package](https://img.shields.io/pypi/v/chilo-api?color=%2334D058&label=pypi%20package)](https://pypi.org/project/chilo-api/)
[![python](https://img.shields.io/pypi/pyversions/chilo-api.svg?color=%2334D058)](https://pypi.org/project/chilo-api)
[![Inline docs](https://inch-ci.org/github/dwyl/hapi-auth-jwt2.svg?branch=master)](https://chiloproject.io)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

# Chilo
Chilo, short for chilorhinophis (meaning two headed snake), is a lightweight, form-meets-function, opinionated (yet highly configurable) api framework.

## Benefits
* No route definitions needed; route based on your directory structure
* Built-in OpenAPI request and response validation
* Ease of use with gunicorn
* Generate OpenAPI spec from code base
* Infinitely customizable with middleware extensions

## Philosophy

The Chilo philosophy is to provide a dry, configurable, declarative framework, which encourages Happy Path Programming (HPP).

Happy Path Programming is an idea in which inputs are all validated before operated on. This ensures code follows the happy path without the need for mid-level, nested exceptions and all the nasty exception handling that comes with that. The library uses layers of customizable middleware options to allow a developer to easily dictate what constitutes a valid input, without nested conditionals, try/catch blocks or other coding blocks which distract from the happy path which covers the majority of the source code's intended operation.

## Documentation & Examples

* [Full Docs](https://chiloproject.io)
* [Examples](https://github.com/dual/chilo-docs/tree/main/examples)
* Tutorial (coming soon)

## Quick Start

#### 0. Install

```bash
$ pip install chilo_api
# pipenv install chilo_api
# poetry add chilo_api
```

#### 1. Create `main.py`

```python
from chilo_api import Chilo


api = Chilo(
    base_path='/',
    handlers='api/handlers',
)
```

#### 2. Create First Handler

`{PWD}/api/handlers/__init__.py`
```python
def get(request, response):
    response.body = {'hello': 'world'}
    return response
```

#### 3. Run your API

```bash
python -m chilo_api serve --api=main --reload=true
```

#### 4. Checkout your API

[http://127.0.0.1:3000/](http://127.0.0.1:3000/)

#### 5. Validate Your Endpoint (optional)

```python
from chilo_api import requirements


@requirements(required_params=['greeting'])
def get(request, response):
    response.body = {'hello': request.query_params['greeting']}
    return response
```

#### 6. Checkout your API (again)

[http://127.0.0.1:3000/?greeting=developer](http://127.0.0.1:3000/?greeting=developer)