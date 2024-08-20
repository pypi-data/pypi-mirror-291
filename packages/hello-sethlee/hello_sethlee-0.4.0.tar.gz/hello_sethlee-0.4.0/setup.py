from setuptools import setup, find_packages

with open("README.md", "r") as f:
  description = f.read()

setup(
    name='hello_sethlee',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[

    ], 
    entry_points={
        'console_scripts': [
            'hello_sethlee=hello_sethlee.main:hello'
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)