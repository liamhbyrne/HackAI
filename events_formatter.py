import pandas as pd
import re

import closest_airports as ca


def e_v_formatting(x):
    split_data = re.split(" - ", str(x))
    formatted_string = split_data[len(split_data) - 1].replace(',', "")
    found_numbers = (re.findall("\d+", formatted_string))

    if len(found_numbers) == 0:
        return -1
    else:
        return int(found_numbers[0])


class FormatEvents:

    def __init__(self, path):
        self.path = path
        self.dataframe = pd.read_csv(path)

    def format_columns(self):
        # description
        self.dataframe['description'].fillna("No Description Given", inplace=True)
        # end_date
        self.dataframe['end_date'] = pd.to_datetime(self.dataframe['end_date'])
        # exhibitors
        self.dataframe['exhibitors'] = self.dataframe['exhibitors'].apply(e_v_formatting)
        # location
        self.dataframe['location'].fillna("No Location Given", inplace=True)
        # name
        self.dataframe['name'].fillna("No Name Given", inplace=True)
        # start_date
        self.dataframe['start_date'] = pd.to_datetime(self.dataframe['start_date'])
        # type
        self.dataframe['type'].fillna("No Type Given", inplace=True)
        # visitors
        self.dataframe['visitors'] = self.dataframe['visitors'].apply(e_v_formatting)

    def save_formatted_csv(self):
        self.dataframe.to_csv(self.path, index=False)

    def get_dataframe_info(self):
        self.dataframe.info()

    def remove_descriptions(self):
        self.dataframe.drop('description', axis=1, inplace=True)


if __name__ == '__main__':
    updater = ca.ClosestAirport("data/events_formatted.csv")
    updater.update_events()

    formatter = FormatEvents("data/events_formatted.csv")
    formatter.format_columns()
    formatter.remove_descriptions()
    formatter.save_formatted_csv()
