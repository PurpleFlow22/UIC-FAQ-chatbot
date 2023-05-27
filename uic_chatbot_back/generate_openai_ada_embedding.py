import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding
import timeit
import faiss
import os


def get_gpt_response(query, model, topk, corpus_q, corpus_a):
    query_embedding = np.asarray(get_embedding(query, engine=model), dtype=np.float32)
    query_embedding = np.reshape(query_embedding, (1, query_embedding.shape[0]))  # numpy.ndarray, [1, 1536]
    index = faiss.read_index('dataset/faiss_gpt.index')
    faiss.normalize_L2(query_embedding)
    D, I = index.search(query_embedding, topk)
    score_list = list(round(d, 3) for d in D[0])
    orig_q_list = list(corpus_q[i] for i in I[0])
    ans_list = list(corpus_a[i] for i in I[0])
    topk_result = list(zip(score_list, orig_q_list, ans_list))
    return topk_result


def write_faiss_index_gpt(corpus, model):
    if not os.path.exists('dataset/text_embedding_ada_002.npy'):
        print("Encoding the corpus. This might take a while")
        corpus_embeddings = generate_gpt_embeddings(corpus, model).astype('float32')  # numpy.ndarray, [508, 1536]
        print("Storing file on disc")
        np.save('dataset/text_embedding_ada_002.npy', corpus_embeddings)  # (508, 1536) in dimension
    else:
        print("Loading pre-computed embeddings from disc")
        corpus_embeddings = np.load('dataset/text_embedding_ada_002.npy').astype('float32')
    index = faiss.index_factory(1536, "Flat", faiss.METRIC_INNER_PRODUCT)
    faiss.normalize_L2(corpus_embeddings)
    index.add(corpus_embeddings)
    faiss.write_index(index, 'dataset/faiss_gpt.index')
    return 0


def generate_gpt_embeddings(corpus, model):
    corpus_embedding = []
    for q in corpus:
        embedding = get_embedding(q, engine=model)
        corpus_embedding.append(embedding)
    corpus_embedding = np.asarray(corpus_embedding)
    return corpus_embedding


if __name__ == '__main__':
    openai.api_key = "YourKeyHere"
    assert openai.api_key is not None, "Your OpenAI API key is not set!"

    data_path = "./dataset/CN_QA_dataset_all.xlsx"
    qa_data = pd.read_excel(data_path)
    q_list = list(qa_data['问题'].values)  # Total 508 unique standard questions

    # embedding model parameters
    embedding_model = "text-embedding-ada-002"
    embedding_encoding = "cl100k_base"  # the tokenizer for text-embedding-ada-002
    max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

    # generate gpt embeddings for all 508 standard questions and save as faiss index
    print('Generating GPT embedding index for standard questions...\n')
    start_time = timeit.default_timer()
    write_faiss_index_gpt(q_list, embedding_model)
    print('...Result saved. Time consumed: --- %s seconds ---' % (timeit.default_timer() - start_time))



