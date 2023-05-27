import openai
from generate_openai_ada_embedding import get_gpt_response
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from sentence_transformers import SentenceTransformer
from SBERT import read_and_split_the_excel, SBERT_get_reply
from BERT_embedding import Bert_em_prepared, Bert_em_reply
from tfidf import TF_IDF_prepared, TF_IDF_reply
from greeting import greet_start, greet_pre, greet_check, greet_none_reply
from translate import translate
import langid
import numpy as np
from statistics import mode

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

openai.api_key = "YourKeyHere"
assert openai.api_key is not None, "Your OpenAI API key is not set!"
gpt_model = "text-embedding-ada-002"

print("数据准备中")
data_path = "./dataset/CN_QA_dataset_all.xlsx"
model_Bert_path = './emb_bert/bert_base_chinese'
stopword_file_path = './dataset/cn_stopwords.txt'
model_SBert_path = 'SBert/SBert_CN_fine_tune'
model_RoBERTa_path = 'SBert/roberta_fine_tune'
model_DeBERTa_path = 'SBert/deberta_fine_tune'


""" preparation for SBERT """
topk_SBert = 3
threshold_SBert = 0.6
model_SBert = SentenceTransformer(model_SBert_path)
model_RoBERTa = SentenceTransformer(model_RoBERTa_path)
model_DeBERTa = SentenceTransformer(model_DeBERTa_path)
question_list_SBert, answer_list_SBert = read_and_split_the_excel(data_path)
question_embeddings_SBert = model_SBert.encode(question_list_SBert, convert_to_tensor=True)
question_embeddings_RoBERTa = model_RoBERTa.encode(question_list_SBert, convert_to_tensor=True)
question_embeddings_DeBERTa = model_DeBERTa.encode(question_list_SBert, convert_to_tensor=True)

""" preparation for BERT_emb """
# tokenizer_BERT, model_BERT, question_list_BERT, answer_list_BERT, doc_vecs_BERT = Bert_em_prepared(
#     data_path, model_Bert_path)
# topk_Bert = 5
# threshold_Bert = 0.95

""" preparation for TF-IDF """
topk_TFIDF = 3
threshold_TFIDF = 0.5
question_list, question_token_list, answer_list, stop_words, dictionary, \
tfidf, corpus_tfidf = TF_IDF_prepared(
    data_path, stopword_file_path)

appid = '20220713001272202'  # 填写你的appid
secretKey = 'v4x3PC6W6X9etHyXO5wu'  # 填写你的密钥


