ifeq (, $(shell which uv ))
  $(error "[ERROR] The 'uv' command is missing from your PATH. Install it from: https://docs.astral.sh/uv/getting-started/installation/")
endif

.PHONY: help
help: ## List phony targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: bootstrap
bootstrap: ## Bootstrap the development environment
	uv venv
	uv pip install -r requirements.txt

.PHONY: install
install: ## Install Plone
	.venv/bin/buildout -c development.cfg

.PHONY: start
start: bin/instance ## Start Zope instance
	bin/instance fg

.PHONY: clean
clean: ## Clean development environment
	rm -rf .venv bin develop-eggs eggs include lib node_modules parts .installed.cfg pyvenv.cfg
