# If the `COPYRIGHT_HOLDER` file exists and contains a string shorter than 50 characters,
# use it as the name of the copyright holder.
# If not, fall back to the default value: "Ethersecurity Inc."
copyright_holder ?= $(shell bash scripts/get_copyright.sh)
change_files ?= $(shell bash scripts/get_changed_files.sh)

install-dev:
	pip install -e .[dev]

test:
	pytest

lint-license:
	reuse lint

annotate-SPD:
	@echo "📎 Annotating files..."
	reuse annotate  --license MPL-2.0 --copyright "${copyright_holder}"  ${change_files}
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
