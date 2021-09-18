
To test our code, run main.py as before with the appropriate arguments.
Usage: main.py [-custom] [-dataset DATASET FOLDER] [-out_folder OUTPUT FOLDER]
               [-segmenter SEGMENTER TYPE (naive|punkt)] [-tokenizer TOKENIZER TYPE (naive|ptb)] 


When the -custom flag is passed, the system will take a query from the user as input. For example:
> python main.py -custom
> Enter query below
> Papers on Aerodynamics
This will print the IDs of the five most relevant documents to the query to standard output.

When the flag is not passed, all the queries in the Cranfield dataset are considered and precision@k, recall@k, f-score@k, nDCG@k and the Mean Average Precision are computed for the top 100 retrieved documents.

In both the cases, *queries.txt files and *docs.txt files will be generated in the OUTPUT FOLDER after each stage of preprocessing of the documents and queries.


In both the cases, precision vs recall plot and evaluation metric plots for various rankings are generated in the ./output folder


In case if you want to implement query expansion (based on wordnet synsets) then go to "stopwordRemoval.py" and set "activate" to 1 (You can find it in the 6th line)

In case if you want to change the extent of query expansion (The extent to which expnasion of query should occur, it means the amount of extra words per token to be appended to the query, which are having same sense as that of query ), extent_of_expansion range is from [1, 3] both ends included.
