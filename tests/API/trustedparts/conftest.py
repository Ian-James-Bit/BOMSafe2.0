import pytest
from src.excel import reading

@pytest.fixture
def real_variables():
    return {
        "BAT54BRW-7-F": {
            "row_number": 2,
            "suppliers": [reading.Supplier(name="Digi-Key", index=2)]
        }
    }