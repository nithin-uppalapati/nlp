from util import *

# Add your import statements here
import re
from nltk.tokenize.treebank import TreebankWordTokenizer


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
		tokenizedText = []

		for i in text:
			tokenizedText.append([temp for temp in re.split(r'([\s,:;?!.-])\s*', i) if temp!=' ' and temp])

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

		tokenizedText = None

		#Fill in code here
		tokenizedText = []

		for i in text:
			tokenizedText.append(TreebankWordTokenizer().tokenize(i))


		return tokenizedText