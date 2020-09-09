"""
Given a set of clusters, generate a dataset with a specified number of true or false labels.
"""

import os
import argparse
import csv
import random
import math
import numpy as np
from torch.nn.functional import cosine_similarity
import torch

def generate(input_data, mapping, ratio=0.5, 
             max_number=None, hard_negative=None, translations=None, maximize_similarity=None):
    print("Starting generation")

    # use first id
    inverse_mapping = {value[0]: key for (key, value) in mapping.items()}
    # id -> question

    if translations is not None:
        print("Cleaning from questions without translation")
        tmp = []
        for split in input_data:
            tmp_split = []
            for cluster in split:
                tmp_cluster = []
                for qid in cluster:
                    all_ids = mapping[inverse_mapping[qid]]   
                    if any([x in translations for x in all_ids]):
                        tmp_cluster.append(qid)
                if len(tmp_cluster) > 0:
                    tmp_split.append(tmp_cluster)
            if len(tmp_split) > 0:
                tmp.append(tmp_split)
        input_data = tmp

    if max_number is None or len(max_number) == 0:
        max_number = [None] * len(input_data)

    res = [_generate(data, inverse_mapping, ratio=ratio, hard_negative=hard_negative,
                     max_number=max_n, maximize_similarity=maximize_similarity) for data, max_n in zip(input_data, max_number)]
    print("Generation done!")
    return res


def _generate(input_data, inverse_mapping, ratio=0.5,
              hard_negative=None, max_number=None, maximize_similarity=None, reverse=False):

    res = []

    ####################
    ### NORMAL CASE ####
    ####################
    if hard_negative is None:
        print("Starting extraction of positives and negatives")
        # adding positive candidates
        for cluster in input_data:
            if len(cluster) > 1:
                for i in range(len(cluster)):
                    for j in range(i+1, len(cluster)):
                        res.append([cluster[i], cluster[j], inverse_mapping[cluster[i]], inverse_mapping[cluster[j]], True])

        false_needed = int(len(res) / ratio)
        
        # adding negative candidates
        for i in range(false_needed):

            cluster1, cluster2 = random.sample(input_data, 2)
            qid1 = random.choice(cluster1)
            qid2 = random.choice(cluster2)
            res.append(
                [qid1, qid2, inverse_mapping[qid1], inverse_mapping[qid2], False]
            )
        random.shuffle(res)

        res = res[:min(max_number, len(res))] if max_number is not None else res

    #####################
    ### HARD NEGATIVE ###
    #####################
    else:
        # set containing all the questions from each cluster
        all_questions = set()
        for cluster in input_data:
            all_questions.update(cluster)

        if maximize_similarity is not None:
            from similarity import score
            print("Computing the score for each question")
            scores = {}
            for i, q in enumerate(all_questions):
                print("Elaborating question {}/{}".format(i, len(all_questions)), end='\r')
                scores[q] = score(inverse_mapping[q])
            print()

        print("Creating dataset")
        for c, cluster in enumerate(input_data):
            print("Elaborating cluster {}/{}".format(c, len(input_data)), end='\r')
            # if there is enough material in this cluster...
            if len(cluster) > 1:
                # create list of questions from all the other clusters given by all questions - actuals
                all_other_questions = all_questions.difference(cluster)

                # for each question with index i in cluster
                for i in range(len(cluster)):
                    # range before and after or only after i
                    second_range = list(range(i+1, len(cluster))) if not reverse else list(range(0, i)) + list(range(i+1, len(cluster)))
                    # for each other question with index j in cluster
                    for j in second_range:
                        # get actual questions
                        question_1, question_2 = cluster[i], cluster[j]

                        # add positive sample and create tmp list
                        tmp = [(question_1, question_2, inverse_mapping[question_1], inverse_mapping[question_2], True)]
                        
                        if maximize_similarity is not None and maximize_similarity >= hard_negative:
                            enemies = random.sample(all_other_questions, maximize_similarity)
                            # sorting indexes
                            
                            a = scores[question_1].unsqueeze(0).repeat(maximize_similarity, 1)
                            b = torch.stack([scores[x] for x in enemies], dim=0)

                            enemies_scores = cosine_similarity(a, b).detach().numpy()
                            # sort enemies based on scores

                            enemies = np.array(enemies)[np.argsort(enemies_scores)][(1 - hard_negative):]
                        else:
                            enemies = random.sample(all_other_questions, hard_negative - 1)

                        for e in enemies:
                            tmp.append(
                                [question_1, e, inverse_mapping[question_1], inverse_mapping[e], False]
                            )
                        res.append(tmp)
        
        random.shuffle(res)
        res = [item for sublist in res for item in sublist]
    
        # if specified N is bigger than available data, keep actual size
        if max_number is not None:
            if max_number % hard_negative != 0:
                max_number = math.ceil(max_number / hard_negative) * hard_negative 
            res = res[:min(max_number, len(res))] 
    
    return res
    
    
