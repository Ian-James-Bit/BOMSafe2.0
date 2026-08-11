import openpyxl
from src.excel import writing
import pytest
from pathlib import Path

def test_add_data_to_bom(test_excel_file, test_excel_file_6):
    for i in range(2):
        if i == 0:
            data = {
                2: {2: {"stock": 10, "price": 5.99, "product_lifecycle_status": "Active"}},
                3: {2: {"stock": 20, "price": 9.99, "product_lifecycle_status": "Discontinued"}},
            }
            writing.add_data_to_bom(test_excel_file, data)
            file = test_excel_file
            workbook = openpyxl.load_workbook(file)
            bom = workbook.active
            assert bom.cell(row=2, column=3).value == 10
            assert bom.cell(row=2, column=4).value == 5.99
            assert bom.cell(row=2, column=5).value == "Active"
            assert bom.cell(row=3, column=3).value == 20
            assert bom.cell(row=3, column=4).value == 9.99
            assert bom.cell(row=3, column=5).value == "Discontinued"
        if  i == 1:
            data = {
                2: {2: {"stock": 10, "price": 5.99, "product_lifecycle_status": "Active"}, 4: {"stock": 15, "price": 7.99, "product_lifecycle_status": "Active"}},
                3: {2: {"stock": 20, "price": 9.99, "product_lifecycle_status": "Discontinued"}, 4: {"stock": 25, "price": 12.99, "product_lifecycle_status": "Discontinued"}},
            }
            writing.add_data_to_bom(test_excel_file_6, data)
            file = test_excel_file_6
            workbook = openpyxl.load_workbook(file)
            bom = workbook.active
            assert bom.cell(row=2, column=3).value == 10
            assert bom.cell(row=2, column=4).value == 5.99
            assert bom.cell(row=2, column=5).value == "Active"
            assert bom.cell(row=2, column=8).value == 15
            assert bom.cell(row=2, column=9).value == 7.99
            assert bom.cell(row=2, column=10).value == "Active"
            assert bom.cell(row=3, column=3).value == 20
            assert bom.cell(row=3, column=4).value == 9.99
            assert bom.cell(row=3, column=5).value == "Discontinued"
            assert bom.cell(row=3, column=8).value == 25
            assert bom.cell(row=3, column=9).value == 12.99
            assert bom.cell(row=3, column=10).value == "Discontinued"

def test_add_new_data_columns(test_excel_file, test_excel_file_6):
    for i in range(2):
        if i == 0:
            file = test_excel_file
            workbook = openpyxl.load_workbook(file)
            bom = workbook.active

            # Create a sample data dictionary to add new columns
            data = {
                2: {2: {"stock": 10, "price": 5.99, "product_lifecycle_status": "Active"}},
                3: {2: {"stock": 20, "price": 9.99, "product_lifecycle_status": "Discontinued"}},
            }

            updated_data = writing.add_new_data_columns(bom, data)

            # Check if new columns were added and headers are correct
            assert bom.cell(row=1, column=3).value == "Stock 1"
            assert bom.cell(row=1, column=4).value == "Price 1"
            assert bom.cell(row=1, column=5).value == "Product Lifecycle Status 1"

            #check column indeces are same
            for row in data:
                for key in data[row]:
                    for updated_key in updated_data[row]:
                        assert key == updated_key
        else:
            for i in range(2):
                file = test_excel_file_6
                workbook = openpyxl.load_workbook(file)
                bom = workbook.active

                if i == 0:
                    data = {
                        2: {2: {"stock": 10, "price": 5.99, "product_lifecycle_status": "Active"}, 4: {"stock": 15, "price": 7.99, "product_lifecycle_status": "Active"}},
                        3: {2: {"stock": 20, "price": 9.99, "product_lifecycle_status": "Discontinued"}, 4: {"stock": 25, "price": 12.99, "product_lifecycle_status": "Discontinued"}},
                    }

                    updated_data = writing.add_new_data_columns(bom, data)

                    # Check if new columns were added and headers are correct
                    assert bom.cell(row=1, column=3).value == "Stock 1"
                    assert bom.cell(row=1, column=4).value == "Price 1"
                    assert bom.cell(row=1, column=5).value == "Product Lifecycle Status 1"
                    assert bom.cell(row=1, column=8).value == "Stock 2"
                    assert bom.cell(row=1, column=9).value == "Price 2"
                    assert bom.cell(row=1, column=10).value == "Product Lifecycle Status 2"

                    #check if column indeces are updated correctly
                    for row in updated_data:
                        for key in data[row]:
                            if key == 4:
                                assert key == data[row][key]+3
                else:
                    #if no data was found of a specific supplier before another supplier, then the column index should be the same as before
                    data = {
                        2: {4: {"stock": 15, "price": 7.99, "product_lifecycle_status": "Active"}},
                        3: {4: {"stock": 25, "price": 12.99, "product_lifecycle_status": "Discontinued"}},
                    }

                    updated_data = writing.add_new_data_columns(bom, data)
                    
                    #check if new columns are headers are correct
                    assert bom.cell(row=1, column=5).value == "Stock 1"
                    assert bom.cell(row=1, column=6).value == "Price 1"
                    assert bom.cell(row=1, column=7).value == "Product Lifecycle Status 1"

                    #check column indeces are same
                    for row in data:
                        for key in data[row]:
                            for updated_key in updated_data[row]:
                                assert key == updated_key
