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
			if (i not in t_collec):# and (i.isalpha()):       ########## only changed this!!!
				t_collec.append(i)

		t_collec=sorted(t_collec)
		# ##################### hardcoding the t_collec, removing all numeric characters by hard-coding #####################
		# new_lst=t_collec.copy()
		# tnew_lst=new_lst[799:]
		# tnew_lst[0] = "x-15"
		# tnew_lst[1] = "15.4"
		# t_collec = tnew_lst.copy()
		# ###################################################################
		tfidf={}

		for i in t_collec:
			tf=np.zeros(len(docIDs))		## tf of term i in every doc.
			cnt=0
			c = 0
			for j in docIDs:
				tf[cnt]=docIDs_dict[j][1].count(i)
				if tf[cnt] != 0:
					c+=1
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
			doc_vecs.append(np.array(dummy)) #appending a list of TFIDF values, for a particular document - a document vector

		for i in range(len(docIDs)):
			docIDs_dict[docIDs[i]].append(doc_vecs[i])

		lsa_doc_vecs=self.lsa_compute(doc_vecs)
		lsa_doc_vecs_list=[]
		for i in range(len(lsa_doc_vecs)):
			lsa_doc_vecs_list.append(lsa_doc_vecs[i])

		
		doc_vecs = lsa_doc_vecs_list.copy()
		

		index = [t_collec, t_dict, docIDs_dict, docIDs, doc_vecs]
		self.index = index
		# 
		# 
		# print(doc_vecs)
		# print("----------------------------------------------")
		# print(lsa_doc_vecs_list)
		# print("----------------------------------------------")
		# print(t_collec)

		

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
		                                # lsa_doc_vecs_list = self.index[5]
		doc_vecs = self.index[4]       #changing this to 5, originally it is 4
		docIDs=self.index[3]
		docIDs_dict = self.index[2]
		t_dict  =self.index[1]
		t_collec=self.index[0]		## All terms in the entire corpus. this also forms the vector space basis (ORDER).

		q_tot=len(queries)

		q_collec=[]  # q_collec is list of tokenised queries [ ["collection", "of", "query_1" , "words"], ["collection", "of", "query_2" , "words"], ... ]
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
			for i in t_collec: # cnt_qvec is incremented for every iter of this loop, (~i)
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
		# 
		# 
		


	def lsa_compute(self,doc_vecs):
		# eigenvals, eigenvecs = np.linalg.eig(S)

		# doc_vecs						# list of document vectors, in the order of doc_IDs
		doc_v_term_array=np.zeros([len(doc_vecs),len(doc_vecs[0])])

		for i in range(len(doc_vecs)):
			for j in range(len(doc_vecs[0])):
				doc_v_term_array[i][j]=doc_vecs[i][j]

		self.U, self.S, self.Vt = svd(doc_v_term_array.T) ## doc_v_term_array is doc vs term matrix.

		print_list=[np.shape(self.U),np.shape(self.S),np.shape(self.Vt)]
		# print(print_list)

		#################
		k=301

		A = np.matmul(self.U[:,0:k], np.diag(self.S[0:k]))
		A = np.matmul(A, self.Vt[0:k,:])
		# print(np.shape(A))
		# for i in range(len(self.S)):
		# 	print(self.S[i])
		return A.T

		# sourceFile = open('demo_print.txt', 'w')
		# print(self.S, file = sourceFile)
		# sourceFile.close()

	def edit_distance(self, str1):

		t_collec=self.index[0]
		# t_collec = list(t_collec)
		results = np.zeros(len(t_collec))
		len1 = len(str1)

		if str1 in t_collec:
			return str1 
		else:
			cnt=0
			for str2 in t_collec:
				len2 = len(str2)
				DP = [[0 for i in range(len1 + 1)] for j in range(2)]

				for i in range(0, len1 + 1):
					DP[0][i] = i

				for i in range(1, len2 + 1):
					for j in range(0, len1 + 1):
						if (j == 0):
							DP[i % 2][j] = i

						elif(str1[j - 1] == str2[i-1]):
							DP[i % 2][j] = DP[(i - 1) % 2][j - 1]

						else:
							DP[i % 2][j] = (1 + min(DP[(i - 1) % 2][j],
												min(DP[i % 2][j - 1],
											DP[(i - 1) % 2][j - 1])))
						
				results[cnt] = DP[len2 % 2][len1]
				cnt+=1
				
			return t_collec[np.argmin(results)]
		# print(sol)




'''
        Code used for BM25 model.
		docs_df = pd.read_json('cranfield/cran_docs.json')
		# qrels = pd.read_json('cranfield/cran_qrels.json')
		# queries = pd.read_json('cranfield/cran_queries.json')
		docs_df = docs_df.drop(["bibliography", "author"], axis=1)

		doc_dict={}
		for line in docs_df.itertuples():
			doc_dict[line[2]] = line[1]

		nlp = spacy.load("en_core_web_sm")
		text_list = docs_df.body.str.lower().values
		tok_text=[] # for our tokenised corpus
		#Tokenising using SpaCy:
		for doc in tqdm(nlp.pipe(text_list, disable=["tagger", "parser","ner"])):
			tok = [t.text for t in doc if t.is_alpha]
			tok_text.append(tok)


		bm25 = BM25Okapi(tok_text)
		index =[bm25, doc_dict, docs_df]
		self.index = index


		ordered_docIDs=[]
		for q in queries:
			[bm25,doc_dict, docs_df] = self.index
			query = q
			tokenized_query = query.lower().split(" ")
			results = bm25.get_top_n(tokenized_query, docs_df.body.values, n=10000)
			temp_lst = []

			for i in results:
				temp_lst.append(doc_dict[i])
			ordered_docIDs.append(temp_lst)
		return ordered_docIDs #doc_IDs_ordered
'''





