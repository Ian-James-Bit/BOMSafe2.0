import openpyxl
from src.excel import reading
import pytest

#TODO: add tests for bad path, bad file, bad sheet

def test_read_excel_file(test_excel_file, test_excel_file_2, test_excel_file_3, test_excel_file_4, test_excel_file_5, variables):
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
            assert reading.read_excel_file(file) == variables
        if i in [1, 2, 3]:
            # For the the three test files after the first, we expect a ValueError to be raised
            with pytest.raises(ValueError):
                reading.read_excel_file(file)
        elif i == 4:
            # For the fifth test file, we expect bad values to be skipped and the function to return the expected data
            assert reading.read_excel_file(file) == {}
    
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

def test_is_mpn_or_supplier():
    assert reading.is_mpn_or_supplier("'MPN",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("Manufacturer Part Number 1",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("MPN - 1",reading.mpn_names) == True
    assert reading.is_mpn_or_supplier("Supplier",reading.mpn_names) == False
    assert reading.is_mpn_or_supplier("",reading.mpn_names) == False
    assert reading.is_mpn_or_supplier("'Supplier",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("Supplier Part Number 1",reading.supplier_names) == False
    assert reading.is_mpn_or_supplier("Distributor Part Number 1",reading.supplier_names) == False
    assert reading.is_mpn_or_supplier("Distributor - 1",reading.supplier_names) == True
    assert reading.is_mpn_or_supplier("MPN",reading.supplier_names) == False
    assert reading.is_mpn_or_supplier("",reading.supplier_names) == False


