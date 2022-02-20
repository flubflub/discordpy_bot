from datetime import datetime
import pytz


timezone = pytz.timezone('Europe/Berlin')


def embed():
    return datetime.now(timezone)


def hour():
    return datetime.now(timezone).strftime('%H:%M:%S')


def date():
    return datetime.now(timezone).strftime('%Y-%m-%d')


def timestamp():
    return datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')


def convert_unix_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
