from util import *

# Add your import statements here

import numpy as np


class InformationRetrieval():

	def __init__(self):
		self.index = None

	def buildIndex(self, docs, docIDs):
		"""
		Builds the document index in terms of the document
		IDs and stores it in the 'index' class variable

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is
			a document and each sub-sub-list is a sentence of the document
		arg2 : list
			A list of integers denoting IDs of the documents
		Returns
		-------
		None
		"""

		index = None

		#Fill in code here
		index = {}
		for i in range(len(docs)): #docs[i] is a doc
			for j in range(len(docs[i])): #docs[i][j] is a sentence
				for k in range(len(docs[i][j])): #docs[i][j][k] is a word
					if docs[i][j][k] in index.keys():
						index[docs[i][j][k]][docIDs[i]-1] += 1
					else:
						index[docs[i][j][k]] = np.zeros(len(docs)) #numpy index 0 --> doc index 1
						index[docs[i][j][k]][docIDs[i]-1] += 1


		# file1 = open("myfile_checkpur.txt", "w")  # write mode
		# file1.write(str([len(index.keys()),list(index["original"]) ]) )
		# file1.close()

		# print(len(index.keys()))
		# # print(list(index["$"]))
		# doc_indx=999
		# print(docs[doc_indx])
		self.index = index
		self.docIDs = docIDs 
		# file1 = open("myfile_checkpur.txt", "w")  # write mode
		# file1.write(str([ docs[100] ]))
		# file1.close()

	def rank(self, queries):
		"""
		Rank the documents according to relevance for each query

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is a query and
			each sub-sub-list is a sentence of the query
		

		Returns
		-------
		list
			A list of lists of integers where the ith sub-list is a list of IDs
			of documents in their predicted order of relevance to the ith query
		"""

		doc_IDs_ordered = []

		#Fill in code here
		index = self.index
		docIDs = self.docIDs
		#IDF
		IDF = {}
		for word in index.keys():
			IDF[word] = np.log10(len(docIDs)/np.count_nonzero(index[word]))

		TFIDF = {}
		for word in index.keys():
			TFIDF[word] = index[word]*IDF[word]

		#print("TFIDF done...")

		wordlist = sorted(list(index.keys()))
		doc_vectors = []
		for i in range(len(docIDs)): #docs[i] is a doc
			dummy=[]
			for j in range(len(wordlist)):
				dummy.append(TFIDF[wordlist[j]][i]) #changed from docIDs[i]-1 to i
			doc_vectors.append(dummy) #appending a list of TFIDF values

		#print("doc vectors done...")
		q_listofvecs = []

		for query in queries:
			dummy = np.zeros(len(wordlist))
			for sent in query:
				for word1 in sent:
					if word1 in wordlist:
						dummy[wordlist.index(word1)] += 1*IDF[word1]
					else:
						#print(word1)
						pass
			q_listofvecs.append(dummy)

		#print("query_listofvecs done...")
		
		queries_sims = []
		for i in range(len(queries)): #queries[i] is one query
			dummy = []
			for j in range(len(docIDs)): #docs[i] is a doc
				if np.linalg.norm(doc_vectors[j]) == 0:
					cos_sim = 0
				else:
					cos_sim = np.dot(np.array(q_listofvecs[i]), np.array(doc_vectors[j]))/((np.linalg.norm(doc_vectors[j]))*(np.linalg.norm(q_listofvecs[i])))
				dummy.append((cos_sim,docIDs[j]))
			queries_sims.append(dummy)
		#print("cos sims done...")
		for i in range(len(queries_sims)):
			queries_sims[i].sort(key = lambda x: x[0])
			sorted_dummy = queries_sims[i]
			listofdocsorted = []
			for (cos_sim,doc_id) in sorted_dummy[::-1]:
				listofdocsorted.append(doc_id)
			doc_IDs_ordered.append(listofdocsorted)

		#print("END...")
		term_indx=3048
		doc_indx=999
		q_indx=166
		# print(wordlist)
		# print(wordlist[term_indx])
		# # print(list(index[wordlist[term_indx]][doc_indx]))
		# print(index[wordlist[term_indx]][doc_indx])
		# print(IDF[wordlist[term_indx]])
		# # print(list(TFIDF[wordlist[term_indx]][doc_indx]))
		# # print(list(doc_vectors[doc_indx][term_indx]))
		# print(TFIDF[wordlist[term_indx]][doc_indx])
		# print(doc_vectors[doc_indx][term_indx])

		# term_indx=3301
		# print(queries[q_indx])
		# print(q_listofvecs[q_indx][term_indx])
		# print(list(q_listofvecs[q_indx]))
		# # print(wordlist)
		# print(queries[q_indx])
		# print(list(q_listofvecs[q_indx]))
		print(doc_IDs_ordered)
		return doc_IDs_ordered




