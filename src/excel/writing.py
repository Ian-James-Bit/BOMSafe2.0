# going to be a "convert_response" function in "API" folder that takes the response from
# whatever API we use and converts it into a dict of dicts, higher level dicts are by row 
# number (from bom dict) representing different mpns holding lower level dicts that are by 
#column index (from bom dict) representing different suppliers, holding stock, price,  ect..
import pathlib
import openpyxl
from typing import Any
def add_data_to_bom(path: pathlib.Path | str, data: dict[int, dict[int, dict[str, Any]]]) -> None:
    if(not isinstance(path, pathlib.Path | str)):
        raise ValueError("Path must be a path object or string.") 
    try:
        excel = openpyxl.load_workbook(path) 

        bom = excel.active 

        data = add_new_data_columns(bom, data)

        #mpn is row number
        for mpn in data:
            #suppplier is column index
            for supplier in data[mpn]:
                #first new column for each supplier is stock, second is price, third is product_lifecycle_status
                bom.cell(row=mpn, column=supplier+1).value = data[mpn][supplier].get("stock")
                bom.cell(row=mpn, column=supplier+2).value = data[mpn][supplier].get("price")
                bom.cell(row=mpn, column=supplier+3).value = data[mpn][supplier].get("product_lifecycle_status")
        excel.save(path)
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        raise
    finally:
        excel.close()

# creating new columns in the excel sheet next to the relevant supplier column if there is any data for that column in the response
# and updating the column indices in the data dict to reflect the new column indices in the excel sheet
def add_new_data_columns(bom, data: dict[int, dict[int, dict[str, Any]]]) -> dict[int, dict[int, dict[str, Any]]]:
    try:
        supplier_list = []
        # if there is a new unique supplier column_index in the data, add it to the list
        # because there is data for it that needs a column space to hold it in at least one row.
        # mpn is row index
        for mpn in data:
            # supplier is column index
            for supplier in data[mpn]:
                if supplier in supplier_list:
                    continue
                else:
                    supplier_list.append(supplier)
        supplier_list.sort() # in case not in order        
        # make 3 new colums for each unique column index and update the column indices
        # depending on how many columns before it were added since everything is shifted now
        i = 1
        for column_index in supplier_list:
            total = 0
            for indices in supplier_list:
                if indices < column_index:
                    total += 1

            new_column_index = column_index + 3*total
            bom.insert_cols(new_column_index + 1,3)
            #name headers of the new columns
            bom.cell(row=1, column=new_column_index +1).value = f"Stock {i}"
            bom.cell(row=1, column=new_column_index + 2).value = f"Price {i}"
            bom.cell(row=1, column=new_column_index + 3).value = f"Product Lifecycle Status {i}"
            i += 1
        # update the column indices in the data dict to reflect the new column indices in the excel sheet
        for mpn in data:
            new_mpn_value = {}
            for supplier in data[mpn]:
                for column_index in supplier_list:
                    total = 0
                    for indices in supplier_list:
                        if indices < column_index:
                            total += 1
                    new_column_index = column_index + 3*total
                    if supplier == column_index:
                        new_mpn_value[new_column_index] = data[mpn][supplier]
            data[mpn] = (new_mpn_value)
        return data
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        raise