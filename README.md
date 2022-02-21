<p align="center">
  <img src="./images/banner.png">
</p>

<p align="center">
  <b>1<sup>st</sup> place</b>
</p>

---

<p align="center">
  <a href="https://github.com/liamhbyrne"><b>Liam Byrne</b>, <a href="https://github.com/samwatsonn"><b>Sam Watson</b></a>, <a href="https://github.com/lucaswarwick02"><b>Lucas Warwick</b></a>
</p>

---

## The Task
Cirium provided us with a dataset of flight ticket searches and events and challenged us to:
  
>**_Find explanations for anomalies in travel demand_** 


It is very useful for airlines to know when there will be an significant increase in demand for a particular destination. One way to predict the future demand of a given flight is to identify which public events (e.g. a tradeshow) contribute most to the increase in flight searches.
  
## Our solution
We decided to break down the task into a pipeline:

`data cleaning -> anomaly detection -> anomaly explanation`
### Data cleaning
A significant proportion of both datasets provided were sparse and inconsistent, for example in `events.csv` there were 3XXX events without a visitor capacity out of a total 7XXX. 
We determined that the visitor capacity was one of the most important features of an event so we decided to fill in the gaps:
#### Word2Vec
Each event has an associated description of varying length. Through data exploration we found that events with similar sounding descriptions tend to have a similar visitor capacity. Comparing similarity between bodies of text is not straightforward, as capturing semantics from a sequence of characters is highly subjective. A **Word2Vec technique** involves decomposing text into a vector (embedding) with several dimensions, such that the _cosine similarity_ between these vectors represents the semantics of the text. We used spaCy to convert each event description into a vector. Each event without a visitor capacity is given the same capacity as the event with the highest cosine similarity.

### Anomaly Detection
The pipeline we created first finds anomalous demand and then tries to give an 'explanation' through associating it with an event. We plotted a time series of demand over time for a given destination or route. 
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/47918966/155037630-1bd7d98b-872d-4a1c-8c40-250c501c7fc2.png">
</p>

To gauge how likely each day is an anomaly, we created a model which fits to the baseline of the curve to capture the underlying seasonal movements of demand. This time series is fairly erratic (R<sup>2</sup> of just 0.16 for Athens with a polynomial regression fit). We had two different approaches to this:
#### Polynomial Regression
To capture the general pattern of the demand, a polynomial fit provides a smooth curve. We found that a polynomial with a degree of 10-15 was sufficient to capture the baseline. However, its tendency to drop close or below zero made it problematic when identifying anomalies as we gauged the liklihood of an anomaly by the _relative_ distance to the line.
![image](https://user-images.githubusercontent.com/47918966/155037269-8fd7f0c6-36e3-4bb3-984d-de43a1cd54ed.png) 
  
_Fig.2 The graph above presents the polynomial fit of the demand from Barcelona to Athens._