@app.route("/")
@app.route("/query-vsbert", methods=['POST', 'GET'])
def query_vsbert():
    try:
        data = json.loads(request.data.decode(encoding='utf8'))
        query = data.get('query', None)
        if query:
            lang = langid.classify(query)[0]
            if lang in ['zh', 'en', 'de']:
                if lang != 'zh':
                    query = translate(query, lang, 'zh', appid, secretKey)
                    sbert_result, sbert_if_valid = SBERT_get_reply(model_SBert, query, question_list_SBert,
                                                                   answer_list_SBert,
                                                                   question_embeddings_SBert, topk_SBert,
                                                                   threshold_SBert)
                    roberta_result, roberta_if_valid = SBERT_get_reply(model_RoBERTa, query, question_list_SBert,
                                                                       answer_list_SBert,
                                                                       question_embeddings_RoBERTa, topk_SBert,
                                                                       threshold_SBert)
                    deberta_result, deberta_if_valid = SBERT_get_reply(model_DeBERTa, query, question_list_SBert,
                                                                       answer_list_SBert,
                                                                       question_embeddings_DeBERTa, topk_SBert,
                                                                       threshold_SBert)
                    tfidf_result, tfidf_if_valid = TF_IDF_reply(query, question_list, answer_list, stop_words,
                                                                topk_TFIDF,
                                                                threshold_TFIDF, dictionary, tfidf, corpus_tfidf)
                    all_suggestions = np.array([tfidf_result, sbert_result, roberta_result, deberta_result])
                    all_if_valid = np.array([tfidf_if_valid, sbert_if_valid, roberta_if_valid, deberta_if_valid])
                    result = mode(all_suggestions)
                    result_index = np.where(all_suggestions == result)
                    if_valid = mode(all_if_valid[result_index])

                    result = translate(result, 'zh', lang, appid, secretKey)
                else:
                    sbert_result, sbert_if_valid = SBERT_get_reply(model_SBert, query, question_list_SBert, answer_list_SBert,
                                                             question_embeddings_SBert, topk_SBert, threshold_SBert)
                    roberta_result, roberta_if_valid = SBERT_get_reply(model_RoBERTa, query, question_list_SBert,
                                                               answer_list_SBert,
                                                               question_embeddings_RoBERTa, topk_SBert, threshold_SBert)
                    deberta_result, deberta_if_valid = SBERT_get_reply(model_DeBERTa, query, question_list_SBert,
                                                               answer_list_SBert,
                                                               question_embeddings_DeBERTa, topk_SBert, threshold_SBert)
                    tfidf_result, tfidf_if_valid = TF_IDF_reply(query, question_list, answer_list, stop_words, topk_TFIDF,
                                                    threshold_TFIDF, dictionary, tfidf, corpus_tfidf)
                    all_suggestions = np.array([tfidf_result, sbert_result, roberta_result, deberta_result])
                    all_if_valid = np.array([tfidf_if_valid, sbert_if_valid, roberta_if_valid, deberta_if_valid])
                    result = mode(all_suggestions)
                    result_index = np.where(all_suggestions == result)
                    if_valid = mode(all_if_valid[result_index])

                if if_valid:
                    greet = translate(greet_pre(), 'zh', lang, appid, secretKey)
                    return jsonify({"answer": greet + "\n" + result})
                else:
                    greet_none = translate(greet_none_reply(), 'zh', lang, appid, secretKey)
                    return jsonify({"answer": greet_none})
            else:
                not_support_ans = translate(
                    "抱歉，该语言暂时不支持哦~", 'zh', lang, appid, secretKey)
                return jsonify({"answer": not_support_ans})
        else:
            return jsonify({'answer': False, 'msg': '请输入您的问题哦！'}), 400
    except ValueError as ve:
        return jsonify({'status': False, 'msg': '输入参数格式不正确！'}), 400


@app.route("/query-sbert", methods=['POST', 'GET'])
def query_sbert():
    try:
        data = json.loads(request.data.decode(encoding='utf8'))
        query = data.get('query', None)
        if query:
            lang = langid.classify(query)[0]
            if lang in ['zh', 'en', 'de']:
                if lang != 'zh':
                    query = translate(query, lang, 'zh', appid, secretKey)
                    result, if_valid = SBERT_get_reply(model_SBert, query, question_list_SBert, answer_list_SBert,
                                                       question_embeddings_SBert, topk_SBert, threshold_SBert)
                    result = translate(result, 'zh', lang, appid, secretKey)
                else:
                    result, if_valid = SBERT_get_reply(model_SBert, query, question_list_SBert, answer_list_SBert,
                                                       question_embeddings_SBert, topk_SBert, threshold_SBert)

                if if_valid:
                    greet = translate(greet_pre(), 'zh', lang, appid, secretKey)
                    return jsonify({"answer": greet + "\n" + result})
                else:
                    greet_none = translate(greet_none_reply(), 'zh', lang, appid, secretKey)
                    return jsonify({"answer": greet_none})
            else:
                not_support_ans = translate(
                    "抱歉，该语言暂时不支持哦~", 'zh', lang, appid, secretKey)
                return jsonify({"answer": not_support_ans})
        else:
            return jsonify({'answer': False, 'msg': '请输入您的问题哦！'}), 400
    except ValueError as ve:
        return jsonify({'status': False, 'msg': '输入参数格式不正确！'}), 400


