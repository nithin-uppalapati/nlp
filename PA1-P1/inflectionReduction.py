from util import *
# from nltk.stem import PorterStemmer, WordNetLemmatizer
# Add your import statements here




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

		# reducedText = None

		#Fill in code here
		wrntl=WordNetLemmatizer()
		ps=PorterStemmer()

		temp=text.copy()
		for i in range(0,len(text)):
			for j in range(0,len(text[i])):
				temp[i][j]=wrntl.lemmatize(text[i][j])
		
		reducedText = temp.copy()
		
		return reducedText
