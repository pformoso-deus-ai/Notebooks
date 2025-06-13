# Notebooks

This repository contains exploratory notebooks and planning documents for a multi-agent system powered by `LLMGraphTransformer`.

- [PRD.md](PRD.md) describes the product requirements for building the agents.
- [PLAN.md](PLAN.md) outlines the development tasks and architecture approach.

## Prerequisites

- Python 3.12
- Install `uv`:
  ```bash
  pip install uv
  ```

## Development Setup

Install dependencies using `uv` and run the pre-configured quality checks via `make`. The commands `make install`, `make lint`, `make format` and `make test` depend on `uv`:

```bash
make install
make lint
make format
make test
```

The project follows a clean architecture layout under the `domain`, `application`, `interfaces`, and `infrastructure` packages.
