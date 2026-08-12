from src.API.trustedparts.utilities import format

def test_format_data(example_response, variables, expected_output):
    result = format.format_data(example_response, variables)
    assert result == expected_output

def test_normalize_supplier_name():
    assert format.normalize_supplier_name("Supplier-Name") == "suppliername"
    assert format.normalize_supplier_name("Supplier Name") == "suppliername"
    assert format.normalize_supplier_name("Supplier123") == "supplier"
    assert format.normalize_supplier_name("SUPPLIER") == "supplier"