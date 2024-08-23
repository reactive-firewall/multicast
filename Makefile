#!/usr/bin/env make -f

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2023, Mr. Walls
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

ifeq "$(LC_CTYPE)" ""
	LC_CTYPE="en_US.UTF-8"
endif


SHELL:=`command -v bash`


ifeq "$(COMMAND)" ""
	COMMAND_CMD=`command -v xcrun || command which which || command -v which || command -v command`
	ifeq "$(COMMAND_CMD)" "*xcrun"
		COMMAND_ARGS=--find
	endif
	ifeq "$(COMMAND_CMD)" "*command"
		COMMAND_ARGS=-v
	endif
	COMMAND=$(COMMAND_CMD) $(COMMAND_ARGS)
endif

ifeq "$(ECHO)" ""
	ECHO=$(COMMAND) echo
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

ifeq "$(MAKE)" ""
	#  just no cmake please
	MAKE=$($(COMMAND) make || $(COMMAND) gnumake) -j1
endif

ifeq "$(PYTHON)" ""
	PYTHON=$(COMMAND) python3 -B
	ifeq "$(COVERAGE)" ""
		COVERAGE=$(PYTHON) -m coverage
		#COV_CORE_SOURCE = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/
		COV_CORE_CONFIG = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/.coveragerc
		COV_CORE_DATAFILE = .coverage
	endif
else
	ifeq "$(COVERAGE)" ""
		COVERAGE=$(PYTHON) -B -m coverage
		#COV_CORE_SOURCE = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/
		COV_CORE_CONFIG = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/.coveragerc
		COV_CORE_DATAFILE = .coverage
	endif
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

PHONY: must_be_root cleanup init

build: init ./setup.py
	$(QUIET)$(PYTHON) -W ignore -m build ./
	$(QUIET)$(PYTHON) -W ignore -m build --sdist --wheel --no-isolation ./
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "build DONE."

init:
	$(QUIET)$(PYTHON) -m pip install --use-pep517 --upgrade --upgrade-strategy eager pip setuptools wheel build 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

install: init build must_be_root
	$(QUIET)$(PYTHON) -m pip install --use-pep517 --upgrade --upgrade-strategy eager --break-system-packages --user -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUIET)$(PYTHON) -m pip uninstall --use-pep517 --no-input -y multicast 2>/dev/null || true
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)$(PYTHON) -W ignore ./setup.py uninstall 2>/dev/null || true
	$(QUIET)$(PYTHON) -W ignore ./setup.py clean || true
	$(QUIET)$(RMDIR) ./build/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./dist/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./.eggs/ 2>/dev/null || true
	$(QUIET)$(RM) ./test-results/junit.xml 2>/dev/null || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

test: cleanup
	$(QUIET)$(COVERAGE) run -p --source=multicast -m unittest discover --verbose --buffer -s ./tests -t $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) || $(PYTHON) -m unittest discover --verbose --buffer -s ./tests -t ./ || DO_FAIL="exit 2" ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v -- || tail -n 500 .tox/py*/log/py*.log 2>/dev/null
	$(QUIET)$(ECHO) "$@: Done."

test-reports:
	$(QUIET)mkdir $(INST_OPTS) ./test-reports 2>/dev/null >/dev/null || true ;
	$(QUIET)$(ECHO) "$@: Done."

test-pytest: cleanup test-reports
	$(QUIET)$(PYTHON) -B -m pytest --cache-clear --doctest-glob=multicast/*.py,tests/*.py --doctest-modules --cov=. --cov-append --cov-report=xml --junitxml=test-reports/junit.xml -v --rootdir=. || DO_FAIL="exit 2" ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup must_have_flake
	$(QUIET)$(PYTHON) -B -m flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count --config=.flake8.ini --show-source || true
	$(QUIET)tests/check_spelling || true
	$(QUIET)tests/check_cc_lines || true
	$(QUIET)$(ECHO) "$@: Done."

must_have_flake:
	$(QUIET)runner=`python3 -m pip freeze --all | grep --count -oF flake` ; \
	if test $$runner -le 0 ; then $(ECHO) "No Linter found for test." ; exit 126 ; fi

cleanup:
	$(QUIET)$(RM) tests/*.pyc 2>/dev/null || true
	$(QUIET)$(RM) tests/*~ 2>/dev/null || true
	$(QUIET)$(RM) tests/__pycache__/* 2>/dev/null || true
	$(QUIET)$(RM) __pycache__/* 2>/dev/null || true
	$(QUIET)$(RM) multicast/*.pyc 2>/dev/null || true
	$(QUIET)$(RM) multicast/*~ 2>/dev/null || true
	$(QUIET)$(RM) multicast/__pycache__/* 2>/dev/null || true
	$(QUIET)$(RM) multicast/*/*.pyc 2>/dev/null || true
	$(QUIET)$(RM) multicast/*/*~ 2>/dev/null || true
	$(QUIET)$(RM) multicast/*.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) multicast/*/*.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) multicast/.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) multicast/*/.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) tests/.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) tests/*/.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) multicast.egg-info/* 2>/dev/null || true
	$(QUIET)$(RM) ./*.pyc 2>/dev/null || true
	$(QUIET)$(RM) ./.coverage 2>/dev/null || true
	$(QUIET)$(RM) ./coverage*.xml 2>/dev/null || true
	$(QUIET)$(RM) ./sitecustomize.py 2>/dev/null || true
	$(QUIET)$(RM) ./.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) ./*/.DS_Store 2>/dev/null || true
	$(QUIET)$(RM) ./*/*~ 2>/dev/null || true
	$(QUIET)$(RM) ./.*/*~ 2>/dev/null || true
	$(QUIET)$(RM) ./*~ 2>/dev/null || true
	$(QUIET)$(RM) ./.*~ 2>/dev/null || true
	$(QUIET)$(RM) ./src/**/* 2>/dev/null || true
	$(QUIET)$(RM) ./src/* 2>/dev/null || true
	$(QUIET)$(RMDIR) ./src/ 2>/dev/null || true
	$(QUIET)$(RMDIR) tests/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast/*/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast.egg-info 2>/dev/null || true
	$(QUIET)$(RMDIR) .pytest_cache/ 2>/dev/null || true
	$(QUIET)$(RMDIR) .eggs 2>/dev/null || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./.tox/ 2>/dev/null || true
	$(QUIET)$(WAIT) ;

clean-docs: ./docs/ ./docs/Makefile
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)$(WAIT) ;

./docs/:
	$(QUIET)$(WAIT) ;

./docs/Makefile: ./docs/
	$(QUIET)$(WAIT) ;

clean: clean-docs cleanup
	$(QUIET)$(ECHO) "Cleaning Up."
	$(QUIET)$(COVERAGE) erase 2>/dev/null || true
	$(QUIET)$(RM) ./test-results/junit.xml 2>/dev/null || true
	$(QUIET)$(ECHO) "All clean."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then $(ECHO) "You are not root." ; exit 1 ; fi

user-install: build
	$(QUIET)$(PYTHON) -m pip install --use-pep517 --user --upgrade --upgrade-strategy eager pip setuptools wheel || true
	$(QUIET)$(PYTHON) -m pip install --use-pep517 --user --upgrade --upgrade-strategy eager -r "https://raw.githubusercontent.com/reactive-firewall/multicast/stable/requirements.txt" 2>/dev/null || true
	$(QUIET)$(PYTHON) -m pip install --use-pep517 --user --upgrade -e "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" 1>&2 ;
	$(QUIET)$(WAIT) ;

