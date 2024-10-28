# Numpy
import numpy as np

from collections.abc import Iterable
import neo.io
import json
import file_comparison.report_generator
import file_comparison.neo as fcneo
import file_comparison.stats as stats
import file_comparison.iterables
import traceback

known_types = [np.lib.npyio.NpzFile, np.ndarray, neo.core.block.Block, neo.core.Segment, str, bytes, list, dict, bool, float, int, neo.core.spiketrain.SpikeTrain, neo.core.analogsignal.AnalogSignal]

# def compare_lists (list1:list, list2:list, comparison_path: str, block_diff: dict ):

#     # block_diff["log"].append(comparison_path+str(type(list1)))
#     if len(list1) != len(list2):
#         block_diff["error"].append(str(comparison_path+str(type(list1))+"->") + "List don't have same length")
#         block_diff["nerrors"] += 1
    
#     for id_ilist in range(min(len(list1), len(list2))):
#         block_diff = file_comparison.iterables.iterable_are_equal (list1[id_ilist], list2[id_ilist], comparison_path+str(type(list1))+"->", block_diff)
    
#     return block_diff

# def compare_dicts (original_item, new_item, comparison_path, block_diff):
#     keys_to_avoid = []
#     common_keys = []
#     # block_diff["log"].append (comparison_path+str(type(original_item)))

#     for ikey in original_item.keys():
#         if not ikey in new_item:
#             keys_to_avoid.append(ikey)

#     for ikey in new_item.keys():
#         if not ikey in original_item:
#             keys_to_avoid.append(ikey)

#     common_keys = original_item.keys() - keys_to_avoid

#     if len(keys_to_avoid) > 0:
#         block_diff["error"].append(str(comparison_path+str(type(original_item))+"->KeysAvoided") +  str(keys_to_avoid))
#         block_diff["nerrors"] += len(keys_to_avoid)
#         block_diff["nvalues"] += len(keys_to_avoid)

#     # Iterate on items of original_item and new_item
#     for item in common_keys:
#         block_diff = file_comparison.iterables.iterable_are_equal(original_item[item], new_item[item], comparison_path+str(type(original_item))+"->"+item+"->", block_diff)
        
#     return block_diff
    

def compare_numpy_arrays (original_item, new_item, comparison_path, block_diff):

    # block_diff["log"].append(comparison_path+str(type(original_item)))
    
    # block_diff = file_comparison.iterables.iterable_are_equal(original_item.tolist(), new_item.tolist(), comparison_path+str(type(original_item))+"->", block_diff)
    print ("Compare Numpy Arrays")

    # Check sizes
    if (len(original_item) - len(new_item)):
        block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different size, missing data")
        block_diff["nerrors"] += abs(len(original_item) - len(new_item))

    # Check type similar
    if (original_item.dtype != new_item.dtype):
        block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different data types")
        block_diff["nerrors"] += abs(len(original_item))
    
    # Check type similar
    if (original_item.dtype != object and new_item.dtype != object):
        # block_delta = file_comparison.report_generator.compute_1list_difference(original_item, new_item)
        print (type(original_item.dtype))

        block_diff["report"].append(file_comparison.report_generator.compute_1list_difference(origin=original_item, new=new_item))
        
        # block_diff["error"].append(comparison_path+str(type(original_item)) + ": Different data types")
        # block_diff["nerrors"] += abs(len(original_item))
            # block_diff["report"].append(file_comparison.report_generator.compute_1el_difference(origin=original_item[iel], new=new_item[iel]))
        block_diff["nvalues"] += min(len(original_item), len(new_item))
    else:
        for iel in range(min(len(original_item), len(new_item))):
            block_diff = file_comparison.iterables.iterable_are_equal (original_item[iel], new_item[iel], comparison_path+str(type(original_item))+"->", block_diff)


    # if len(new_item) != len(original_item):
    #     block_diff["nerrors"] += abs(len(new_item) - len(original_item))
    #     block_diff["error"].append("Nummy array have different sizes, missing data")
    

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
        block_diff["error"].append("NPZ compute_differences_report: " + str("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))
        block_diff["nerrors"] += 1
        print ("NPZ compute_differences_report: " + str("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))

    return block_diff

# 2
def check_file_formats (filepath):
    try:
        np.load(filepath, allow_pickle=True)
        return True, None
    except Exception as e:
        print ("NPZ check_file_format: " + str("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))
        return False, str(e)

# def file_comparison.iterables.iterable_are_equal (original_item, new_item, comparison_path, block_diff):
    
#     if (type (original_item) not in known_types or type(new_item) not in known_types):
#         # Return error, unkown type
#         block_diff["log"].append(comparison_path + " " + str(type(original_item)) + " " + str(type(new_item)))
#         block_diff ["error"].append(comparison_path + " " + str(type(original_item)) + " " + str(type(new_item)) + " are not in KNOWN Types")
#         block_diff["nerrors"]+=1
#         block_diff["nvalues"]+=1

#     #############   NUMPY.NPZ.Files  #################
#     # Convert npz files into compatible arrays
#     if ((type(original_item) == np.lib.npyio.NpzFile) and (type(new_item) == np.lib.npyio.NpzFile)):
        
#         block_diff = compare_numpy_npz (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)

#     #############   NUMPY.arrays  #################
#     # Convert numpy arrays into compatible arrays
#     elif ((type(original_item) == np.ndarray) and (type(new_item) == np.ndarray)):
#         block_diff = compare_numpy_arrays (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)

#     #############   NEO.BLOCK   ###################
#     # TODO
#     elif (type(original_item) == neo.core.block.Block) and (type(new_item) == neo.core.block.Block):
#         # TODO
#         block_diff = fcneo.compare_neo_blocks (original_item, new_item, comparison_path+str(original_item.name)+str(type(original_item))+"->", block_diff)

#     ############    NEO.SEGMENT ##################
#     # TODO
#     elif (type(original_item) == neo.core.Segment) and (type(new_item) == neo.core.Segment):
#         block_diff = fcneo.compare_segments(original_item, new_item, comparison_path+str(original_item.name)+str(type(original_item))+"->", block_diff)
        
#     elif ((isinstance(original_item, Iterable)) and (isinstance(new_item, Iterable)) and (type(original_item)!=str) and (type(original_item)!= bytes) ):

#         #################   LIST    ###################
#         if ((type(original_item) == list) and (type(new_item) == list)):
#             block_diff = compare_lists (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)
            
#         #################   DICT    ###################
#         # Check if original_item and new_item provide keys to check keys
#         elif ((type(original_item) == dict) and (type(new_item) == dict)):
#             block_diff = compare_dicts (original_item, new_item, comparison_path+str(type(original_item))+"->", block_diff)
#         else:
#             block_diff["error"].append(comparison_path+str(type(original_item)) + " iterable not supported")
#             block_diff["nerrors"] += 1
            

#     # If original_item and new_item are not iterable (are values)
#     else :
#         block_diff["nvalues"] += 1
#         # if values are not equal
#         if (original_item != new_item):
#             block_delta = file_comparison.report_generator.compute_1el_difference (original_item, new_item)
#             block_delta["log"].append(str(comparison_path+str(type(original_item))+"->"+str(original_item)))
#             block_diff["report"].append(block_delta)
#             block_diff["nerrors"] += 1
        
#     return block_diff
