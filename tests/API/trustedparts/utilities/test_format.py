from src.API.trustedparts.utilities import format

def test_format_data(example_response, variables, expected_output):
    result = format.format_data(example_response, variables)
    assert result == expected_output