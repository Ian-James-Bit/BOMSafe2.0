import os
from src.API.trustedparts import request
import pytest
from dotenv import load_dotenv

def test_send_get_request(real_variables):
    # Create a sample payload for testing
    load_dotenv(".env.test")
    payload = request.create_get_request(real_variables, os.getenv("MY_SECRET_API_KEY"), os.getenv("MY_SECRET_COMPANY_ID"))
    response = request.send_get_request(payload)
    assert isinstance(response, dict)
    assert isinstance(response["PartResults"], list)
    assert len(response["PartResults"]) > 0
    assert response["PartResults"][0]["PartNumber"] == "BAT54BRW-7-F"
    assert "Distributors" in response["PartResults"][0]

def test_create_get_request(variables):
    test_payload = request.create_get_request(variables, "fake_test_key", "fake_test_id")
    assert test_payload == {
            "CompanyId": "fake_test_id",
            "ApiKey": "fake_test_key",
            "Queries": [{"SearchToken": "12345"}, {"SearchToken": "67890"}],
            "IsCrawler": False,
            "LanguageCode": "en",
            "CountryCode": "US",
            "CurrencyCode": "USD",
            "Distributors": ["Supplier A", "Supplier B"],
            "InStockOnly": False,
            "ExactMatch": False,
            "UseCachedData": False,
            "UserAgent": "BOMSAFE2.0 1A",
        }

def test_load_API_key(monkeypatch):
    monkeypatch.setenv("MY_SECRET_API_KEY", "fake_test_key")
    assert request.load_API_key() == "fake_test_key"

    monkeypatch.delenv("MY_SECRET_API_KEY", raising=False)
    #skip the load_dotenv function to avoid loading the .env file during the test
    monkeypatch.setattr("src.API.trustedparts.request.load_dotenv",lambda: None)
    with pytest.raises(ValueError):
        request.load_API_key()

def test_load_Company_ID(monkeypatch):
    monkeypatch.setenv("MY_SECRET_COMPANY_ID", "fake_test_id")
    assert request.load_Company_ID() == "fake_test_id"

    monkeypatch.delenv("MY_SECRET_COMPANY_ID", raising=False)
    #skip the load_dotenv function to avoid loading the .env file during the test
    monkeypatch.setattr("src.API.trustedparts.request.load_dotenv",lambda: None)
    with pytest.raises(ValueError):
        request.load_Company_ID()

def test_check_credentials():
    # Test with valid credentials
    load_dotenv(".env.test")
    assert request.check_credentials(os.getenv("MY_SECRET_COMPANY_ID"),os.getenv("MY_SECRET_API_KEY"))

    # Test with invalid credentials
    invalid_company_id = "invalid_test_id"
    invalid_api_key = "invalid_test_key"
    assert not request.check_credentials(invalid_company_id, invalid_api_key)