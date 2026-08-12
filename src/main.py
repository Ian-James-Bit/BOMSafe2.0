import pathlib
import shutil

from src.excel.reading import read_excel_file
from src.API.trustedparts import request
from src.API.trustedparts.utilities import format
from src.excel.writing import add_data_to_bom

def main():
    input_path = pathlib.Path("data/input/Test_Bom.xlsx")
    output_path = pathlib.Path("data/output/Test_Bom.xlsx")

    shutil.copy2(input_path, output_path)

    variables = read_excel_file(input_path)
    payload = request.create_get_request(variables, request.load_API_key(), request.load_Company_ID())
    data = request.send_get_request(payload)
    data = format.format_data(data, variables)
    add_data_to_bom(output_path, data)
    print("Data added to BOM successfully.")

if __name__ == "__main__":
    main()