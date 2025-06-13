.PHONY: install lint format test precommit build

install:
	uv pip install --system -e .[develop]

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

run:
	@ROLE=$${ROLE:-arx}; \
	docker build -f Dockerfile.$${ROLE} -t multi-agent-system-$${ROLE} . && \
	docker run --rm multi-agent-system-$${ROLE}
