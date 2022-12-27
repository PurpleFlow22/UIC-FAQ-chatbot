# UIC-chatbot
A multi-language chatbot based on deep learning and natural language processing, the content is about the UIC admission question. The project is primarily based on a retrieval-based approach to question answering.

## File Description
### uic_chatbot_back
The file mainly cosist of the Back end of QA system, and it needs the model obtain from [hugging face](https://huggingface.co/models) which consist of: 

1. bert-base-chinese
2. roberta-chinese-base
3. sn-xlm-roberta-base
4. sbert-base-chinese
5. deberta-v3-base-qa

Besides, it also contains the fine-tuning model which can download by the following link:

1. [SBERT after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-finet-fyp/data)
2. [SRoBERTa after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-ro-fit-fyp/data)
3. [SDeBERTa after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-de-finet-fyp/data)

After you download the model, you can just run the main.py to run the back end. If you follow the instruction of uic_chatbot_front, you can deploy the project locally!

Beside, in the UIC-FAQ-chatbot/uic_chatbot_back/main.py, we apply the baidu translation api, you need to modify the appid and secret key to yours, or you can change to another translation api to use. 

The pure model example can be found by the following link, which is from the author [shadow-catt](https://github.com/shadow-catt).

https://github.com/shadow-catt/UIC_QA_Model/tree/main/back_end_alg

### fine-tune
This folder contain the our fine-tuning for the SBERT. We have fine-tuned the following three SBERT models, and the corresponding source files can be found on kaggle.

1. [sbert-base-chinese](https://huggingface.co/uer/sbert-base-chinese-nli)
2. [sn-xlm-roberta-base](https://huggingface.co/symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli)
3. [deberta-v3-base-qa](https://huggingface.co/jamescalam/deberta-v3-base-qa)

The fine-tuning kaggle file can be found by the following hyperlink:

1. [sbert-base-chinese](https://www.kaggle.com/shadowcattin/sentence-embedding-fyp)
2. [sn-xlm-roberta-base](https://www.kaggle.com/shadowcattin/sentence-embedding-roberta-fyp)
3. [deberta-v3-base-qa](https://www.kaggle.com/shadowcattin/sentence-embedding-deberta-fyp)

### evaluation
This folder mainly talk about how we evaluate the model. We totally evaluate the performance of the QA system by using the method of TF-IDF, BERT, SBERT separatly. 
The jupyter notebook are store in the evaluation folder, which includes 8 models. The source file can be found in the kaggle by using the hyperlink below.

1. [TF-IDF](https://www.kaggle.com/code/shadowcattin/ealuation-tfidf-fyp)
2. [BERT](https://www.kaggle.com/code/shadowcattin/ealuation-bert-emb-fyp)
3. [RoBERTa](https://www.kaggle.com/code/shadowcattin/sentence-embedding-roberta-fyp)
4. [SBERT](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-base-fyp)
5. [SRoBERTa](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-ro-fit-fyp)
6. [SDeBERTa](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-deber-fyp)
7. [SBERT after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-finet-fyp)
8. [SRoBERTa after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-ro-fit-fyp)
9. [SDeBERTa after fine-tune](https://www.kaggle.com/code/shadowcattin/ealuation-sbert-de-finet-fyp)

### uic_chatbot_front
This is a front-end which achieve
  > UIC question-answer system
  > Multi-user-real time chat room
if you want to use it, you can follow the instruction below
1. Initialize npm, Express, bad-words, socket.io and any other package require to install.
2. run **npm run dev**
3. vist **localhost:3000** to sign in

This front end mainly has two page
 > sign in page
 > chat room page
If you want to ask the chatbot question, plase type the folling format to send in the caht room page
 > ** @Bot question**
