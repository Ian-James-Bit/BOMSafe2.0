import openpyxl
from typing import Any
from dataclasses import dataclass
from typing import Tuple

# TODO: add more asserts once more test excel sheets are added to relevant test
from src.excel import reading
import pytest
from pathlib import Path

@pytest.fixture
def test_excel_file():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["MPN", "Supplier", "Description"])
    sheet.append([12345, "Supplier A", "Test Description 1"])
    sheet.append([67890, "Supplier B", "Test Description 2"])
    workbook.save(test_file_path)
    yield test_file_path
    test_file_path.unlink()  # Clean up the temporary file after the test

@pytest.fixture
def test_excel_file_2():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_2_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["MPN", "Random Name", "Description"])
    sheet.append([12345, "Supplier A", "Test Description 1"])
    sheet.append([67890, "Supplier B", "Test Description 2"])
    workbook.save(test_file_path)
    yield test_file_path
    test_file_path.unlink()  # Clean up the temporary file after the test

@pytest.fixture
def test_excel_file_3():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_3_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["Random Number", "Supplier", "Description"])
    sheet.append([12345, "Supplier A", "Test Description 1"])
    sheet.append([67890, "Supplier B", "Test Description 2"])
    workbook.save(test_file_path)
    yield test_file_path
    test_file_path.unlink()  # Clean up the temporary file after the test

@pytest.fixture
def test_excel_file_4():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_4_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["Random Number", "Random Name", "Description"])
    sheet.append([12345, "Supplier A", "Test Description 1"])
    sheet.append([67890, "Supplier B", "Test Description 2"])
    workbook.save(test_file_path)
    yield test_file_path
    test_file_path.unlink()  # Clean up the temporary file after the test

@pytest.fixture
def test_excel_file_5():
    # Create a temporary Excel file for testing
    test_file_path = Path(__file__).parent / "test_5_excel.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "TestSheet"
    sheet.append(["MPN", "Supplier", "Description"])
    sheet.append(["nioe", None, "Test Description 1"])
    sheet.append([None, 434, "Test Description 2"])
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
def test_relevant_column_indices(test_excel_file, test_excel_file_2, test_excel_file_3, test_excel_file_4, test_excel_file_5):
    # Test with the first Excel file
    for i in range(5):
        if i == 0:
            file = test_excel_file
        elif i == 1:
            file = test_excel_file_2
        elif i == 2:
            file = test_excel_file_3
        elif i == 3:
            file = test_excel_file_4
        else:
            file = test_excel_file_5

        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        mpn_index, supplier_indices = reading.relevant_column_indices(sheet)

        if i == 0:
            assert mpn_index == 1  # MPN is in the first column
            assert supplier_indices == [2]  # Supplier is in the second column
        elif i == 1:
            assert mpn_index == 1  # MPN is in the first column
            assert supplier_indices == []  # No supplier column found
        elif i == 2:
            assert mpn_index is None  # No MPN column found
            assert supplier_indices == [2]  # Supplier is in the second column
        elif i == 3:
            assert mpn_index is None  # No MPN column found
            assert supplier_indices == []  # No supplier column found
        else:
            assert mpn_index == 1  # MPN is in the first column
            assert supplier_indices == [2]  # Supplier is in the second column

#TODO: fix this
def test_read_excel_file(test_excel_file, test_excel_file_2, test_excel_file_3, test_excel_file_4, test_excel_file_5):
    for i in range(5):
        if i == 0:
            file = test_excel_file
        elif i == 1:
            file = test_excel_file_2
        elif i == 2:
            file = test_excel_file_3
        elif i == 3:
            file = test_excel_file_4
        elif i == 4:
            file = test_excel_file_5
        if(i == 0):
            # For the first test file, we expect the function to return the expected data
            assert reading.read_excel_file(file) == [
                {
                    "mpn": 12345,
                    "row_number": 2,
                    "suppliers": [reading.Supplier(name="Supplier A", index=2)]
                },
                {
                    "mpn": 67890,
                    "row_number": 3,
                    "suppliers": [reading.Supplier(name="Supplier B", index=2)]
                }
            ]
        if i in [1, 2, 3]:
            # For the the three test files after the first, we expect a ValueError to be raised
            with pytest.raises(ValueError):
                reading.read_excel_file(file)
        elif i == 4:
            # For the fifth test file, we expect bad values to be skipped and the function to return the expected data
            assert reading.read_excel_file(file) == []
    