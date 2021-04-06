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
				# tempr=j.strip('.')	## ASSUMPTION, SENTENCES DOES NOT END WITH PUNCTUATION MARKS AND DOES NOT CONTAIN ANY PUNCT MARKS
				# print(i)
				# tempr=j.lower() #tempr=tempr.lower()
				# tempr=tempr.split()
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

		for i in t_collec:
			tf=np.zeros(len(docIDs))		## tf of term i in every doc.
			cnt=0
			for j in docIDs:
				tf[cnt]=docIDs_dict[j][1].count(i)
				cnt+=1
			IDF=np.log10( len(docIDs) / len(np.where(tf!=0)[0]) )
			temp_vec=IDF*tf
			t_dict.update({i:[tf, IDF, temp_vec] }) # the ordering in "a*IDF" are according to docIDs order. each element corresponds to tf*IDF
			# For IDF find the no. of zeros in the a and then calc. log accordingly and multiply back to

		doc_vecs=np.zeros([len(docIDs),len(t_collec)])
		cnt_docs=0## goes from 0 to len(docIDs)
		for j in doc_vecs:
			cnt_t=0   ## goes from 0 to len(t_collec)
			for i in t_collec:
				j[cnt_t]=t_dict[i][2][cnt_docs]
				cnt_t+=1
			cnt_docs+=1

		cnt=0
		for i in docIDs:
			docIDs_dict[i].append(doc_vecs[cnt])
			cnt+=1

		index = [t_collec, t_dict, docIDs_dict, docIDs]
		############################################################
		############################################################
		#						Testing AREA
		print(len(t_collec))
		# print("total Docs = ", len(docIDs))
		# print("total terms = ", len(t_collec))
		# print("doc_vec[147] = ", docIDs_dict[471][2])
		# tttt=docIDs_dict[471][2]
		# # print(len(tttt))
		# # print(tttt.shape)
		# # print(tttt[0]==0)
		# # print(tttt[10]==0)
		# print("no. of 0's in above vec = ", len(np.where(tttt==0)[0]))
		
		# truth_lst=[]
		# for i in t_collec:
		# 	if i in docIDs_dict[471][1]:
		# 		truth_lst.append(1)
		# print(truth_lst)
		
		# print(docIDs_dict[471])
		# print(docs[470])
		# print("994", docs[994] )
		# # print(docIDs)
		# print(docIDs.index(471))
		
		# print("tf of terms in this doc:")
		############################################################
		############################################################

		self.index = index


		# IDEA:
		# no. of docs =n
		# create empty list of n lists
		# append them with bag of terms in resp. docs and count the frequency of terms.
		# also cal IDF of the terms.
		# Create a term doc matrix.
		# map the order to the IDs (list indices)
		# >>> d=[[]]*3
		# >>> d
		# [[], [], []]

		# Additional points:
		# 1.strip periods
		# 2.lowercase terms



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

		docIDs=self.index[3]
		q_tot=len(queries)

		q_collec=[]  # q_collec is list of tokenised queries [ ["collection", "of", "query_1" , "words"], [], ... ]
		qt_dict={}
		for i in range(q_tot): #queries
			temp=[]
			for j in queries[i]: #i   ### error is coming ass i is list, and lists cannot be key...
				# tempr=j.strip('.')
				# print(i)
				# tempr=tempr.lower()
				# tempr=tempr.split()
				temp.extend(j) #temp.extend(tempr)
			q_collec.append(temp)
			qt_dict.update({i:[temp]})
		
		docIDs_dict = self.index[2]
		t_dict  =self.index[1]
		t_collec=self.index[0]		## All terms in the entire corpus. this also forms the vector space basis (ORDER).

		# q_vecs_lst=[]
		# q_vec=np.zeros(len(t_collec)) ## Append q_vec to dict.

		for j in range(q_tot): #queries
			q_vec=np.zeros(len(t_collec)) ## Append q_vec to dict.
			cnt_qvec=0
			cnt_qcollec=0
			for i in t_collec:
				q_vec[cnt_qvec]= (q_collec[cnt_qcollec].count(i)) * t_dict[i][1]
				cnt_qvec+=1
			qt_dict[j].append(q_vec)
			cnt_qcollec+=1
		
		
		for i in range(q_tot): #queries
			# Capture the IDs of docs while calc the dot prods and ordering the dots should order the IDs...
			temp_res=np.zeros(len(docIDs))
			cnt=0
			for j in docIDs:
				dot_prod=np.dot(qt_dict[i][1], docIDs_dict[j][2])
				m1=np.linalg.norm(qt_dict[i][1],2)
				m2=np.linalg.norm(docIDs_dict[j][2],2)
				##############################
				dot_prod= dot_prod/m1
				# print(j)
				if m2!=0:
					temp_res[cnt]=dot_prod/m2
				if m2==0:
					temp_res[cnt]=0
				# if m2==0:
				# 	print(i,j)
					# print(docIDs_dict[j][2])
				##############################	
				cnt+=1
			order=temp_res.argsort()
			order=order[::-1]
			temp_lst=[]
			for k in order:
				temp_lst.append(docIDs[k])
			doc_IDs_ordered.append(temp_lst)
		# print(doc_IDs_ordered[0])
		# print(len(queries))

		# print(doc_IDs_ordered[8])
		# print(doc_IDs_ordered[0]==doc_IDs_ordered[8])
		return doc_IDs_ordered




