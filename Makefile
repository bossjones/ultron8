# -*- coding: utf-8 -*-
# SOURCE: https://github.com/autopilotpattern/jenkins/blob/master/makefile
MAKEFLAGS += --warn-undefined-variables
# .SHELLFLAGS := -eu -o pipefail

SHELL = /bin/bash

CI_PYENV_DOCKER_IMAGE := bossjones/docker-pyenv:latest


# SOURCE: https://github.com/wk8838299/bullcoin/blob/8182e2f19c1f93c9578a2b66de6a9cce0506d1a7/LMN/src/makefile.osx
HAVE_BREW=$(shell brew --prefix >/dev/null 2>&1; echo $$? )

.PHONY: list help default all check fail-when-git-dirty

.PHONY: FORCE_MAKE

PR_SHA                := $(shell git rev-parse HEAD)

define ASCILOGO
ultron8
=======================================
endef

export ASCILOGO

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

# verify that certain variables have been defined off the bat
check_defined = \
    $(foreach 1,$1,$(__check_defined))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $(value 2), ($(strip $2)))))

export PATH := ./bin:./bash:./venv/bin:$(PATH)

MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_FOLDER := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))
CURRENT_DIR := $(shell pwd)
MAKE := make

list_allowed_args := product ip command role tier cluster non_root_user host

default: all

all: info

##############################################################################
# Auto generated from pygitrepo 0.0.27
#
# This Makefile is a dev-ops tool set.
# Compatible with:
#
# - Windows
# - MacOS
# - MacOS + pyenv + pyenv-virtualenv tool set
# - Linux
#
# The file structure should like this:
#
# repo_dir
#     |--- make (collection of Makefile)
#         |--- python_env.mk (python environment relative Makefile)
#     |--- source_dir (package source code dir)
#         |--- __init__.py
#         |--- ...
#     |--- build (build python installation file tmp dir)
#     |--- dist (distribution python install file tmp dir)
#     |--- docs (documents dir)
#         |--- build (All build html will be here)
#         |--- source (doc source)
#         |--- Makefile (auto-generated by sphinx)
#         |--- make.bat (for windows)
#     |--- tests (unittest dir)
#         |--- all.py (run all test from python)
#         |--- ... (other test)
#     |--- README.rst (readme file)
#	  |--- readthedocs.yml (ReadTheDocs builder config file)
#     |--- release-history.rst
#     |--- setup.py (installation behavior definition)
#     |--- requirements.txt (dependencies)
#     |--- requirements-dev.txt (dependencies for dev)
#     |--- requirements-doc.txt (dependencies for doc)
#     |--- requirements-test.txt (dependencies for test)
#     |--- LICENSE.txt
#	  |--- AUTHORS.rst
#     |--- MANIFEST.in (specified files need to be included in source code archive)
#     |--- tox.ini (tox setting)
#     |--- .travis.yml (travis-ci setting)
#     |--- .coveragerc (code coverage text setting)
#     |--- .gitattributes (git attribute file)
#     |--- .gitignore (git ignore file)
#	  |--- .circleci (circle-ci setting)
#     |--- fixcode.py (autopep8 source code and unittest code)
#
# Frequently used make command:
#
# - make up
# - make clean
# - make install
# - make test
# - make tox
# - make build_doc
# - make view_doc
# - make deploy_doc
# - make reformat
# - make publish


#--- User Defined Variable ---
PACKAGE_NAME="ultron8"

# Python version Used for Development
PY_VER_MAJOR="3"
PY_VER_MINOR="6"
PY_VER_MICRO="8"

#  Other Python Version You Want to Test With
# (Only useful when you use tox locally)
TEST_PY_VER3="3.7.3"

# If you use pyenv-virtualenv, set to "Y"
USE_PYENV="Y"

# S3 Bucket Name
DOC_HOST_BUCKET_NAME="NoBucket"


#--- Derive Other Variable ---

# Virtualenv Name
VENV_NAME="${PACKAGE_NAME}_venv"

# Project Root Directory
GIT_ROOT_DIR=${shell git rev-parse --show-toplevel}
PROJECT_ROOT_DIR=${shell pwd}

OS=${shell uname -s}

