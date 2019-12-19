"""
Given the complete mapping between IDs and question, generate a similar file
containing only the IDs of the questions present in the input split.
"""


import os
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate mappings file for a particular list of clusters')
    parser.add_argument("-i", "--input_split", required=True, type=str,
                        help="Cluster list (in CSV)")
    parser.add_argument("-m", "--input_mapping", required=True, type=str,
                        help="Input file in which all the pair id question are listed (in CSV)")
    parser.add_argument("-o", "--output_mapping", required=True, type=str,
                        help="Output file in which each question id is mapped to a question")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")
    
    args = parser.parse_args()

    input_split = args.input_split
    input_mapping = args.input_mapping
    output_mapping = args.output_mapping
    force = args.force_overwrite

    if not os.path.exists(input_split):
        print("Input file {} does not exists".format(input_split))
        exit(1)

    if not os.path.exists(input_mapping):
        print("Input file {} does not exists".format(input_mapping))
        exit(1)

    if os.path.exists(output_mapping):
        if force:
            os.remove(output_mapping)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_mapping))
            exit(1)


    # Read CSV split file
    questions_ids = set()
    with open(input_split) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for i, row in enumerate(csv_reader):    
            row = [int(x) for x in row]
            questions_ids.update(row)

     # Read CSV split file
    mappings = dict()
    with open(input_mapping) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for i, row in enumerate(csv_reader):    
            mappings[int(row[0])] = row[1].strip()

    # specific id-question pair for this split file
    res_mappings = dict()
    for id in questions_ids:
        res_mappings[id] = mappings[id]

    # write mapping to the output_mapping file
    with open(output_mapping, mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for key, value in res_mappings.items():
            writer.writerow([key, value])

    print("Done!")
