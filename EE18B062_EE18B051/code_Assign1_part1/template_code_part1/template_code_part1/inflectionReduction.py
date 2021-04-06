from util import *

# Add your import statements here
from nltk.stem import PorterStemmer 

class InflectionReduction:

	def reduce(self, text):
		"""
		Stemming/Lemmatization

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of
			stemmed/lemmatized tokens representing a sentence
		"""

		reducedText = None

		#Fill in code here
		reducedText = []
		ps = PorterStemmer()
		for i in text:
			list1 = []
			for token in i:
				list1.append(ps.stem(token))
			reducedText.append(list1)
		return reducedText


