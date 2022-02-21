<p align="center">
  <img src="./images/banner.png">
</p>

<p align="center">
  <b>1<sup>st</sup> place</b>
</p>

---

<p align="center">
  <a href="https://github.com/liamhbyrne"><b>Liam Byrne</b>, <a href="https://github.com/samwatsonn"><b>Sam Watson</b></a> and <a href="https://github.com/lucaswarwick02"><b>Lucas Warwick</b></a>
</p>

---

## The Task
Cirium provided us with a dataset of flight ticket searches and events and challenged us to:
  
>**_Find explanations for anomalies in travel demand_** 

It is very useful for airlines to know when there will be an significant increase in demand for a particular destination. One way to predict the future demand of a given flight is to identify which public events (e.g. a tradeshow) contribute most to the increase in flight searches.
  
## Our solution
We decided to break down the task into a pipeline:

`data cleaning -> anomaly detection -> anomaly identification`
### Data cleaning
A significant proportion of both datasets provided were sparse and inconsistent, for example in `events.csv` there were 3XXX events without a visitor capacity out of a total 7XXX. 
We determined that the visitor capacity was one of the most important features of an event so we decided to fill in the gaps:
#### Word2Vec
Each event has an associated description of varying length. Through data exploration we found that events with similar sounding descriptions tend to have a similar visitor capacity. Comparing similarity between bodies of text is not straightforward, as capturing semantics from a sequence of characters is highly subjective. A Word2Vec technique involves decomposing text into a vector with several dimensions, such that the cosine similarity between these vectors represents the semantics of the text. We used spaCy to convert each event description into a vector. Each event without a visitor capacity is given the same capacity as the event with the highest cosine similarity.
