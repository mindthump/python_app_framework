#!/usr/bin/env python
# coding=utf-8
"""
A framework for Python "applications".
DO NOT COPY AND EDIT THIS FILE !!!
Subclass and refactor, don't fork.
"""

# ONLY STOCK PYTHON PACKAGES HERE
# Our stuff comes later. Some of these might be used only in subclasses.
from __future__ import print_function

import json
import logging
import os
import sys


# WORKSPACE is primarily for Jenkins but can be useful elsewhere.
WORKSPACE = (
    os.environ["WORKSPACE"]
    if os.path.isdir(os.getenv("WORKSPACE", ""))
    else os.getcwd()
)

# I hate it when users see traceback except for debugging.
# sys.tracebacklimit = 0


class AppFramework(object):
    """
    Override additional_arguments() and run(), implement super()
    """

    def __init__(self):
        """
        Call this from subclasses:
        super
        # Arguments
        # My philosophy of arguments, options, etc. is:
        # command-line > config-file > env-var > default

        Make parameters into fields, get the DB, etc.
        This assumes every subclass needs the DB.
        """
        self.app_args = None
        os.environ["ORIGINAL_SYSPATH"] = json.dumps(sys.path)
        self.toolbox_root = locate_toolbox_root()
        # Ugly but flexible.
        app_syspath = {
            "ROOT": "{toolbox}".format(toolbox=self.toolbox_root),
            "TOOLBOX": "{toolbox}/toolbox".format(toolbox=self.toolbox_root),
            "DB": "{toolbox}/DB".format(toolbox=self.toolbox_root),
        }
        # Save the current sys.path just in case (?)
        os.environ["APP_SYSPATH"] = json.dumps(app_syspath)
        update_syspath()

        # From here on it should be safe to import any local packages
        from toolbox import urllib3
        from toolbox import requests
        from toolbox import configargparse
        from toolbox import app_utils

        self.logger = app_utils.initialize_logging()
        # requests.packages.urllib3.disable_warnings()
        # Quiet stupid requests "http connection" messages
        logging.getLogger("toolbox.requests.packages.urllib3").setLevel(
            logging.WARNING
        )

        # NOTE: This is *not* the native argument parser,
        #   it is augmented for env-vars and config files
        self.parser = configargparse.ArgParser(
            default_config_files=["{}.cfg".format(os.path.basename(__file__))]
        )

    def parse_app_arguments(self, app_args):
        """
        :param app_args: raw argument list
        :return: Nothing
        """
        self.parser.add_argument(
            "-v",
            "--log_verbose",
            help="Log ALL messages.",
            env_var="LOG_VERBOSE",
            action="store_true",
        )
        self.parser.add_argument(
            "-D",
            "--app_debug",
            help="Turn on debugging mode (developer use only).",
            env_var="APP_DEBUG",
            action="store_true",
        )
        self.parser.add_argument("--logname", action="store", default="ci_app.log")
        self.additional_arguments()
        self.app_args = self.parser.parse_args(app_args)
        # We occasionally subprocess() other python tasks; We need the
        # final values back in the env so "external" scripts can see them
        os.environ["LOG_VERBOSE"] = str(self.app_args.log_verbose)
        os.environ["APP_DEBUG"] = str(self.app_args.app_debug)
        pass

    def additional_arguments(self):
        # Override to add app-specific arguments.
        pass

    def prepare(self):
        # Override to set up app-specific structure.
        pass

    def run(self):
        # Override to do the main work of the app
        pass

    def cleanup(self):
        # Override to clean up any messes.
        pass

    def execute(self):
        # I want the actual arg parsing to be out of the hands of the
        # subclasses. Normally a subclass would not implement/override
        # this, or should at least call this super(). Tests could
        # probably mock this and set self.args to a custom Namespace.
        self.parse_app_arguments(sys.argv[1:])
        # These should be implemented in the subclass.
        self.prepare()
        return self.run()


def errprint(*args, **kwargs):
    """
    Print on stderr
    """
    print(*args, file=sys.stderr, **kwargs)


class CIAppFrameworkError(Exception):
    """
    This is abuse of exceptions. Normally exceptions are intended to be
    caught by a try/catch but this is more like a soft landing zone for
    problems that are known but insumountable.
    """

    def __init__(self, message, fail_app=True):
        from toolbox import app_utils
        self.logger = app_utils.initialize_logging()
        # Get the class name without hardcoding (reusable)
        if message:
            self.logger.error(
                "{errsrc}: {msg}".format(errsrc=self.__class__.__name__, msg=message)
            )
        if fail_app:
            self.logger.critical("Error is forcing application exit.")
            sys.exit(1)


# A path management mechanism
# Having a proper structure is crucial to using libraries, and ours are
# currently very messy. We mitigate that by careful sys.path management.
# We locate our repo root and add it along with the others using relative
# paths converted to absolutes. We stash the required paths as JSON
# in an environment variable then update sys.path from there.


def locate_toolbox_root():
    # First put the repo root directory on sys.path from the root, the
    # parent, or a subdirectory. Users do need to start from one of
    # these places, otherwise it raises an exception. This lets us get
    # at our own packages in the usrlocallib directory. It
    # looks relative to the current working directory(os.getcwd), not
    # the location of the script (__file__).
    toolbox_root = ""
    if os.path.isdir("toolbox"):
        toolbox_root = "."
    elif os.path.isdir("../toolbox"):
        # We're in a repo root subdirectory (e.g., PushVerify).
        toolbox_root = ".."
    else:
        subdirs = next(os.walk("."))[1]
        for subdir in subdirs:
            # Look for a known directory
            if os.path.isdir(os.path.join(subdir, "toolbox")):
                # We're in the parent of repo root.
                toolbox_root = subdir
                break
    return os.path.abspath(toolbox_root)


def update_syspath():
    # Use to ensure required modules and packages are on sys.path[].
    # Put the required paths in APP_SYSPATH so we can call this from
    # anywhere.
    try:
        required_paths = json.loads(os.getenv("APP_SYSPATH", ""))
        # str() is for libpath2 Paths (TBD)
        for (name, path) in {n: str(p) for n, p in required_paths.items()}.items():
            if path and os.path.exists(path) and path not in sys.path:
                sys.path.append(path)
    except Exception as ex:
        raise CIAppFrameworkError("Could not update sys.path: {}".format(ex.message))


if __name__ == "__main__":
    # Setup and run the application.
    # FOR TEST ONLY, USE A SUBCLASS !!
    raw_parameters = sys.argv[1:]
    # pprint.pprint(raw_parameters)
    app = AppFramework()
    app.parse_app_arguments(raw_parameters)
    result = app.run()
    sys.exit(result)
