from transformers import BertTokenizer, BertModel
import torch
from torch.nn.functional import cosine_similarity

pre_trained_name = 'bert-base-multilingual-cased'

tokenizer = BertTokenizer.from_pretrained(pre_trained_name)
model_embeddings = BertModel.from_pretrained(pre_trained_name).embeddings

def score(question_1):

    question_1_ids = torch.tensor(tokenizer.encode(question_1), dtype=torch.long)
    embedding_question_1 = model_embeddings.word_embeddings(question_1_ids)
    embedding_question_1 = torch.sum(embedding_question_1, dim=0)

    return embedding_question_1

