# Notebooks

This repository contains exploratory notebooks and planning documents for a multi-agent system powered by `LLMGraphTransformer`.

- [PRD.md](PRD.md) describes the product requirements for building the agents.
- [PLAN.md](PLAN.md) outlines the development tasks and architecture approach.

## Development Setup

Install dependencies using `uv` and run the pre-configured quality checks via `make`:

```bash
make install
make lint
make format
make test
```

The project follows a clean architecture layout under the `domain`, `application`, `interfaces`, and `infrastructure` packages.
