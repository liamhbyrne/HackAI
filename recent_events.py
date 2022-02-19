import pandas as pd
import numpy as np


class RecentEvents:
    def __init__(self):
        # Load up events_formatted.csv
        self.ef = pd.read_csv("data/events_formatted.csv")

    def find_recent_events (self, destination, date):
        # Selects all events with the same destination
        self.ef = self.ef[self.ef['closest_iata'] == destination]

        date_boundary = (pd.date_range(date, periods=2, freq="14D"))[-1].date()
        self.ef = self.ef[(self.ef['start_date'] >= str(date)) & (self.ef['end_date'] <= str(date_boundary))]
        self.ef = self.ef.sort_values(by='visitors')

        return self.ef



if __name__ == "__main__":
    correlator = RecentEvents()
    print(correlator.find_recent_events("ATH", "2018-12-20"))