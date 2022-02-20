import logging
import math

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

class AnomalySearcher:
    def __init__(self, path='./data/flights_searches.csv'):
        self._df = pd.read_csv(path)
        self._dest: str

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

        self._df = self._df.sort_values('arrival_date')
        # fitting
        x = self._df['arrival_date']
        y = self._df['volume']

        y_std = y.std()

        rolling7 = y.rolling(7).mean()
        rolling14 = y.rolling(14).mean()
        rm28 = y.rolling(28).mean()
        rs28 = y.rolling(28).std() #+ (3*y_std)
        r28 = rm28 + (3*rs28)

        anomsL=[]
        for xi, yi, ri in zip(x,y,r28):
            diff = yi - ri
            if diff > 0:
                anomsL.append([xi, yi, diff**0.5, self._dest])

        anoms = pd.DataFrame(anomsL)
        ordered_anoms = anoms.sort_values(2,ascending=False)
        ordered_anoms = ordered_anoms.rename(columns={0: "arrival_date", 1: "volume", 2: "error", 3: "destination"})
        return ordered_anoms
        """
        fig, ax = plt.subplots()
        ax.scatter(x,y,marker=".")
        ax.scatter(anoms[0],anoms[1],s=anoms[2],marker=".", color="red")
        #ax.plot(x,r28, color="red")
        fig.autofmt_xdate()
        ax.set_xlim([datetime.date(2017, 12, 30), datetime.date(2019, 12, 1)])

        print(f'x: {x.head()}')
        print(f'y: {y.head()}')

        plt.title(self._dest)
        plt.show()


        """"""
        polyModel = np.poly1d(np.polyfit([i for i in range(len(x))], y, 10))
        fitted_line = np.linspace(1, len(x), np.max(y).astype(int))
        logging.info("R-Squared: {}".format(r2_score(y, polyModel(x))))
        logging.info("R-Squared: {}".format(r2_score(y, polyModel(x))))

        rolling = y.rolling(28).mean()
        rolling = rolling.dropna()
        print(rolling.head())

        # Anomaly finder
        self._df['anomaly'] = (
                (self._df['volume'] - polyModel(self._df['nth'])) > (3 * polyModel(self._df['nth'])) + (0.5*np.average(self._df['volume'])))

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
        """

if __name__ == '__main__':
    destination_finder = AnomalySearcher()
    dests = destination_finder.forAllDestinations()
    anomalies = {}
    for d in dests:
        anon_searcher = AnomalySearcher()
        anon_searcher.preprocess(d)
        df = anon_searcher.findAnomalies(True)