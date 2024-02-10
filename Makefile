PRETTIER_DIFF=$(shell prettier . --list-different)
GIT_FILES=git ls-files -z | tr '\0' '\n'
GIT_UNTRACKED_FILES=git ls-files -z --exclude-standard --others | tr '\0' '\n'
# If there is no deleted file, "grep --invert-match" is deactivated by the NULL string returned by "echo -e '\0'",
#    otherwise, "grep --invert-match" uses the list of deleted files.
GREP_NOT_DELETED=grep --invert-match "$$( ( [ -z "$$(git ls-files --deleted)" ] && echo -e '\0' ) || ( git ls-files -z --deleted | tr '\0' '\n' ) )"
GREP_PACKAGE=grep '^compass/'
GREP_TESTS=grep '^tests/'
GREP_PYTHON=grep '\.py$$'
GREP_NOT_PYTHON=grep --invert-match '\.py$$'
GREP_SHELL=grep '\.sh$$'
PACKAGE_SRC=$(shell ${GIT_FILES} | ${GREP_PACKAGE} | ${GREP_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_PACKAGE} | ${GREP_PYTHON})
PACKAGE_DATA=$(shell ${GIT_FILES} | ${GREP_PACKAGE} | ${GREP_NOT_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_PACKAGE} | ${GREP_NOT_PYTHON})
TESTS_SRC=$(shell ${GIT_FILES} | ${GREP_TESTS} | ${GREP_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_TESTS} | ${GREP_PYTHON})
TESTS_DATA=$(shell ${GIT_FILES} | ${GREP_TESTS} | ${GREP_NOT_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_TESTS} | ${GREP_NOT_PYTHON})
SHELL_SRC=$(shell ${GIT_FILES} | ${GREP_SHELL} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_SHELL})
VENV_BIN=.venv/bin/
PYTHON=$(shell env --ignore-environment which python)
TOUCH=@mkdir --parents .cache/make && date > $@

## devcontainer: Create devcontainer.
.PHONY: devcontainer
devcontainer:
	bash .devcontainer/devcontainer.sh

## devenv      : Setup development environment (.bashrc, .bash_aliases and pre-commit hooks).
.PHONY: devenv
devenv: .cache/make/sync
	bash .devcontainer/bash.sh
	${VENV_BIN}pre-commit install --overwrite --hook-type=pre-commit --hook-type=pre-push

## clean       : Delete caches and files generated during the build.
clean:
	rm -rf .venv .cache/make compass.egg-info .pytest_cache tests/.pytest_cache dist requirements-dev-*.txt

## main        : Run all necessary rules to build the Python package (default).
.DEFAULT_GOAL:=main
main: venv install lock sync format secure lint test package smoke
.PHONY: main

## venv        : Create virtual environemnt.
${VENV_BIN}activate: ${PYTHON} Makefile .devcontainer/devcontainer.dockerfile
	${PYTHON} -m venv --clear --prompt='compass' .venv
.PHONY: venv
venv: ${VENV_BIN}activate

## install     : Install most recent versions of the development dependencies.
.cache/make/install: ${VENV_BIN}activate pyproject.toml requirements-dev.txt constraints.txt
	${VENV_BIN}pip install --quiet --requirement=requirements-dev.txt --editable=. --constraint=constraints.txt
	${TOUCH}
.PHONY: install
install: .cache/make/install

## lock        : Lock development and production dependencies.
requirements-dev.lock: .cache/make/install requirements-dev.txt constraints.txt pyproject.toml requirements-prod.txt
	${VENV_BIN}pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml --constraint=constraints.txt
requirements-prod.lock: pyproject.toml requirements-prod.txt requirements-dev.lock
	${VENV_BIN}pip-compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml --constraint=requirements-dev.lock
.PHONY: lock
lock: requirements-dev.lock requirements-prod.lock

## unlock      : Unlock development and production dependencies.
.PHONY: unlock
unlock:
	rm -rf requirements-*.lock

