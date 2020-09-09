"""
Given a Quora dataset, cluster it, split it in different files (without overlapping questions)
and finally create training datasets.
"""

import os
import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze Quora-Question-Pairs dataset and translations')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset (in CSV format)")
    parser.add_argument("-t", "--translation", required=True, type=str,
                        help="Translate output datasets in italian (requires do_generation)")
    parser.add_argument("-o", "--output_file", required=False, type=str)

    args = parser.parse_args()

    # Inputs
    input_file = args.input_file

    # Translation
    translations = args.translation

    # Check file existence
    assert os.path.exists(input_file), "Input file {} does not exists".format(input_file)
    assert os.path.exists(translations), "Translation file {} does not exists".format(translations)

    # Import data
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        input_data = list(csv_reader)

    with open(translations) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        translations_dict = { int(row[0]): row[1].strip() for row in csv_reader}

    map_ids_to_questions = dict()
    map_questions_to_ids = dict()
    true_labels, false_labels = 0, 0

    for row in input_data:
        id_1, id_2 = int(row[1]), int(row[2])
        q1, q2 = row[3].strip(), row[4].strip()

        # ID -> Question
        if id_1 in map_ids_to_questions:
            map_ids_to_questions[id_1].add(q1)
        else:
            map_ids_to_questions[id_1] = set([q1])

        if id_2 in map_ids_to_questions:
            map_ids_to_questions[id_2].add(q2)
        else:
            map_ids_to_questions[id_2] = set([q2])

        # Quesion -> ID
        if q1 in map_questions_to_ids:
            map_questions_to_ids[q1].add(id_1)
        else:
            map_questions_to_ids[q1] = set([id_1])

        if q2 in map_questions_to_ids:
            map_questions_to_ids[q2].add(id_2)
        else:
            map_questions_to_ids[q2] = set([id_2])

        label = int(row[5])
        if label > 0:
            true_labels += 1
        else:
            false_labels += 1

    #print(map_questions_to_ids["What is the step by step guide to invest in share market in india?"]); exit()

    """
    for question, ids in map_questions_to_ids.items():
        alternative_questions_sets = [map_ids_to_questions[_id] for _id in ids]

        alternative_questions = set()
        for x in alternative_questions_sets:
            alternative_questions.update(x)

        if len(alternative_questions) > 1:
            print(question, ids, alternative_questions)

    print(f"IDs used for more than 1 question {sum([len(v) > 1 for k, v in map_ids_to_questions.items()])}/{len(map_ids_to_questions)}")
    print(f"Questions with more than 1 id {sum([len(v) > 1 for k, v in map_questions_to_ids.items()])}/{len(map_questions_to_ids)}")

    missing = []
    question_to_transl = dict()
    for question, ids in map_questions_to_ids.items():
        for _id in ids:
            if _id in translations_dict:
                if question in question_to_transl:
                    question_to_transl[question].append(translations_dict[_id])
                    print(f"WARN: This question: '{question}' has more than 1 translation: {question_to_transl[question]}")
                else:
                    question_to_transl[question] = [translations_dict[_id]]

        if question not in question_to_transl:
            missing.append([ids.pop(), question])

    if args.output_file is not None:
        with open(args.output_file, "w") as fo:
            for line in missing:
                fo.write(f"{line[0]}\t{line[1]}" + "\n")

    print(f"True/False labels: {true_labels}/{false_labels}")
    print(f"Questions missing / not missing translation: {len(missing)}/{len(question_to_transl)}")
    """

    question, ids = None, None

    for q, i in map_questions_to_ids.items():
        res = set()
        for j in i:
            res.update(map_ids_to_questions[j])

        if len(res) > 1:
            question, ids = q, i
            break

    print("1", question, ids)
    questions_2 = [map_ids_to_questions[_id] for _id in ids]
    print("2", questions_2)

    