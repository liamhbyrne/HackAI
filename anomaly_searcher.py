import logging

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt


class AnomalySearcher:
    def __init__(self, path='./data/flights_searches.csv'):
        self._df = pd.read_csv(path)
        self._dest : str

    def preprocess(self, destination):
        self._dest = destination
        self._df[["arrival_date", "return_date"]] = self._df[["arrival_date", "return_date"]].apply(pd.to_datetime)
        self._df = self._df.groupby(['origin', 'destination', 'arrival_date'], as_index=False).agg(
            {'origin': 'first', 'destination': 'first',
             'arrival_date': 'first', 'return_date': 'first',
             'volume': 'sum'})
        self._df = self._df.loc[(self._df['destination'] == destination)]
        self._df['nth'] = np.arange(len(self._df))

    def forAllDestinations(self):
        return self._df.destination.unique()

    def findAnomalies(self, plot=False):
        # fitting
        x = self._df['nth']
        y = self._df['volume']
        polyModel = np.poly1d(np.polyfit([i for i in range(len(x))], y, 10))
        fitted_line = np.linspace(1, len(x), np.max(y).astype(int))
        logging.info("R-Squared: {}".format(r2_score(y, polyModel(x))))
        logging.info("R-Squared: {}".format(r2_score(y, polyModel(x))))
        # Anomaly finder
        self._df['anomaly'] = (
                (self._df['volume'] - polyModel(self._df['nth'])) > (2 * polyModel(self._df['nth'])) + (0.5*np.average(self._df['volume'])))

        self._df['error'] = (self._df['volume'] - polyModel(self._df['nth']))/polyModel(self._df['nth'])

        anomalies = self._df.loc[self._df['anomaly']]
        ordered_anomalies = anomalies.sort_values('error', ascending=False)


        print(ordered_anomalies.head())

        if plot:
            highlight = [True, False]
            sns.relplot(data=self._df, x='nth', y='volume', hue='anomaly', hue_order=highlight, aspect=1.61)
            plt.scatter(ordered_anomalies['nth'].head(10), ordered_anomalies['volume'].head(10), color='red')
            plt.title(self._dest)
            plt.plot(fitted_line, polyModel(fitted_line))
            plt.show()

        return ordered_anomalies[['destination', 'arrival_date']]

if __name__ == '__main__':
    destination_finder = AnomalySearcher()
    dests = destination_finder.forAllDestinations()
    anomalies = {}
    for d in dests:
        anon_searcher = AnomalySearcher()
        anon_searcher.preprocess(d)
        df = anon_searcher.findAnomalies(True)