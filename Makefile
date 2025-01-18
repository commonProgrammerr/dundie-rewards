.PHONY: install virtualenv ipython clean


install:
	@echo "Installing for dev environment"
	@.venv/bin/python -m pip install -e '.[dev]'


virtualenv:
	@.venv/bin/python -m pip -m venv .venv


ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/pflake8

test:
	@.venv/bin/pytest -s --forked

watch: 
	# @.venv/bin/ptw -- -s
	@ls **/*.py | entr pytest --forked

docs:
	@mkdocs build --clean

docs-serve:
	@mkdocs serve

clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

build:
	@python setup.py sdist bdist_wheel

publish-test:
	@twine upload --repository testpypi dist/*