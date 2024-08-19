from setuptools import setup, find_packages

setup(
    name="barwex-startapp",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "x-startapp=barwex_startapp.main:main",
        ],
    },
)
