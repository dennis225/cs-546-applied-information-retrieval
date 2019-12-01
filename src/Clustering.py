# Import built-in libraries
from collections import defaultdict

# Import third-party libraries
import numpy as np

class Clustering:
    def __init__(self, linkage, threshold, doc_vectors):
        self._linkage = linkage
        self._threshold = threshold
        self._clusters = []
        self._doc_vectors = doc_vectors
    
    def add_doc_to_cluster(self, doc_id):
        max_similarity = 0
        best_cluster = None

        for cluster in self._clusters:
            similarity = cluster.calculate_similarity(doc_id, self._doc_vectors)
            if similarity > self._threshold:
                if similarity > max_similarity:
                    best_cluster = cluster
        
        if not best_cluster:
            best_cluster = Cluster(self._linkage)
            self._clusters.append(best_cluster)
        
        best_cluster.add_doc_id(doc_id, self._doc_vectors)

    def get_clusters(self):
        return self._clusters

class Cluster:
    def __init__(self, linkage):
        self._linkage = linkage
        self._doc_ids = []
        self._doc_vectors_in_cluster = []
        self._centroid = defaultdict(float)
        self._term_occurrences = defaultdict(int)
    
    def add_doc_id(self, doc_id, doc_vectors):
        self._doc_ids.append(doc_id)
        doc_vector = doc_vectors[doc_id].get_doc_vector()
        self._doc_vectors_in_cluster.append(doc_vector)
        for term_id, term_value in doc_vector.items():
            self._centroid[term_id] += term_value
            self._term_occurrences[term_id] += 1
    
    def get_doc_ids(self):
        return self._doc_ids
    
    def get_doc_vectors(self):
        return self._doc_vectors_in_cluster
    
    def calculate_similarity(self, doc_id, doc_vectors):
        if self._linkage == 'min':
            return self.min_linkage_similarity(doc_id, doc_vectors)
        elif self._linkage == 'max':
            return self.max_linkage_similarity(doc_id, doc_vectors)
        elif self._linkage == 'avg':
            return self.avg_linkage_similarity(doc_id, doc_vectors)
        elif self._linkage == 'mean':
            return self.mean_linkage_similarity(doc_id, doc_vectors)
    
    def min_linkage_similarity(self, doc_id, doc_vectors):
        min_similarity = 1
        new_doc_vector = doc_vectors[doc_id].get_doc_vector()
        for doc_vector in self._doc_vectors_in_cluster:
            similarity = self.dot_product(new_doc_vector, doc_vector)
            min_similarity = min(min_similarity, similarity)
        return min_similarity
    
    def max_linkage_similarity(self, doc_id, doc_vectors):
        max_similarity = 0
        new_doc_vector = doc_vectors[doc_id].get_doc_vector()
        for doc_vector in self._doc_vectors_in_cluster:
            similarity = self.dot_product(new_doc_vector, doc_vector)
            max_similarity = max(max_similarity, similarity)
        return max_similarity
    
    def avg_linkage_similarity(self, doc_id, doc_vectors):
        avg_similarity = 0
        new_doc_vector = doc_vectors[doc_id].get_doc_vector()
        for doc_vector in self._doc_vectors_in_cluster:
            avg_similarity += self.dot_product(new_doc_vector, doc_vector)
            avg_similarity /= len(self._doc_vectors_in_cluster)
        return avg_similarity
    
    def mean_linkage_similarity(self, doc_id, doc_vectors):
        new_doc_vector = doc_vectors[doc_id].get_doc_vector()
        centroid = defaultdict(float)
        for term_id, term_value in self._centroid.items():
            num_occurrences = self._term_occurrences[term_id]
            centroid[term_id] = term_value / num_occurrences
        centroid = self.normalize(centroid)
        similarity = self.dot_product(new_doc_vector, centroid)
        return similarity
    
    def dot_product(self, doc_vector_1, doc_vector_2):
        similarity = 0
        for term_id, term_value in doc_vector_1.items():
            similarity += term_value * doc_vector_2[term_id]
        return similarity
    
    def normalize(self, doc_vector):
        numerator = np.array(list(doc_vector.values()))
        denominator = np.linalg.norm(numerator)
        normalized_doc_vector = defaultdict(float)
        for term_id, term_value in doc_vector.items():
            normalized_doc_vector[term_id] = term_value / denominator
        return normalized_doc_vector
