.PHONY: install test lint format clean dev-install precommit build

install:
	uv pip install --system -e .[develop]

dev-install:
	uv pip install -e .[develop]

test:
	pytest

lint:
	ruff check .

format:
	black .
	ruff check --fix .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

precommit:
	pre-commit run --all-files

build:
	echo "Build placeholder"

run:
	@ROLE=$${ROLE:-arx}; \
	docker build -f Dockerfile.$${ROLE} -t multi-agent-system-$${ROLE} . && \
	docker run --rm multi-agent-system-$${ROLE}
