import pandas as pd
from datetime import timedelta

holidays = [
    {
        "name": "Christmas Day",
        "month": 12,
        "day": 25
    },
{
        "name": "New Years",
        "month": 1,
        "day": 1
    },
]

class HolidayChecker:
    def __init__(self):
            # No Construction needed

    def find_recent_holidays (self, destination, date):
        date_boundary = (pd.date_range(date, periods=2, freq="14D"))[-1].date()
        dates_to_check = pd.date_range(date, date_boundary-timedelta(days=1), freq='d')
        for holiday in holidays:
            for date_time in dates_to_check:
                if (date_time.day == holiday["day"]) & (date_time.month == holiday["month"]):
                    return holiday["name"]


if __name__ == '__main__':
    checker = HolidayChecker()
    print(checker.find_recent_holidays("ATH", "2018-12-20"))