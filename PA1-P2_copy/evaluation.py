from util import *

# Add your import statements here
import numpy as np



class Evaluation():

	def queryPrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
		"""
		Computation of precision of the Information Retrieval System
		at a given value of k for a single query

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance to a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			The list of IDs of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The precision value as a number between 0 and 1
		"""

		precision = -1

		#Fill in code here
		r = 0
		for ret_doc in query_doc_IDs_ordered[:k]:
			if ret_doc in true_doc_IDs:
				r += 1

		precision = r/k

		return precision


	def meanPrecision(self, doc_IDs_ordered, query_ids, qrels, k):
		"""
		Computation of precision of the Information Retrieval System
		at a given value of k, averaged over all the queries

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
		arg4 : int
			The k value

		Returns
		-------
		float
			The mean precision value as a number between 0 and 1
		"""

		meanPrecision = -1

		#Fill in code here

		i = 0
		p = 0
		for ith_sublist in doc_IDs_ordered: #ith_sublist --> ith_query
			true_doc_IDs = []
			for j in qrels:
				if j["query_num"]==str(query_ids[i]):
					true_doc_IDs.append(int(j["id"]))

			p += self.queryPrecision(ith_sublist, query_ids[i], true_doc_IDs, k)
			'''
			QUESTION 16: '''
			if i == 8 and k ==10:
				print("query 9:")
				print("**********TRUE DOCS*************")
				print(true_doc_IDs)
				print("**********Predicted DOCS*************")
				print(ith_sublist)
			if i == 18 and k ==10:
				print("query 19:")
				print("**********TRUE DOCS*************")
				print(true_doc_IDs)
				print("**********Predicted DOCS*************")
				print(ith_sublist)
			pres = self.queryPrecision(ith_sublist, query_ids[i], true_doc_IDs, k)
			p += pres
			if pres==0 and k!=1 and k!=2:
				print("PRECISION ZERO")
				print(f"doc id = {query_ids[i]} for k = {k}")
			i+=1
		
		meanPrecision = p/len(doc_IDs_ordered)
		
		return meanPrecision

	
	def queryRecall(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
		"""
		Computation of recall of the Information Retrieval System
		at a given value of k for a single query

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance to a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			The list of IDs of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The recall value as a number between 0 and 1
		"""

		recall = -1
		

		#Fill in code here

		
		r = 0
		for ret_doc in query_doc_IDs_ordered[:k]:
			if ret_doc in true_doc_IDs:
				r += 1

		recall = r/len(true_doc_IDs)
		return recall


	def meanRecall(self, doc_IDs_ordered, query_ids, qrels, k):
		"""
		Computation of recall of the Information Retrieval System
		at a given value of k, averaged over all the queries

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
		arg4 : int
			The k value

		Returns
		-------
		float
			The mean recall value as a number between 0 and 1
		"""

		meanRecall = -1

		#Fill in code here
		i = 0
		rcl = 0
		for ith_sublist in doc_IDs_ordered:
			true_doc_IDs = []
			for j in qrels:
				if j["query_num"]==str(query_ids[i]):
					true_doc_IDs.append(int(j["id"]))
			rcl += self.queryRecall(ith_sublist, query_ids[i], true_doc_IDs, k)
			i+=1
		
		meanRecall = rcl/len(doc_IDs_ordered)

		return meanRecall


	def queryFscore(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
		"""
		Computation of fscore of the Information Retrieval System
		at a given value of k for a single query

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance to a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			The list of IDs of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The fscore value as a number between 0 and 1
		"""

		fscore = -1

		#Fill in code here
		pr = 2*(self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs, k))*(self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k))
		p_plus_r = (self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs, k))+(self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k))
		
		if p_plus_r==0:
			fscore = 0
		else:
			fscore = pr/p_plus_r
		
		return fscore


	def meanFscore(self, doc_IDs_ordered, query_ids, qrels, k):
		"""
		Computation of fscore of the Information Retrieval System
		at a given value of k, averaged over all the queries

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
		arg4 : int
			The k value
		
		Returns
		-------
		float
			The mean fscore value as a number between 0 and 1
		"""

		meanFscore = -1

		#Fill in code here
		i = 0
		f = 0
		for ith_sublist in doc_IDs_ordered:
			true_doc_IDs = []
			for j in qrels:
				if j["query_num"]==str(query_ids[i]):
					true_doc_IDs.append(int(j["id"]))
			f += self.queryFscore(ith_sublist, query_ids[i], true_doc_IDs, k)
			i+=1
		
		meanFscore = f/len(doc_IDs_ordered)

		return meanFscore
	

	def queryNDCG(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
		"""
		Computation of nDCG of the Information Retrieval System
		at given value of k for a single query

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance to a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			The list of IDs of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The nDCG value as a number between 0 and 1
		"""

		nDCG = -1

		#Fill in code here
		DCG = 0
		ideal_order = []
		for i in range(1,k+1):
			temp = 0
			for td in true_doc_IDs:
				if query_doc_IDs_ordered[i-1] == td[0]:
					DCG += td[1]/np.log2(i+1)
					ideal_order.append(td[1])
					temp+=1
			if temp==0:
				ideal_order.append(0)


		
		#for td in true_doc_IDs:
		#	ideal_order.append(td[1])
		#for tup in query_doc_IDs_ordered[:k]:
		#	ideal_order.append(tup[1])

		ideal_order.sort(reverse = True)
		idcg = 0
		for i in range(len(ideal_order[:k])):
			idcg += ideal_order[i]/np.log2(i+2)

		if idcg==0:
			nDCG = 0
		else:
			nDCG = DCG/idcg

		return nDCG


	def meanNDCG(self, doc_IDs_ordered, query_ids, qrels, k):
		"""
		Computation of nDCG of the Information Retrieval System
		at a given value of k, averaged over all the queries

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
		arg4 : int
			The k value

		Returns
		-------
		float
			The mean nDCG value as a number between 0 and 1
		"""

		meanNDCG = -1

		#Fill in code here
		i = 0
		ndcg = 0
		for ith_sublist in doc_IDs_ordered:
			true_doc_IDs = []
			for j in qrels:
				if j["query_num"]==str(query_ids[i]):
					true_doc_IDs.append( ( int(j["id"]) , j["position"] ) )
			ndcg += self.queryNDCG(ith_sublist, query_ids[i], true_doc_IDs, k)
			i+=1
		
		meanNDCG = ndcg/len(doc_IDs_ordered)

		return meanNDCG


	def queryAveragePrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
		"""
		Computation of average precision of the Information Retrieval System
		at a given value of k for a single query (the average of precision@i
		values for i such that the ith document is truly relevant)

		Parameters
		----------
		arg1 : list
			A list of integers denoting the IDs of documents in
			their predicted order of relevance to a query
		arg2 : int
			The ID of the query in question
		arg3 : list
			The list of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The average precision value as a number between 0 and 1
		"""

		avgPrecision = -1

		#Fill in code here
		ap = 0
		r = 0 #no. of relevant docs till n
		#p_at_n = 0
		for n in range(k):
			
			if (query_doc_IDs_ordered[:k][n]) in true_doc_IDs:
				r += 1
				ap += r/(n+1)
				#p_at_n += self.queryPrecision(query_doc_IDs_ordered,query_id,true_doc_IDs,n)

		if r==0:
			avgPrecision = 0
		else:
			avgPrecision = ap/r  ###SHLD BE DIVIDED BY RRRRR
			#p_at_n/r #

		return avgPrecision


	def meanAveragePrecision(self, doc_IDs_ordered, query_ids, q_rels, k):
		"""
		Computation of MAP of the Information Retrieval System
		at given value of k, averaged over all the queries

		Parameters
		----------
		arg1 : list
			A list of lists of integers where the ith sub-list is a list of IDs
			of documents in their predicted order of relevance to the ith query
		arg2 : list
			A list of IDs of the queries
		arg3 : list
			A list of dictionaries containing document-relevance
			judgements - Refer cran_qrels.json for the structure of each
			dictionary
		arg4 : int
			The k value

		Returns
		-------
		float
			The MAP value as a number between 0 and 1
		"""

		meanAveragePrecision = -1

		#Fill in code here
		i = 0
		ap = 0
		for ith_sublist in doc_IDs_ordered:
			true_doc_IDs = []
			for j in q_rels:
				if j["query_num"]==str(query_ids[i]):
					true_doc_IDs.append(int(j["id"]))
			ap += self.queryAveragePrecision(ith_sublist, query_ids[i], true_doc_IDs, k)
			i+=1
		
		meanAveragePrecision= ap/len(doc_IDs_ordered)

		return meanAveragePrecision

