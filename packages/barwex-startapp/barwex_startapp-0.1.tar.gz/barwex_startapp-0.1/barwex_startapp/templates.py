setup = """
from setuptools import setup, find_packages

setup(
    name="{{{package_name}}}",
    version="{{{package_version}}}",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "{{{command_name}}}={{{module_name}}}.main:main",
        ],
    },
)
"""


main = """
from argparse import ArgumentParser


def parse():
    parser = ArgumentParser()
    args = parser.parse_args()
    return args


def main():
    args = parse()
    print("This is auto created by barwex-startapp")
"""


vscode = """
{
  "[jsonc]": {
    "editor.tabSize": 2,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "black-formatter.args": ["--line-length", "200"],
  "files.exclude": {
    "*.egg-info": true
  }
}
"""

gitignore = """
dist/
*.egg-info/
.vscode/*
!.vscode/settings.readme.json
"""

build = """
#!/bin/bash

version=$1

if [ -z "$version" ]; then
    echo "Version is required"
    exit 1
fi

python setup.py sdist
pip uninstall {{{package_name}}} -y
pip install dist/{{{module_name}}}-$version.tar.gz --force-reinstall
# twine upload dist/{{{module_name}}}-$version.tar.gz
"""
