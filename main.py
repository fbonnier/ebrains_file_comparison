import os
import file_comparison.bijective as bijective
import file_comparison.method as method
import profile
import argparse
import json
import sys
import traceback

def run_file_comparison (origin, new, jsonfile_out):
    error_glob = []
    pairs = None
    
    try:
        # Build Adjacency Matrix from list of files
        # The matrix is compacted as a list of pairs
        pairs = bijective.find_bijective (produced_outputs=new, expected_outputs=origin)

        # Get adviced method
        for ipair in pairs:
            ipair = method.get_adviced_method (ipair)

        # Compare the files
        for ipair in pairs:
            imethod = method.Method (ipair)

            # Compare hash of files 
            imethod.compare_hash()

            # Compute differences between data
            imethod.compute_differences ()

            # Compute different scores and stats
            imethod.compute_score ()

            # Get all data from associated method and pair
            ipair = imethod.topair(ipair)
            
    except Exception as e:
        error_glob.append (str("".join(traceback.format_exception(e))))
        print (str("".join(traceback.format_exception(e))))

    # Write data in JSON file
    with open(jsonfile_out, "w") as f:
        json_data_out = {}
        json_data_out["Verification Method Reusability"] = {"error": [], "score": 0, "advice": [], "log": [], "report": {}}
        if error_glob:
            json_data_out["Verification Method Reusability"]["error"] += error_glob
        
        n_valid_values = 0
        total_score = 0.
        for ipair in pairs:
            if ipair["error"]:
                json_data_out["Verification Method Reusability"]["error"] += ipair["error"]
            if ipair["log"]:
                json_data_out["Verification Method Reusability"]["log"] += ipair["log"]
            if ipair["advice"]:
                json_data_out["Verification Method Reusability"]["advice"] += ipair["advice"]
            if ipair["score"]:
                total_score += ipair["score"]
                n_valid_values += 1
        
        json_data_out["Verification Method Reusability"]["score"] =  total_score/n_valid_values if n_valid_values else 0.
        json_data_out["Verification Method Reusability"]["report"] = pairs
    
        # Methods report
        json.dump(json_data_out, f, indent=4)

def run_file_comparison_json (jsonfile, jsonfile_out):
    error_glob = []
    json_data = None
    with open(jsonfile, "r") as f:
        try:
            json_data = json.load (f)
            run_file_comparison (origin=json_data["Metadata"]["run"]["outputs"], new=json_data["Outputs"], jsonfile_out=jsonfile_out)
            
        except Exception as e:
            error_glob.append (str("".join(traceback.format_exception(e))))
            print (str("".join(traceback.format_exception(e))))


def run_file_comparison_files(origin_files, new_files, jsonfile_out):
    error_glob = []
    origin = []
    new = []
    for ifile in origin_files:
        origin.append({"path": ifile.name, "filename": os.path.basename(ifile.name), "size": os.path.getsize(ifile.name)})
    for ifile in new_files:
        new.append({"path": ifile.name, "filename": os.path.basename(ifile.name), "size": os.path.getsize(ifile.name)})
    
    try:
        
        run_file_comparison (origin=origin, new=new, jsonfile_out=jsonfile_out)
            
    except Exception as e:
        error_glob.append (str("".join(traceback.format_exception(e))))
        print (str("".join(traceback.format_exception(e))))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Computes file comparison using ')
    parser.add_argument('--expected-results', type=argparse.FileType('r'), dest='expected', nargs="+", help='Files to compare')
    parser.add_argument('--simulated-results', type=argparse.FileType('r'), dest='simulated', nargs="+", help='Files to compare')
    parser.add_argument('--json', type=argparse.FileType('r'), metavar='json', nargs=1,
                        help='JSON File containing metadata of files to compare')
    parser.add_argument('--out', type=argparse.FileType('w'), metavar='out', nargs=1,
                        help='JSON File containing results of file comparison')

    parser.add_argument('--profile', dest='profile', action='store_true',
                        help='Profiling the method')


    args = parser.parse_args()
    jsonfile = args.json[0] if args.json else None
    jsonfile_out = args.out[0] if args.out else None

    expected_results = args.expected if args.expected else None
    simulated_results = args.simulated if args.simulated else None
    
    if args.profile:
        if jsonfile and jsonfile_out:
            try:
                profile.run('run_file_comparison_json(jsonfile.name, jsonfile_out.name)')
            except Exception as e1:
                print (str("".join(traceback.format_exception(e1))))
        elif expected_results and simulated_results:
            try:
                profile.run('run_file_comparison_files(expected_results, simulated_results)')
            except Exception as e2:
                print (str("".join(traceback.format_exception(e2))))

    else:
        if jsonfile and jsonfile_out:
            try:
                run_file_comparison_json(jsonfile=jsonfile.name, jsonfile_out=jsonfile_out.name)
            except Exception as e1:
                print (str("".join(traceback.format_exception(e1))))
        elif expected_results and simulated_results:
            try:
                run_file_comparison_files(expected_results, simulated_results, jsonfile_out=jsonfile_out.name)
            except Exception as e2:
                print (str("".join(traceback.format_exception(e2))))
                

    # Exit Done ?
    sys.exit()