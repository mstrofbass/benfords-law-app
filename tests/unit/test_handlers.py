import pytest

from src.handlers import handle_upload, validate_file, parse_csv, get_cols


class TestGetCols:
    def test_get_cols(self):
        input = [{"col1": "foo", "col2": "bar"}, {"col1": "baz", "col2": "bat"}]

        expected = ["col1", "col2"]
        actual = get_cols(input)

        assert actual == expected

    def test_no_rows(self):
        input = []

        with pytest.raises(ValueError):
            get_cols(input)
