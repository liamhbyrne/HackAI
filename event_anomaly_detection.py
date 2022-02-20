from closest_airports import ClosestAirport
from events_formatter import FormatEvents
import recent_events as re
from anomaly_searcher import AnomalySearcher

# Find closest airport for each event
updater = ClosestAirport("data/events_formatted.csv")
updater.update_events()

# Format events.csv and create events_formatted.csv
formatter = FormatEvents("data/events_formatted.csv")
formatter.format_columns()
formatter.remove_descriptions()
formatter.save_formatted_csv()

# Generate anomalies
destination_finder = AnomalySearcher()
dests = destination_finder.forAllDestinations()
anomalies = {}
for d in dests:
    anon_searcher = AnomalySearcher()
    anon_searcher.preprocess(d)
    anomalies[d] = anon_searcher.findAnomalies()

for anomaly in anomalies:
    print(anomaly)

# Generate list of possible events for each anomaly
#correlator = re.RecentEvents()
#for anomaly in anomalies:
#    print(correlator.find_recent_events(anomaly["destination"], anomaly["start_date"]))