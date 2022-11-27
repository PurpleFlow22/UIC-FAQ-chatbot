# UIC-chatbot
A multi-language chatbot based on deep learning and natural language processing.

## notice
### back end algorithm
The file back_end_alg needs the model obtain from [hugging face](https://huggingface.co/models) which consist of:

1. bert-base-chinese
2. roberta-chinese-base
3. sn-xlm-roberta-base
4. sbert-base-chinese
5. deberta-v3-base-qa

### Fine-tuning for the SBERT
We have fine-tuned the following three SBERT models, and the corresponding source files can be found on kaggle.

1. [sbert-base-chinese](https://huggingface.co/uer/sbert-base-chinese-nli)
2. [sn-xlm-roberta-base](https://huggingface.co/symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli)
3. [deberta-v3-base-qa](https://huggingface.co/jamescalam/deberta-v3-base-qa)

The fine-tuning kaggle file can be found by the following hyperlink:

1. [sbert-base-chinese](https://www.kaggle.com/shadowcattin/sentence-embedding-fyp)
2. [sn-xlm-roberta-base](https://www.kaggle.com/shadowcattin/sentence-embedding-roberta-fyp)
3. [deberta-v3-base-qa](https://www.kaggle.com/shadowcattin/sentence-embedding-deberta-fyp)

### Evaluation
We totally evaluate the performance of the QA system by using the method of TF-IDF, BERT, SBERT separatly. 
The jupyter notebook are store in the path evaluation, which includes 8 models.
