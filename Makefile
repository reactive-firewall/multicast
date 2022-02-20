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

ifeq "$(LC_CTYPE)" ""
	LC_CTYPE="en_US.UTF-8"
endif

ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif

ifeq "$(MAKE)" ""
	MAKE=make
endif

ifeq "$(PYTHON)" ""
	PYTHON=`command -v python3` -B
endif

ifeq "$(COVERAGE)" ""
	ifeq "$(COVERAGE)" ""
		COVERAGE=`command -v coverage`
	endif
	ifeq "$(COVERAGE)" ""
		COVERAGE=`command -v coverage3`
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
endif

ifeq "$(DO_FAIL)" ""
	DO_FAIL=$(ECHO) "ok"
endif

ifeq "$(RM)" ""
	RM=`command -v rm` -f
	ifeq "$(RMDIR)" ""
		RMDIR=$(RM)Rd
	endif
endif

PHONY: must_be_root cleanup

build:
	$(QUIET)$(ECHO) "INFO: No need to build. Try make -f Makefile install"
	$(QUIET)$(PYTHON) ./setup.py build
	$(QUIET)$(ECHO) "build DONE."

init:
	$(QUIET)$(ECHO) "$@: Done."

install: must_be_root
	$(QUIET)$(PYTHON) -m pip install --upgrade pip setuptools wheel || true
	$(QUIET)$(PYTHON) -m pip install "git+https://github.com/reactive-firewall/multicast.git#egg=multicast"
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)$(PYTHON) -m pip uninstall multicast || true
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)$(PYTHON) -m pip uninstall multicast && python -m pip uninstall multicast || true
	$(QUIET)$(RMDIR) ./build/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./.eggs/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

test: cleanup
	$(QUIET)$(COVERAGE) run -p --source=multicast* -m unittest discover --buffer --verbose -s ./tests -t ./ tests 2>/dev/null || $(PYTHON) -m unittest discover --verbose --buffer -s ./tests -t ./ tests || DO_FAIL="exit 2" ;
	$(QUIET)$(COVERAGE) combine 2>/dev/null || true ;
	$(QUIET)$(COVERAGE) report --include=multicast* 2>/dev/null || true ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v -- || tail -n 500 .tox/py*/log/py*.log 2>/dev/null
	$(QUIET)$(ECHO) "$@: Done."

test-reports:
	$(QUIET)mkdir test-reports 2>/dev/null >/dev/null || true ;
	$(QUIET)$(ECHO) "$@: Done."

test-pytest: cleanup test-reports
	$(QUIET)$(PYTHON) -m pytest --doctest-modules --cov=./ --cov-report=xml --junitxml=test-reports/junit.xml -v tests || python -m pytest --doctest-modules --cov=./ --cov-report=xml --junitxml=test-reports/junit.xml -v tests ; wait ;
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup
	$(QUIET)flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count --config=.flake8.ini
	$(QUIET)tests/check_spelling 2>/dev/null || true
	$(QUIET)tests/check_codecov 2>/dev/null || true
	$(QUIET)tests/check_cc_line.bash 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

cleanup:
	$(QUIET)$(COVERAGE) erase 2>/dev/null || true
	$(QUIET)$(RM) tests/*.pyc 2>/dev/null || true
	$(QUIET)$(RM) tests/*~ 2>/dev/null || true
	$(QUIET)$(RM) tests/__pycache__/* 2>/dev/null || true
	$(QUIET)$(RM) multicast/*.pyc 2>/dev/null || true
	$(QUIET)$(RM) multicast/*~ 2>/dev/null || true
	$(QUIET)$(RM) multicast//__pycache__/* 2>/dev/null || true
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
	$(QUIET)$(RMDIR) tests/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast/*/__pycache__ 2>/dev/null || true
	$(QUIET)$(RMDIR) multicast.egg-info 2>/dev/null || true
	$(QUIET)$(RMDIR) .pytest_cache/ 2>/dev/null || true
	$(QUIET)$(RMDIR) .eggs 2>/dev/null || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./.tox/ 2>/dev/null || true
	$(QUIET)$(WAIT) ;

clean: cleanup
	$(QUIET)$(RM) ./test-results/junit.xml 2>/dev/null || true
	$(QUIET)$(RMDIR) ./test-results/ 2>/dev/null || true
	$(QUIET)$(RMDIR) ./build/ 2>/dev/null || true
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then $(ECHO) "You are not root." ; exit 1 ; fi

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;

