import pytest
from unittest import mock
from etl_pipeline import fetch_data_from_api, transform_data, load_data_to_s3, lambda_handler

# Mocked API response
mock_api_response = [
    {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 50000,
        "market_cap": 900000000000,
        "total_volume": 45000000000,
    },
    {
        "id": "ethereum",
        "symbol": "eth",
        "name": "Ethereum",
        "current_price": 4000,
        "market_cap": 500000000000,
        "total_volume": 30000000000,
    },
]

# Test the fetch_data_from_api function
def test_fetch_data_from_api():
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_response
        
        data = fetch_data_from_api()
        assert len(data) == 2  # Ensure we have 2 coins in the response
        assert data[0]["id"] == "bitcoin"  # Ensure the first coin's ID is "bitcoin"

# Test the transform_data function
def test_transform_data():
    transformed_data = transform_data(mock_api_response)
    
    assert len(transformed_data) == 2  # Ensure there are 2 transformed coins
    assert "price_usd" in transformed_data[0]  # Ensure transformed data has price_usd field
    assert transformed_data[0]["price_usd"] == 50000  # Check if price is transformed correctly

# Test the load_data_to_s3 function
def test_load_data_to_s3():
    with mock.patch('boto3.client') as mock_boto3:
        mock_s3 = mock_boto3.return_value
        load_data_to_s3(mock_api_response)
        
        # Check that the put_object function was called once
        mock_s3.put_object.assert_called_once_with(
            Bucket="s3-crypto-data-pipeline",
            Key="transformed/crypto_data.json",
            Body=mock.ANY  # Check if the body is passed as any data
        )

# Test the entire ETL pipeline using the lambda_handler function
def test_lambda_handler():
    event = {}
    context = {}
    
    # Mock the calls for API request and S3
    with mock.patch('requests.get') as mock_get, mock.patch('boto3.client') as mock_boto3:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_api_response
        mock_s3 = mock_boto3.return_value
        
        response = lambda_handler(event, context)
        
        # Check if the lambda_handler function returns a success status
        assert response["statusCode"] == 200
        assert "Transformed data successfully saved" in response["body"]
        
        # Verify the put_object was called to upload data to S3
        mock_s3.put_object.assert_called_once_with(
            Bucket="s3-crypto-data-pipeline",
            Key="transformed/crypto_data.json",
            Body=mock.ANY
        )