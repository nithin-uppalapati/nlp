from sentenceSegmentation import SentenceSegmentation
from tokenization import Tokenization
from inflectionReduction import InflectionReduction
from stopwordRemoval import StopwordRemoval
from informationRetrieval import InformationRetrieval
from evaluation import Evaluation

from sys import version_info
import argparse
import json
import matplotlib.pyplot as plt

# Input compatibility for Python 2 and Python 3
if version_info.major == 3:
    pass
elif version_info.major == 2:
    try:
        input = raw_input
    except NameError:
        pass
else:
    print ("Unknown python version - input function not safe")


class SearchEngine:

	def __init__(self, args):
		self.args = args

		self.tokenizer = Tokenization()
		self.sentenceSegmenter = SentenceSegmentation()
		self.inflectionReducer = InflectionReduction()
		self.stopwordRemover = StopwordRemoval()

		self.informationRetriever = InformationRetrieval()
		self.evaluator = Evaluation()


	def segmentSentences(self, text):
		"""
		Call the required sentence segmenter
		"""
		if self.args.segmenter == "naive":
			return self.sentenceSegmenter.naive(text)
		elif self.args.segmenter == "punkt":
			return self.sentenceSegmenter.punkt(text)

	def tokenize(self, text):
		"""
		Call the required tokenizer
		"""
		if self.args.tokenizer == "naive":
			return self.tokenizer.naive(text)
		elif self.args.tokenizer == "ptb":
			return self.tokenizer.pennTreeBank(text)

	def reduceInflection(self, text):
		"""
		Call the required stemmer/lemmatizer
		"""
		return self.inflectionReducer.reduce(text)

	def removeStopwords(self, text, t):
		"""
		Call the required stopword remover
		"""
		return self.stopwordRemover.fromList(text, t)


	def preprocessQueries(self, queries):
		"""
		Preprocess the queries - segment, tokenize, stem/lemmatize and remove stopwords
		"""

		# Segment queries
		segmentedQueries = []
		for query in queries:
			segmentedQuery = self.segmentSentences(query)
			segmentedQueries.append(segmentedQuery)
		json.dump(segmentedQueries, open(self.args.out_folder + "segmented_queries.txt", 'w'))
		# Tokenize queries
		tokenizedQueries = []
		for query in segmentedQueries:
			tokenizedQuery = self.tokenize(query)
			tokenizedQueries.append(tokenizedQuery)
		json.dump(tokenizedQueries, open(self.args.out_folder + "tokenized_queries.txt", 'w'))
		# Stem/Lemmatize queries
		reducedQueries = []
		for query in tokenizedQueries:
			reducedQuery = self.reduceInflection(query)
			reducedQueries.append(reducedQuery)
		json.dump(reducedQueries, open(self.args.out_folder + "reduced_queries.txt", 'w'))
		# Remove stopwords from queries
		stopwordRemovedQueries = []
		for query in reducedQueries:
			stopwordRemovedQuery = self.removeStopwords(query, 1)
			stopwordRemovedQueries.append(stopwordRemovedQuery)
		json.dump(stopwordRemovedQueries, open(self.args.out_folder + "stopword_removed_queries.txt", 'w'))

		preprocessedQueries = stopwordRemovedQueries
		return preprocessedQueries

	def preprocessDocs(self, docs):
		"""
		Preprocess the documents
		"""
		
		# Segment docs
		segmentedDocs = []
		for doc in docs:
			segmentedDoc = self.segmentSentences(doc)
			segmentedDocs.append(segmentedDoc)
		json.dump(segmentedDocs, open(self.args.out_folder + "segmented_docs.txt", 'w'))
		# Tokenize docs
		tokenizedDocs = []
		for doc in segmentedDocs:
			tokenizedDoc = self.tokenize(doc)
			tokenizedDocs.append(tokenizedDoc)
		json.dump(tokenizedDocs, open(self.args.out_folder + "tokenized_docs.txt", 'w'))
		# Stem/Lemmatize docs
		reducedDocs = []
		for doc in tokenizedDocs:
			reducedDoc = self.reduceInflection(doc)
			reducedDocs.append(reducedDoc)
		json.dump(reducedDocs, open(self.args.out_folder + "reduced_docs.txt", 'w'))
		# Remove stopwords from docs
		stopwordRemovedDocs = []
		for doc in reducedDocs:
			stopwordRemovedDoc = self.removeStopwords(doc, 0)
			stopwordRemovedDocs.append(stopwordRemovedDoc)
		json.dump(stopwordRemovedDocs, open(self.args.out_folder + "stopword_removed_docs.txt", 'w'))

		preprocessedDocs = stopwordRemovedDocs
		return preprocessedDocs


	def evaluateDataset(self):
		"""
		- preprocesses the queries and documents, stores in output folder
		- invokes the IR system
		- evaluates precision, recall, fscore, nDCG and MAP 
		  for all queries in the Cranfield dataset
		- produces graphs of the evaluation metrics in the output folder
		"""

		# Read queries
		queries_json = json.load(open(args.dataset + "cran_queries.json", 'r'))[:]
		query_ids, queries = [item["query number"] for item in queries_json], \
								[item["query"] for item in queries_json]
		# Process queries 
		processedQueries = self.preprocessQueries(queries)

		# Read documents
		docs_json = json.load(open(args.dataset + "cran_docs.json", 'r'))[:]
		doc_ids, docs = [item["id"] for item in docs_json], \
								[item["body"] for item in docs_json]
		# Process documents
		processedDocs = self.preprocessDocs(docs)

		# Build document index
		self.informationRetriever.buildIndex(processedDocs, doc_ids)
		# Rank the documents for each query
		doc_IDs_ordered = self.informationRetriever.rank(processedQueries)

		# Read relevance judements
		qrels = json.load(open(args.dataset + "cran_qrels.json", 'r'))[:]

		# Calculate precision, recall, f-score, MAP and nDCG for k = 1 to 10
		precisions, recalls, fscores, MAPs, nDCGs = [], [], [], [], []
		k_count = 100
		for k in range(1, k_count):
			precision = self.evaluator.meanPrecision(
				doc_IDs_ordered, query_ids, qrels, k)
			precisions.append(precision)
			recall = self.evaluator.meanRecall(
				doc_IDs_ordered, query_ids, qrels, k)
			recalls.append(recall)
			fscore = self.evaluator.meanFscore(
				doc_IDs_ordered, query_ids, qrels, k)
			fscores.append(fscore)
			print("Precision, Recall and F-score @ " +  
				str(k) + " : " + str(precision) + ", " + str(recall) + 
				", " + str(fscore))
			MAP = self.evaluator.meanAveragePrecision(
				doc_IDs_ordered, query_ids, qrels, k)
			MAPs.append(MAP)
			nDCG = self.evaluator.meanNDCG(
				doc_IDs_ordered, query_ids, qrels, k)
			nDCGs.append(nDCG)
			print("MAP, nDCG @ " +  
				str(k) + " : " + str(MAP) + ", " + str(nDCG))

		# Plot the metrics and save plot 
        
		plt.plot(range(1, k_count), precisions, label="Precision")
		plt.plot(range(1, k_count), recalls, label="Recall")
		plt.plot(range(1, k_count), fscores, label="F-Score")
		plt.plot(range(1, k_count), MAPs, label="MAP")
		plt.plot(range(1, k_count), nDCGs, label="nDCG")
		plt.legend()
		plt.title("Evaluation Metrics - Cranfield Dataset")
		plt.xlabel("k")
		plt.savefig(args.out_folder + "eval_plot.png")

		# plt.plot(precisions, recalls, label="P_v_R")
		# plt.savefig(args.out_folder + "precision_vs_recall.png")
		# print(precisions)
		# print(recalls)

		plt.clf()
		plt.cla()

		old_pres = [0.6622222222222223, 0.5511111111111111, 0.4829629629629631, 0.4288888888888889, 0.39111111111111124, 0.3607407407407406, 0.33523809523809545, 0.3194444444444444, 0.3017283950617288, 0.28133333333333355, 0.26626262626262637, 0.25296296296296295, 0.24034188034188042, 0.23206349206349217, 0.22222222222222235, 0.2127777777777778, 0.20392156862745103, 0.19530864197530878, 0.18783625730994155, 0.1813333333333334, 0.17629629629629617, 0.1709090909090909, 0.16560386473429942, 0.16092592592592594, 0.15608888888888864, 0.15179487179487194, 0.1469958847736625, 0.14412698412698424, 0.1403831417624521, 0.13688888888888903, 0.133620071684588, 0.13083333333333333, 0.1275420875420877, 0.12522875816993473, 0.12266666666666638, 0.11999999999999998, 0.11819819819819821, 0.11567251461988307, 0.11339031339031314, 0.11144444444444446, 0.10970189701896997, 0.10793650793650798, 0.10625322997416006, 0.10474747474747463, 0.10340740740740718, 0.10183574879227045, 0.10014184397163114, 0.0983333333333333, 0.0968707482993198, 0.09555555555555546, 0.09429193899782112, 0.09307692307692311, 0.09190775681341733, 0.09061728395061724, 0.08985858585858597, 0.08888888888888899, 0.0877972709551656, 0.08666666666666668, 0.0854990583804144, 0.08414814814814822, 0.08320582877959921, 0.08215053763440872, 0.08119929453262767, 0.08041666666666666, 0.07931623931623913, 0.07838383838383849, 0.0774129353233832, 0.07653594771241835, 0.07568438003220607, 0.07504761904761892, 0.07411580594679189, 0.07314814814814813, 0.07238964992389653, 0.07201201201201202, 0.07140740740740731, 0.07064327485380116, 0.07007215007215015, 0.06940170940170923, 0.06880450070323504, 0.06811111111111108, 0.06727023319615909, 0.06655826558265575, 0.06602409638554217, 0.06555555555555562, 0.06488888888888873, 0.06428940568475443, 0.06370370370370379, 0.06303030303030296, 0.06252184769038696, 0.06202469135802455, 0.0614407814407813, 0.06101449275362314, 0.06050179211469547, 0.05995271867612295, 0.05941520467836256, 0.05907407407407407, 0.0585567010309277, 0.05800453514739232, 0.05759820426487096]
		old_recall = [0.11342478263729099, 0.18385862754100185, 0.22928203520498822, 0.2661549352296123, 0.29677949358224087, 0.3229823480988209, 0.3448495755595682, 0.3693792016839312, 0.3885869859238317, 0.401107411757983, 0.41758897340621115, 0.4285845421201706, 0.4409778401801353, 0.45859719177987907, 0.46845510547112607, 0.476647073996428, 0.48550068951671027, 0.4891825573117056, 0.4961514217805701, 0.5030787105411922, 0.51151255086009, 0.5199748640504734, 0.5246112770202197, 0.5317233192989284, 0.5366884609111289, 0.5399059212285892, 0.5419120940680953, 0.5490029723256404, 0.5524597624490971, 0.5568883338776687, 0.5611853658217595, 0.5668954523116402, 0.5703204964033509, 0.5753627134455679, 0.5808371402533282, 0.5835503036331583, 0.5894058431553644, 0.5916983407811953, 0.5949277780106325, 0.5986512027340571, 0.6033774813936693, 0.6086235131397013, 0.6133631315459863, 0.6190108259120713, 0.6243547412559868, 0.6272609603092648, 0.631520219568524, 0.6335995846478891, 0.6363636680590313, 0.6394300376868043, 0.6424423833658167, 0.6460371546076469, 0.6493196807235065, 0.6525357301062227, 0.6575547777252703, 0.6607898526120694, 0.6631796148965683, 0.6648936601106135, 0.6666448718618252, 0.6670489122658656, 0.670675174892128, 0.6730911293080825, 0.6749104969411757, 0.6779787681761136, 0.6791639533612988, 0.6822346604320058, 0.6829248961222413, 0.684949587480266, 0.6867581492888277, 0.6909292251265703, 0.6921197013170466, 0.692437161634507, 0.6946739081849791, 0.6990622852400228, 0.7024178964903707, 0.7034666294338404, 0.7057651043793742, 0.7082180958323656, 0.7107715349858048, 0.7126974609117306, 0.7126974609117306, 0.7132456090598789, 0.7162977976120675, 0.719742242056512, 0.7205304193964135, 0.7210415305075245, 0.7219876993484302, 0.7234691808299116, 0.7258882841437518, 0.7285302594523939, 0.7296969261190605, 0.7321398389567102, 0.7330022643805392, 0.7340207828990577, 0.7347211195993943, 0.7390687226136642, 0.739843133388075, 0.7401394296843713, 0.7425098000547415]

		plt.plot(old_recall,old_pres, label="VS-Model (Baseline)" )
		plt.plot(recalls,precisions, label="Current Model")
		plt.legend()
		plt.title("Precision vs Recall - Cranfield Dataset")
		plt.xlabel("k")
		plt.savefig(args.out_folder + "precision_vs_recall.png")

	def handleCustomQuery(self):
		"""
		Take a custom query as input and return top five relevant documents
		"""

		#Get query
		print("Enter query below")
		query = input()
		# Process documents
		processedQuery = self.preprocessQueries([query])[0]

		# Read documents
		docs_json = json.load(open(args.dataset + "cran_docs.json", 'r'))[:]
		doc_ids, docs = [item["id"] for item in docs_json], \
							[item["body"] for item in docs_json]
		# Process documents
		processedDocs = self.preprocessDocs(docs)

		# Build document index
		self.informationRetriever.buildIndex(processedDocs, doc_ids)
		# Rank the documents for the query
		doc_IDs_ordered = self.informationRetriever.rank([processedQuery])[0]

		# Print the IDs of first five documents
		print("\nTop five document IDs : ")
		for id_ in doc_IDs_ordered[:5]:
			print(id_)



if __name__ == "__main__":

	# Create an argument parser
	parser = argparse.ArgumentParser(description='main.py')

	# Tunable parameters as external arguments
	parser.add_argument('-dataset', default = "cranfield/", 
						help = "Path to the dataset folder")
	parser.add_argument('-out_folder', default = "output/", 
						help = "Path to output folder")
	parser.add_argument('-segmenter', default = "punkt",
	                    help = "Sentence Segmenter Type [naive|punkt]")
	parser.add_argument('-tokenizer',  default = "ptb",
	                    help = "Tokenizer Type [naive|ptb]")
	parser.add_argument('-custom', action = "store_true", 
						help = "Take custom query as input")
	
	# Parse the input arguments
	args = parser.parse_args()

	# Create an instance of the Search Engine
	searchEngine = SearchEngine(args)

	# Either handle query from user or evaluate on the complete dataset 
	if args.custom:
		searchEngine.handleCustomQuery()
	else:
		searchEngine.evaluateDataset()
