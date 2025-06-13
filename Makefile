.PHONY: install lint format test precommit build

install:
uv pip install -e .[develop]

lint:
ruff .

format:
black .

precommit:
pre-commit run --all-files

test:
pytest

build:
echo "Build placeholder"
