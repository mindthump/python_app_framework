#!/usr/bin/env python
# coding=utf-8
"""
A framework for command-line Python "applications", with features that I was in need of at the time.
"""

import logging
import os
import sys
import json
from app_utils import utils

# These imports assume this is the "main" script and this file is
# located at the project root. The directory of the file executed
# with the 'python' command is pushed onto sys.path, so all package
# directories are accessible to 'import'.
# NOTE: This means any root-level script should automatically be OK
#  for all our standard tool imports, but any script in a lower
#  directory won't be able to reach them without sys.path management.


# I hate it when users see traceback except for debugging.
# sys.tracebacklimit = 0


class AppFramework(object):
    """
    Override additional_arguments() and run(), implement super()
    """

    def __init__(self):
        """
        Call this from subclasses with 'super'
        """
        self.app_args = None

        # From here on it should be safe to import any local packages
        import requests
        import configargparse

        self.logger = utils.initialize_logging()
        self.app_args = None
        self.requests = requests
        # Quiet requests "http connection" messages
        self.requests.packages.urllib3.disable_warnings()
        logging.getLogger("gk_third_party.requests.packages.urllib3").setLevel(
            logging.WARNING
        )

        # NOTE: This is *not* the native argument parser,
        #   it is augmented for env-vars and config files
        self.parser = configargparse.ArgParser(
            default_config_files=["{}.cfg".format(os.path.basename(__file__))]
        )

    def parse_app_arguments(self, raw_arg_list):
        """
        NOTE: Arguments can also be specified in a "config file".
        :param raw_arg_list: raw argument list
        :return: Nothing
        """
        self.parser.add_argument(
            # Intended for verbose end-user data, use '--debug' for debugging.
            "-V",
            "--log_verbose",
            help="Log ALL messages.",
            env_var="LOG_VERBOSE",
            action="store_true",
        )
        self.parser.add_argument(
            "-D",
            "--debug",
            help="Turn on debugging mode (developer use only).",
            env_var="AFW_DEBUG",
            action="store_true",
        )
        self.parser.add_argument(
            "--config_file",
            help="Supply arguments in a configuration file.",
            is_config_file=True,
            required=False,
        )
        self.additional_arguments()
        self.app_args = self.parser.parse_args(raw_arg_list)
        if self.app_args.debug:
            self.logger.debug("Arguments:\n{}".format(self.parser.format_values()))

    def additional_arguments(self):
        # Override to add app-specific arguments.
        # command line > environment > config file > defaults
        pass

    def prepare(self):
        # Override to set up app-specific structure.
        pass

    def run(self):
        # Override to do the main work of the app.
        return 0

    def cleanup(self):
        # Override to clean up any messes. This will *usually* run, barring accidents.
        pass

    def execute(self, raw_args=sys.argv[1:], args_dict=None):
        # I want the actual arg parsing to be out of the hands of the
        # subclasses. Normally a subclass would not implement/override
        # this, or should at least call this super().

        if args_dict:
            # args_dict will override raw_args
            # NOTE: item value needs to be None for no-value types like store_true
            args = self.args_from_dict(args_dict)
        else:
            args = raw_args
        self.parse_app_arguments(args)
        self.prepare()
        try:
            rc = self.run()
        except Exception as ex:
            raise AppFrameworkError(f"Exception type {type(ex)} in run() method: {ex.args}")
        finally:
            self.cleanup()
        self.logger.debug(f"CIAppFramework execute() exiting, RC={rc}.")
        return rc

    def args_from_dict(self, args_dict):
        # TODO: Find the argument's Actions object?
        args = []
        for k, v in args_dict.items():
            if v is None:
                args.append(
                    self.parser.get_command_line_key_for_unknown_config_file_setting(k)
                )
            else:
                args.extend(self.parser.convert_item_to_command_line_arg(None, k, v))
        return args


def errprint(*args, **kwargs):
    """
    Print on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


class AppFrameworkError(Exception):
    """
    This is abuse of exceptions. Normally exceptions are intended to be
    caught by a try/catch but this is more like a soft landing zone for
    problems that are known but insumountable.
    """

    def __init__(self, message, fail_app=True):

        self.logger = utils.initialize_logging()
        # Get the class name without hardcoding (reusable)
        if message:
            self.logger.error(
                "{self.__class__.__name__}: {message}"
            )
        if fail_app:
            self.logger.critical("Error is forcing application exit.")
            sys.exit(1)


if __name__ == "__main__":
    # Setup and run the application.
    # FOR TEST ONLY, USE A SUBCLASS !!
    app = AppFramework()
    result = app.execute()
    sys.exit(result)
