SHELL:=/bin/bash
PRETTIER_DIFF=$(shell prettier . --list-different)
GIT_FILES=git ls-files
GIT_UNTRACKED_FILES=git ls-files --exclude-standard --others
# If there is no deleted file, "grep --invert-match" is deactivated by the string returned by "echo -e '//'",
#    otherwise, "grep --invert-match" uses the list of deleted files.
GREP_NOT_DELETED=grep --invert-match "$$( ( [ -z "$$(git ls-files --deleted)" ] && echo -e '//' ) || ( git ls-files --deleted ) )"
GREP_PACKAGE=grep '^compass/'
GREP_TESTS=grep '^tests/'
GREP_PYTHON=grep '\.py$$'
GREP_NOT_PYTHON=grep --invert-match '\.py$$'
GREP_SHELL=grep '\.sh$$'
GREP_NOT_TEMPLATE=grep --invert-match '{{cookiecutter.project_slug}}/'
PACKAGE_SRC=$(shell ${GIT_FILES} | ${GREP_PACKAGE} | ${GREP_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_PACKAGE} | ${GREP_PYTHON})
PACKAGE_DATA=$(shell ${GIT_FILES} | ${GREP_PACKAGE} | ${GREP_NOT_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_PACKAGE} | ${GREP_NOT_PYTHON})
TESTS_SRC=$(shell ${GIT_FILES} | ${GREP_TESTS} | ${GREP_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_TESTS} | ${GREP_PYTHON})
TESTS_DATA=$(shell ${GIT_FILES} | ${GREP_TESTS} | ${GREP_NOT_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_TESTS} | ${GREP_NOT_PYTHON})
MYPY_SRC=$(shell ${GIT_FILES} | ${GREP_NOT_TEMPLATE} | ${GREP_PYTHON} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_NOT_TEMPLATE} | ${GREP_PYTHON})
SHELL_SRC=$(shell ${GIT_FILES} | ${GREP_SHELL} | ${GREP_NOT_DELETED}) $(shell ${GIT_UNTRACKED_FILES} | ${GREP_SHELL})
VENV_BIN=.venv/bin/
PYTHON=$(shell env --ignore-environment which python)
UV_VERSION=$(shell cat requirements-dev.lock 2>/dev/null | grep '^uv==' | grep --extended-regexp --only-matching '==[.0-9]+')
SKIP=[ $$(stat -c %Y $|) -gt $$(stat -c %Y $@ 2> /dev/null || echo 0) ] || 
GIT_STATUS=git status --porcelain
DONE=@echo $@ done.
TOUCH=@mkdir --parents .cache/make && date > $@

## devcontainer: Create devcontainer.
.PHONY: devcontainer
devcontainer:
	bash .devcontainer/devcontainer.sh

## env      : Setup environment (.bashrc, .bash_aliases and pre-commit hooks).
~/.bash_aliases: .devcontainer/bash.sh
	bash .devcontainer/bash.sh
.git/hooks/pre-commit: .cache/make/install .pre-commit-config.yaml
	${VENV_BIN}pre-commit install --overwrite --hook-type=pre-commit --hook-type=pre-push
.PHONY: env
env: ~/.bash_aliases .git/hooks/pre-commit

## clean       : Delete caches and files generated during the build.
clean:
	rm -rf .venv .cache/make compass.egg-info .pytest_cache tests/.pytest_cache dist requirements-dev-*.txt

## main        : Run all necessary rules to build the Python package (default).
.DEFAULT_GOAL:=main
main: venv lock install format secure lint test package smoke
.PHONY: main

## venv        : Create virtual environemnt.
${VENV_BIN}activate: Makefile .devcontainer/devcontainer.dockerfile
	${PYTHON} -m venv --clear --prompt='compass' .venv
.PHONY: venv
venv: ${VENV_BIN}activate
	${DONE}

## lock        : Lock development and production dependencies.
# Tf there is pending changes, run gha-update.
${VENV_BIN}uv: ${VENV_BIN}activate
	${VENV_BIN}pip install --quiet uv${UV_VERSION}
requirements-dev.lock: ${VENV_BIN}uv requirements-dev.txt constraints.txt pyproject.toml requirements-prod.txt
	${VENV_BIN}uv pip compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-dev.lock --no-header --no-annotate requirements-dev.txt pyproject.toml --constraint=constraints.txt
requirements-prod.lock: pyproject.toml requirements-prod.txt requirements-dev.lock
	${VENV_BIN}uv pip compile --quiet --resolver=backtracking --generate-hashes --strip-extras --allow-unsafe --output-file=requirements-prod.lock --no-header --no-annotate pyproject.toml --constraint=requirements-dev.lock
.cache/make/lock: requirements-dev.lock
	${VENV_BIN}uv pip install --quiet $$(cat requirements-dev.lock 2>/dev/null | grep --extended-regexp --only-matching '^gha-update==[.0-9]+')
	[ -z "$$(${GIT_STATUS})" ] || ${VENV_BIN}gha-update
	${TOUCH}
.PHONY: lock
lock: requirements-dev.lock requirements-prod.lock .cache/make/lock
	${DONE}

## unlock      : Unlock development and production dependencies.
.PHONY: unlock
unlock:
	rm -rf requirements-*.lock

## install     : Install development dependencies according to requirements-dev.lock.
.cache/make/install: pyproject.toml requirements-dev.lock
	${VENV_BIN}uv pip sync --quiet requirements-dev.lock
	${VENV_BIN}uv pip install --quiet --editable=.
	${TOUCH}
