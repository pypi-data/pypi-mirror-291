### Introduction to the ft_yde_goes_package

This package was created as a requirement to the last exercise of Day 00 during the Python for Data Science piscine at 42 School. The objective was to teach the students how to create a Python package and how to distribute it.

### Package structure

```
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── example_package_YOUR_USERNAME_HERE/
│       ├── __init__.py
│       └── example.py
└── tests/
```

Above is the package structure used as a reference:
- `__init.py__`: this file must located at each sub-directory, which is also the sub-module of a given package. It will map all the methods present in each sub-module;
- `pyproject.toml`: contains the key-value configuration of the package with all its related information to build it. It's also possible to use a `setup.py` or `setup.cfg` instead.

### How to test the package

To test the package, run the command below at the same folder where `pyproject.toml` is located:
```
pip install --editable .
```

To check if the package was successfully installed, run:
```
pip show -v ft-package
```

To uninstall the package, run:
```
pip uninstall <package_name>
```

Create a Python program at the same folder where `pyproject.toml` is located to see if you can use the package module without any problems when running it with `python3`.

### How to build and distribute the package

We're going to need to packages:

```
python3 -m pip install twine
python3 -m pip install build
```

Then we need to build the source distribution and the wheel, which checks if the package contains pure Python to adjust the compilation settings accordingly.
```
python3 -m build --sdist
python3 -m build --wheel
```

To distribute the package, we need to create an account at PyPi, enable 2FA and create an API token. It's recommend to save the account information at `~/HOME/.pypirc`.

Last but not least, update the package:
```
twine upload dist/* --verbose
```

### References

[Build your first Python package](https://www.freecodecamp.org/news/build-your-first-python-package/) by [freeCodeCamp](https://www.freecodecamp.org/)

[Official PyPi Website](https://pypi.org/)

Setuptools Official Docs:

- [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#)

- [Packaging and distributing projects](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#packaging-and-distributing-projects)