"""
Given a set of clusters, generate a dataset with a specified number of true or false labels
"""

import os
import argparse
import csv
from random import shuffle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Join a set of clusters with the correspoding questions')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Clusters dataset in CSV format")
    parser.add_argument("-m", "--question_mapping", required=True, nargs='+', type=int,
                        help="id-question pairs file (saved as CSV)")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output file name (saved as CSV)")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="output_file and question_mapping are overwritten if they do already exists")

    args = parser.parse_args()

    input_file = args.input_file
    mapping = args.question_mapping
    output_file = args.output_file
    force = args.force_overwrite

    if not os.path.exists(input_file):
        print("Input file {} does not exists".format(input_file))
        exit(1)

    if os.path.exists(output_file):
        if force:
            os.remove(output_file)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_file))
            exit(1)
    
    

    #### JOIN and SAVE ####
    raise NotImplemented("This functionality has not been implemented yet")

    print("Done!")

    
