import re
import textwrap
from math import log
from collections import Counter
import numpy as np

def load_document(file_path):
    documents = []
    with open(file_path, "r") as file:
        doc = []
        for lin in file:
            if lin.strip() == "":
                documents.append(" ".join(doc))
                doc = []
            else:
                doc.append(lin.strip().lower())
        if doc:
            documents.append(" ".join(doc))
    return documents

def load_keywords(file_path, delimitter):
    with open(file_path, "r") as file:
        keywords = file.read()
        keywords = keywords.split(delimitter)
        keywords = [keyword.strip() for keyword in keywords]
        keywords = [keyword.lower() for keyword in keywords]
    return keywords

def preprocess(doc):
    doc = doc.lower()
    doc = re.sub(r'[^\w\s]', '', doc)
    return doc



def compute_idfs(docs, keywords):
    idfs = {}
    N = len(docs)
    for keyword in keywords:
        df = sum(1 for doc in docs if keyword in doc)
        idf = log((N+1) / (df+1))+1
        idfs[keyword] = idf
    return idfs

def compute_tfs(docs, idfs):
    tfs = []
    for doc in docs:
        words = [d for d in doc.split() if d !=""]
        tf = Counter(words)
        tf = {word: tf[word] / len(words) * idfs.get(word, 0) for word in tf}
        tfs.append(tf)
    return tfs

def process_query(query, idfs):
    words = query.lower().split()
    tf = Counter(words)
    tf = {word: tf[word] / len(words) * idfs.get(word, 0) for word in tf}
    return tf



def compute_similarity(query_tf, doc_tfs):
    similarities = []
    for doc_tf in doc_tfs:
        dot_product = sum(query_tf.get(word, 0) * doc_tf.get(word, 0) for word in query_tf)
        query_norm = np.linalg.norm(list(query_tf.values()))
        doc_norm = np.linalg.norm(list(doc_tf.values()))
        similarity = dot_product / (query_norm * doc_norm)
        similarities.append(similarity)
    return similarities

documents = load_document("/content/drive/MyDrive/sem 9/IRL/documents.txt")
keywords = load_keywords("/content/drive/MyDrive/sem 9/IRL/keywords.txt", "\n")

documents = [preprocess(doc) for doc in documents]

idfs = compute_idfs(documents, keywords)
tfs = compute_tfs(documents, idfs)

def get_top_k(query, documents, doc_tfs, k):
    query = process_query(query, idfs)
    query_tf = compute_tfs(query, idfs)
    temp_tf = {}
    for q in query_tf:
        key, val = next(iter(q.items()))
        temp_tf[key] = val
    query_tf = temp_tf
    similarities = compute_similarity(query, doc_tfs)
    sorted_documents = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)
    return sorted_documents[:k]

query = "Sixteenth International Conference on Machine Learning"
results = get_top_k(query, documents, tfs, 5)

for i, item in enumerate(results):
    doc, score = item
    print(f"Rank: {i+1}\n")
    print('\n'.join(textwrap.wrap(doc, 50, break_long_words=False))+'.')
    print(f"\nScore: {score}")
    print("-"*50)
