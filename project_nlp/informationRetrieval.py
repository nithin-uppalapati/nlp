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
			doc_vecs.append(np.array(dummy)) #appending a list of TFIDF values

		for i in range(len(docIDs)):
			docIDs_dict[docIDs[i]].append(doc_vecs[i])

		lsa_doc_vecs=self.lsa_compute(doc_vecs)
		lsa_doc_vecs_list=[]
		for i in range(len(lsa_doc_vecs)):
			lsa_doc_vecs_list.append(lsa_doc_vecs[i])

		index = [t_collec, t_dict, docIDs_dict, docIDs, doc_vecs, lsa_doc_vecs_list]
		self.index = index
		# 
		# 
		# print(doc_vecs)
		# print("----------------------------------------------")
		# print(lsa_doc_vecs_list)
		# print("----------------------------------------------")
		print(t_collec)

		

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

		################# k=?
		k=200

		A = np.matmul(self.U[:,0:k], np.diag(self.S[0:k]))
		A = np.matmul(A, self.Vt[0:k,:])
		print(np.shape(A))
		return A.T

		# sourceFile = open('demo_print.txt', 'w')
		# print(self.S, file = sourceFile)
		# sourceFile.close()


	# A Space efficient Dynamic Programming
	# based Python3 program to find minimum
	# number operations to convert str1 to str2
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
				DP = [[0 for i in range(len1 + 1)]
						for j in range(2)];

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

Precision, Recall and F-score @ 1 : 0.6755555555555556, 0.11496590817841652, 0.18843213929047953
[[3, 1]]
MAP, nDCG @ 1 : 0.6755555555555556, 0.6755555555555556
Precision, Recall and F-score @ 2 : 0.5688888888888889, 0.18341297127194076, 0.26054129197675074
[[3, 1], [2, 2]]
MAP, nDCG @ 2 : 0.7288888888888889, 0.7120402953069217
Precision, Recall and F-score @ 3 : 0.49629629629629624, 0.2310348885970573, 0.29328531831774207
[[3, 1], [2, 2]]
MAP, nDCG @ 3 : 0.7333333333333333, 0.7133219039229007
Precision, Recall and F-score @ 4 : 0.43444444444444447, 0.2646124273877237, 0.3036436543765438
[[3, 1], [3, 4], [2, 2]]
MAP, nDCG @ 4 : 0.7244444444444444, 0.7066748254528757
Precision, Recall and F-score @ 5 : 0.39288888888888907, 0.2958096296170424, 0.3114343022609903
[[4, 5], [3, 1], [3, 4], [2, 2]]
MAP, nDCG @ 5 : 0.7139320987654321, 0.7054433222874519
Precision, Recall and F-score @ 6 : 0.3629629629629628, 0.322210611631152, 0.31480221494371247
[[4, 5], [3, 1], [3, 4], [3, 6], [2, 2]]
MAP, nDCG @ 6 : 0.7018395061728394, 0.700029848569553
Precision, Recall and F-score @ 7 : 0.3377777777777781, 0.3462125220663958, 0.3156536128122123
[[4, 5], [3, 1], [3, 4], [3, 6], [2, 2]]
MAP, nDCG @ 7 : 0.692953968253968, 0.6996919951711315
Precision, Recall and F-score @ 8 : 0.315, 0.3654682021161935, 0.312663384538961
[[4, 5], [3, 1], [3, 4], [3, 6], [2, 2]]
MAP, nDCG @ 8 : 0.6788688082640464, 0.6910442243289701
Precision, Recall and F-score @ 9 : 0.29827160493827193, 0.3893342175947173, 0.31214430920091985
[[4, 5], [3, 1], [3, 4], [3, 6], [2, 2], [1, 9]]
MAP, nDCG @ 9 : 0.6620049508692366, 0.6827356325517444
Precision, Recall and F-score @ 10 : 0.28044444444444455, 0.40177973666304334, 0.3055186784754231
[[4, 5], [3, 1], [3, 4], [3, 6], [2, 2], [1, 9]]
MAP, nDCG @ 10 : 0.6569899848828422, 0.6821936638765895

'''


'''
		TO DO
		1. remove commas and other shit in tokenization
		2. think of other inefficiencies in the system.
		3. Implement perfect LSA
		4. Optimize the hyperparameter - k in lsa
		5. how to remove backslash from text!?


'''