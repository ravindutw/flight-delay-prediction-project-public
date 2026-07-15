import pandas as pd
from src.utils.config import load_config 
from src.utils.s3_paths import build_pandas_s3_data_lake_path
from timezonefinder import TimezoneFinder

def _load_raw_weather_data():
    s3_key = 'raw/Flight_Delay_Prediction_Datasets/other_data/airports_list.csv'

    s3_path = build_pandas_s3_data_lake_path(s3_key)

    header_cols = ['id', 'airport_name', 'city', 'country', 'IATA', 'ICAO', 'lon', 'lat', 'alt', 'tz', 'dst', 'timezone', 'type', 'source']

    return pd.read_csv(
        s3_path,
        header=None,
        names=header_cols
    )


def _load_raw_weather_data_new():
    s3_key = 'raw/Flight_Delay_Prediction_Datasets/other_data/airports_list.csv'

    s3_path = build_pandas_s3_data_lake_path(s3_key)

    return pd.read_csv(s3_path)


def fetch_tzs():
    raw_df = _load_raw_weather_data_new()

    filtered_df = raw_df[
        (raw_df["iata_code"].notna()) &
        (raw_df["iata_code"] != "")
    ].copy()

    tf = TimezoneFinder()

    filtered_df["timezone"] = filtered_df.apply(
        lambda row: tf.timezone_at(
            lng=row["longitude_deg"],
            lat=row["latitude_deg"]
        ),
        axis=1
    )

    result_df = filtered_df[
        [
            "iata_code",
            "ident",
            "name",
            "municipality",
            "latitude_deg",
            "longitude_deg",
            "timezone",
        ]
    ]

    return result_df