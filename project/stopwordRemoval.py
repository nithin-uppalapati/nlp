from util import *
# from nltk.corpus import stopwords
# Add your import statements here


activate = 0            ### Change this to 1, if query expansion to be performed before lemmatization.
extent_of_expansion = 1 ### The extent to which expnasion of query should occur, it means the amount of extra words per token to be appended to the query, which are having same sense as that of query 

class StopwordRemoval():

	def fromList(self, text, t):
		"""
		StopWord Removal from a sentence which is segmented from a text.

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence,    [ ["word", "word"],  ["word", "word"], ["word", "word"]  ]

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence with stopwords removed
		"""
		stwords = set(stopwords.words('english'))
		stopwordRemovedText = []

		#Fill in code here

		for i in text:
			for j in stwords:
				while(i.count(j)):
					i.remove(j)
			stopwordRemovedText.append(i)
		final_stopwordRemovedText = stopwordRemovedText.copy()

		if ((activate) and (t)):
			new_lst = []
			for i in stopwordRemovedText: #[ ["A", "b"],  ["c", "d"], ["e", "f"]  ]
				temp=[]
				for j in i:
					temp.append(j)
					count=0
					for syn in wordnet.synsets(j):
						for l in syn.lemmas():
							if(count<extent_of_expansion):
								if l.name() not in temp:
									temp.append(l.name())
									count+=1
				new_lst.append(temp)
			final_stopwordRemovedText = new_lst.copy()


		return final_stopwordRemovedText




	
