"""
Boilerplate script frame, so a tiny command-line script has
basic organization, arguments, etc.
"""
import os
import sys
import argparse
import logging


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
        if self.args.flag:
            print("FLAG!")

    def run(self):
        # PRIMARY CODE GOES HERE
        message = f"{self.args.positional} {self.args.optional_value or ''}".rstrip()
        logging.info(f"Working, message is '{message}'.")

    def cleanup(self):
        print("Done.")
        pass


def parse_app_args(raw_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("positional")
    parser.add_argument("--optional_value", "-o")
    parser.add_argument("--flag", "-f", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    parsed_args = parse_app_args(sys.argv[1:])
    app = App(parsed_args)
    sys.exit(app.execute())
