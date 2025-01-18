# Cryptocurrency ETL Pipeline

This project demonstrates an ETL pipeline to extract cryptocurrency data from the CoinGecko API, transform it, and store it in AWS S3.

## Features
- Automated Data Extraction: Retrieves data for the top 10 crypto by mkt capitalization.
- Data Transformation: Filters and restructures data into a simplified and readable format.
- AWS Integration: Stores raw and transformed data in an AWS S3.
- Unit Testing: Includes test cases to ensure the transformation logic is correct.

## Technologies Used
- Programming Language: Python
- AWS Services:
    - S3 for data storage
- External Libraries:
    - boto3 for AWS interaction
    - requests for API calls
    - pytests for testing

## Setup Instructions
1. Prerequisites
- Python 3.7 or higher
- AWS account with S3 bucket configured

2. Clone the Repo to your local machine:
git clone https://github.com/tmori94/crypto-etc-project-aws.git
cd crypto-etl-project

3. Set up a VENV
- Steps for MacOS:
    python3 -m venv venv
    source venv/bin/activate

4. Install Dependencies:
    pip install -r requirements.txt

5. Configure AWS:
    aws configure

6. Run the ETL Pipeline:
    python etl_pipeline.py

## Testing the Pipeline
    pytest tests/

## Transformed Data sample
[
  {
    "id": "bitcoin",
    "name": "Bitcoin",
    "symbol": "btc",
    "price_usd": 50000,
    "market_cap_usd": 900000000000,
    "volume_usd": 45000000000
  },
  {
    "id": "ethereum",
    "name": "Ethereum",
    "symbol": "eth",
    "price_usd": 4000,
    "market_cap_usd": 500000000000,
    "volume_usd": 30000000000
  }
]

## Transformation process is purely demonstrative. Several additional transformation could still be applied. 