ifeq (${OS}, Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif


# ---------

# Windows
ifeq (${DETECTED_OS}, Windows)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/Scripts"
    SITE_PACKAGES="${VENV_DIR_REAL}/Lib/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/Lib64/site-packages"

    GLOBAL_PYTHON="/c/Python${PY_VER_MAJOR}${PY_VER_MINOR}/python.exe"
    OPEN_COMMAND="start"
endif


# MacOS
ifeq (${DETECTED_OS}, Darwin)

ifeq ($(USE_PYENV), "Y")
    ARCHFLAGS="-arch x86_64"
    LDFLAGS="-L/usr/local/opt/openssl/lib"
    CFLAGS="-I/usr/local/opt/openssl/include"
    VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
    VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
else
    ARCHFLAGS="-arch x86_64"
    LDFLAGS="-L/usr/local/opt/openssl/lib"
    CFLAGS="-I/usr/local/opt/openssl/include"
    # VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    # VENV_DIR_LINK="./${VENV_NAME}"
    VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
    VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
endif
    ARCHFLAGS="-arch x86_64"
    LDFLAGS="-L/usr/local/opt/openssl/lib"
    CFLAGS="-I/usr/local/opt/openssl/include"

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


# Linux
ifeq (${DETECTED_OS}, Linux)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    VENV_DIR_LINK="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


BASH_PROFILE_FILE = "${HOME}/.bash_profile"

BIN_ACTIVATE="${BIN_DIR}/activate"
BIN_PYTHON="${BIN_DIR}/python"
BIN_PIP="${BIN_DIR}/pip"
BIN_ISORT="${BIN_DIR}/isort"
BIN_JINJA="${BIN_DIR}/jinja2"

PY_VERSION="${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_MICRO}"

.PHONY: help
help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#--- Make Commands ---
.PHONY: info
info: ## ** Show information about python, pip in this environment
	@printf "Info:\n"
	@printf "=======================================\n"
	@printf "$$GREEN venv:$$NC                               ${VENV_DIR_REAL}\n"
	@printf "$$GREEN python executable:$$NC                  ${BIN_PYTHON}\n"
	@printf "$$GREEN pip executable:$$NC                     ${BIN_PIP}\n"
	@printf "$$GREEN site-packages:$$NC                      ${SITE_PACKAGES}\n"
	@printf "$$GREEN site-packages64:$$NC                    ${SITE_PACKAGES64}\n"
	@printf "$$GREEN venv-dir-real:$$NC                      ${VENV_DIR_REAL}\n"
	@printf "$$GREEN venv-dir-link:$$NC                      ${VENV_DIR_LINK}\n"
	@printf "$$GREEN venv-bin-dir:$$NC                       ${BIN_DIR}\n"
	@printf "$$GREEN bash-profile-file:$$NC                  ${BASH_PROFILE_FILE}\n"
	@printf "$$GREEN bash-activate:$$NC                      ${BIN_ACTIVATE}\n"
	@printf "$$GREEN bin-python:$$NC                         ${BIN_PYTHON}\n"
	@printf "$$GREEN bin-isort:$$NC                          ${BIN_ISORT}\n"
	@printf "$$GREEN py-version:$$NC                         ${PY_VERSION}\n"
	@printf "$$GREEN use-pyenv:$$NC                          ${USE_PYENV}\n"
	@printf "$$GREEN venv-name:$$NC                          ${VENV_NAME}\n"
	@printf "$$GREEN git-root-dir:$$NC                       ${GIT_ROOT_DIR}\n"
	@printf "$$GREEN project-root-dir:$$NC                   ${PROJECT_ROOT_DIR}\n"
	@printf "$$GREEN brew-is-installed:$$NC                  ${HAVE_BREW}\n"
	@printf "\n"

#--- Virtualenv ---
.PHONY: brew_install_pyenv
brew_install_pyenv: ## ** Install pyenv and pyenv-virtualenv
	-brew install pyenv
	-brew install pyenv-virtualenv

.PHONY: setup_pyenv
setup_pyenv: brew_install_pyenv enable_pyenv ## ** Do some pre-setup for pyenv and pyenv-virtualenv
	pyenv install ${PY_VERSION} -s
	pyenv rehash

.PHONY: bootstrap_venv
bootstrap_venv: pre_commit_install init_venv dev_dep show_venv_activate_cmd ## ** Create virtual environment, initialize it, install packages, and remind user to activate after make is done
# bootstrap_venv: init_venv dev_dep ## ** Create virtual environment, initialize it, install packages, and remind user to activate after make is done

.PHONY: bootstrap
bootstrap: pip-tools bootstrap_venv

.PHONY: init_venv
init_venv: ## ** Initiate Virtual Environment
ifeq (${USE_PYENV}, "Y")
	# Install pyenv
	#-brew install pyenv
	#-brew install pyenv-virtualenv

	# # Edit Config File
	# if ! grep -q 'export PYENV_ROOT="$$HOME/.pyenv"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'export PATH="$$PYENV_ROOT/bin:$$PATH"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'eval "$$(pyenv init -)"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'eval "$$(pyenv init -)"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'eval "$$(pyenv virtualenv-init -)"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'eval "$$(pyenv virtualenv-init -)"' >> "${BASH_PROFILE_FILE}" ;\
	# fi

	# pyenv install ${PY_VERSION} -s
	# pyenv rehash

	@printf "=======================================\n"
	@printf "$$GREEN Creating virtualenv ${VENV_NAME}:$$NC
	-pyenv virtualenv ${PY_VERSION} ${VENV_NAME}
	@printf "FINISHED:\n"
	@printf "=======================================\n"
	@printf "$$GREEN Run to activate virtualenv:$$NC                               pyenv activate ${VENV_NAME}\n"
else

ifeq ($(HAVE_BREW), 0)
	DEPSDIR='ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"'
	$(DEPSDIR) virtualenv -p ${GLOBAL_PYTHON} ${VENV_NAME}
endif

	virtualenv -p ${GLOBAL_PYTHON} ${VENV_NAME}
endif


.PHONY: up
up: init_venv ## ** Set Up the Virtual Environment


.PHONY: clean_venv
clean_venv: ## ** Clean Up Virtual Environment
ifeq (${USE_PYENV}, "Y")
	-pyenv uninstall -f ${VENV_NAME}
else
	test -r ${VENV_DIR_REAL} || echo "DIR exists: ${VENV_DIR_REAL}" || rm -rv ${VENV_DIR_REAL}
endif


#--- Install ---

.PHONY: uninstall
uninstall: ## ** Uninstall This Package
	# -${BIN_PIP} uninstall -y ${PACKAGE_NAME}
	-${BIN_PIP} uninstall -y requirements.txt

.PHONY: install
# install: uninstall ## ** Install This Package via setup.py
install: ## ** Install This Package via setup.py
ifeq ($(HAVE_BREW), 0)
	DEPSDIR='ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"'
	$(DEPSDIR) ${BIN_PIP} install -r requirements.txt
else
	${BIN_PIP} install -r requirements.txt
endif


.PHONY: dev_dep
dev_dep: ## ** Install Development Dependencies

ifeq ($(HAVE_BREW), 0)
	( \
		cd ${PROJECT_ROOT_DIR}; \
		ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" ${BIN_PIP} install -r requirements.txt; \
		ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" ${BIN_PIP} install -r requirements-dev.txt; \
		ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" ${BIN_PIP} install -r requirements-doc.txt; \
		ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" ${BIN_PIP} install -r requirements-test.txt; \
	)
else
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PIP} install -r requirements.txt; \
		${BIN_PIP} install -r requirements-dev.txt; \
		${BIN_PIP} install -r requirements-test.txt; \
		${BIN_PIP} install -r requirements-doc.txt; \
	)
