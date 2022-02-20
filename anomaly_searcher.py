import logging

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score


class AnomalySearcher:
    def __init__(self, path='./data/flights_searches.csv'):
        self._df = pd.read_csv(path)

    def preprocess(self, destination):
        self._df[["arrival_date", "return_date"]] = self._df[["arrival_date", "return_date"]].apply(pd.to_datetime)
        self._df = self._df.groupby(['origin', 'destination', 'arrival_date'], as_index=False).agg(
            {'origin': 'first', 'destination': 'first',
             'arrival_date': 'first', 'return_date': 'first',
             'volume': 'sum'})
        self._df = self._df.loc[(self._df['destination'] == destination)]
        self._df['nth'] = np.arange(len(self._df))

    def forAllDestinations(self):
        return self._df.destination.unique()

    def findAnomalies(self):
        # fitting
        x = self._df['nth']
        y = self._df['volume']
        polyModel = np.poly1d(np.polyfit([i for i in range(len(x))], y, 10))
        # fitted_line = np.linspace(1, len(x), np.max(y).astype(int))
        logging.info("R-Squared: {}".format(r2_score(y, polyModel(x))))
        # Anomaly finder
        self._df['anomaly'] = (
                (self._df['volume'] - polyModel(self._df['nth'])) > (2 * polyModel(self._df['nth'])))
        anomalies = self._df.loc[self._df['anomaly']]
        ordered_anomalies = anomalies.loc[(anomalies.volume - polyModel(anomalies.nth)).sort_values(ascending=False).index]
        return ordered_anomalies[['destination', 'arrival_date']]

