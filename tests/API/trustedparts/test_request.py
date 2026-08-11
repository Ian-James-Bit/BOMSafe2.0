from src.API.trustedparts import request
import pytest

def test_create_get_request(variables):
    payload = request.create_get_request(variables, "fake_test_key", "fake_test_id")
    assert payload == {
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
    monkeypatch.setattr(
    "src.API.trustedparts.request.load_dotenv",
    lambda: None
    )
    with pytest.raises(ValueError):
        request.load_API_key()

def test_load_Company_ID(monkeypatch):
    monkeypatch.setenv("MY_SECRET_COMPANY_ID", "fake_test_id")
    assert request.load_Company_ID() == "fake_test_id"

    monkeypatch.delenv("MY_SECRET_COMPANY_ID", raising=False)
    #skip the load_dotenv function to avoid loading the .env file during the test
    monkeypatch.setattr(
    "src.API.trustedparts.request.load_dotenv",
    lambda: None
    )
    with pytest.raises(ValueError):
        request.load_Company_ID()