endif

install-dev: dev_dep ## ** Install Development Dependencies


.PHONY: show_venv_activate_cmd
show_venv_activate_cmd: ## ** Show activate command when finished
	@printf "Don't forget to run this activate your new virtualenv:\n"
	@printf "=======================================\n"
	@echo
	@printf "$$GREEN pyenv activate $(VENV_NAME)$$NC\n"
	@echo
	@printf "=======================================\n"

# Frequently used make command:
#
# - make up
# - make clean
# - make install
# - make test
# - make tox
# - make build_doc
# - make view_doc
# - make deploy_doc
# - make reformat
# - make publish

###########################################################
# Pyenv initilization - 12/23/2018 -- END
# SOURCE: https://github.com/MacHu-GWU/learn_datasette-project/blob/120b45363aa63bdffe2f1933cf2d4e20bb6cbdb8/make/python_env.mk
###########################################################

list:
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sort

# Compile python modules against homebrew openssl. The homebrew version provides a modern alternative to the one that comes packaged with OS X by default.
# OS X's older openssl version will fail against certain python modules, namely "cryptography"
# Taken from this git issue pyca/cryptography#2692
install-virtualenv-osx:
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt
pre_commit_install:
	-cp git_hooks/pre-commit .git/hooks/pre-commit

travis:
	tox



