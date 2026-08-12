import pathlib
import shutil

from src.excel.reading import read_excel_file
from src.API.trustedparts import request
from src.API.trustedparts.utilities import format
from src.excel.writing import add_data_to_bom

def main():
    # Define the input and output directories
    input_dir = pathlib.Path("data/input")
    output_dir = pathlib.Path("data/output")

    # Find the first .xlsx file in the input directory
    # Next(..., None) safely returns None if no file is found
    input_path = next(input_dir.glob("*.xlsx"), None)

    if input_path:
        # Reuse the exact same file name for the output path
        output_path = output_dir / input_path.name
    else:
        print("No Excel file found in the input directory.")
        return

    shutil.copy2(input_path, output_path)

    variables = read_excel_file(input_path)
    payload = request.create_get_request(variables, request.load_API_key(), request.load_Company_ID())
    data = request.send_get_request(payload)
    data = format.format_data(data, variables)
    add_data_to_bom(output_path, data)
    print("Data added to BOM successfully.")

if __name__ == "__main__":
    main()