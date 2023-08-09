import os
import pytest

from src.handlers import handle_upload, parse_csv, get_cols

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def get_data_file(fn: str) -> str:
    return os.path.join(DATA_DIR, fn)


class TestParseCSV:
    def test_valid_csv(self):
        csv_data = get_data_file("validcsv.csv")

        expected = [
            {
                "col1": "test1",
                "col2": "test2",
                "col3": "test3",
            },
            {
                "col1": "test4",
                "col2": "test5",
                "col3": "test6",
            },
        ]

        actual = parse_csv(csv_data)
        print(actual)
        assert actual == expected

    def test_empty_field(self):
        csv_data = get_data_file("empty-fields.csv")

        expected = [
            {
                "col1": "test1",
                "col2": "test2",
                "col3": "test3",
            },
            {
                "col1": "test4",
                "col2": "",
                "col3": "",
            },
        ]

        actual = parse_csv(csv_data)
        assert actual == expected

    def test_missing_column(self):
        csv_data = get_data_file("missing-columns.csv")

        expected = [
            {
                "col1": "test1",
                "col2": "test2",
                "col3": "test3",
            },
            {
                "col1": "test4",
                "col2": "",
                "col3": None,
            },
        ]

        actual = parse_csv(csv_data)

        assert actual == expected


class TestGetCols:
    def test_get_cols(self):
        parsed_csv = [{"col1": "foo", "col2": "bar"}, {"col1": "baz", "col2": "bat"}]

        expected = ["col1", "col2"]
        actual = get_cols(parsed_csv)

        assert actual == expected

    def test_no_rows(self):
        input = []

        with pytest.raises(ValueError):
            get_cols(input)
