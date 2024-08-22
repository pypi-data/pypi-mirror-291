**ava-shared-resources** is a shared library for AVA Platform.

# Features

TODO


# Development

For this project [Poetry](https://python-poetry.org/) is used.
Poetry can be installed:
* As system-wide package as described in [docs](https://python-poetry.org/docs/#installation).
* As python package inside virtual environment (should be used when cannot be installed system-wide).

**Poetry is responsible only for python packaging and dependency management**.

In order to create virtual environment with specific version of python (that required by the project and might not be installed on your system) you'll have to use either:
* [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (preferrable option)
* [Pyenv](https://github.com/pyenv/pyenv) ([windows version](https://github.com/pyenv-win/pyenv-win)) (works perfectly on UNIX-based OS, **not on Windows!**)

## **Configure poetry**

1) **[Optional]** First let's tell poetry to not create virtual env by default (only needed if poetry is installed as system package, not as pip package):

    ```bash
    poetry config virtualenvs.create false
    ```

2) Setup credentials for WK's private PyPi repository

    2.1) You need to have a PyPi Artifactory account.
    Make sure that you have read permissions to  [https://artifactory.wolterskluwer.io/ui/repos/tree/General/dxg-ava-pypi/](https://artifactory.wolterskluwer.io/ui/repos/tree/General/dxg-ava-pypi/).  If you don't have it you can reach [TSD-Development-Support@wolterskluwer.com](TSD-Development-Support@wolterskluwer.com).

    2.2) Set the account with the following command:

    ```bash
    pip config set global.extra-index-url https://${username}:${API_Key}@artifactory.wolterskluwer.io/artifactory/api/pypi/dxg-ava-pypi/simple
    ```
   You can get the API Key from https://artifactory.wolterskluwer.io (from user profile)

    2.3) As the code is managed by poetry, Artifactory account has to be also specified for it (WK username should work):

    ```bash
    poetry config repositories.artifactory https://artifactory.wolterskluwer.io/artifactory/api/pypi/dxg-ava-pypi/
    poetry config http-basic.artifactory ${username} ${API_Key}
    ```
   You can get the API Key from https://artifactory.wolterskluwer.io (from user profile)

## **Create virtual environment**

### **a) Create virtual env with Conda**

1) In order to create virtual environment with conda run this command:

    ```bash
    conda create --name [env name] python=[version] --no-default-packages
    ```

    For example:

    ```bash
    conda create --name ava-configurations python=3.10.13 --no-default-packages
    ```

2) And activate this environment:

    ```bash
    conda activate ava-configurations
    ```

3) **[Optional]** Installing poetry as python package (if not installed system-wide):

    ```bash
    pip install poetry-core==1.4.0 poetry==1.3.0
    ```

### **b) Create virtual env with Pyenv (for UNIX-like OS)**

**CAUTION**: windows version of pyenv doesn't not compile python from source code unlike version for UNIX-like OS. That means that it relies on prebuilt python version which is available on official python website. If there is no such version - you are out of luck.

In order to create virtual environment with Pyenv do these steps:

1) Install pyenv as it's explained in pyenv's github [README file](https://github.com/pyenv/pyenv).

2) Install python with:

    ```bash
    pyenv install [python version]
    ```

    For example:

    ```bash
    pyenv install 3.7.11
    ```

3) Make just installed python used system-wide by default

    ```bash
    pyenv global 3.7.11
    ```

4) Create virtual environment with python's default venv module:

    ```bash
    python -m venv [venv_name]
    ```

5) Activate virtual environment:

    ```bash
    source [venv_name]/bin/activate
    ```

    or

    ```bash
    . [venv_name]/bin/activate
    ```

6) **[Optional]** Installing poetry as python package (if not installed system-wide):

    ```bash
    pip install poetry-core==1.4.0 poetry==1.3.0
    ```

All next steps should be done with activated virtual environment.

## **Install packages**

Inside project you can find two files:

* **pyproject.toml**: describes dependencies and version restrictions

* **poetry.lock**: specifies exact version of packages ("frozen" version)

For installing packages poetry provides two commands:

* **poetry install**: will install packages with "frozen" versions if _poetry.lock_ is provided. If not will find best suitable package version (with no conflicts with all other packages) and write down it into poetry.lock file.

* **poetry update**: will find best suitable package versions and update poetry.lock file.

**IMPORTANT**: for reproducibility use only **poetry install** command.

```bash
poetry install
```

## **Updating poetry.lock**

`poetry.lock` file can be updated with command:

```bash
poetry update
```

and executed in two cases:

1) When we want to update packages and write their versions into poetry.lock file

2) If any changes are made to `pyproject.toml` file. Other way poetry will raise warning that poetry.lock file is outdated as it is not synced with pyproject.toml

## **Configure pre-commit hook**

After setting up the environment, to install the pre-commit hook in the system, run the following command: 

   ```bash
   pre-commit install
   ```
This will install the hook and set it up to run automatically before each commit.

## **Committing with pre-commit hook**

After making code changes, follow the standard process for commit and push:

   1) Add the files:
      ```bash
      git add .
      ```
   2) Commit the changes (the pre-commit hook will run automatically from .pre-commit-config.yaml):
      ```bash
      git commit -m "commit message"
      ```
      
      To commit while skipping one of the hooks, set the SKIP environment variable to the ID of the hook you want to skip. For example:
      ```bash
      SKIP=flake8 git commit -m "commit message"
      ```
   3) Push the changes:
      ```bash
      git push
      ```
      
## **Release to PyPi Artifactory**

After making changes to the code it has to be pushed as a package to PyPi Artifactory.

For pushing to repository next steps has to be done:

1) If needed update package version in _pyproject.toml_ file (in _tool.poetry.version_ section).


2) You need to have a PyPi Artifactory account.
Make sure that you have **not only read but also write permissions** to  [https://artifactory.wolterskluwer.io/ui/repos/tree/General/dxg-ava-pypi/](https://artifactory.wolterskluwer.io/ui/repos/tree/General/dxg-ava-pypi/).  If you don't have it you can reach [TSD-Development-Support@wolterskluwer.com](TSD-Development-Support@wolterskluwer.com).


3) Set the account with the following command:

    ```bash
    pip config set global.extra-index-url https://${username}:${API_Key}@artifactory.wolterskluwer.io/artifactory/api/pypi/dxg-ava-pypi/simple
    ```
   You can get the API Key from https://artifactory.wolterskluwer.io (from user profile)


4) As the code is managed by poetry, Artifactory account has to be also specified for it (WK username should work):

    ```bash
    poetry config repositories.at https://artifactory.wolterskluwer.io/artifactory/api/pypi/dxg-ava-pypi/
    poetry config http-basic.at ${username} ${API_Key}
    ```
   You can get the API Key from https://artifactory.wolterskluwer.io (from user profile)


5) Build and publish package:

   Build and publish the repo using script ```ava-shared-resources/utils/build_publish_repo.py```. 

   It will build the package and place it in `/dist` folder with .whl extension. Before building make sure the package version is not already present in the artifactory, else function will give an error. Same package will be uploaded in the Artifactory repository. Try to install it and check if it works as expected.