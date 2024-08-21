from setuptools import setup, find_packages

setup(
    name="barwex-startapp",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "barwex-startapp=barwex_startapp.main:main",
        ],
    },
)
