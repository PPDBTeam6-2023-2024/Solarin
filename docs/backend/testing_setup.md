# Testing Setup

## Overview
The way we integrated testing in our backend.

## Technologies used
- **pytest**: A simple testing library for Python.
- **GitHub Actions**: Continuous Integration (CI) service for automating the testing process.

## Description

### Pytest
In our backend we will use [pytest](https://docs.pytest.org/en/8.0.x/). Which is a simple testing library in python.

All the tests will be put inside the `/tests` folder. If you want to organise test a bit more, you can create a subfolder inside `/tests`, but you cannot forget a `__init__.py` file!

Inside a testfolder you can add test files. These files follow following naming convention: **test_[feature]**.

Inside a testfile you can create test functions with this naming convention: **test_[name test]**. Inside test functions you can use `assert` to test for expecting values.

A simple example test:
```python
# test_capitalize.py

def capital_case(x):
    return x.capitalize()

def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'
```

To run tests locally follow these steps:
- make sure all dependencies are installed: `poetry install --no-interaction --no-root`
- run the tests: `poetry run pytest`

### Github actions
When pushing to the main branch or doing a pull-request to the main branch, github actions will automatically run pytest. This ensures that you are promptly notified if all tests have passed.


## Issues


## Additional Information

To create a github action you need to add a .yml file inside the folder `.github/workflows`. Github will then recognise the actions inside that folder and will execute the .yml files.

This is the yml file for backend testing:
```YAML
name: Backend Tests  # Name of the workflow

on:  # Events that trigger the workflow
  push:  # Triggered on push events
    branches:  # For specific branches
      - main  # Only the main branch triggers this workflow
  pull_request:  # Triggered on pull requests
    branches:  # For specific branches
      - main  # Only the main branch triggers this workflow

jobs:  # Definition of jobs to be executed
  test:  # Job named "test"
    runs-on: ubuntu-latest  # Executes on Ubuntu's latest version

    steps:  # Sequence of steps to execute within the job
      - uses: actions/checkout@v4  # Action to checkout the repository's code
      - uses: actions/setup-python@v4  # Action to set up Python
        with:
          python-version: 3.10.12  # Python version to be used

      - uses: snok/install-poetry@v1  # Action to install Poetry (a Python dependency management tool)
        with:
          version: 1.7.0  # Version of Poetry to install

      - run: poetry install --no-interaction --no-root  # Command to install dependencies using Poetry
        working-directory: ./backend  # Directory where the command should be executed

      - run: poetry run pytest  # Command to run pytest (a Python testing framework)
        working-directory: ./backend  # Directory where the command should be executed
```
