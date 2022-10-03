## node.txt

289 datasets + 462 models

* The first column is the node's ID.
* The second column is the node's type: '0' for 'model' and '1' for 'data'.
* The third column is the feature list (10 digits):
	* data node:
		* 1~5: metadata -> vector generated by Word2Vec based on data information ['centerName', 'username', 'sampleName'].
		* 6~10: statistics -> [min\_x, min\_y, max\_x, max\_y, mean\_y].
	* model node:
		* 1: model type -> '0' for Peakutils and '1' for Scipy.
		* 2~5: source code structure -> vector generated by [ast2vec](https://gitlab.com/bpaassen/ast2vec).
		* 6~10: hyperparameters -> ['distance', 'threshold', 'prominence', 'height', 'width'].
		

## edge.txt

98257 edges

* The first column is (model.id,data.id).
* The second column is the performance list: [runningTime(s), f1_score, precision, recall, Cosine similarity, Jaccard similarity].
* Only show the edges who has f1_score + precision + recall + Cosine similarity + Jaccard similarity doesn't equal to 0.
