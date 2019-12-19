"""
Given a set of clusters, generate a dataset with a specified number of true or false labels.
"""


import os
import argparse
import csv
from random import shuffle, randint, sample, choice

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Join a set of clusters with the correspoding questions')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Split file containing clusters in CSV format")
    parser.add_argument("-m", "--question_mapping", required=True, type=str,
                        help="id-question pairs file (saved as CSV)")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output file name (saved as CSV)")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="output_file and question_mapping are overwritten if they do already exists")
    parser.add_argument("-r", "--ratio", required=False, default=0.5, type=float,
                        help="ratio between True and False pairr")
    parser.add_argument("-n", "--number", required=False, default=None, type=int,
                        help="output_file and question_mapping are overwritten if they do already exists")

    args = parser.parse_args()

    input_file = args.input_file
    mapping = args.question_mapping
    output_file = args.output_file
    force = args.force_overwrite
    ratio = args.ratio
    number = args.number

    if not os.path.exists(input_file):
        print("Input file {} does not exists".format(input_file))
        exit(1)

    if os.path.exists(output_file):
        if force:
            os.remove(output_file)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_file))
            exit(1)
    
    # Read id-question mapping
    questions = dict()
    with open(mapping) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            if len(row) > 0:
                questions[int(row[0])] = row[1].strip()

    # Read cluster list
    clusters = []
    with open(input_file) as f:
        for line in f:
            clusters.append(
                [int(l.strip()) for l in line.strip().split(',')]
            )
        
    final = []
    # adding positive candidates
    for cluster in clusters:
        if len(cluster) > 1:
            for i in range(len(cluster)):
                for j in range(i+1, len(cluster)):
                    final.append(
                        [cluster[i], cluster[j], questions[cluster[i]], questions[cluster[j]], True]
                    )

    false_needed = int(len(final) / ratio)
    # adding negative candidates
    for i in range(false_needed):

        cluster1, cluster2 = sample(clusters, 2)
        qid1 = choice(cluster1)
        qid2 = choice(cluster2)
        final.append(
            [qid1, qid2, questions[qid1], questions[qid2], False]
        )

    shuffle(final)
    # if specified N is bigger than available data, keep actual size
    final = final[:min(number, len(final))]    

    with open(output_file, mode='w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        for c in final:
            writer.writerow(c)

    print("Done!")

    
