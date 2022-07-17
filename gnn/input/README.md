### node.txt

Node list: 

* The first column is ID.
* The second column is the node's type: '0' for 'model' and '1' for 'data'.

### edge.txt

Edge list:

* The first column is (model.id,data.id).
* The second column is the list of performance: [runningTime(s), f1_score, precision, recall].
* Only show the edge whose F1 score is not null.

### top5.txt

Edge list for top5 edges for each dataset:

* Performance = 0.4 * f1_score + 0.1 * precision + 0.1 * recall - 0.01 * runningTime(s).
* Show the edges who get the top 5 performance for each dataset.