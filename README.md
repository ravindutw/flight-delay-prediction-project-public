# Flight Delay Prediction Project

An end-to-end machine learning pipeline that predicts U.S. flight delays by combining **over 10 million flight records** from the **U.S. Bureau of Transportation Statistics (BTS)** with historical **airport weather data** from the **Iowa Environmental Mesonet (IEM)**. The project covers the full data lifecycle — from raw data extraction, through a scalable ELT pipeline, feature engineering, data lake/warehouse design, all the way to training and evaluating delay-prediction classification models.

---

## Project Overview

Flight delays are influenced by a wide range of factors, including weather conditions at origin/destination airports, carrier performance, and scheduling. This project builds a scalable data engineering and machine learning pipeline to:

1. Extract raw flight and weather data from public sources.
2. Clean, transform, and integrate the datasets at scale using Apache Spark.
3. Organize the data into a structured **data lake** and **data warehouse** on AWS.
4. Perform exploratory data analysis (EDA) to understand delay patterns.
5. Engineer predictive features and train classification models (Gradient Boosting, PyTorch) to predict flight delays.

---

## Architecture

```
                ┌────────────────────┐        ┌───────────────────────┐
                │  BTS Flight Data   │        │  IEM Weather Data /   │
                │  (Monthly CSVs)    │        │  ASOS API             │
                └─────────┬──────────┘        └──────────┬────────────┘
                          │                              │
                          ▼                              ▼
                 ┌───────────────────────────────────────────────┐
                 │              EXTRACT (ELT/src/extract)        │
                 │  - Pull raw flight CSVs from S3               │
                 │  - Fetch weather data via Mesonet ASOS API    │
                 └───────────────────┬───────────────────────────┘
                                     ▼
                 ┌───────────────────────────────────────────────┐
                 │              LOAD (ELT/src/load)              │
                 │  - Persist raw data to S3 Data Lake           │
                 └───────────────────┬───────────────────────────┘
                                     ▼
                 ┌───────────────────────────────────────────────┐
                 │            TRANSFORM (ELT/src/transform)      │
                 │  - Data cleaning & standardization            │
                 │  - Data integration (flight + weather joins)  │
                 │  - Feature engineering                        │
                 └───────────────────┬───────────────────────────┘
                                     ▼
                 ┌───────────────────────────────────────────────┐
                 │      Data Warehouse (AWS S3 + AWS Glue +      │
                 │                  Amazon Athena)               │
                 └───────────────────┬───────────────────────────┘
                                     ▼
                 ┌─────────────────────────────────────────────┐
                 │   EDA (Jupyter Notebooks) + Model Training  │
                 │   Gradient Boosting / PyTorch classifiers   │
                 └─────────────────────────────────────────────┘
```

---

## Technology Stack

| Category                  | Technologies                                 |
|----------------------------|-----------------------------------------------|
| Language                  | Python                                       |
| Distributed Processing    | Apache Spark, PySpark                        |
| Data Manipulation         | Pandas                                       |
| Cloud Storage / Data Lake | Amazon S3                                    |
| Data Catalog / ETL        | AWS Glue                                     |
| Ad-hoc Querying           | Amazon Athena                                |
| Modeling                  | Gradient Boosting, PyTorch                   |

---

## Project Structure

```
Flight Delay Prediction Project/
├── EDA/                                  # Exploratory Data Analysis notebooks
│   ├── 01_eda_flight_data.ipynb
│   ├── 02_documentation_flight_data.ipynb
│   ├── 03_query_flight_data.ipynb
│   ├── 04_eda_weather_data.ipynb
│   └── 05_query_weather_data.ipynb
│
├── ELT/                                  # Extract-Load-Transform pipeline
│   ├── config/
│   │   ├── config.yaml                   # Spark, AWS, and logging configuration
│   │   └── log4j2.properties
│   │
│   ├── notebooks/
│   │   ├── 01_extract/                   # Data extraction notebooks
│   │   │   ├── 01_flight_data_extract.ipynb
│   │   │   ├── 02_weather_api_fetch.ipynb
│   │   │   └── 03_weather_data_extract.ipynb
│   │   └── 02_transform/                 # Data transformation notebooks
│   │       ├── 01_transform_flight_data.ipynb
│   │       ├── 02_transform_weather_data.ipynb
│   │       └── 03_transform_joining.ipynb
│   │
│   └── src/                              # Core ELT source code
│       ├── extract/                      # Flight & weather data extraction
│       ├── load/                         # Data lake write utilities
│       ├── transform/                    # Cleaning & feature engineering logic
│       └── utils/                        # Config, logging, S3 paths, Spark session
│
├── LICENSE
└── README.md
```

---

## ELT Pipeline

### 1. Extract
- **Flight data**: Monthly flight delay CSVs (Jan–Dec 2025) sourced from the U.S. Bureau of Transportation Statistics are read from S3 and combined into a single Spark DataFrame (`ELT/src/extract/flight_data.py`).
- **Weather data**: Historical airport weather observations are fetched from the [Iowa Environmental Mesonet ASOS API](https://mesonet.agron.iastate.edu/) with automatic retries/backoff (`ELT/src/extract/weather_api.py`, `weather_data.py`).

### 2. Load
- Raw extracted data (flight and weather) is written to an **Amazon S3 data lake**, partitioned and organized under a `raw/` prefix for reproducible downstream processing (`ELT/src/load/`).

### 3. Transform
- **Cleaning**: Standardizing date/time fields, correcting malformed HHMM timestamps, dropping/filling missing values (`ELT/src/transform/flight_data.py`, `weather_data.py`).
- **Integration**: Joining flight records with corresponding airport weather observations by station, date, and time window (`ELT/notebooks/02_transform/03_transform_joining.ipynb`).
- **Feature Engineering**: Deriving delay indicators, weather severity features, and time-based features to feed into the classification models.

### 4. Data Warehouse
- Cleaned and integrated datasets are cataloged using **AWS Glue** and queried with **Amazon Athena**, enabling scalable SQL-based exploration and validation on top of the data lake.

---

## Exploratory Data Analysis

The `EDA/` directory contains notebooks used to:
- Profile and document the raw flight and weather datasets.
- Query the data lake/warehouse using Athena/Spark SQL.
- Visualize delay trends, seasonal patterns, and weather correlations to inform feature engineering.

---

## Modeling (Coming soon)


---

## References

- [U.S. Bureau of Transportation Statistics](https://www.transtats.bts.gov/) for flight delay data.
- [Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/) for historical airport weather data.
