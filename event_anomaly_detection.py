import pandas as pd

from closest_airports import ClosestAirport
from events_formatter import FormatEvents
from recent_events import RecentEvents
from holiday_checker import HolidayChecker
from anomaly_searcher import AnomalySearcher
from repairVisitorCount import EventEventComparator

# Find closest airport for each event
updater = ClosestAirport("data/events_formatted.csv")
updater.update_events()

# Format events.csv and create events_formatted.csv
formatter = FormatEvents("data/events_formatted.csv")
formatter.format_columns()
formatter.save_formatted_csv()

correlator = RecentEvents()
holiday_check = HolidayChecker()

total_events = 0
all_events = []

def print_anomaly(row):
    correlated_events = correlator.find_recent_events(row.destination, str(row.arrival_date.date()))
    all_events.append(correlated_events)

# Generate anomalies
destination_finder = AnomalySearcher()
dests = destination_finder.forAllDestinations()
anomalies = {}
for d in dests:
    anon_searcher = AnomalySearcher()
    anon_searcher.preprocess(d)
    df = anon_searcher.findAnomalies()
    df.head(10).apply(print_anomaly, axis=1)

all_anomalous_events = pd.concat(all_events, ignore_index=True)
eec = EventEventComparator(all_anomalous_events)
all_anomalous_events = eec.clean()

all_anomalous_events = all_anomalous_events.sort_values("visitors", ascending=False)
all_anomalous_events.to_csv("final_results.csv")




