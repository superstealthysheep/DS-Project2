# Project 2 Analysis

## Deliverable A: Accuracy vs Vectors Searched

*Results pending — experiments to be run with multiple MAX_VECTORS_PER_NODE values.*

| Threshold | Avg Vectors Searched | Search Fraction | Avg Returned Score | Avg Oracle Score | Overall Score |
|-----------|---------------------|-----------------|--------------------|------------------|---------------|
| 250       |                     |                 |                    |                  |               |
| 500       |                     |                 |                    |                  |               |
| 1000      |                     |                 |                    |                  |               |
| 2000      |                     |                 |                    |                  |               |

*Analysis pending.*

## Deliverable B: Does Insertion Order Matter?

The following were run with `MAX_VECTORS_PER_NODE=1000`

| Insertion order                 | Avg Vectors Searched | Search Fraction | Avg Returned Score | Avg Oracle Score | Overall Score |
|---------------------------------|----------------------|-----------------|--------------------|------------------|---------------|
| Shuffled                        | 675.73               | 0.5115          | 0.5861             | 0.5812           | 1.9611        |
| Sequential by type and file     | 593.40               | 0.4516          | 0.5637             | 0.5812           | 2.1856        |

Analysis: Clearly, there is a difference here. However, the difference is not enormous.
One effect of using a non-shuffled insertion order is that the early entries have a strong effect on the grouping of the data.
In this case, since there is only one split occurring, the only important property of the ordering is what vectors are present at the moment that the dataset is split. This happens at 1000 out of 1321 entries. 
For this reason, we repeat the experiment with `MAX_VECTORS_PER_NODE=250`:

| Insertion order                 | Avg Vectors Searched | Search Fraction | Avg Returned Score | Avg Oracle Score | Overall Score |
|---------------------------------|----------------------|-----------------|--------------------|------------------|---------------|
| Shuffled                        | 128.66               | 0.0974          | 0.5454             | 0.5812           | 11.1313       |
| Sequential by type and file     | 116.43               | 0.0885          | 0.5327             | 0.5812           | 13.0166       |

For this sort of online k-means clustering that we're doing, it may make sense to try to (if possible) add data in related clumps at a time. The reason is that, generally, clusters with narrow diameters are more "useful" clusters (i.e. they are more tighly related to each other and to the centroid, thus the centroid provides a good "gist" of what you can find if you look in the cluster). If we consider the opposite case, high-variance clusters are not particularly useful because from the centroid alone it is not easy to determine if your query vector is to be found at that node.

Sorting the vectors temporally should result in a sequence of vectors that from moment to moment should be quite semantically similar. Intuition for this is that within one lecture, the materials will all be about one topic. And from one lecture to the next, the topics tend to be relatively related. You might say that "the course's semantic content varies rather smoothly over time". 

For this reason, building clusters in this order may result in lower-variance clusters, meaning it is easier to from the centroid alone find the vectors you're querying for.


## Deliverable C: Proposed Alternative Search Scheme

Right now the controller picks the single closest node by centroid and sends the search there. This is fast but it misses records on other nodes that might actually be more relevant, especially if the query lands near a partition boundary.

**Proposal: search the top 2 closest nodes instead of just 1**

The controller compares the query against all centroids, picks the 2 closest nodes, sends SearchLocal to both, merges the results, and returns the top k. That is basically the only change needed.

**Why this helps:**

When a node splits, records that were semantically similar sometimes end up on different nodes depending on insertion order. A query near that boundary only gets half the relevant records under the current scheme. Searching both nodes fixes that.

**The tradeoff:**

You are searching roughly twice as many vectors per query and making two gRPC calls instead of one. For queries that are clearly in the center of one partition this extra work does not help at all. But for boundary queries the quality improvement is real.

Whether it is worth it depends on how well separated the partitions are, which itself depends on insertion order and threshold size, exactly what Deliverables A and B analyze.

## Deliverable D: Extend Evaluation

Extended evaluate.py to run across all questions in questions_scored.jsonl instead of one random question. Aggregate metrics including average hit rate and average vectors searched are now reported at the end.