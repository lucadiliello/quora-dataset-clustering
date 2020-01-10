"""
Given a Quora dataset, cluster it, split it in different files (without overlapping questions)
and finally create training datasets.
"""

import os
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora-Question-Pairs dataset in clusters')
    parser.add_argument("-i", "--input_files_splits", required=True, nargs='+', type=str,
                        help="Splits to be verified being disjoint")

    args = parser.parse_args()

    # Inputs
    input_files = args.input_files_splits

    for f in input_files:
        assert os.path.isfile(f), "File {} does no exists".format(f)

    # Load data
    input_data = []
    for f in input_files:
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            #next(csv_reader, None)
            ids = set()
            questions = set()

            for row in csv_reader:
                ids.add(int(row[0]))
                ids.add(int(row[1]))
                questions.add(row[2].strip())
                questions.add(row[3].strip())

            input_data.append((f, ids, questions))

    # Checking intersections
    for i in range(len(input_data) - 1):
        for j in range(i + 1, len(input_data)):
            print("Files {} and {} have {} ids and {} questions in common".format(
                input_data[i][0],
                input_data[j][0],
                len(input_data[i][1].intersection(input_data[j][1])),
                len(input_data[i][2].intersection(input_data[j][2]))
            ))

    print("Done!")