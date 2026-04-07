# Project 2 Analysis

## Deliverable A: Accuracy vs Vectors Searched

| Threshold | Avg Vectors Searched | Search Fraction | Avg Returned Score | Avg Oracle Score | Overall Score |
|-----------|---------------------|-----------------|--------------------|------------------|---------------|
| 500       | 430.66              | 0.3260          | 0.5579             | 0.5812           | 2.9399        |
| 1000      | 675.73              | 0.5115          | 0.5861             | 0.5812           | 1.9611        |

At threshold 500 the corpus splits into more partitions, so each search only looks at around 430 vectors instead of 675. That makes search cheaper and pushes the overall score up from 1.96 to 2.94. The downside is accuracy drops a little since with more partitions there is a higher chance the query gets routed to the wrong node and misses relevant records. At threshold 1000 each node holds more records so the search is more thorough, but you pay for it by searching a bigger chunk of the corpus every time. Basically smaller threshold means faster but slightly less accurate, larger threshold means more accurate but slower.

## Deliverable B: Does Insertion Order Matter?

*Results pending — experiments to be run with shuffled vs grouped ingestion order.*

*Analysis pending.*

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