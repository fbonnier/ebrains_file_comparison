# Numpy
import json
import file_comparison.report_generator
import file_comparison.stats as stats
import file_comparison.error_handler as error_handler

def compute_differences_report (origin, new):
    # Initialize difference block for the pair of files
    block_diff = {"report": [], "nerrors": 0, "nvalues": 0, "nequalvalues": 0, "log": [], "error": [], "ndiff": 0, "advice": []}

    try:
    # Check if files can be opened as json
        if not new["path"].endswith("json") and not origin["path"].endswith("json"):
            
            with open (new["path"], mode="r", encoding="utf-8") as fnew, open (origin["path"], mode="r", encoding="utf-8") as forigin:
                
                origin_data = json.load(forigin)
                new_data = json.load(fnew)
                
                comparison_path = new["path"]

                block_diff = compare_line (origin=origin_data[iline], new=new_data[iline], comparison_path=comparison_path + "->L" + str(iline), block_diff=block_diff)
        else:
            raise Exception(new["path"] + " or " + origin["path"] + " are not JSON format")


    except Exception as e:
        block_diff["error"].append("JSON compute_differences_report: " + str(error_handler.get_traceback(e)))
        block_diff["nerrors"] += 1
        print ("JSON compute_differences_report: " + str(error_handler.get_traceback(e)))

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


# 2
def check_file_formats (filepath):
    try:
        return True, None
    except Exception as e:
        print ("TXT check_file_format: " + str(error_handler.get_traceback(e)))
        return False, str(e)

