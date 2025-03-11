#!/usr/bin/env make -f

# Multicast Python Module
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ifeq "$(LANG)" ""
	LANG="en_US.UTF-8"
endif

ifeq "$(LC_CTYPE)" ""
	LC_CTYPE="en_US.UTF-8"
endif

ifndef SHELL
	SHELL:=command -pv bash
endif

ifeq "$(ERROR_LOG_PATH)" ""
	ERROR_LOG_PATH="/dev/null"
endif

ifeq "$(COMMAND)" ""
	COMMAND_CMD!=`command -v xcrun || command which which || command -v which || command -v command`
	ifeq "$(COMMAND_CMD)" "*xcrun"
		COMMAND_ARGS=--find
	endif
	ifeq "$(COMMAND_CMD)" "*command"
		COMMAND_ARGS=-pv
	endif
	COMMAND=$(COMMAND_CMD) $(COMMAND_ARGS)
endif

ifeq "$(MAKE)" ""
	#  just no cmake please
	MAKEFLAGS=$(MAKEFLAGS) -s
	MAKE!=`$(COMMAND) make 2>$(ERROR_LOG_PATH) || $(COMMAND) gnumake 2>$(ERROR_LOG_PATH)`
endif

ifeq "$(ECHO)" ""
	ECHO=printf "%s\n"
endif

ifdef "$(ACTION)"
	SET_FILE_ATTR=$(COMMAND) xattr
endif

ifdef "$(SET_FILE_ATTR)"
	CREATEDBYBUILDSYSTEM=-w com.apple.xcode.CreatedByBuildSystem true
	BSMARK=$(SET_FILE_ATTR) $(CREATEDBYBUILDSYSTEM)
else
	BSMARK=$(COMMAND) touch -a
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif

ifeq "$(PYTHON)" ""
	PY_CMD=$(COMMAND) python3
	ifneq "$(PY_CMD)" ""
		PY_ARGS=-B
	else
		PY_CMD=$(COMMAND) python
	endif
	PYTHON=$(PY_CMD) $(PY_ARGS)
endif

ifeq "$(COVERAGE)" ""
	COVERAGE=$(PYTHON) -m coverage
	#COV_CORE_SOURCE = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/
	COV_CORE_CONFIG = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/.coveragerc
	COV_CORE_DATAFILE = .coverage
	COVERAGE_ARGS := --cov=. --cov-append --cov-report=xml
else
	COVERAGE_ARGS :=
endif
ifeq "$(COVERAGE)" ""
	COVERAGE!=$(COMMAND) coverage
endif

ifndef PYTEST
	PYTEST=$(PYTHON) -m pytest --cache-clear --junitxml=test-reports/junit.xml -v --rootdir=.
endif

ifndef PIP_COMMON_FLAGS
	# Define common pip install flags
	PIP_COMMON_FLAGS := --use-pep517 --exists-action s --upgrade --upgrade-strategy eager
endif

# Define environment-specific pip install flags
ifeq ($(shell uname),Darwin)
	PIP_ENV_FLAGS := --break-system-packages
else
	PIP_ENV_FLAGS :=
endif

ifeq "$(WAIT)" ""
	WAIT=wait
endif

ifeq "$(INSTALL)" ""
	INSTALL=install
	ifeq "$(INST_OWN)" ""
		INST_OWN=-o root -g staff
	endif
	ifeq "$(INST_OPTS)" ""
		INST_OPTS=-m 755
	endif
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
	ifeq "$(DO_FAIL)" ""
		DO_FAIL=$(ECHO) "ok"
	endif
endif

ifeq "$(DO_FAIL)" ""
	DO_FAIL=$(COMMAND) :
endif

ifeq "$(RM)" ""
	RM=$(COMMAND) rm -f
endif

ifeq "$(RMDIR)" ""
	RMDIR=$(RM)Rd
endif

.PHONY: all clean test cleanup init help clean-docs must_be_root must_have_flake must_have_pytest uninstall cleanup-dev-backups

help:
	$(QUIET)printf "HELP\nHouse-keeping:\n\tmake help - this help text\n\tmake build - packages the module\n\tmake clean - cleans up a bit\n\tmake init - sets up requirements for first time\nInstall/Remove:\n\tmake install - installs the module properly\n\tmake user-install - tries an unprivileged install (may not work for some users)\n\tmake uninstall - uninstalls the module\n\tmake purge - uninstalls the module, and resets most related things\n\t\t(the big exception is init)\nMisc:\n\tmake build-docs - generate documentation (using sphinx)\n\tmake test - run minimal acceptance testing\n\tmake test-style - run some code-style testing\n\tmake test-pytest - run extensive testing (with pytest)\n\n";

