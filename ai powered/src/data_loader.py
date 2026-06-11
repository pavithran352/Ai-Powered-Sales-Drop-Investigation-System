import pandas as pd
from config.config import *


def load_data():

    df = pd.read_csv(PROCESSED_DATA_PATH)

    df["date"] = pd.to_datetime(df["date"])

    return df