## sync        : Syncronize development dependencies in the environment according to requirements-dev.lock.
.cache/make/sync: pyproject.toml requirements-dev.lock
	${VENV_BIN}pip-sync --quiet requirements-dev.lock
	${VENV_BIN}pip install --quiet --editable=.
	${TOUCH}
.PHONY: sync
sync: .cache/make/sync

## format      : Format source code.
# If docformatter fails, the script ignores exit status 3, because that code is returned when docformatter changes any file.
# If the variable PRETTIER_DIFF is not empty, prettier is executed. Ignore errors because prettier is not available in GitHub Actions.
.cache/make/format: .cache/make/sync ${PRETTIER_DIFF} ${PACKAGE_SRC} ${TESTS_SRC}
	${VENV_BIN}pyupgrade --py311-plus --exit-zero-even-if-changed ${PACKAGE_SRC} ${TESTS_SRC}
	${VENV_BIN}isort --profile black compass tests
	${VENV_BIN}black compass tests
	${VENV_BIN}docformatter --in-place --recursive compass tests || [ "$$?" -eq "3" ]
	-[ -z "${PRETTIER_DIFF}" ] || prettier ${PRETTIER_DIFF} --write
	${TOUCH}
.PHONY: format
format: .cache/make/format

## secure      : Run vulnerability scanners on source code and production dependencies.
.cache/make/pip-audit: .cache/make/sync requirements-prod.lock
	${VENV_BIN}pip-audit --cache-dir=${HOME}/.cache/pip-audit --requirement=requirements-prod.lock
	${TOUCH}
.cache/make/bandit: .cache/make/format ${PACKAGE_SRC}
	${VENV_BIN}bandit --recursive compass
	${TOUCH}
.PHONY: secure
secure: .cache/make/pip-audit .cache/make/bandit

## lint        : Run static code analysers on source code.
.cache/make/lint: .cache/make/format ${PACKAGE_SRC} ${TESTS_SRC} ${SHELL_SRC} .pylintrc mypy.ini .shellcheckrc
	${VENV_BIN}pylint compass
	${VENV_BIN}mypy compass tests
	shellcheck ${SHELL_SRC}
	${TOUCH}
.PHONY: lint
lint: .cache/make/lint

## test        : Run automated tests.
.cache/make/test: .cache/make/format ${PACKAGE_SRC} ${PACKAGE_DATA} ${TESTS_SRC} ${TESTS_DATA}
	${VENV_BIN}pytest --cov=compass --cov-report=term-missing tests
	${TOUCH}
.PHONY: test
test: .cache/make/test
	
## package     : Create wheel.
.cache/make/package: .cache/make/format ${PACKAGE_SRC} ${PACKAGE_DATA} pyproject.toml
	rm -rf dist/
	${VENV_BIN}python -m build
	${TOUCH}
.PHONY: package
package: .cache/make/package

## smoke       : Smoke test wheel.
.cache/make/smoke: .cache/make/package
	${VENV_BIN}pip install --quiet dist/*.whl
	${VENV_BIN}compass --help
	${VENV_BIN}compass --version
	${VENV_BIN}pip install --quiet --editable=.
	${TOUCH}
.PHONY: smoke
smoke: .cache/make/smoke

## testpypi    : Upload Python package to https://test.pypi.org/.
.PHONY: testpypi
testpypi: .cache/make/sync
	${VENV_BIN}twine upload --repository testpypi dist/*.whl

## cookie      : Update project using cookiecutter-python-vscode-github template.
.PHONY: cookie
cookie: .cache/make/sync
	${VENV_BIN}cookiecutter --overwrite-if-exists --output-dir=.. --no-input --config-file=cookiecutter.yaml $$(cookiecutter-python-vscode-github)

## help        : Show this help message.
.PHONY: help
help:
	@sed -n 's/^##//p' Makefile
