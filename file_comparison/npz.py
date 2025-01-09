# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
import file_comparison.report_generator
import file_comparison.neo as fcneo
import file_comparison.stats as stats
import file_comparison.iterables
import traceback


# Compare Numpy Arrays
def compare_numpy_arrays (original_item, new_item, comparison_path, block_diff):

    # Check sizes
    if (len(original_item) - len(new_item)):
        block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different size, missing data")
        block_diff["nerrors"] += abs(len(original_item) - len(new_item))

    # Check type similar
    if (original_item.dtype != new_item.dtype):
        block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different data types")
        block_diff["nerrors"] += abs(len(original_item))
    
    # Compare values
    if (original_item.dtype != object and new_item.dtype != object):
        
        block_diff["report"].append(file_comparison.report_generator.compute_1list_difference(origin=original_item, new=new_item))
        
        block_diff["nvalues"] += min(len(original_item), len(new_item))
    else:
        for iel in range(min(len(original_item), len(new_item))):
            block_diff = file_comparison.iterables.iterable_are_equal (original_item[iel], new_item[iel], comparison_path+str(type(original_item))+"->", block_diff)
    

    return block_diff

def compare_numpy_npz (original_item, new_item, comparison_path, block_diff):

    keys_to_avoid = []
    common_keys = []

    # Check keys_to_avoid# # TODO
    for ikey in original_item.files:
        if not ikey in new_item.files:
            keys_to_avoid.append(ikey)
        elif not ikey in common_keys:
            common_keys.append(ikey)

    for ikey in new_item.files:
        if not ikey in original_item.files:
            keys_to_avoid.append(ikey)
        elif not ikey in common_keys:
            common_keys.append(ikey)

    # common_keys = original_item.files - keys_to_avoid
    if len(keys_to_avoid) > 0:
        block_diff["error"].append(str(comparison_path+str(type(original_item))+"->KeysAvoided") + str( keys_to_avoid))
        block_diff["nerrors"] += len(keys_to_avoid)
        block_diff["nvalues"] += len(keys_to_avoid)

    # Iterate on keys
    for ivar in common_keys:
        block_diff = file_comparison.iterables.iterable_are_equal(original_item[ivar], new_item[ivar], comparison_path+str(type(original_item))+"->"+str(ivar)+"->", block_diff)
    return block_diff


# 4
def compute_score (number_of_errors, number_of_values):
    #TODO Catch Exception instead of assert
    assert number_of_values > 0, "No data to compare, score is divided by 0"
    print ("Number of errors = " + str (number_of_errors))
    print ("Number of values = " + str (number_of_values))
    # print ("Number of failures = " + str (len(self.all_failures)) + "\n")

    score = 100. - (number_of_errors*100./number_of_values)

    return (score)

# 3
def compute_differences_report (original_file, new_file):

    block_diff = {"report": [], "nerrors": 0, "nvalues": 0, "log": [], "error": [], "ndiff": 0, "advice": []}
    comparison_path = new_file["path"]
    try:
        original_data = np.load(original_file["path"], allow_pickle=original_file["allow_pickle"], encoding=original_file["encoding"])
        new_data = np.load(new_file["path"], allow_pickle=new_file["allow_pickle"], encoding=new_file["encoding"])

        block_diff = file_comparison.iterables.iterable_are_equal (original_data, new_data, comparison_path, block_diff)
        # print (block_diff)
        # print ("\n")

    except Exception as e:
        block_diff["error"].append("NPZ compute_differences_report: " + str("".join(traceback.format_exception(e))))
        block_diff["nerrors"] += 1
        print ("NPZ compute_differences_report: " + str("".join(traceback.format_exception(e))))

    return block_diff

# 2
def check_file_formats (filepath):
    try:
        np.load(filepath, allow_pickle=True)
        return True, None
    except Exception as e:
        print ("NPZ check_file_format: " + str("".join(traceback.format_exception(e))))
        return False, str(e)