"""
Given a Quora dataset, cluster it, split it in different files (without overlapping questions)
and finally create training datasets.
"""

import os
import argparse
import csv
import random
import shutil
from cluster import cluster
from split import split

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora-Question-Pairs dataset in clusters')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset (in CSV format)")
    parser.add_argument("-t", "--translation_file", required=True, type=str,
                        help="Translate output datasets in italian (requires do_generation)")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output folder in which results will be saved (in CSV)")
   
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")

    parser.add_argument("-l", "--limit", required=False, type=int, default=None,
                        help="max number of entries for each split. Default is maximum, computed based on ratio")

    args = parser.parse_args()

    # Args
    input_file = args.input_file
    force = args.force_overwrite
    translations = args.translation_file
    output_file = args.output_file
    limit = args.limit

    # Check file existence
    assert os.path.exists(input_file), "Input file {} does not exists".format(input_file)
    assert translations is None or os.path.exists(translations), "Translation file {} does not exists".format(translations)
    if os.path.exists(output_file):
        assert force, "{} does already exists. Use -f option to overwrite it".format(output_file)
        os.remove(output_file)

    # Import data
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        input_data = list(csv_reader)

    with open(translations) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        translations_dict = { int(row[0]): row[1].strip() for row in csv_reader}

    missed = {0: 0, 1: 1}

    with open(output_file, "w") as fo:
        csv_writer = csv.writer(fo, delimiter=',') 
        for _id, qid1, qid2, question1, question2, is_duplicate in input_data:
            try:
                csv_writer.writerow(
                    [qid1, qid2, translations_dict[int(qid1)], translations_dict[int(qid2)], is_duplicate]
                )
            except KeyError:
                missed[int(is_duplicate)] += 1

    print(f"Done! {missed} questions didn't have a traduction.")

    