import os
import logging
import logging.handlers
from toolbox.pathlib2 import Path


def initialize_logging(
    log_id=None,
    file_log_level=logging.DEBUG,
    console_log_level=logging.INFO,
    ci_log_name=os.environ.get("CI_LOG_NAME", "common.log"),
    fw_root=os.environ.get("WORKSPACE", "."),
):
    """
    This implementation is in-between using the basic logger and
    a fully custom system. Since we don't have a nice module
    structure, the __name__ trick doesn't help us and this has one
    less layer that can get mis-configured.
    """
    if log_id is None:
        # Use the root logger.
        logger = logging.getLogger()
    else:
        # This is so you can give it a name (log_id) if you insist, and
        # it will derive from the root. The log file will be named after
        # the log_id + '.log'
        logger = logging.getLogger(log_id)
        ci_log_name = "{}.log".format(log_id)
    # Log name and path
    log_file = Path(fw_root).resolve() / ci_log_name
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
    return logger
