import pandas as pd
import numpy as np


class RecentEvents:
    def __init__(self):
        # Load up events_formatted.csv
        self.ef = pd.read_csv("data/events_formatted.csv")

    def find_recent_events (self, destination, date):
        # Selects all events with the same destination
        df = self.ef[self.ef['closest_iata'] == destination]

        date_boundary = (pd.date_range(str(date), periods=2, freq="14D"))[-1].date()
        df2 = df[(df['start_date'] >= str(date)) & (df['end_date'] <= str(date_boundary))]
        df3 = df2.sort_values(by='visitors')

        return df3



if __name__ == "__main__":
    correlator = RecentEvents()
    print(correlator.find_recent_events("ATH", "2018-06-20"))