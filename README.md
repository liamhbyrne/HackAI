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
A significant proportion of both datasets provided were sparse and inconsistent, for example in `events.csv` there were 3361 events without a visitor capacity out of a total 5000. 
We determined that the visitor capacity was one of the most important features of an event so we decided to fill in the gaps:
#### Word2Vec
Each event has an associated description of varying length. Through data exploration we found that events with similar sounding descriptions tend to have a similar visitor capacity. Comparing similarity between bodies of text is not straightforward, as capturing semantics from a sequence of characters is highly subjective. A **Word2Vec technique** involves decomposing text into a vector (embedding) with several dimensions, such that the _cosine similarity_ between these vectors represents the semantics of the text. We used spaCy to convert each event description into a vector. Each event without a visitor capacity is given the same capacity as the event with the highest cosine similarity. 
![wordcloud](https://user-images.githubusercontent.com/47918966/155113585-f8a91b16-03e0-42bd-bab2-388ddedd8637.png)
_Fig.1 A wordcloud of key words in the event descriptions, generated by the Python wordcloud library_

### Anomaly Detection
The pipeline we created first finds anomalous demand and then tries to give an 'explanation' through associating it with an event. We plotted a time series of demand over time for a given destination or route. 
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/47918966/155037630-1bd7d98b-872d-4a1c-8c40-250c501c7fc2.png">
</p> 

_Fig.2 The graph above presents the demand from Barcelona to Athens._

To gauge how likely each day is an anomaly, we created a model which fits to the baseline of the curve to capture the underlying seasonal movements of demand. This time series is fairly erratic (R<sup>2</sup> of just 0.16 for Athens with a polynomial regression fit). We had two different approaches to this:
#### Polynomial Regression
To capture the general pattern of the demand, a polynomial fit provides a smooth curve. We found that a polynomial with a degree of 10-15 was sufficient to capture the baseline. However, its tendency to drop close or below zero made it problematic when identifying anomalies as we gauged the likelihood of an anomaly by the _relative_ distance to the line.

![image](https://user-images.githubusercontent.com/47918966/155037269-8fd7f0c6-36e3-4bb3-984d-de43a1cd54ed.png) 

_Fig.3 The graph above presents the polynomial fit of the demand from Barcelona to Athens._

#### Confidence Intervals
Our second approach attempted to improve on polynomial regression by more accurately modelling the trends and reflecting the spread of the volume. To this effect, we used a combination of rolling mean and rolling standard deviation with a confidence level of 0.95. We found rolling periods of multiplies of 7 abstracted away the weekly variations so used a period of 28 days to avoid overfitting and capture broader seasonal trends. We used the upper confidence interval first as a threshold for anomalies, but found a large number of data points close to the line which were clearly not anomalies.

To deal with this, we instead used the distance of each data point from the confidence interval. To decide where on this scale to threshold datapoints we began by studying its distribution. Visually, it resembled a normal distribution (although more work would be required to judge exactly how closely) and given that we were only looking for increases in demand rather than decreases, we opted to categorise anomalies as data points whose distance from the upper confidence level was above 2 standard deviations from the mean distance. This allowed us to only capture the most extreme deviations from the baseline.

<p align="center">
  <img src="https://user-images.githubusercontent.com/61391776/155058318-17bf64bc-bb08-41f1-affd-dec346ef07d8.png">
</p> 

_Fig.4 The confidence interval anomaly identification strategy on flight searches from Barcelona to Singapore._

### Anomaly Explanation
A list of identified anomalies is passed to this final stage of the pipeline - using events to explain each anomaly. At this point we know the destination, visitor capacity and the period in time of each anomaly. First, events are filtered by their geographical distance (Haversine) to that airport. Next, only events in the two weeks running up to the spike are considered. The remaining events are ranked by the product of the distance from the baseline and the visitor capacity (including the ones generated by Word2Vec). The top 100 most impactful events can be found at [final.csv](https://github.com/liamhbyrne/HackAI/blob/main/final.csv).

![map](https://media.discordapp.net/attachments/943289646509592576/944980177845358622/unknown.png?width=1060&height=676)
_Fig.5 A map of the location of each event, revealing the clustering around airports_

## If we were given more than 36 hours
If time permitted, we would have looked into identifying which origin airports the visitors would of most likely travelled from. For example, leading up to an international football match - you would expect a surge in demand from the away team.

## Acknowledgements
We would like to thank Cirium for the challenge, we thoroughly enjoyed the task and appreciate all the effort of designing the task, running the event, and evaluating all the submissions. Additionally, congratulations to the University of Southampton AI society on hosting their first hackathon. 
