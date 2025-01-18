import json
import boto3
import requests

# Function to fetch data from the CoinGecko API
def fetch_data_from_api():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error if the API call fails
    return response.json()  # Parse and return the JSON response

# Function to transform the data into the desired format
def transform_data(data):
    transformed_data = []
    for coin in data:
        transformed_coin = {
            "id": coin["id"],
            "name": coin["name"],
            "symbol": coin["symbol"],
            "price_usd": coin["current_price"],
            "market_cap_usd": coin["market_cap"],
            "volume_usd": coin["total_volume"],
        }
        transformed_data.append(transformed_coin)
    return transformed_data

# Function to load the transformed data into S3
def load_data_to_s3(transformed_data):
    s3 = boto3.client("s3")
    bucket_name = "s3-crypto-data-pipeline"  # Your S3 bucket name
    file_key = "transformed/crypto_data.json"  # Path for storing transformed data

    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(transformed_data),
    )

# Lambda handler function that orchestrates the ETL process
def lambda_handler(event, context):
    try:
        # Step 1: Extract data from the API
        data = fetch_data_from_api()

        # Step 2: Transform the data
        transformed_data = transform_data(data)

        # Step 3: Load the transformed data to S3
        load_data_to_s3(transformed_data)

        # Step 4: Return success response
        return {
            "statusCode": 200,
            "body": "Transformed data successfully saved to S3"
        }

    except Exception as e:
        # Handle any error that occurs during the ETL process
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }