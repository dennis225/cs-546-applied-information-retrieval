class Clustering:
    def __init__(self, linkage, threshold, doc_vectors):
        """
        This class defines an interface for Agglomerative Clustering
        which can be easily extended for other types of clustering
        str linkage: The type of linkage to be used for clustering
        float threshold: The threshold to check to assign a cluster to a doc
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def add_doc_to_cluster(self, doc_id):
        """
        Assigns a cluster to a document
        If a cluster doesn't fit, a new cluster is created for the doc
        int doc_id: The ID of the document to assign a cluster to
        """

    def get_clusters(self):
        """
        Returns all the clusters for a given threshold and linkage
        """

class Cluster:
    def __init__(self, linkage):
        """
        This class defines methods for various types of cost calculation
        for clustering the documents in the dataset
        str linkage: The type of linkage to be used for clustering
        """
    
    def add_doc_id(self, doc_id, doc_vectors):
        """
        Adds the given doc ID to the cluster
        Also adds the doc vector the cluster's doc vectors list
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def get_doc_ids(self):
        """
        Returns all the doc IDs in the cluster
        """
    
    def get_doc_vectors(self):
        """
        Returns all the doc vectors in the cluster
        """
    
    def calculate_similarity(self, doc_id, doc_vectors):
        """
        Calculates the similarity between two document vectors and
        returns the similarity value based on the given linkage type
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def min_linkage_similarity(self, doc_id, doc_vectors):
        """
        Uses the minimum linkage strategy for calculating similarity
        of the given doc vector to the doc vectors in the cluster
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def max_linkage_similarity(self, doc_id, doc_vectors):
        """
        Uses the maximum linkage strategy for calculating similarity
        of the given doc vector to the doc vectors in the cluster
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def avg_linkage_similarity(self, doc_id, doc_vectors):
        """
        Uses the average linkage strategy for calculating similarity
        of the given doc vector to the doc vectors in the cluster
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def mean_linkage_similarity(self, doc_id, doc_vectors):
        """
        Uses the mean linkage strategy for calculating similarity
        of the given doc vector to the doc vectors in the cluster
        int doc_id: The ID of the document to assign a cluster to
        hashmap doc_vectors: The document vectors in the dataset
        """
    
    def dot_product(self, doc_vector_1, doc_vector_2):
        """
        Returns the dot product of two document vectors given in
        normalized form as unit vectors
        hashmap doc_vector_1: First document vector
        hashmap doc_vector_2: Second document vector
        """
    
    def normalize(self, doc_vector):
        """
        Returns a normalized form of the given doc vector as unit vector
        hashmap doc_vector: The document vector to normalize
        """
