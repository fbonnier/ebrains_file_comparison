# Report generator Module
import numpy as np
import traceback
import sys

error_diff_types = ["type", "len"]


def get_traceback (exception):
    if sys.version_info < (3, 10):
        # For Python 3.10 and earlier
        return "".join(traceback.format_exception(exception.__class__, exception, exception.__traceback__))
    else:
        # For Python 3.10 and later
        return "".join(traceback.format_exception(exception))

