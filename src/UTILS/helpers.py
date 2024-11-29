# utils/helpers.py

import datetime

def validar_data(data_str):
    try:
        return datetime.datetime.strptime(data_str, "%d-%m-%Y")
    except ValueError:
        return None
