import pytest
from src.excel import reading
#test excel files for reading and writing functions with different column names and data types

@pytest.fixture
def variables():
    return {
                "12345": {
                    "row_number": 2,
                    "suppliers": [reading.Supplier(name="Supplier A", index=2)]
                },
                "67890": {
                    "row_number": 3,
                    "suppliers": [reading.Supplier(name="Supplier B", index=2)]
                }
            }