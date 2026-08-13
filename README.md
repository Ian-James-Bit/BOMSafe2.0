# BOMSafe2.0
A program that lets you access an API via python using manufacturer part numbers and supplier names to query for supplier stock and pricing data, as well as product lifecycle data for sensitive BOM excell sheets.

BOMSafe Instructions

1. Open BOMSafe.exe
2. Input your API Company ID and API Key.
2. Select your BOM Excel file.
3. Click Process BOM.
4. The processed BOM will be saved beside the original file.

The original BOM will not be modified.

# BOMSafe 2.0

BOMSafe reads an Excel BOM, retrieves supplier stock, pricing, and risk information from TrustedParts, and creates an updated Excel BOM.

## Requirements

- Python 3.12+
- Git
- TrustedParts API Company ID
- TrustedParts API Key

## Project Setup

Clone the repository:

```bash
git clone https://github.com/Ian-James-Bit/BOMSafe2.0.git
cd BOMSafe2.0
python3 -m venv virtual_environment
source virtual_environment/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m src.main
python -m pytest