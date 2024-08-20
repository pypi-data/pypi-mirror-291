import math
from collections import defaultdict
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def load_keywords(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_documents(filename):
    documents = []
    current_doc = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                current_doc.append(line.strip())
            elif current_doc:
                documents.append(' '.join(current_doc))
                current_doc = []
    if current_doc:
        documents.append(' '.join(current_doc))
    return documents

class IRSystem:
    def __init__(self, documents, keywords):
        self.documents = documents
        self.keywords = set(keywords)
        self.doc_count = len(documents)
        self.inverted_index = defaultdict(list)
        self.idf = {}
        self.tf = defaultdict(dict)
        self.doc_vectors = {}
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

        self.preprocess()
        self.calculate_idf()
        self.calculate_tf()
        self.create_inverted_index()
        self.create_document_vectors()

    def preprocess(self):
        for i, doc in enumerate(self.documents):
            self.documents[i] = self.preprocess_text(doc)

    def preprocess_text(self, text):
        # Convert to lowercase, remove punctuation, and split
        words = re.findall(r'\w+', text.lower())
        # Remove stop words and stem
        words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]
        return words

    def calculate_idf(self):
        for term in self.keywords:
            stemmed_term = self.stemmer.stem(term)
            doc_freq = sum(1 for doc in self.documents if stemmed_term in doc)
            self.idf[stemmed_term] = math.log(self.doc_count / (1 + doc_freq))

    def calculate_tf(self):
        for i, doc in enumerate(self.documents):
            doc_length = len(doc)
            for term in set(doc):
                self.tf[i][term] = doc.count(term) / doc_length

    def create_inverted_index(self):
        for i, doc in enumerate(self.documents):
            for term in set(doc):
                if self.stemmer.stem(term) in self.keywords:
                    self.inverted_index[term].append(i)

    def create_document_vectors(self):
        for i in range(self.doc_count):
            self.doc_vectors[i] = {
                term: self.tf[i].get(term, 0) * self.idf.get(term, 0)
                for term in self.documents[i]
            }
            # Normalize the vector
            magnitude = math.sqrt(sum(score**2 for score in self.doc_vectors[i].values()))
            if magnitude > 0:
                self.doc_vectors[i] = {term: score/magnitude for term, score in self.doc_vectors[i].items()}

    def process_query(self, query):
        query_terms = self.preprocess_text(query)
        query_vector = {}
        for term in query_terms:
            if term in self.idf:
                tf = query_terms.count(term) / len(query_terms)
                query_vector[term] = tf * self.idf[term]
        # Normalize the query vector
        magnitude = math.sqrt(sum(score**2 for score in query_vector.values()))
        if magnitude > 0:
            query_vector = {term: score/magnitude for term, score in query_vector.items()}
        return query_vector

    def calculate_similarity(self, query_vector, doc_vector):
        return sum(query_vector.get(term, 0) * doc_vector.get(term, 0) for term in set(query_vector) | set(doc_vector))

    def search(self, query):
        query_vector = self.process_query(query)
        similarities = [(i, self.calculate_similarity(query_vector, doc_vector))
                        for i, doc_vector in self.doc_vectors.items()]
        return sorted(similarities, key=lambda x: x[1], reverse=True)

    def boolean_search(self, query):
        query_terms = self.preprocess_text(query)
        result = set(range(self.doc_count))
        for term in query_terms:
            if term in self.inverted_index:
                result = result.intersection(set(self.inverted_index[term]))
        return list(result)

    def explain(self, query, doc_id):
        query_vector = self.process_query(query)
        doc_vector = self.doc_vectors[doc_id]
        similarity = self.calculate_similarity(query_vector, doc_vector)

        explanation = f"Similarity between query and document {doc_id}: {similarity}\n\n"
        explanation += "Term-by-term breakdown:\n"

        for term in set(query_vector.keys()) | set(doc_vector.keys()):
            query_score = query_vector.get(term, 0)
            doc_score = doc_vector.get(term, 0)
            contribution = query_score * doc_score
            explanation += f"{term}: Query score = {query_score:.4f}, Doc score = {doc_score:.4f}, Contribution = {contribution:.4f}\n"

        return explanation

def evaluate(ir_system, queries, relevant_docs):
    results = {}
    total_ap = 0
    for query, relevant in zip(queries, relevant_docs):
        retrieved = ir_system.search(query)
        retrieved_docs = [doc[0] for doc in retrieved]

        precision = len(set(retrieved_docs[:10]) & set(relevant)) / 10
        recall = len(set(retrieved_docs) & set(relevant)) / len(relevant)
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # Calculate Average Precision
        ap = 0
        relevant_count = 0
        for i, doc in enumerate(retrieved_docs):
            if doc in relevant:
                relevant_count += 1
                ap += relevant_count / (i + 1)
        ap /= len(relevant) if relevant else 1
        total_ap += ap

        results[query] = {'precision@10': precision, 'recall': recall, 'f1': f1, 'ap': ap}

    # Calculate Mean Average Precision
    map_score = total_ap / len(queries)
    results['MAP'] = map_score

    return results

# Load keywords and documents
keywords = load_keywords('/content/keywords.txt')
documents = load_documents('/content/documents.txt')

# Create IR system
ir_system = IRSystem(documents, keywords)

print("Ranked search results:")
print(ir_system.search("machine learning"))

print("\nBoolean search results:")
print(ir_system.boolean_search("machine learning"))

print("\nExplanation:")
print(ir_system.explain("machine learning", 0))

queries = ["machine learning", "data mining"]
relevant_docs = [[0, 1, 2], [1, 3]]

print("\nEvaluation results:")
print(evaluate(ir_system, queries, relevant_docs))