.PHONY: install
install: .cache/make/install
	${DONE}

## format      : Format source code.
# If docformatter fails, the script ignores exit status 3, because that code is returned when docformatter changes any file.
# If the variable PRETTIER_DIFF is not empty, prettier is executed. Ignore errors because prettier is not available in GitHub Actions.
.cache/make/format-all: .cache/make/install
	${VENV_BIN}pyupgrade --py312-plus --exit-zero-even-if-changed ${PACKAGE_SRC} ${TESTS_SRC}
	${VENV_BIN}isort --profile black ${PACKAGE_SRC} ${TESTS_SRC}
	${VENV_BIN}black --quiet ${PACKAGE_SRC} ${TESTS_SRC}
	${VENV_BIN}docformatter --in-place ${PACKAGE_SRC} ${TESTS_SRC} || [ "$$?" -eq "3" ]
	[ -z "${PRETTIER_DIFF}" ] || prettier ${PRETTIER_DIFF} --write
	${TOUCH}
.cache/make/format-change: ${PACKAGE_SRC} ${TESTS_SRC} | .cache/make/format-all
	${SKIP}${VENV_BIN}pyupgrade --py312-plus --exit-zero-even-if-changed $?
	${SKIP}${VENV_BIN}isort --profile black $?
	${SKIP}${VENV_BIN}black --quiet $?
	${SKIP}${VENV_BIN}docformatter --in-place $? || [ "$$?" -eq "3" ]
	${TOUCH}
.cache/make/prettier-change: ${PRETTIER_DIFF} | .cache/make/format-all
	${SKIP}[ -z "$?" ] || prettier $? --write
	${TOUCH}
.cache/make/format: .cache/make/format-all .cache/make/format-change .cache/make/prettier-change
	${TOUCH}
.PHONY: format
format: .cache/make/format
	${DONE}

## secure      : Run vulnerability scanners on source code and production dependencies.
.cache/make/pip-audit: .cache/make/install requirements-prod.lock
	${VENV_BIN}pip-audit --cache-dir=${HOME}/.cache/pip-audit --requirement=requirements-prod.lock
	${TOUCH}
.cache/make/bandit-all: .cache/make/install | .cache/make/format
	${VENV_BIN}bandit --quiet ${PACKAGE_SRC}
	${TOUCH}
.cache/make/bandit-change: ${PACKAGE_SRC} | .cache/make/bandit-all
	${SKIP}${VENV_BIN}bandit --quiet $?
	${TOUCH}
.PHONY: secure
secure: .cache/make/pip-audit .cache/make/bandit-all .cache/make/bandit-change
	${DONE}

## lint        : Run static code analysers on source code.
.cache/make/lint-all: .cache/make/install .pylintrc mypy.ini .shellcheckrc | .cache/make/format
	${VENV_BIN}pylint ${PACKAGE_SRC}
	${VENV_BIN}mypy ${MYPY_SRC}
	shellcheck ${SHELL_SRC}
	${TOUCH}
.cache/make/pylint-change: ${PACKAGE_SRC} | .cache/make/lint-all
	${SKIP}${VENV_BIN}pylint $?
	${TOUCH}
.cache/make/mypy-change: ${MYPY_SRC} | .cache/make/lint-all
	${SKIP}${VENV_BIN}mypy $?
	${TOUCH}
.cache/make/shellcheck-change: ${SHELL_SRC} | .cache/make/lint-all
	${SKIP}shellcheck $?
	${TOUCH}
.cache/make/lint: .cache/make/lint-all .cache/make/pylint-change .cache/make/mypy-change .cache/make/shellcheck-change
	${TOUCH}
.PHONY: lint
lint: .cache/make/lint
	${DONE}

## test        : Run automated tests.
.cache/make/test: .cache/make/format ${PACKAGE_SRC} ${PACKAGE_DATA} ${TESTS_SRC} ${TESTS_DATA}
	${VENV_BIN}pytest --cov=compass --cov-report=term-missing tests
	${TOUCH}
.PHONY: test
test: .cache/make/test
	${DONE}
	
## package     : Create wheel.
.cache/make/package: .cache/make/format ${PACKAGE_SRC} ${PACKAGE_DATA} pyproject.toml
	rm -rf dist/
	${VENV_BIN}python -m build --wheel
	${TOUCH}
.PHONY: package
package: .cache/make/package
	${DONE}

## smoke       : Smoke test wheel.
.cache/make/smoke: .cache/make/package
	${VENV_BIN}uv pip install --quiet dist/*.whl
	${VENV_BIN}compass --help
	${VENV_BIN}compass --version
	${VENV_BIN}uv pip install --quiet --editable=.
	${TOUCH}
.PHONY: smoke
smoke: .cache/make/smoke
	${DONE}

## check       : Check if there are pending changes in the working tree.
.PHONY: check
check:
	${GIT_STATUS}
	[ -z "$$(${GIT_STATUS})" ]
	${DONE}

## testpypi    : Upload Python package to https://test.pypi.org/.
.PHONY: testpypi
testpypi: .cache/make/package
	${VENV_BIN}twine upload --repository testpypi dist/*.whl

## cookie      : Update project using cookiecutter-python-vscode-github template.
.PHONY: cookie
cookie: .cache/make/install
	${VENV_BIN}cookiecutter --overwrite-if-exists --output-dir=.. --no-input --config-file=cookiecutter.yaml $$(cookiecutter-python-vscode-github)

## help        : Show this help message.
.PHONY: help
help:
	@sed -n 's/^##//p' Makefile
