from util import *

# Add your import statements here




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
		# print(query_doc_IDs_ordered)
		#Fill in code here
		cnt=0
		for i in range(k):
			if query_doc_IDs_ordered[i] in true_doc_IDs:
				cnt+=1

		precision = cnt/k			# intersec / retrieved
		# print(cnt)
		# print(k)

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
		
		q_rel_docs={} ## {qID : List of Rel Docs}
		for i in query_ids:
			q_rel_docs.update({i:[]})

		sum_pres=0
		for i in qrels:
			if int(i["query_num"]) in query_ids:
				# temp = i["query_num"] - 1
				q_rel_docs[ int(i["query_num"]) ].append( int(i["id"]) )
		
		cnt=0
		for i in query_ids:
			sum_pres = sum_pres + self.queryPrecision(doc_IDs_ordered[cnt], i-1, q_rel_docs[i], k)
			cnt+=1

		meanPrecision = sum_pres/len(query_ids)

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
		cnt=0
		for i in range(k):
			if query_doc_IDs_ordered[i] in true_doc_IDs:
				cnt+=1

		recall = cnt/len(true_doc_IDs)			# intersec / relevant

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

		q_rel_docs={} ## {qID : List of Rel Docs}
		for i in query_ids:
			q_rel_docs.update({i:[]})

		sum_rel=0
		for i in qrels:
			if int(i["query_num"]) in query_ids:
				# temp = i["query_num"] - 1
				q_rel_docs[ int(i["query_num"]) ].append( int(i["id"]) )
		
		cnt=0
		for i in query_ids:
			sum_rel = sum_rel + self.queryRecall(doc_IDs_ordered[cnt], i-1, q_rel_docs[i], k)
			cnt+=1

		meanRecall = sum_rel/len(query_ids)
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

		# #Fill in code here
		precision=self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs, k)
		recall	 =self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k)
		
		if precision==0:
			fscore = 0
		if recall==0:
			fscore = 0
		else:
			fscore = (1/precision) + (1/recall)
			fscore=2/fscore
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
		q_rel_docs={} ## {qID : List of Rel Docs}
		for i in query_ids:
			q_rel_docs.update({i:[]})

		sum_fsc=0
		for i in qrels:
			if int(i["query_num"]) in query_ids:
				# temp = i["query_num"] - 1
				q_rel_docs[ int(i["query_num"]) ].append( int(i["id"]) )
		
		cnt=0
		for i in query_ids:
			sum_fsc = sum_fsc + self.queryFscore(doc_IDs_ordered[cnt], i-1, q_rel_docs[i], k)
			cnt+=1

		meanFscore = sum_fsc/len(query_ids)

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
		arg3 : list of list
			The sub-list is [IDs, relevance] of documents relevant to the query (ground truth)
		arg4 : int
			The k value

		Returns
		-------
		float
			The nDCG value as a number between 0 and 1
		"""

		nDCG = -1

		#Fill in code here
		DCG=0
		iDCG=0
		relevance=[]

		for i in range(k):
			rel = 0
			for j in range(len(true_doc_IDs[0])):
				if query_doc_IDs_ordered[i] == true_doc_IDs[0][j]:
					DCG += true_doc_IDs[1][j]/np.log2(i+2)
					relevance.append(true_doc_IDs[1][j])
					rel+=1
			if rel==0:
				relevance.append(0)


		relevance.sort()
		relevance=relevance[::-1]

		for i in range(k):	
			iDCG=iDCG +  ( relevance[i] / np.log2(i+2) )
		
		if iDCG==0: nDCG=0
		else: nDCG = DCG/iDCG

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

		# #Fill in code here
		sumnDCG = 0
		q_rel_docs={} ## {qID : List of Rel Docs}
		for i in query_ids:
			q_rel_docs.update({i:[[],[]]})
		for i in qrels:
			if int(i["query_num"]) in query_ids:
				q_rel_docs[int(i["query_num"])][0].append( int(i["id"]) )
				q_rel_docs[int(i["query_num"])][1].append( i["position"] )

		for i in range(len(query_ids)):
			sumnDCG = sumnDCG + self.queryNDCG(doc_IDs_ordered[i], query_ids[i], q_rel_docs[query_ids[i]] , k)
		
		meanNDCG = sumnDCG / len(query_ids)

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

		rel_docs=0
		sum_apr=0
		for i in range(k):
			if query_doc_IDs_ordered[i] in true_doc_IDs:
				rel_docs+=1
				sum_apr+= rel_docs / (i+1)
		
		if rel_docs==0:	avgPrecision=0
		else: avgPrecision = sum_apr/rel_docs	# sum_precission / no. of retrieved

		return avgPrecision


	def meanAveragePrecision(self, doc_IDs_ordered, query_ids, qrels, k):
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

		q_rel_docs={} ## {qID : List of Rel Docs}
		for i in query_ids:
			q_rel_docs.update({i:[]})

		sum_map=0
		for i in qrels:
			if int(i["query_num"]) in query_ids:
				# temp = i["query_num"] - 1
				q_rel_docs[ int(i["query_num"]) ].append( int(i["id"]) )
		
		cnt=0
		for i in query_ids:
			sum_map = sum_map + self.queryAveragePrecision(doc_IDs_ordered[cnt], i-1, q_rel_docs[i], k)
			cnt+=1

		meanAveragePrecision = sum_map/len(query_ids)


		return meanAveragePrecision

