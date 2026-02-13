import logging
import os
import pathlib
from pprint import pformat
import argparse

import termrun


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--scripts_dir",
        type=pathlib.Path,
        help="Path to scripts directory for parsing",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--log_file",
        type=pathlib.Path,
        help=".log file path for system info",
        default=pathlib.Path("termrun.log"),
    )
    args = parser.parse_args()
    logging.basicConfig(filename=args.log_file, level=logging.INFO, filemode="w")

    loaded_modules = termrun.load_all_modules_from(args.scripts_dir)
    logging.info(f"Loaded modules: \n{pformat(loaded_modules, indent=2)}")

    menu_fsm = termrun.CliMenu()
    while menu_fsm.draw():
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    print(f"\n{'-' * 30}\nBye bye...")
