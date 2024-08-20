# Sample Project To Publish Python Package

[Project Link](https://pypi.org/project/hello-sethlee/)

## Setting Up

1. Create virtual env
```
python -m venv venv
source venv/bin/activate
```
2. Install dependencies
```
pip install setuptools wheel twine
```

3. Update `name`, `version` and `install_requires` in `setup.py`

4. Build Package
```
python setup.py sdist bdist_wheel
```

5. Test Locally
```
pip install dist/hello_sethlee-0.2-py3-none-any.whl
python test.py
```

6. Publish to PyPI
Configure your PyPI environment variables:
```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<YOUR_PASSWORD>
```

7. Publish to PyPI
```
twine upload dist/*
```

8. Usage Anywhere
```
pip install hello-sethlee
```