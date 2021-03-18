from util import *

# Add your import statements here




class Evaluation():


	def precision(self, doc_IDs_ordered, query_id, qrels, k):
		"""
		Computation of precision of the Information Retrieval System
		at at given value of k

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			A list of dictionaries containing document-relevance
			judgements - Refer cran_qrels.json for the structure of each
			dictionary

		Returns
		-------
		float
			The recall value as a number between 0 and 1
		"""

		precision = -1

		#Fill in code here

		return precision


	def recall(self, doc_IDs_ordered, query_id, qrels, k):
		"""
		Computation of recall of the Information Retrieval System
		at at given value of k

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			A list of dictionaries containing document-relevance
			judgements - Refer cran_qrels.json for the structure of each
			dictionary

		Returns
		-------
		float
			The recall value as a number between 0 and 1
		"""

		recall = -1

		#Fill in code here

		return recall


	def fscore(self, doc_IDs_ordered, query_id, qrels, k):
		"""
		Computation of f-score of the Information Retrieval System
		at a given value of k

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			A list of dictionaries containing document-relevance
			judgements - Refer cran_qrels.json for the structure of each
			dictionary

		Returns
		-------
		float
			The f-score value as a number between 0 and 1
		"""

		fscore = -1

		#Fill in code here

		return fscore


	def MAP(self, doc_IDs_ordered_all, query_ids, q_rels):
		"""
		Evaluation of the Information Retrieval System
		through Mean Average Precision

		Parameters
		----------
		arg1 : list
			A list of lists of integers where the ith sub-list is a list of IDs
			of documents in their predicted order of relevance to the ith query
		arg2 : list
			A list of IDs of the queries for which the documents are ordered
		arg3 : list
			A list of dictionaries containing document-relevance
			judgements - Refer cran_qrels.json for the structure of each
			dictionary

		Returns
		-------
		float
			The MAP value as a number between 0 and 1
		"""

		MAP = -1

		#Fill in code here

		return MAP


