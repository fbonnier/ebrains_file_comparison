# Numpy
import json
import file_comparison.report_generator
import file_comparison.stats as stats
import traceback

def compute_differences_report (origin, new):
    # Initialize difference block for the pair of files
    block_diff = {"report": [], "nerrors": 0, "nvalues": 0, "log": [], "error": [], "ndiff": 0, "advice": []}

    try:
    # Check if files can be opened as text
        with open (new["path"], mode="r", encoding="utf-8") as fnew, open (origin["path"], mode="r", encoding="utf-8") as forigin:
            
            origin_data = forigin.readlines()
            new_data = fnew.readlines()

            # Check number or lines
            if len(origin_data) != len(new_data):
                block_diff["ndiff"] += abs(len(origin_data) - len(new_data))
                block_diff["log"].append(str(origin["path"]) + " and " + str(new["path"]) + " files are not the same size. Diff=" + str(block_diff["ndiff"]) + " lines")
            
            nlines = min(len(origin_data), len(new_data))
            comparison_path = new["path"]

            for iline in range(nlines):
                block_diff = compare_line (origin=origin_data[iline], new=new_data[iline], comparison_path=comparison_path + "->L" + str(iline), block_diff=block_diff)


    except Exception as e:
        block_diff["error"].append("TEXT compute_differences_report: " + str("".join(traceback.format_exception(e))))
        block_diff["nerrors"] += 1
        print ("TEXT compute_differences_report: " + str("".join(traceback.format_exception(e))))

    return block_diff

    


def compare_line(origin:str, new:str, comparison_path: str, block_diff:dict):
    if origin != new:
        # Check each word in line
        origin_words = origin.split()
        new_words = new.split()
        if len(origin_words) != len(new_words):
            block_diff["ndiff"] += abs(len(origin_words) - len(new_words))
            block_diff["log"].append("lines are not the same size. Diff=" + str(block_diff["ndiff"]) + " lines")

        nwords = min(len(origin_words), len(new_words))

        for iword in range(nwords):
            block_diff = compare_word (origin=origin_words[iword], new=new_words[iword], comparison_path=comparison_path, block_diff=block_diff)
    return block_diff

def compare_word (origin:str, new:str, comparison_path: str, block_diff:dict):
    if origin == None or new == None:
        block_diff["error"].append (comparison_path + "")
        return block_diff
    else:
        try:
            block_diff = file_comparison.iterables.iterable_are_equal (origin, new, comparison_path, block_diff)
        except:
            pass
    return block_diff

def compare_char ():
    pass    



# 4
def compute_score (number_of_errors, number_of_values):
    #TODO Catch Exception instead of assert
    assert number_of_values > 0, "No data to compare, score is divided by 0"
    print ("Number of errors = " + str (number_of_errors))
    print ("Number of values = " + str (number_of_values))
    # print ("Number of failures = " + str (len(self.all_failures)) + "\n")

    score = 100. - (number_of_errors*100./number_of_values)

    return (score)


# 2
def check_file_formats (filepath):
    try:
        # np.load(filepath, allow_pickle=True)
        return True, None
    except Exception as e:
        print ("TXT check_file_format: " + str("".join(traceback.format_exception(e))))
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
