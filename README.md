# Notebooks

This repository contains exploratory notebooks and planning documents for a multi-agent system powered by `LLMGraphTransformer`.

The core functionality relies on the `llm-graph-transformer` package, which will be installed automatically when running `make install`.

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

## Continuous Integration

All contributions are validated by a GitHub Actions workflow that executes `make lint`, `make format --check` and `make test` on every pull request.

The project follows a clean architecture layout under the `domain`, `application`, `interfaces`, and `infrastructure` packages.

## CLI Usage

Run the command-line interface with Python's `-m` option:

```bash
python -m multi_agent_system execute-command hello
```

## Running with Docker

You can build and run an agent container using the `make run` target. Pass the
desired agent role via the `ROLE` variable (`arx` for the architect agent or
`d` for the developer agent). For example:

```bash
make run ROLE=arx  # build and start the architect container
make run ROLE=d    # build and start the developer container
```

## License

This project is licensed under the [MIT License](LICENSE).

