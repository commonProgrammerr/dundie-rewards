# Contributing to Dundie Project

Summary of Project

## Guideline

- Backwards compatibility
- Multi-platform
- Python 3 only

## Code of conduct

- Be gentle

## How to contribute

### Fork repository

- Click fork button on [repo](https://github.com/commonProgrammerr/dundie-rewards)

### Clone on local dev environment

```bash
git clone http://github.com/youruser/fork-name
``` 

### Prepare the virtual env
```bash
cd fork-name
make virtualenv
make install
``` 

### Run tests
```bash
pip install -e .[test]
make test
# or 
pip install -e .[test]
make watch
```

### Commit rules

- We follow conventional commit messages. eg: `[bugfix] reason #issue`
- We require signed commits

### Pull request rules

- We require all tests to be passing 