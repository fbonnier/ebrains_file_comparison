# Downloader Module to download files from given URLs from input JSON file
import json

def download_results (json_file, dest_path):

    with open (json_file) as jfile:
        jcontent = json.load (jfile)
        results = jcontent ["results"]
        print (jcontent)
        print (results)
