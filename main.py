import os
import file_comparison.file_compare as fc
# import file_comparison.nilsimsa as nl
# import file_comparison.npz as npz
# import file_comparison.neo as neo
# import file_comparison.hamming as hm
# import file_comparison.levenshtein as lv
# import file_comparison.report_generator as report
# import file_comparison.downloader as downloader
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
                
            ########## USELESS ##########
            # # Check files format
            # check, error = imethod.check_file_formats ()
            # if not check:
            #     # if the files are not the same format: Error
            #     ipair["error"].append (error)
            #     continue
            ##############################

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
        
    # print (json.dumps(final_report, indent=4))

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
    # parser.add_argument('--watchdog', type=argparse.FileType('r'), metavar='watchdog', nargs='1',
    #                     help='Watchdog File containing files to compare with JSON report')
    # parser.add_argument('--hamming', dest='hamming', action='store_const',
    #                     const=hm.hamming_files,
    #                     help='Find the Hamming distance using bit comparison')
    # parser.add_argument('--fuzzy', dest='fuzzy', action='store_const',
    #                     const=lv.levenshtein,
                        # help='Find the Levenshtein distance using FuzzyWuzzy module')
    # parser.add_argument('--nilsimsa', dest='nilsimsa', action='store_const',
    #                     const=nl.nilsimsa_files,
    #                     help='Find the Nilsimsa hash using nilsimsa module')
    # parser.add_argument('--npz', dest='npz', action='store_const',
    #                     const=npz.npz_values,
    #                     help='Find the differences between two NPZ files')
    # parser.add_argument('--neo', dest='neo', action='store_const',
    #                     const=neo.compare_neo_file,
    #                     help='Find the differences between two NEO files')
    # parser.add_argument('--finfo', dest='finfo', action='store_const',
    #                     const=fc.hash_from_file_info,
    #                     help='Hash from file infos')
    # parser.add_argument('--bijective', dest='bijective', action='store_const',
    #                     const=fc.find_bijective,
    #                     help='Hash from file infos')
    parser.add_argument('--profile', dest='profile', action='store_true',
                        help='Profiling the method')
    # parser.add_argument('--buffersize', type=int, metavar='Buffer_Size', nargs=1, dest='buffersize', default=32,
    #                     help='Size of buffer used in bytes (default is 32 bytes)')
    # parser.add_argument('--hex', type=int, metavar='Hexadigest_option', nargs=1, dest='hex', default=1,
    #                     help='Option to specify the files that contains hexadigest filenames.\n\
    #                     0: Both files contain plain urls and complete paths of result files\n\
    #                     1: First file contains urls that should be hashed to retreive corresponding filenames\n\
    #                     2: Both files contain urls/paths that should be hashed to retreive corresponding filenames')

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

    
    # method = ""
    # if args.hamming:
    #     method = "hamming"
    # elif args.fuzzy:
    #     method = "fuzzy"
    # elif args.nilsimsa:
    #     method = "nilsimsa"
    # elif args.npz:
    #     method = "npz"
    # elif args.neo:
    #     method = "neo"
    # elif args.finfo:
    #     method = "finfo"

    # # Build Adjacency Matrix from list of files
    # # The matrix is compacted as a list of pairs
    # adjacency_matrix = fc.find_bijective (args.files[0].name, args.files[1].name, args.hex[0])
    # # print (adjacency_matrix)

    # # Get adviced method
    # advice_methods = fc.get_adviced_method (adjacency_matrix)

    # final_report = []
    # # Compare the files
    # for icouple, imethod in zip(adjacency_matrix, advice_methods):
    #     # print(icouple, imethod)
    #     # score, file_diff = report.compute_differences(icouple[0], icouple[1], imethod)
    #     # final_report.append(report.generate_report_1_file (icouple[0], icouple[1], imethod, score, file_diff))
    #     method = Method (imethod, icouple[0], icouple[1])
    #     is_checked, check_error = method.check_file_formats()

    #     print (is_checked)
    #     if (is_checked):
    #         method.compute_differences_report()
    #         method.compute_score()
    #         final_report.append (method.differences_report)


    # # Generate Comparison Report
    # # for ifile1, ifile2 in adjacency_matrix:
    # #     final_report.append(report.generate_report_1_file (ifile1, ifile2, method, score, differences))

    # print ("FINAL REPORT:")
    # print (json.dumps(final_report, indent=4))

    # if args.bijective:
    #     args.bijective(args.files[0].name, args.files[1].name, args.hex[0])
    #
    # if args.profile:
    #     if args.hamming:
    #         profile.run('args.hamming(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.fuzzy:
    #         profile.run('args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.nilsimsa:
    #         profile.run('args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)')
    #     elif args.npz:
    #         profile.run('args.npz(args.files[0].name, args.files[1].name')
    #     elif args.neo:
    #         profile.run('args.neo(args.files[0].name, args.files[1].name')
    #     elif args.finfo:
    #         profile.run('args.finfo(args.files[0].name, args.files[1].name)')
    # else:
    #     if args.hamming:
    #         args.hamming(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.fuzzy:
    #         args.fuzzy(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.nilsimsa:
    #         args.nilsimsa(args.files[0].name, args.files[1].name, args.buffersize)
    #     elif args.npz:
    #         args.npz(args.files[0].name, args.files[1].name)
    #     elif args.neo:
    #         args.neo(args.files[0].name, args.files[1].name)
    #     elif args.finfo:
    #         args.finfo(args.files[0].name, args.files[1].name)
