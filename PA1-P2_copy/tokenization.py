from util import *
# from nltk.tokenize import word_tokenize 
# Add your import statements here




class Tokenization():

	def naive(self, text):
		"""
		Tokenization using a Naive Approach

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""

		tokenizedText = None

		#Fill in code here
		lst=[]
		for i in text:
			i.replace("\n"," ")
			lst.append(i.split(" "))
		
		tokenizedText=lst
		return tokenizedText



	def pennTreeBank(self, text):
		"""
		Tokenization using the Penn Tree Bank Tokenizer

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""
		l = []
		for i in text:
			w = word_tokenize(i)
			l.append(w)
			
		tokenizedText=l
		return tokenizedText
