from utils.formatting import format_currency

def test_format_currency():
    assert format_currency(1234.5) == 'USD 1,234.50'