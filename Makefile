#!/usr/bin/env make -f

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2022, Mr. Walls
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


ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif

ifeq "$(MAKE)" ""
	MAKE=make
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
endif

ifeq "$(DO_FAIL)" ""
	DO_FAIL=$(ECHO) "ok"
endif

PHONY: must_be_root cleanup

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install: must_be_root
	$(QUIET)python3 -m pip install "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)python3 -m pip uninstall multicast || true
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

test-reports:
	$(QUIET)mkdir test-reports 2>/dev/null >/dev/null || true ;
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)python3 -m pip uninstall multicast && python -m pip uninstall multicast || true
	$(QUIET)$(ECHO) "$@: Done."

test: cleanup
	$(QUIET)coverage run -p --source=multicast -m unittest discover --verbose -s ./tests -t ./ || python3 -m unittest discover --verbose -s ./tests -t ./ || python -m unittest discover --verbose -s ./tests -t ./ || DO_FAIL=exit 2 ;
	$(QUIET)coverage combine 2>/dev/null || true
	$(QUIET)coverage report --include=multicast* 2>/dev/null || true
	$(QUIET)$(DO_FAIL);
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v -- || tail -n 500 .tox/py*/log/py*.log 2>/dev/null
	$(QUIET)$(ECHO) "$@: Done."

test-pytest: cleanup test-reports
	$(QUIET)python3 -m pytest --junitxml=test-reports/junit.xml -v tests || python -m pytest --junitxml=test-reports/junit.xml -v tests
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup
	$(QUIET)flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count --config=.flake8.ini
	$(QUIET)tests/check_spelling 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

cleanup:
	$(QUIET)rm -f tests/*.pyc 2>/dev/null || true
	$(QUIET)rm -f tests/*~ 2>/dev/null || true
	$(QUIET)rm -Rf tests/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f multicast/*.pyc 2>/dev/null || true
	$(QUIET)rm -Rf multicast/__pycache__ 2>/dev/null || true
	$(QUIET)rm -Rf multicast/*/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f multicast/*~ 2>/dev/null || true
	$(QUIET)rm -f *.pyc 2>/dev/null || true
	$(QUIET)rm -f multicast/*/*.pyc 2>/dev/null || true
	$(QUIET)rm -f multicast/*/*~ 2>/dev/null || true
	$(QUIET)rm -f *.DS_Store 2>/dev/null || true
	$(QUIET)rm -Rf .pytest_cache/ 2>/dev/null || true
	$(QUIET)rmdir ./test-reports/ 2>/dev/null || true
	$(QUIET)rm -f multicast/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f multicast/*/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f multicast.egg-info/* 2>/dev/null || true
	$(QUIET)rmdir multicast.egg-info 2>/dev/null || true
	$(QUIET)rm -f ./*/*~ 2>/dev/null || true
	$(QUIET)rm -f ./*~ 2>/dev/null || true
	$(QUIET)coverage erase 2>/dev/null || true
	$(QUIET)rm -f ./.coverage 2>/dev/null || true
	$(QUIET)rm -f ./coverage*.xml 2>/dev/null || true
	$(QUIET)rm -f ./sitecustomize.py 2>/dev/null || true
	$(QUIET)rm -f ./.*~ 2>/dev/null || true
	$(QUIET)rm -Rf ./.tox/ 2>/dev/null || true

clean: cleanup
	$(QUIET)rm -f test-results/junit.xml 2>/dev/null || true
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then echo "You are not root." ; exit 1 ; fi

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;

