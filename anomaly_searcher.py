import logging
import math

import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

def gen_rolling_conf_ints(confidence_level, period, ax_y):
    rolling_mean = ax_y.rolling(period).mean()
    rolling_std = ax_y.rolling(period).std()
    conf_int_upper = rolling_mean + (confidence_level * rolling_std)
    conf_int_lower = rolling_mean - (confidence_level * rolling_std)
    return conf_int_upper, conf_int_lower


class AnomalySearcher:
    def __init__(self, path='./data/flights_searches.csv'):
        self._df = pd.read_csv(path)
        self._dest: str
        self.colorDark = (44/255, 47/255, 51/255)
        self.colorLight = (.9,.9,.9)

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

        # Evaluate each origin pairing to given destination
        output_anoms = pd.DataFrame()
        for origin in self._df["origin"].unique():
            origin_to_dest = self._df[self._df["origin"] == origin]

            x = origin_to_dest['arrival_date']
            y = origin_to_dest['volume']

            # Generate rolling confidence intervals
            conf_int_upper, conf_int_lower = gen_rolling_conf_ints(0.95, 14, y)

            # Create column 'error' which is the distance of each
            # point from upper confidence interval
            origin_to_dest["error"] = y - conf_int_upper

            # Calculate anomalies
            error_std = origin_to_dest["error"].std()
            anoms_origin_to_dest = origin_to_dest.loc[origin_to_dest['error'] - error_std > 0]

            # Add pair specific anomalies to destination anomalies
            if output_anoms.empty:
                output_anoms = anoms_origin_to_dest
            else:
                pd.concat([output_anoms, anoms_origin_to_dest]).drop_duplicates('nth')

            # Plot Results
            if plot:
                fig, ax = plt.subplots()
                ax.scatter(x, y, marker=".",
                           label="Volume")
                ax.scatter(anoms_origin_to_dest["arrival_date"], anoms_origin_to_dest["volume"], marker=".",color="red",
                           label="Anomaly")
                ax.plot(x, conf_int_upper, color="orange",
                           label="99% Upper\n Confidence\n Interval")
                ax.plot(x, conf_int_lower, color="pink",
                           label="99% Lower\n Confidence\n Interval")
                ax.bar(origin_to_dest["arrival_date"], origin_to_dest["error"], color="red", alpha=0.5,
                           label="Error")

                self.formatChart(fig, ax)
                plt.title(f'{origin} to {self._dest}', color=self.colorLight)
                plt.show()

        return output_anoms

    def formatChart(self, fig, ax):
        fig.autofmt_xdate()
        ax.set_xlim([datetime.date(2017, 12, 30), datetime.date(2019, 12, 1)])
        fig.patch.set_facecolor(self.colorDark)
        ax.set_facecolor(self.colorDark)

        ax.set_ylabel("Flight Search Volume")
        ax.set_xlabel("Date")

        ax.xaxis.label.set_color([x * .9 for x in self.colorLight])
        ax.yaxis.label.set_color([x * .9 for x in self.colorLight])

        ax.tick_params(color=self.colorLight, labelcolor=self.colorLight)
        for spine in ax.spines.values():
            spine.set_edgecolor(self.colorLight)

        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                  facecolor=self.colorDark, labelcolor=self.colorLight)
        return fig, ax

if __name__ == '__main__':
    destination_finder = AnomalySearcher()
    dests = destination_finder.forAllDestinations()
    anomalies = {}
    for d in dests:
        anon_searcher = AnomalySearcher()
        anon_searcher.preprocess(d)
        df = anon_searcher.findAnomalies(True)