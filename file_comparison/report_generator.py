# Report generator Module
import os
import file_comparison.stats as stats
import numpy as np
import traceback

error_diff_types = ["type", "len"]


def compute_1el_difference (origin, new):
    return compute_1list_difference (np.array(origin, ndmin=1), np.array(new, ndmin=1))


def compute_1list_difference (origin:np.ndarray, new:np.ndarray):
 
    block_diff_1list = {"origin": {"type": str(type(origin.tolist())), "value": origin.tolist()}, "new": {"type": str(type(new.tolist())), "value": new.tolist()}, "levenshtein": None, "nilsimsa": None, "rmspe": None, "mspe": None, "mape": None, "mpe": None, "rpd": None , "max delta": None, "delta": None, "error": [], "log": [], "ndiff": 0, "advice": []}


    # Test mean delta
    # Compute Mean Absolute difference between two values
    try:
        block_diff_1list["delta"] = stats.delta(origin, new).item()
        # block_diff_1list["delta"] = np.nanmean(np.absolute(origin - new))
    except Exception as e:
        block_diff_1list["log"].append("Mean Delta Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["delta"] = None

    # Test maximum delta
    # Compute Maximum difference in dataset
    try:
        block_diff_1list["max delta"] = stats.maximum_delta(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("Max Delta Stat:" + str("".join(traceback.format_exception(e))))
        block_diff_1list["max delta"] = None

    # Test string values
    # Compute Levenshtein distance percentage between two strings
    try:
        block_diff_1list["levenshtein"] = stats.mean_levenshtein_distance_percentage(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("Levenshtein Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["levenshtein"] = None

    # Test mape
    # Compute Absolute Percentage Error between two values
    try:
        block_diff_1list["mape"] = stats.mean_absolute_percentage_error(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("MAPE Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["mape"] = None
    
    # Test mspe
    # Compute Mean Squared Percentage Error between two values
    # TODO
    try:
        block_diff_1list["mspe"] = stats.mean_squared_percentage_error(origin, new).item()        
    except Exception as e:
        block_diff_1list["log"].append("MSPE Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["mspe"] = None

    # Test rmspe
    # Compute Root Mean Squared Percentage Error between two lists
    try:
        block_diff_1list["rmspe"] = stats.root_mean_squared_percentage_error(origin, new).item()        
    except Exception as e:
        block_diff_1list["log"].append("RMSPE Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["rmspe"] = None

    # Test mpe
    # Compute Mean Percentage Error between two lists
    try:
        block_diff_1list["mpe"] = stats.mean_percentage_error(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("MPE Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["mpe"] = None
    
    # Test rpd
    # Compute Relative Percentage Difference between two lists
    try:
        block_diff_1list["rpd"] = stats.mean_relative_percentage_difference(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("RPD Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["rpd"] = None
            
    # Test nilsimsa
    # Compute Nilsimsa Distane between two lists
    try:
        block_diff_1list["nilsimsa"] = stats.mean_nilsimsa_distance(origin, new).item()
    except Exception as e:
        block_diff_1list["log"].append("Mean Nilsimsa Stat: " + str("".join(traceback.format_exception(e))))
        block_diff_1list["nilsimsa"] = None

    # Count the number of value differences
    for iel in range(min(origin.size, new.size)):
        try:
            if origin[iel] != new[iel]:
                block_diff_1list["ndiff"] += 1
        except Exception as e:
            block_diff_1list["log"].append("report_generator - Count differences: " + str(type(origin[iel])) + " - " + str(type(new[iel])) + " " + str("".join(traceback.format_exception(e))))
            block_diff_1list["error"].append("report_generator - Count differences: " + str(type(origin[iel])) + " - " + str(type(new[iel])) + " " + str("".join(traceback.format_exception(e))))
            print ("report_generator - Count differences: " + str(type(origin[iel])) + " - " + str(type(new[iel])) + " " + str("".join(traceback.format_exception(e))))

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