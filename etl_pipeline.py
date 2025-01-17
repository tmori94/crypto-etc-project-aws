import boto3
import json
import requests

# AWS Configurations
s3 = boto3.client("s3")
BUCKET_NAME = "s3-crypto-data-pipeline"  # AWS S3 bucket name
RAW_KEY = "raw/crypto_data.json"
TRANSFORMED_KEY = "transformed/crypto_data_transformed.json"

def extract_crypto_data():
    """
    Extracts cryptocurrency data from CoinGecko API.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def transform_data(data):
    """
    Transforms the raw cryptocurrency data.
    Filters and restructures the data.
    """
    return [
        {"name": item["name"], "symbol": item["symbol"], "price": item["current_price"]}
        for item in data
    ]

def load_to_s3(data, key):
    """
    Loads data to an S3 bucket.
    """
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data),
    )
    print(f"Data successfully saved to {BUCKET_NAME}/{key}")

if __name__ == "__main__":
    print("Starting ETL process...")

    # Extract
    print("Extracting data...")
    raw_data = extract_crypto_data()

    # Load Raw Data to S3
    print("Loading raw data to S3...")
    load_to_s3(raw_data, RAW_KEY)

    # Transform
    print("Transforming data...")
    transformed_data = transform_data(raw_data)

    # Load Transformed Data to S3
    print("Loading transformed data to S3...")
    load_to_s3(transformed_data, TRANSFORMED_KEY)

    print("ETL process completed.")