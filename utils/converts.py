from datetime import datetime


def get_day_of_week_from_string(date_string) -> str:
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = datetime.strptime(date_string, "%Y-%m-%d %H:%M").weekday()
    return days[day]
