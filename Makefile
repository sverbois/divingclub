.PHONY: help  # List phony targets
help:
	@cat "Makefile" | grep '^.PHONY:' | sed -e "s/^.PHONY:/- make/"

.PHONY: install  # Install development environment
install: bin/buildout
	bin/buildout -c development.cfg

.PHONY: start  # Start Zope instance
start: bin/instance
	bin/instance fg

.PHONY: clean  # Clean development environment
clean:
	rm -r .vscode bin develop-eggs include lib parts .installed.cfg pyvenv.cfg

bin/instance: bin/buildout

bin/buildout: bin/pip
	bin/pip install -r https://dist.plone.org/release/6.0.6/requirements.txt

bin/pip:
	python3.9 -m venv .