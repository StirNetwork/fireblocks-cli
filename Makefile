install-dev:
	pip install -e .[dev]

test:
	pytest

lint-license:
	reuse lint

annotate-SPD:
	@echo "📎 Annotating files..."
	reuse annotate  --license MPL-2.0 --copyright "Ethersecurity"  $(shell git ls-files '*.py' '*.sh')
pre-commit-refresh:
	@echo "🧹 Cleaning pre-commit cache..."
	pre-commit clean
	@echo "🔄 Installing pre-commit hooks..."
	pre-commit install --hook-type pre-commit
	@echo "⬆️  Updating pre-commit hooks..."
	pre-commit autoupdate
	@echo "🚀 Running all pre-commit hooks..."
	pre-commit run --all-files
build-pypi:
	python -m build
