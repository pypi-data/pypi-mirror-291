# project-S8cceS7f

## Introduction

This document provides instructions on how to run and work with this project. It includes guidelines for setting up a development environment, working with branches, and ensuring code quality using `pre-commit`, `black`, and `flake8`.

## Development Workflow

### 1. Cloning the Repository:
To start working on the project, clone the repository to your local machine (! USE SSH !):

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Setting Up the Virtual Environment:
A virtual environment has been set up to manage dependencies. Activate the virtual environment before running the project:

```bash
python3 -m venv venv
```

!!! If you cannot get the virtual environment to start, try creating it with the command 

```bash
/usr/bin/python3 -m venv .venv
```
and repeat the following steps. 

# On Windows:

```bash
venv\Scripts\activate
```

# On Mac/Linux:
```bash
source venv/bin/activate
```

### 3. Installing Dependencies
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Once the virtual environment is activated, you can run the project and any necessary commands.

### 4. Working with Branches
All development work should be done in separate branches created from the dev branch. Follow these steps to ensure a smooth workflow:

- Pull the latest changes from dev:

```bash
git checkout dev
git pull origin dev
```

- Create a new branch for your feature or bug fix:

```bash
git checkout -b your-feature-branch
```


### 5. Ensuring Code Quality
This project uses pre-commit hooks to enforce code quality standards. Before committing any changes, ensure you follow these steps:

- Run black for Code Formatting (black is a code formatter that ensures your code adheres to PEP8 standards. This command formats all the Python files in your project.) Run it before committing your code :

```bash
black .
```

- Run flake8 for Code Linting (flake8 checks your code for linting errors.) If flake8 identifies any issues, fix them before proceeding with the commit. Run it before committing your code:

```bash
flake8 .
```

### 6. Committing Changes
Once your code is formatted and linted -> add changes -> commit them -> and push! The `pre-commit` hooks will automatically run `black` and `flake8` to check the code formatting and linting. If any issues are found, the commit process will be interrupted, and you will need to fix these issues before committing again.


### 7. Reviewing and Fixing Errors During Commit

If errors are detected during the commit (for example, from `black` or `flake8`), you will see messages in your terminal indicating what went wrong. Here's how to handle these errors:

1. **Check the log output**:

   Carefully read the output in your terminal. The log will tell you which files or lines have issues and what those issues are.

2. **Fix the identified issues**:

   Based on the log output, correct the errors in your code. This might involve reformatting code according to `black` or fixing linting issues reported by `flake8`.

3. **Re-run the pre-commit checks**:

   After fixing the issues, stage the changes again.


### 8. Updating Dependencies
If you install any new dependencies, you must update the requirements.txt file so that others can easily install them.

- Install the new package:
```bash
pip install <package-name>
```

- Update requirements.txt:
```bash
pip freeze > requirements.txt
```

= Commit the updated requirements.txt (step 5 and 6). Make sure that you included the updated requirements.txt in your Pull Request!!!

### 8. Create package in pip repository
- Create files for pip  
```bash
python setup.py sdist bdist_wheel
```
- Insert your username and passport of pipy repository
- Publish on pipy our project
```bash
twine upload dist/*
```
- Input your usename and password or provide API-KEY
- Check your pip account








