import os
import sys

# We should be able to import toolbox stuff here b/c this module is
# imported after the sys.path setup
from pathlib2 import Path
import contextlib
import logging
import logging.handlers

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


# Note: because of the singleton nature of the 'logging' package,
#   stand-alone functions can use it as an object directly to get
#   messages into the log. However, it skips our formatting, etc... You
#   can run initialize_logging() in any function here; it costs little
#   and ensures uniformity of our logs.
def initialize_logging(
    log_id=None,
    file_log_level=logging.DEBUG,
    console_log_level=logging.INFO,
    # WORKSPACE is a Jenkins thing
    app_root_dir=os.environ.get("WORKSPACE", "."),
    propagate=False,
):
    """
    This implementation is in-between using the basic logger and a fully
    custom system. Since we don't have a nice module structure where I
    currently work, the __name__ trick doesn't help us and this has one
    less layer that can get mis-configured.
    NOTE: IF log_id is not specified it uses the root logger.
    """
    # Log name and path
    if log_id is None:
        # This is the root log.
        logger = logging.getLogger()
        # This is only applicable to the root, others use the log_id.
        ci_log_name = os.environ.get("CI_LOG_NAME", "application.log")
    else:
        # This is to create a child of the root logger.
        logger = logging.getLogger(log_id)
        # The argument 'propagate' == True will copy records up
        # the logger hierarchy; this only makes sense for non-root
        # loggers. These records WILL be in the console if
        # the record's level > console_log_level.
        logger.propagate = propagate
        ci_log_name = "{}.log".format(log_id)

    ci_log_dir = os.getenv("CI_LOG_DIR", ".")
    log_file = Path(app_root_dir).resolve() / ci_log_dir / ci_log_name
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # Set the overall lowest level to report
    logger.setLevel(logging.DEBUG)
    # Start with no handlers - This can be the cause of duplicate messages
    logger.handlers = []
    # File handler, logs everything
    fh = logging.handlers.RotatingFileHandler(
        str(log_file), mode="a", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    fh.setLevel(file_log_level)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(module)s.%(funcName)s():L%(lineno)d - %(levelname)s - %(message)s"
    )
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)
    # Console handler, generally only for INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)
    # Stop requests/urllib messages: "Starting new HTTP connection (1)"
    logging.getLogger("requests").setLevel(logging.WARNING)
    # DEBUG: logging.info("Started logger '{}' at '{}'".format(log_id, log_file))
    return logger


@contextlib.contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = str(Path().resolve())
    # Use str() to coerce in case we get a Path
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)
