# Report generator Module
import os
import file_comparison.stats as stats
import numpy as np
import file_comparison.error_handler as error_handler

error_diff_types = ["type", "len"]


def compute_1el_difference (origin:np.ndarray, new:np.ndarray):
    return compute_1list_difference (origin, new)

def compute_1el_difference_str (origin:np.ndarray, new:np.ndarray):
    return compute_1list_difference_str (origin, new)

def compute_1list_difference_str (origin:np.ndarray, new:np.ndarray):

    block_diff_1list = {"origin": {"type": str(origin.dtype), "value": [str(i) for i in origin.tolist()]}, "new": {"type": str(new.dtype), "value": [str(i) for i in new.tolist()]}, "levenshtein": None, "nilsimsa": None, "rmspe": None, "mspe": None, "mape": None, "mpe": None, "rpd": None , "max delta": None, "delta": None, "quantity": None, "error": [], "log": [], "ndiff": 0, "advice": []}

    # If data is STRING, we can compute Levenshtein distance
    # if (origin.dtype == "str" and new.dtype == "str") or (origin.dtype == np.string_ and new.dtype == np.string_) or (origin.dtype == "bytes" and new.dtype == "bytes") or (origin.dtype == np.bytes_ and new.dtype == np.bytes_):
    try:
        block_diff_1list["levenshtein"] = stats.mean_levenshtein_distance_percentage(origin, new)
    except Exception as e:
        block_diff_1list["log"].append("Levenshtein Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["levenshtein"] = None

    # Test nilsimsa
    # Compute Nilsimsa Distane between two lists
    try:
        block_diff_1list["nilsimsa"] = stats.mean_nilsimsa_distance(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["error"].append("Mean Nilsimsa Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["nilsimsa"] = None

    # Test count_diffs
    # Count the number of value differences
    _ndiff, _error = stats.count_diffs (origin, new)
    block_diff_1list["ndiff"] += _ndiff
    block_diff_1list["error"].append(_error)
    block_diff_1list["quantity"] = max(len(origin), len(new)) - block_diff_1list["ndiff"]

    return block_diff_1list

def compute_1list_difference (origin:np.ndarray, new:np.ndarray):

    block_diff_1list = {"origin": {"type": str(origin.dtype), "value": origin.tolist()}, "new": {"type": str(new.dtype), "value": new.tolist()}, "levenshtein": None, "nilsimsa": None, "rmspe": None, "mspe": None, "mape": None, "mpe": None, "rpd": None , "max delta": None, "delta": None, "quantity": None, "error": [], "log": [], "ndiff": 0, "advice": []}

    # Test mean delta
    # Compute Mean Absolute difference between two values
    try:
        block_diff_1list["delta"] = stats.delta(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["error"].append("Mean Delta Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["delta"] = None

    # Test maximum delta
    # Compute Maximum difference in dataset
    try:
        block_diff_1list["max delta"] = stats.maximum_delta(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["error"].append("Max Delta Stat:" + str(error_handler.get_traceback(e)))
        block_diff_1list["max delta"] = None

    # Test string values
    # Compute Levenshtein distance percentage between two strings
    try:
        block_diff_1list["levenshtein"] = stats.mean_levenshtein_distance_percentage(origin.astype(np.float64), new.astype(np.float64))
    except Exception as e:
        block_diff_1list["error"].append("Levenshtein Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["levenshtein"] = None

    # Test mape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1list["mape"] = stats.mean_absolute_percentage_error(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["error"].append("MAPE Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["mape"] = None
        
    # Test mspe
    # Compute Mean Squared Percentage Error between two values
    # TODO
    try:
        block_diff_1list["mspe"] = stats.mean_squared_percentage_error(origin.astype(np.float64), new.astype(np.float64)).item()        
    except Exception as e:
        block_diff_1list["error"].append("MSPE Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["mspe"] = None

    # Test rmspe
    # Compute Root Mean Squared Percentage Error between two lists
    try:
        block_diff_1list["rmspe"] = stats.root_mean_squared_percentage_error(origin.astype(np.float64), new.astype(np.float64)).item()        
    except Exception as e:
        block_diff_1list["error"].append("RMSPE Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["rmspe"] = None

    # Test mpe
    # Compute Mean Percentage Error between two lists
    try:
        block_diff_1list["mpe"] = stats.mean_percentage_error(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["log"].append("MPE Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["mpe"] = None
        
    # Test rpd
    # Compute Relative Percentage Difference between two lists
    # TO FIX
    try:
        block_diff_1list["rpd"] = stats.mean_relative_percentage_difference(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["log"].append("RPD Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["rpd"] = None
                
    # Test nilsimsa
    # Compute Nilsimsa Distance between two lists
    try:
        block_diff_1list["nilsimsa"] = stats.mean_nilsimsa_distance(origin.astype(np.float64), new.astype(np.float64)).item()
    except Exception as e:
        block_diff_1list["error"].append("Mean Nilsimsa Stat: " + str(error_handler.get_traceback(e)))
        block_diff_1list["nilsimsa"] = None

    # Test count_diffs
    # Count the number of value differences
    _ndiff, _error = stats.count_diffs (origin, new)
    block_diff_1list["ndiff"] += _ndiff
    block_diff_1list["error"].append(_error)
    block_diff_1list["quantity"] = max(len(origin), len(new)) - block_diff_1list["ndiff"]

    return block_diff_1list
"""
Differences object should look like:
------------------
neo objects
{
    'block x':
    {
        'segment y':
        {
            'data array z':
            {
                'item i': abs (item m - item n)
            }
        }
    }
    'missing data':
    {
        'block x':
        {
            'segment y':
            {
                'data array z': [item m, item n, ...]
            }
        }
    }
}

-------------------
numpy objects
{
    'array x':
    {
        'item i': abs (item m - item n)
    }
}
-------------------
byte method objects
{
    'block x':
}
"""