.PHONY: run-black-check
run-black-check: ## CHECK MODE: sensible pylint ( Lots of press over this during pycon 2018 )
	black --check --verbose .

.PHONY: run-black
run-black: ## sensible pylint ( Lots of press over this during pycon 2018 )
	black --verbose .

.PHONY: pip-tools
pip-tools:
ifeq (${DETECTED_OS}, Darwin)
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install pip-tools pipdeptree
else
	pip install pip-tools pipdeptree
endif


.PHONY: pip-tools-osx
pip-tools-osx: pip-tools

.PHONY: pip-tools-upgrade
pip-tools-upgrade:
ifeq (${DETECTED_OS}, Darwin)
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install pip-tools pipdeptree --upgrade
else
	pip install pip-tools pipdeptree --upgrade
endif


.PHONY: pip-compile-upgrade-all
pip-compile-upgrade-all: pip-tools
	pip-compile --output-file requirements.txt requirements.in --upgrade
	pip-compile --output-file requirements-dev.txt requirements-dev.in --upgrade
	pip-compile --output-file requirements-test.txt requirements-test.in --upgrade
	pip-compile --output-file requirements-doc.txt requirements-doc.in --upgrade

.PHONY: pip-compile
pip-compile: pip-tools
	pip-compile --output-file requirements.txt requirements.in
	pip-compile --output-file requirements-dev.txt requirements-dev.in
	pip-compile --output-file requirements-test.txt requirements-test.in
	pip-compile --output-file requirements-doc.txt requirements-doc.in

.PHONY: pip-compile-rebuild
pip-compile-rebuild: pip-tools
	pip-compile --rebuild --output-file requirements.txt requirements.in
	pip-compile --rebuild --output-file requirements-dev.txt requirements-dev.in
	pip-compile --rebuild --output-file requirements-test.txt requirements-test.in
	pip-compile --rebuild --output-file requirements-doc.txt requirements-doc.in

.PHONY: install-deps-all
install-deps-all:
ifeq (${DETECTED_OS}, Darwin)
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements.txt
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements-dev.txt
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements-test.txt
	ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip install -r requirements-doc.txt
else
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -r requirements-test.txt
	pip install -r requirements-doc.txt
endif

.PHONY: install-all
install-all: install-deps-all

yamllint-role:
	bash -c "find .* -type f -name '*.y*ml' ! -name '*.venv' -print0 | xargs -I FILE -t -0 -n1 yamllint FILE"

install-ip-cmd-osx:
	brew install iproute2mac

flush-cache:
	@sudo killall -HUP mDNSResponder


###############################

# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.PHONY: git-clean git-env pipenv-test pipenv-test-cover pipenv-test-cli help2

git-clean: ## Remove files and directories ignored by git
	git clean -d -X -f

pipenv-env: ## Run `pipenv install --dev` to create dev environment
	pipenv --python 3
	pipenv install --dev

pipenv-test: ## Run tests
	pipenv run py.test

pipenv-test-cover: ## Run tests - with coverage report
	pipenv run py.test --cov=. --cov-report=term-missing

pipenv-test-cli: ## Run CLI with example Via JSON data
	pipenv run image-annotation-convert tests/annotation-data/via_example.json --output-format=sensei_csv

help2:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docker-pyenv-cli:
	docker run --rm -it \
	-w /mnt \
	-v $(CURRENT_DIR):/mnt \
	$(CI_PYENV_DOCKER_IMAGE) bash

download-roles: ## Download ansible roles in local directory ./roles/
	ansible-galaxy install -r requirements.yml --roles-path ./roles/

download-roles-force: ## FORCE: Download ansible roles in local directory ./roles/
	ansible-galaxy --force install -r requirements.yml --roles-path ./roles/

download-roles-global: ## Download ansible roles in global directory /etc/ansible/roles
	ansible-galaxy install -r requirements.yml --roles-path=/etc/ansible/roles

download-roles-global-force: ## FORCE: Download ansible roles in global directory /etc/ansible/roles
	ansible-galaxy install --force -r requirements.yml --roles-path=/etc/ansible/roles

vagrant-ansible-provision: download-roles-global
	ansible-playbook -vv -c local -i inventory.ini vagrant_playbook.yml
