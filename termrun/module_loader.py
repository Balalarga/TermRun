import importlib.util
import logging
import os
import pathlib
import sys
import typing


def load_all_modules_from(modules_dir: pathlib.Path) -> typing.Dict[str, pathlib.Path]:
    modules_dir = modules_dir.absolute()
    if not modules_dir.exists():
        raise FileNotFoundError(f"Directory '{modules_dir}' with scripts does not exist!")

    old_cwd = os.getcwd()
    os.chdir(modules_dir)
    loaded_modules = dict()

    files = modules_dir.absolute().rglob("*.py")
    for file in files:
        module = load_module(file)
        if module is None:
            logging.error(f"Cannot load module from '{file}'")
            continue

        existing_module = loaded_modules.get(module.__name__)
        if existing_module:
            raise Exception(f"Duplicate file names\n\t{file}\n\t{existing_module}")
        loaded_modules[module.__name__] = file

    os.chdir(old_cwd)
    return loaded_modules


def load_module(path: pathlib.Path):
    if not path.is_file():
        return None

    logging.debug(f"Loading module {path}")
    return load_named_module(path.stem, path)


def load_named_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
