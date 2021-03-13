from util import *
# from nltk.corpus import stopwords
# Add your import statements here




class StopwordRemoval():

	def fromList(self, text):
		"""
		StopWord Removal from a sentence which is segmented from a text.

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence with stopwords removed
		"""
		stopwords = set(stopwords.words('english'))
		stopwordRemovedText = []

		#Fill in code here

		for i in text:
			if i not in stopwords:
				stopwordRemovedText.append(i)
			
			
		return stopwordRemovedText




	
