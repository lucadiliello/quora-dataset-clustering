"""
Given a dataset of question pairs, create a list of clusters such that
questions in the same cluster are labelled as duplicates (have the same meaning).
"""

import os
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora-Question-Pairs dataset in clusters')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset (in CSV format)")

    args = parser.parse_args()
    input_file = args.input_file

    if not os.path.exists(input_file):
        print("Input file {} does not exists".format(input_file))
        exit(1)

    questions = dict()

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        
        for i, row in enumerate(csv_reader):
            print("Elaborating line {}".format(i), end='\r')    
            
            # Extract data
            pair_id = int(row[0])
            qid_1 = int(row[1])
            qid_2 = int(row[2])
            question_1 = row[3]
            question_2 = row[4]
            is_duplicate = bool(int(row[5]))

            if question_1 in questions:
                questions[question_1].append(qid_1)
            else:
                questions[question_1] = [qid_1]

            if question_2 in questions:
                questions[question_2].append(qid_2)
            else:
                questions[question_2] = [qid_2]
    
    number_wit_more_than_one_id = 0
    for key, value in questions.items():
        if len(value) > 1:
            number_wit_more_than_one_id += 1
    
    print("Questions with more than 1 id: {}".format(number_wit_more_than_one_id))