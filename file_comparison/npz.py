# Numpy
import numpy as np

from collections.abc import Iterable
import file_comparison.report_generator
import file_comparison.iterables
import traceback
from copy import deepcopy


# Compare Numpy Arrays
def compare_numpy_arrays (original_item, new_item, comparison_path, block_diff):

    # Check array length
    if len(original_item) - len(new_item):
        block_diff["error"].append (comparison_path+str(type(original_item)) + ": Different size, missing data")
        block_diff["nerrors"] += 1
        block_diff["ndiff"] += abs(len(original_item) - len(new_item))

    # Check type similar
    if (original_item.dtype != new_item.dtype):
        block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different data types")
        block_diff["nerrors"] += 1
    
    # Compare values
    if (isinstance(original_item.dtype, Iterable) and isinstance(new_item.dtype, Iterable)):
        
        for iel in range(min(len(original_item), len(new_item))):
            block_diff = file_comparison.iterables.iterable_are_equal (\
                original_item[iel],\
                new_item[iel],\
                comparison_path+str(type(original_item))+"->",\
                block_diff)
    else:
        block_diff["report"].append(file_comparison.report_generator.compute_1list_difference(origin=original_item, new=new_item))
        block_diff["nvalues"] += min(len(original_item), len(new_item))
        
    

    return block_diff

def compare_numpy_npz (original_desc, new_desc, comparison_path, block_diff):

    try:
        original_data = np.load(original_desc["path"], allow_pickle=original_desc["allow_pickle"], encoding=original_desc["encoding"])
        new_data = np.load(new_desc["path"], allow_pickle=new_desc["allow_pickle"], encoding=new_desc["encoding"])

        block_diff = file_comparison.iterables.compare_dicts(original_data, new_data, comparison_path+str(type(original_data))+"->", block_diff)

    except Exception as e:
        block_diff["error"].append("NPZ compare_numpy_npz: " + str("".join(traceback.format_exception(e))))
        block_diff["nerrors"] += 1
        print ("NPZ compare_numpy_npz: " + str("".join(traceback.format_exception(e))))

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
        block_diff = compare_numpy_npz (original_file, new_file, comparison_path, block_diff)

        # elif ((type(original_file["path"]) == np.lib.npyio.NpyFile) and (type(new_file["path"]) == np.lib.npyio.NpyFile)):
        # # print ("iterable_are_equal NPZ type")
        #     # block_diff = compare_numpy_npz (original_file, new_file, comparison_path, block_diff)
        #     print ("NPY files are not supported yet, please convert to NPZ")
        #     block_diff["error"].append("NPY files are not supported yet, please convert to NPZ")
        #     block_diff["nerrors"] += 1

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