from util import *

# Add your import statements here




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
		
		# Adding a tag to period ---> TAG: <\nk> (making it as .<\nk>)
		self.text=text
		[cnt,k]=[0,0]
		lst=[]
		# var=text.replace('\n',' ')
		for i in text:
			# implement a for loop  extracting in indices of periods
			s={".","?","!"}
			for j in i:
				if j in s:
					senten=text[k:cnt+1].strip()
					lst.append(senten)
					k=cnt+1
			cnt=cnt+1






		# segmentedText = None

		return segmentedText

		#Fill in code here

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
			A list of strings where each strin is a single sentence
		"""

		segmentedText = None

		#Fill in code here
		
		return segmentedText