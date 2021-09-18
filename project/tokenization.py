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
# ---------------------------------------
		tokenizedText = None

		#Fill in code here
		lst=[]
		for i in text:
			i.replace("\n"," ")
			lst.append(i.split(" "))
		
		tokenizedText=lst
		return tokenizedText
# ---------------------------------------




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

		trim_set = {"/", ".", "!", "?", "'", '"', "_", "*", "(", ")", "{", "}", "[", "]", "<", ">", "-", "+", "\\", ",", "$"} 
		for i in text:
			temp_lst = []
			w = word_tokenize(i)
			for j in w:
				if not(j[0] in trim_set) and not(j[-1] in trim_set):
					temp_lst.append(j)

				elif (j[0] in trim_set) and not(j[-1] in trim_set):
					final_trimmed_word = j[1:]
					temp_lst.append(final_trimmed_word)

				elif (j[-1] in trim_set) and not(j[0] in trim_set):
					final_trimmed_word = j[:-1]
					temp_lst.append(final_trimmed_word)

				else:
					j_new = j[1:]
					final_trimmed_word = j_new[:-1]
					temp_lst.append(final_trimmed_word)

			l.append(temp_lst)
			# l.append(w)
			
		tokenizedText=l
		# print(tokenizedText)
		return tokenizedText