MANIFEST.in: init
	$(QUIET)$(ECHO) "include requirements.txt" >"$@" ;
	$(QUIET)$(BSMARK) "$@" 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(ECHO) "include README.md" >>"$@" ;
	$(QUIET)$(ECHO) "include LICENSE.md" >>"$@" ;
	$(QUIET)$(ECHO) "include CHANGES.md" >>"$@" ;
	$(QUIET)$(ECHO) "include HISTORY.md" >>"$@" ;
	$(QUIET)$(ECHO) "recursive-include . *.txt" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .gitignore" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .deepsource.toml" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.ini" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.yml" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.yaml" >>"$@" ;
	$(QUIET)$(ECHO) "exclude package.json" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude .git" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude codecov_env" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude .DS_Store" >>"$@" ;
	$(QUIET)$(ECHO) "prune .gitattributes" >>"$@" ;
	$(QUIET)$(ECHO) "prune test-reports" >>"$@" ;
	$(QUIET)$(ECHO) "prune .github" >>"$@" ;
	$(QUIET)$(ECHO) "prune .circleci" >>"$@" ;
	$(QUIET)$(ECHO) "prune venv" >>"$@" ;

build: init ./setup.py MANIFEST.in
	$(QUIET)$(PYTHON) -W ignore -m build --sdist --wheel --no-isolation ./ || $(QUIET)$(PYTHON) -W ignore -m build ./ ;
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "build DONE."

init:
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) "pip>=24.3.1" "setuptools>=75.0" "wheel>=0.44" "build>=1.1.1" 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -r requirements.txt 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(ECHO) "$@: Done."

install: init build must_be_root
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUIET)$(PYTHON) -m pip uninstall --use-pep517 $(PIP_ENV_FLAGS) --no-input -y multicast 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

legacy-purge: clean uninstall
	$(QUIET)$(PYTHON) -W ignore ./setup.py uninstall 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(PYTHON) -W ignore ./setup.py clean 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./build/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./dist/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./.eggs/ 2>$(ERROR_LOG_PATH) || :

purge: legacy-purge
	$(QUIET)$(RM) ./test-reports/*.xml 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./test-reports/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(ECHO) "$@: Done."

test: just-test
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(COVERAGE) combine 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(COVERAGE) report -m --include=* 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(ECHO) "$@: Done."

test-tox: build
	$(QUIET)tox -v -- || tail -n 500 .tox/py*/log/py*.log 2>$(ERROR_LOG_PATH)
	$(QUIET)$(COVERAGE) combine 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(COVERAGE) report -m --include=* 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(ECHO) "$@: Done."

test-reports:
	$(QUIET)mkdir $(INST_OPTS) ./test-reports 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(BSMARK) ./test-reports 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(ECHO) "$@: Done."

test-reqs: test-reports init
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -r tests/requirements.txt 2>$(ERROR_LOG_PATH) || true

docs-reqs: ./docs/ ./docs/requirements.txt init
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -r docs/requirements.txt  2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;

# === Test Group Targets ===
just-test: cleanup MANIFEST.in ## Run all minimum acceptance tests
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) $(COVERAGE_ARGS) || DO_FAIL="exit 2" ; \
	else \
		$(COVERAGE) run -p --source=multicast -m unittest discover --verbose --buffer -s ./tests -t $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) || $(PYTHON) -m unittest discover --verbose --buffer -s ./tests -t ./ || DO_FAIL="exit 2" ; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-mat: test-mat-build test-mat-bootstrap test-mat-basic test-mat-say test-mat-hear test-mat-usage test-mat-doctests ## Run all minimum acceptance tests
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-mat-%: MANIFEST.in ## Run specific MAT category (basic|doctests|say|hear|usage|build|bootstrap)
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) tests/ --verbose $(COVERAGE_ARGS) --junitxml=test-reports/junit.xml -v --rootdir=. -m "mat and $*" || DO_FAIL="exit 2" ; \
	else \
		$(COVERAGE) run -p --source=multicast -m tests.run_selective --group mat --category $*; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-extra: ## Run all extra tests
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) tests/ --verbose $(COVERAGE_ARGS) -m "extra" || DO_FAIL="exit 2" ; \
	else \
		$(COVERAGE) run -p --source=multicast -m tests.run_selective --group extra; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-extra-%: ## Run specific extra test category
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) tests/ --verbose $(COVERAGE_ARGS) -m "extra and $*" || DO_FAIL="exit 2" ; \
	else \
		$(COVERAGE) run -p --source=multicast -m tests.run_selective --group extra --category $*; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-fuzzing: ## Run all fuzzing tests
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) tests/ --verbose $(COVERAGE_ARGS) -m "fuzzing" || DO_FAIL="exit 2" ; \
	else \
		$(COVERAGE) run -p --source=multicast -m tests.run_selective --group fuzzing; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-perf: ## Run all performance tests
	$(QUIET)if [ -n "$$TESTS_USE_PYTEST" ]; then \
		$(PYTEST) tests/ --verbose $(COVERAGE_ARGS) -m "performance"; \
	else \
		$(COVERAGE) run -p --source=multicast -m tests.run_selective --group performance; \
	fi
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test-pytest: cleanup MANIFEST.in must_have_pytest test-reports
	$(QUIET)$(ECHO) "WARNING: The target '$@' is deprecated;"
	$(QUIET)$(ECHO) "Use 'TESTS_USE_PYTEST=1 make test' instead"
	$(QUIET)$(PYTEST) $(COVERAGE_ARGS) || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup must_have_flake
	$(QUIET)$(PYTHON) -m flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count --config=.flake8.ini --show-source || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)tests/check_spelling || true
	$(QUIET)tests/check_cc_lines || true
	$(QUIET)$(ECHO) "$@: Done."

