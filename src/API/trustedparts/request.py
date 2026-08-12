import os
from typing import Any
from dotenv import load_dotenv
import requests

url = "https://api.trustedparts.com/v2/search"
headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

def send_get_request(payload: dict) -> dict:
    try:
        response = requests.post(url, headers = headers, json = payload)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# variables is a dictionary of MPNs and their corresponding suppliers that we get from excel file
def create_get_request(variables: dict[str,dict[str,int | Any]], key: str, ID: str) -> dict:
    if not variables:
        raise ValueError("The 'variables' dictionary is empty. Please provide valid data.")
    if(not isinstance(key, str)):
        raise ValueError("Key must be a string. Please provide a valid API key.") 
    if(not isinstance(ID, str)):
        raise ValueError("ID must be a string. Please provide a valid Company ID.")
    try:
        MPNs = []
        Queries = []
        Distributors = []
        for mpn in variables:
            #dont add duplicates
            if not mpn in MPNs:
                MPNs.append(mpn)
                query = {
                    "SearchToken": mpn,
                }
                Queries.append(query)
            for attribute in variables[mpn]:
                if attribute == "suppliers":
                    for supplier in variables[mpn][attribute]:
                        if not supplier.name in Distributors:
                            Distributors.append(supplier.name)
        return {
            "CompanyId": ID,
            "ApiKey": key,
            "Queries": Queries,
            "IsCrawler": False,
            "LanguageCode": "en",
            "CountryCode": "US",
            "CurrencyCode": "USD",
            "Distributors": Distributors,
            "InStockOnly": False,
            "ExactMatch": False,
            "UseCachedData": False,
            "UserAgent": "BOMSAFE2.0 1A",
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def load_API_key() -> str:
    try:
        # Explicitly load the environment variables from the .env file
        load_dotenv()
        # Retrieve the secret key
        api_key = os.getenv("MY_SECRET_API_KEY")
        if not api_key:
            raise ValueError("API key missing. Check your local .env file.")
        return api_key
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    
def load_Company_ID() -> str:
    try:
        # Explicitly load the environment variables from the .env file
        load_dotenv()
        # Retrieve the secret key
        company_ID = os.getenv("MY_SECRET_COMPANY_ID")
        if not company_ID:
            raise ValueError("Company ID missing. Check your local .env file.")
        return company_ID
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
