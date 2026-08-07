import openpyxl
from typing import Any
from dataclasses import dataclass
from typing import Tuple

# TODO: add more asserts once more test excel sheets are added to relevant test
from src.excel import reading
import pytest
from pathlib import Path
from openpyxl import load_workbook

@pytest.fixture
def test_excel_file():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["MPN", "Supplier", "Description"])
    sheet.append(["12345", "Supplier A", "Test Description 1"])
    sheet.append(["67890", "Supplier B", "Test Description 2"])
    workbook.save(test_file_path)
    yield test_file_path
    test_file_path.unlink()  # Clean up the temporary file after the test

def test_is_mpn_or_supplier():
    assert reading.is_mpn_or_supplier("'MPN",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("Manufacture Part Number 1",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("MPN - 1",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("Supplier",reading.mpn_names) == False
    assert reading.is_mpn_or_supplier("",reading.mpn_names) == False
    assert reading.is_mpn_or_supplier("'Supplier",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("Supplier Number 1",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("Distributor Number 1",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("Distributor - 1",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("MPN",reading.supplier_names) == False
    assert reading.is_mpn_or_supplier("",reading.supplier_names) == False

#TODO: add an assert for the case where there is no MPN column and no supplier column
def test_relevant_column_indices(test_excel_file):
    workbook = load_workbook(test_excel_file)
    sheet = workbook.active
    mpn_index, supplier_indices = reading.relevant_column_indices(sheet)
    assert mpn_index == 1  # MPN is in the first column
    assert supplier_indices == [2]  # Supplier is in the second column

#TODO: fix this
def test_read_excel_file(test_excel_file):
    load_workbook(test_excel_file)
    assert reading.read_excel_file("test_excel.xlsx") == [
        {
            "mpn": "12345",
            "row_number": 2,
            "suppliers": ["Supplier A",2]
        },
        {
            "mpn": "67890",
            "row_number": 3,
            "suppliers": ["Supplier B",2]
        }
    ]