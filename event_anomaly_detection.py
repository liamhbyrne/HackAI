from closest_airports import ClosestAirport
from events_formatter import FormatEvents
from recent_events import RecentEvents
from holiday_checker import HolidayChecker
from anomaly_searcher import AnomalySearcher

# Find closest airport for each event
updater = ClosestAirport("data/events_formatted.csv")
updater.update_events()

# Format events.csv and create events_formatted.csv
formatter = FormatEvents("data/events_formatted.csv")
formatter.format_columns()
formatter.remove_descriptions()
formatter.save_formatted_csv()

correlator = RecentEvents()
holiday_check = HolidayChecker()
def print_anomaly(row):
    correlated_events = correlator.find_recent_events(row.destination, str(row.arrival_date.date()))
    holiday_num = holiday_check.find_recent_holidays(row.destination, str(row.arrival_date.date()))

    anomaly_string = str(row.arrival_date.date()) + " has " + str(len(correlated_events.index)) + " event possibilites"
    if holiday_num > 0:
        anomaly_string += ", and " + str(holiday_num) + "holiday possibilites"

    print(anomaly_string)

# Generate anomalies
destination_finder = AnomalySearcher()
dests = destination_finder.forAllDestinations()
anomalies = {}
for d in dests:
    anon_searcher = AnomalySearcher()
    anon_searcher.preprocess(d)
    dest = d
    df = anon_searcher.findAnomalies()
    print("########## " + dest + " ##########")
    df.apply(print_anomaly, axis=1)
    print("")




