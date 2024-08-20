.DEFAULT_GOAL := help

help: ## Displays makefile commands
	@grep -E '^[a-zA-Z0-9_-]+:.?## .$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

install:  ## Install dev-requirements and pre-commit
	@echo "----Installing Developer Requirements----"
	pip install -r dev-requirements.txt
	@echo "----Installing Requirements----"
	pip install -r src/requirements.txt
	@echo "----Installing Commit Hooks----"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "----Done----"

download-data:  ## Downloads agents and maps data from Valorant API
	@echo "----Downloading agents and maps data----"
	python download_data.py
	@echo "----Done----"

download-assets:  ## Downloads agent and map assets from Valorant API
	@echo "----Downloading agent and map assets----"
	python asset_downloader.py
	@echo "----Done----"
