# Python Flow Worker

![Testing (pytest) and linting (Flake8)](https://github.com/corcoja/worker.python/actions/workflows/python-app.yml/badge.svg)
![CodeQL Analysis](https://github.com/corcoja/worker.python/actions/workflows/codeql-analysis.yml/badge.svg)

## Table of Contents

- [Python Flow Worker](#python-flow-worker)
  - [Table of Contents](#table-of-contents)
  - [Design](#design)
  - [Develop](#develop)
    - [How to run in a virtual environment with Python (Recommended)](#how-to-run-in-a-virtual-environment-with-python-recommended)
      - [Prerequisites for virtual environment](#prerequisites-for-virtual-environment)
      - [Steps to run in virtual environment](#steps-to-run-in-virtual-environment)
    - [How to run locally with Python](#how-to-run-locally-with-python)
      - [Prerequisites for local environment](#prerequisites-for-local-environment)
      - [Steps to run in local environment](#steps-to-run-in-local-environment)
  - [Test](#test)
  - [Package](#package)
    - [Through IBM Services Essentials CICD](#through-ibm-services-essentials-cicd)
    - [Manual packaging](#manual-packaging)
  - [Licence](#licence)

## Design

TBD

## Develop

### How to run in a virtual environment with Python (Recommended)

#### Prerequisites for virtual environment

- Python 3.6 or higher
- Pip 19.0 or higher

#### Steps to run in virtual environment

1. Create a virtual environment. To create a new virtual environment, decide upon a directory where you want to place it, and run the `venv` module as a script with the directory path. We recommend naming directory `.venv`, since it is also ignored by git through `.gitignore` rules.

    ```sh
    python3 -m venv .venv
    ```

2. Once you’ve created a virtual environment, you may activate it.

    ```sh
    source .venv/bin/activate
    ```

3. After activating the virtual environment, you can run the `pyworker` module.

    ```sh
    python3 -m pyworker
    ```

4. To leave the virtual environment, simply deactivate it.

    ```sh
    deactivate
    ```

5. You may also want to delete the created virtual environment to free up space on your disk.

    ```sh
    rm -r .venv
    ```

### How to run locally with Python

#### Prerequisites for local environment

- Python 3.6 or higher

#### Steps to run in local environment

1. Run the `pyworker` module.

    ```sh
    python3 -m pyworker
    ```

## Test

TBD

## Package

### Through IBM Services Essentials CICD

**Note:** In order to use CICD tool of IBM Services Essentials platform, you must be a member of a team, have CICD service added and approved for the same team, configure a new CICD component to build and deploy from this repository. See more in the [docs][2].

To start a new build and/or deploy activity in CICD, create a new tag trigger, then create and push a new tag in your repository.

1. Create a new git tag matching the CICD trigger regular expression.
2. Push the created git tag to the remote.
3. Check the activity screen in IBM Services Essentials CICD.

### Manual packaging

Build a new Docker image.

```sh
docker build --tag flow-python-worker:0.0.1 .
```

## Licence

[Apache License 2.0][1]

[1]: https://github.com/corcoja/worker.python/blob/main/LICENSE
[2]: https://servicesessentials.ibm.com/docs/boomerang-cicd/8.1.0/introduction/overview
