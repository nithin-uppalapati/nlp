from util import *

# Add your import statements here
# import nltk.data



class SentenceSegmentation():

	def naive(self, text):
		"""
		Sentence Segmentation using a Naive Approach

		Parameters
		----------
		arg1 : str
			A string (a bunch of sentences)

		Returns
		-------
		list
			A list of strings where each string is a single sentence
		"""
		
		# segmentedText = None


		# self.text=text
		[cnt,k]=[0,0]
		lst=[]
		#### var=text.replace('\n',' ')
		s={".","?","!"} 		# Set of defined punctuation marks which results in end of a sentence
		for i in text:
			# implement a for loop for tracking indices of punctuation marks and appending the sentence accordingly
			if i in s:
				senten=text[k:cnt+1].strip() # Segmenting the sentence from a given text
				lst.append(senten)
				k=cnt+1
			cnt=cnt+1

		segmentedText=lst

		return segmentedText





	def punkt(self, text):
		"""
		Sentence Segmentation using the Punkt Tokenizer

		Parameters
		----------
		arg1 : str
			A string (a bunch of sentences)

		Returns
		-------
		list
			A list of strings where each string is a single sentence
		"""
		# segmentedText = None


		# self.text=text
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		segmentedText=sent_detector.tokenize(text.strip())

		
		return segmentedText