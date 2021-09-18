# Add your import statements here
import numpy as np
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from scipy.linalg import svd
from nltk.corpus import wordnet



        # syn_collec = []
        # for i in t_collec:
        #     syn_collec.append(wordnet.synsets('i')[0])

        # QE = np.zeros([len(t_collec), len(t_collec)])               ## additional lines for query expansion                   
        # for i in len(t_collec):                                     ## additional lines for query expansion
        #     for j in len(t_collec):                                 ## additional lines for query expansion
        #         QE[i][j] = syn_collec[i].wup_similarity(syn_collec[j])    ## additional lines for query expansion

            # inter_vec = np.matmul(QE,q_vec) ## additional lines for query expansion
            # q_vec = inter_vec.copy()        ##  additional lines for query expansion


# Add any utility functions here

# Comment by Nithin