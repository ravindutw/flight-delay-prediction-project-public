import pandas as pd
import json
import boto3
import os
import ast
import time
import gzip
from src.utils.config import load_config 
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from tenacity import retry_if_exception_type
from src.load.weather_data import write_to_datalake


def load_airports():
    cfg = load_config()
    s3_bucket = cfg["aws"]["s3"]["data-lake-bucket"]
    s3_path = 'raw/Flight_Delay_Prediction_Datasets/other_data/airports.json'

    s3_client = boto3.client('s3')

    airports = s3_client.get_object(
        Bucket=s3_bucket,
        Key=s3_path
    )['Body'].read().decode('utf-8')
    
    airport_list = json.loads(airports)
    return airport_list


@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(min=2, max=30),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout)),
    reraise=True
)
def fetch_and_write_batch(batch):
    data = _fetch_batch(batch)
    write_to_datalake(raw_text=data, i=hash(tuple(batch)) % 10_000)
    return len(batch)


def _fetch_batch(station_list, year="2025"):
    station_param = ",".join(station_list)
    url = (
        "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
        f"station={station_param}"
        "&data=tmpf,dwpf,relh,sknt,gust,vsby,skyc1,skyc2,skyc3,wxcodes,p01i,alti"
        f"&year1={year}&month1=1&day1=1"
        f"&year2={int(year)+1}&month2=1&day2=1"
        "&tz=UTC&format=onlycomma&latlon=no&missing=M&trace=T&direct=no&report_type=3"
    )
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    return response.text 