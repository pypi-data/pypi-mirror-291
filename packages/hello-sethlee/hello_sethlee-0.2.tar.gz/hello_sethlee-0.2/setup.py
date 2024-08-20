from setuptools import setup, find_packages

setup(
    name='hello_sethlee',
    version='0.2',
    packages=find_packages(),
    install_requires=[

    ], 
    entry_points={
        'console_scripts': [
            'hello_sethlee=hello_sethlee.main:hello'
        ]
    }
)