must_have_flake:
	$(QUIET)runner=`$(PYTHON) -m pip freeze --all | grep --count -oF flake` ; \
	if test $$runner -le 0 ; then $(ECHO) "No Linter found for test." ; exit 126 ; fi

must_have_pytest: init
	$(QUIET)runner=`$(PYTHON) -m pip freeze --all | grep --count -oF pytest` ; \
	if test $$runner -le 0 ; then $(ECHO) "No python framework (pytest) found for test." ; exit 126 ; fi

cleanup-dev-backups::
	$(QUIET)$(RM) ./*/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./.*/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./**/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./.*~ 2>$(ERROR_LOG_PATH) || :

cleanup-mac-dir-store::
	$(QUIET)$(RM) ./.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/**/.DS_Store 2>$(ERROR_LOG_PATH) || :

cleanup-py-caches: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) ./*.pyc 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/*.pyc 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/__pycache__/* 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/*/*.pyc 2>$(ERROR_LOG_PATH) || :

cleanup-py-cache-dirs: cleanup-py-caches
	$(QUIET)$(RMDIR) ./tests/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./*/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./*/*/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./__pycache__ 2>$(ERROR_LOG_PATH) || :

cleanup-hypothesis::
	$(QUIET)$(RM) ./.hypothesis/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./.hypothesis/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.hypothesis/ 2>$(ERROR_LOG_PATH) || true

cleanup-tests: cleanup-hypothesis cleanup-py-cache-dirs cleanup-py-caches
	$(QUIET)$(RM) ./test_env/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./test_env/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./test_env/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) .pytest_cache/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.tox/ 2>$(ERROR_LOG_PATH) || true

cleanup-multicast: cleanup-py-cache-dirs cleanup-py-caches
	$(QUIET)$(RM) multicast/*.pyc 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) multicast/*~ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) multicast/__pycache__/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) multicast/*/*.pyc 2>$(ERROR_LOG_PATH) || true

cleanup-multicast-eggs: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) multicast.egg-info/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) multicast.egg-info 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) .eggs 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.eggs/ 2>$(ERROR_LOG_PATH) || true

cleanup-src-dir: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) ./src/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./src/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./src/ 2>$(ERROR_LOG_PATH) || true

cleanup: cleanup-tests cleanup-multicast cleanup-multicast-eggs cleanup-src-dir
	$(QUIET)$(RM) ./.coverage 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./coverage*.xml 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./sitecustomize.py 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(WAIT) ;

build-docs: ./docs/ ./docs/Makefile docs-reqs
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile html 2>$(ERROR_LOG_PATH) || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)mkdir $(INST_OPTS) ./docs/www 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(BSMARK) ./docs/www 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;
	$(QUIET)cp -fRp ./docs/_build/ ./docs/www/ 2>$(ERROR_LOG_PATH) || DO_FAIL="exit 35" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(ECHO) "Documentation should be in docs/www/html/"
	$(QUIET)$(DO_FAIL) ;

clean-docs: ./docs/ ./docs/Makefile
	$(QUIET)$(RM) ./docs/www/* 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(RMDIR) ./docs/www/ 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;

./docs/:
	$(QUIET)test -d "$@" || DO_FAIL="exit 77" ;  # set fail if can't verify directory
	$(QUIET)test -e "$@" || DO_FAIL="exit 69" ;  # overwrite exitcode if does not exsist.
	$(QUIET)$(DO_FAIL) ;

./docs/Makefile: ./docs/
	$(QUIET)$(WAIT) ;

clean: clean-docs cleanup
	$(QUIET)$(ECHO) "Cleaning Up."
	$(QUIET)$(COVERAGE) erase 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./test-results/junit.xml 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./MANIFEST.in 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(ECHO) "All clean."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then $(ECHO) "You are not root." ; exit 1 ; fi

user-install: build
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user "pip>=24.3.1" "setuptools>=75.0" "wheel>=0.44" "build>=1.1.1" 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user -r "https://raw.githubusercontent.com/reactive-firewall/multicast/stable/requirements.txt" 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" 1>&2 ;
	$(QUIET)$(WAIT) ;

