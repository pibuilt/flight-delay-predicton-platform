import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """
    Load the raw flights dataset.
    """

    df = pd.read_csv(path)

    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning steps.
    """

    # Drop rows where arrival delay is missing
    df = df.dropna(subset=["ARRIVAL_DELAY"])

    return df


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create binary delay target.
    """

    df["delayed"] = (df["ARRIVAL_DELAY"] > 15).astype(int)

    return df


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select the columns used for training.
    """

    columns = [
        "AIRLINE",
        "ORIGIN_AIRPORT",
        "DESTINATION_AIRPORT",
        "DEPARTURE_TIME",
        "DISTANCE",
        "DAY_OF_WEEK",
        "delayed",
    ]

    df = df[columns]

    # Ensure categorical columns are strings
    df["AIRLINE"] = df["AIRLINE"].astype(str)
    df["ORIGIN_AIRPORT"] = df["ORIGIN_AIRPORT"].astype(str)
    df["DESTINATION_AIRPORT"] = df["DESTINATION_AIRPORT"].astype(str)

    return df