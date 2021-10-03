"""
Boilerplate script frame, so a tiny command-line script has
basic organization, arguments, etc.
"""
# import os
import sys
import argparse
import logging
from pathlib import Path


class App:
    def __init__(self, app_args):
        self.args = app_args
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            filename="app.log",
            filemode="w",
        )
        # logging.debug('A debug message')

    def execute(self):
        print("Executing.")
        self.prepare()
        self.run()
        self.cleanup()
        return 0

    def prepare(self):
        print(f"Preparing {self.args.app_name}.")

    def run(self):
        # PRIMARY CODE GOES HERE
        logging.info(f"Running {self.args.app_name}.")

    def cleanup(self):
        print(f"Cleaning up {self.args.app_name}.")


def parse_app_args(raw_args):
    parser = argparse.ArgumentParser(raw_args)
    # parser.add_argument("positional")
    # parser.add_argument("--optional_value", "-o")
    # parser.add_argument("--flag", "-f", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    parsed_args = parse_app_args(sys.argv[1:])
    parsed_args.app_name = Path(sys.argv[0]).name
    app = App(parsed_args)
    sys.exit(app.execute())
