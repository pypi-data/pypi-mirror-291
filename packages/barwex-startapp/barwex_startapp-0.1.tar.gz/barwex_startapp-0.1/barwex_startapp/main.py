import os
from os.path import join, dirname, exists
from argparse import ArgumentParser
from barwex_startapp import b3, templates


def parse():
    parser = ArgumentParser()
    parser.add_argument("-d", "--app-dir", dest="app_dir", required=True)
    parser.add_argument("-c", "--command", dest="command_name", required=True)
    args = parser.parse_args()
    if not exists(args.app_dir):
        os.makedirs(args.app_dir)
    return args


def main():
    args = parse()
    app_dir: str = args.app_dir
    command_name: str = args.command_name

    package_name = f"barwex-{command_name}"
    module_name = package_name.replace("-", "_")
    data = {
        "package_name": package_name,
        "package_version": "0.1",
        "module_name": module_name,
        "command_name": command_name,
    }

    text = b3.read_b3text(templates.setup.lstrip(), data=data)
    b3.save_file(text, join(app_dir, "setup.py"))
    b3.save_file(templates.gitignore, join(app_dir, ".gitignore"))
    text = b3.read_b3text(templates.build.lstrip(), data=data)
    b3.save_file(text, join(app_dir, "build.sh"))

    mod_path = join(app_dir, module_name)
    if not exists(mod_path):
        os.mkdir(mod_path)

    b3.save_file("\n", join(mod_path, "__init__.py"))
    b3.save_file(templates.main.lstrip(), join(mod_path, "main.py"))

    vscode_dir = join(app_dir, ".vscode")
    if not exists(vscode_dir):
        os.mkdir(vscode_dir)

    b3.save_file(templates.vscode, join(vscode_dir, "settings.readme.json"))
    b3.save_file(templates.vscode, join(vscode_dir, "settings.json"))
