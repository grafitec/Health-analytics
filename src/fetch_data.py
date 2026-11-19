import pandas as pd

def get_data():
    print('get_data')
    # Main table
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrJGzD0jzGTe39oYvdwuko85MzaoATsdis4fNPVXON_EfB_JPnnV-x13K9TeS4jh-t8FS9Zxwn-klg/pub?gid=593133795&single=true&output=csv"
    df = pd.read_csv(url)

    # Point table
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrJGzD0jzGTe39oYvdwuko85MzaoATsdis4fNPVXON_EfB_JPnnV-x13K9TeS4jh-t8FS9Zxwn-klg/pub?gid=1344432105&single=true&output=csv"
    dfPoints = pd.read_csv(url)
    return df, dfPoints


