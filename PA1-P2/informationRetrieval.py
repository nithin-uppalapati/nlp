from util import *

# Add your import statements here




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

		t_collec=[]
		t_dict={}
		docIDs_dict={}
		cnt=0
		# print(docs[147])
		for i in docs:
			temp=[]
			for m in i:
				j=[]
				for k in m:
					j.append(k.lower())
				temp.extend(j) #temp.extend(tempr)
			docIDs_dict.update({docIDs[cnt]:[i,temp]})
			t_collec.extend(temp)
			cnt+=1

		# t_collec is collection of all terms in the corpus.
		# t_collec=list(set(t_collec))		## All unique terms in the entire corpus. this also forms the vector space basis (ORDER).

		temp_t_collec = t_collec.copy()

		t_collec.clear()
		for i in temp_t_collec:
			if i not in t_collec:
				t_collec.append(i)

		t_collec=sorted(t_collec)
		tfidf={}

		for i in t_collec:
			tf=np.zeros(len(docIDs))		## tf of term i in every doc.
			cnt=0
			for j in docIDs:
				tf[cnt]=docIDs_dict[j][1].count(i)
				cnt+=1
			IDF=np.log10( len(docIDs) / np.count_nonzero(tf) )
			temp_vec=IDF*tf
			tfidf[i]=temp_vec				####added
			t_dict.update({i:[tf, IDF, temp_vec] }) # the ordering in "a*IDF" are according to docIDs order. each element corresponds to tf*IDF

		doc_vecs=[]
		for i in range(len(docIDs)): #docs[i] is a doc
			dummy=[]
			for j in range(len(t_collec)):
				dummy.append(t_dict[t_collec[j]][2][i])  #changed from docIDs[i]-1 to i
			doc_vecs.append(np.array(dummy)) #appending a list of TFIDF values

		for i in range(len(docIDs)):
			docIDs_dict[docIDs[i]].append(doc_vecs[i])

		index = [t_collec, t_dict, docIDs_dict, docIDs, doc_vecs]
		self.index = index


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

		doc_vecs = self.index[4]
		docIDs=self.index[3]
		docIDs_dict = self.index[2]
		t_dict  =self.index[1]
		t_collec=self.index[0]		## All terms in the entire corpus. this also forms the vector space basis (ORDER).

		q_tot=len(queries)

		q_collec=[]  # q_collec is list of tokenised queries [ ["collection", "of", "query_1" , "words"], [], ... ]
		qt_dict={}
		for i in range(q_tot): #queries
			temp=[]
			for j in queries[i]:
				temp.extend(j) #temp.extend(tempr)
			q_collec.append(temp)
			qt_dict.update({i:[temp]})
		
		q_vecs=[]
		for j in range(q_tot): #queries
			q_vec=np.zeros(len(t_collec)) ## Append q_vec to dict.
			cnt_qvec=0
			temp=[]
			for i in t_collec:
				q_vec[cnt_qvec]= (q_collec[j].count(i)) * t_dict[i][1]
				cnt_qvec+=1
				# temp.append( (q_collec[j].count(i)) * t_dict[i][1] )
			qt_dict[j].append(q_vec)
			q_vecs.append(q_vec)
		
		for i in range(q_tot): #queries
			# Capture the IDs of docs while calc the dot prods and ordering the dots should order the IDs...
			temp_res=np.zeros(len(docIDs))
			cnt=0
			for j in range(len(docIDs)):
				dot_prod=np.dot(q_vecs[i], doc_vecs[j] )# qt_dict[i][1] docIDs_dict[docIDs[j]][2])
				m1=np.linalg.norm(q_vecs[i],2) # qt_dict[i][1]
				m2=np.linalg.norm(doc_vecs[j],2) # docIDs_dict[docIDs[j]][2])
				dot_prod= dot_prod/m1
				if m2!=0:
					temp_res[cnt]=dot_prod/m2
				if m2==0:
					temp_res[cnt]=0

				cnt+=1
			order=temp_res.argsort()
			order=order[::-1]
			temp_lst=[]
			for k in order:
				temp_lst.append(docIDs[k])
			doc_IDs_ordered.append(temp_lst)
		# print(doc_IDs_ordered)
		return doc_IDs_ordered




