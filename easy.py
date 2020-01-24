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
from generate import generate
from translate import translate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora-Question-Pairs dataset in clusters')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset (in CSV format)")
    parser.add_argument("-t", "--translation", required=False, default=None,
                        help="Translate output datasets in italian (requires do_generation)")
    parser.add_argument("-o", "--output_folder", required=True, type=str,
                        help="Output folder in which results will be saved (in CSV)")
   
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")

    parser.add_argument("-s", "--splits", required=True, nargs='+', type=int,
                        help="List of splits in which the clusters should be divided in a balanced way"
                        "E.g. 10 10 40 40")
    parser.add_argument("-n", "--max_number", required=False, nargs='*', type=int,
                        help="max number of entries for each split. Default is maximum, computed based on ratio")
    parser.add_argument("-u", "--min_cluster_size", required=False, default=1, type=int,
                        help="Consider only clusters with a size >= than argument")
    parser.add_argument("-m", "--max_cluster_size", required=False, default=1000, type=int,
                        help="Consider only clusters with a size <= than argument")
    parser.add_argument("--seed", required=False, default=999, type=int,
                    help="seed for shuffling")

    parser.add_argument("-r", "--ratio", required=False, default=0.5, type=float,
                        help="ratio between True and False pair")
    parser.add_argument("--hard_negative_dataset", required=False, default=None, type=int,
                        help="Build a hard negative dataset where each mini batch of size h has 1 positive label and h-1 negative ones")
    
    parser.add_argument("-g", "--do_generation", action="store_true",
                        help="Generate the datasets, otherwise only the splits of the clusters will be saved")

    args = parser.parse_args()

    # Inputs
    input_file = args.input_file
    force = args.force_overwrite
    output_folder = args.output_folder
    
    # Splits
    splits = args.splits
    min_cluster_size = args.min_cluster_size
    max_cluster_size = args.max_cluster_size

    # Generation
    ratio = args.ratio
    max_number = args.max_number
    do_generation = args.do_generation
    hard_negative = args.hard_negative_dataset

    # Translation
    translations = args.translation
    
    # Mapping
    random.seed(args.seed)

    # Check over arguments
    assert sum([int(x) for x in splits]) == 100, "Splits MUST sum to 100"
    assert translations is None or do_generation, "translation requires do_generation"
    assert not max_number or len(splits) == len(max_number), "You must provide the same number of splits and max_numbers"

    # Check file existence
    assert os.path.exists(input_file), "Input file {} does not exists".format(input_file)
    assert translations is None or os.path.exists(translations), "Translation file {} does not exists".format(translations)

    if os.path.exists(output_folder):
        assert force, "{} does already exists. Use -f option to overwrite it".format(output_folder)
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # Import data
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        input_data = list(csv_reader)
    
    if translations is not None:
        with open(translations) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            translations_dict = { int(row[0]): row[1].strip() for row in csv_reader}
    else:
        translations_dict = None

    # Clusterize
    clusters, mapping = cluster(input_data)
    """
    Clusters
    2342,2341,12
    ...

    Mapping
    "Yes baby": [13, 3423]
    ...
    """

    # Split
    res = split(clusters, min_cluster_size=min_cluster_size, max_cluster_size=max_cluster_size, splits=splits)
    """
    3123,3123
    23212,44
    ...

    1233,33
    980,99
    ...

    ...
    """

    # Generate
    if do_generation:
        res = generate(res, mapping, ratio=ratio, max_number=max_number, hard_negative=hard_negative,
                       translations=translations_dict if translations is not None else None)
        """
        3123,3123,"Am I italian?","Am I english?",False
        23212,44,"What did Giovannino say?","What did Massimino say?",False
        ...

        1233,33,"Is it a nice day?","It's sunny?",True
        980,99,"Do you have two credit cards?","Why do people ask on Quora when they can simply ask Google?",False
        ...
        """

        if translations is not None:
            translated = translate(res, translations_dict, mapping)

            """
            3123,3123,"Sono italiano?","Sono inglese?",False
            23212,44,"Cosa ha detto Giovannino?","Cosa ha detto Wender?",True
            ...

            1233,33,"È una bella giornata?","C'è il sole?",True
            980,99,"Lei ha due carte di credito?","Perchè la gente fa domande su Quora mentre potrebbe chiedere a Google?",False
            ...
            """
        
    for i, split in enumerate(splits):
        # writing originale eng questions
        with open(os.path.join(output_folder, "{}-{}-en.csv".format(i, split)), mode='w') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            for a in res[i]:
                writer.writerow(a)
        # if requested, write also translated versions of the questions
        if translations is not None:
            with open(os.path.join(output_folder, "{}-{}-it.csv".format(i, split)), mode='w') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                for a in translated[i]:
                    writer.writerow(a)

    print("Results written to {}, exiting!".format(output_folder))


    