@app.route("/query-bert", methods=['POST', 'GET'])
def query_bert():
    try:
        data = json.loads(request.data.decode(encoding='utf8'))
        query = data.get('query', None)
        if query:
            lang = langid.classify(query)[0]
            if lang in ['zh', 'en', 'de']:
                if lang != 'zh':
                    query = translate(query, 'auto', 'zh', appid, secretKey)
                    result, if_valid = Bert_em_reply(query, tokenizer_BERT, model_BERT, question_list_BERT, answer_list_BERT, doc_vecs_BERT, topk_Bert, threshold_Bert)
                    result = translate(result, 'zh', lang, appid, secretKey)
                else:
                    result, if_valid = Bert_em_reply(query, tokenizer_BERT, model_BERT, question_list_BERT, answer_list_BERT, doc_vecs_BERT,
                        topk_Bert, threshold_Bert)
            else:
                not_support_ans = translate(
                    "抱歉，该语言暂时不支持哦~", 'zh', lang, appid, secretKey)
                return jsonify({"answer": not_support_ans})

            if if_valid:
                return jsonify({"answer": greet_pre() + result})
            else:
                return jsonify({"answer": greet_none_reply()})
        else:
            return jsonify({'status': False, 'msg': '请输入您的问题哦！'}), 400
    except ValueError as ve:
        return jsonify({'status': False, 'msg': '输入参格式不正确！'}), 400


@app.route("/query-tfidf", methods=['POST', 'GET'])
def query_tfidf():
    try:
        data = json.loads(request.data.decode(encoding='utf8'))
        query = data.get('query', None)
        if query:
            lang = langid.classify(query)[0]
            if lang in ['zh', 'en', 'de']:
                if lang != 'zh':
                    query = translate(query, 'auto', 'zh', appid, secretKey)
                    result, if_valid = TF_IDF_reply(query, question_list, answer_list, stop_words, topk_TFIDF,
                                                    threshold_TFIDF, dictionary, tfidf, corpus_tfidf)
                    result = translate(result, 'zh', lang, appid, secretKey)
                else:
                    result, if_valid = TF_IDF_reply(query, question_list, answer_list, stop_words, topk_TFIDF,
                                                    threshold_TFIDF, dictionary, tfidf, corpus_tfidf)
            else:
                not_support_ans = translate(
                    "抱歉，该语言暂时不支持哦~", 'zh', lang, appid, secretKey)
                return jsonify({"answer": not_support_ans})

            if if_valid:
                return jsonify({"answer": greet_pre() + result})
            else:
                return jsonify({"answer": greet_none_reply()})
        else:
            return jsonify({'status': False, 'msg': '请输入您的问题哦！'}), 400
    except ValueError as ve:
        return jsonify({'status': False, 'msg': '输入参格式不正确！'}), 400


@app.route("/query-gpt", methods=['POST', 'GET'])
def query_gpt():
    try:
        data = json.loads(request.data.decode(encoding='utf8'))
        query = data.get('query', None)

        if query:
            lang = langid.classify(query)[0]
            if lang in ['zh', 'en', 'de']:
                if lang != 'zh':
                    query = translate(query, 'auto', 'zh', appid, secretKey)
                    result = get_gpt_response(query, gpt_model, 1, question_list, answer_list)[0][2]
                    result = translate(result, 'zh', lang, appid, secretKey)
                else:
                    result = get_gpt_response(query, gpt_model, 1, question_list, answer_list)[0][2]
            else:
                not_support_ans = translate(
                    "抱歉，该语言暂时不支持哦~", 'zh', lang, appid, secretKey)
                return jsonify({"answer": not_support_ans})
            return jsonify({"answer": greet_pre() + result})
        else:
            return jsonify({'status': False, 'msg': '请输入您的问题哦！'}), 400
    except ValueError as ve:
        return jsonify({'status': False, 'msg': '输入参格式不正确！'}), 400


if __name__ == "__main__":
    app.run()
