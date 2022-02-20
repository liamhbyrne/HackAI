import closest_airports as ca
import events_formatter as ef
import recent_events as re

# Find closest airport for each event
updater = ca.ClosestAirport("data/events_formatted.csv")
updater.update_events()

# Format events.csv and create events_formatted.csv
formatter = ef.FormatEvents("data/events_formatted.csv")
formatter.format_columns()
formatter.remove_descriptions()
formatter.save_formatted_csv()

# TODO: GENERATE ANOMALIES, use 'anomalies' until implemented
anomalies = [
    {
        "destination": "ATH",
        "start_date": "2018-06-20"
    }
]

# Generate list of possible events for each anomaly
correlator = re.RecentEvents()
for anomaly in anomalies:
    print(correlator.find_recent_events(anomaly["destination"], anomaly["start_date"]))