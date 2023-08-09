import csv
import json
import os

from typing import Dict, List

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "source"
)
ANALYSES_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "analyses"
)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(ANALYSES_FOLDER):
    os.makedirs(ANALYSES_FOLDER)


class InvalidFileError(Exception):
    def __init__(self, errors):
        self.errors = errors


def handle_upload(fp: str, csv_delimiter: str) -> List[str]:
    print(csv_delimiter)
    csv_data = parse_csv(fp, csv_delimiter)

    return get_cols(csv_data)


def handle_analyze(filename: str, column: str, delimiter: str):
    file_to_process = os.path.join(UPLOAD_FOLDER, filename)
    csv_data = parse_csv(file_to_process, delimiter)

    count_tuples, errors = process_column(csv_data, column)

    save_analysis(filename, count_tuples, errors)

    return count_tuples, errors


def save_analysis(filename: str, count_tuples: List, errors: List):
    analysis_path = os.path.join(ANALYSES_FOLDER, filename + ".json")
    with open(analysis_path, "wt") as fout:
        json.dump({"count_tuples": count_tuples, "errors": errors}, fout)


def to_pct(val):
    return round(val * 100)


def process_column(csv_data: List[Dict[str, str]], column: str):
    counts = {}
    errors = []

    for idx, row in enumerate(csv_data):
        val = row.get(column)

        if not val or val.strip() == "":
            errors.append(f"Missing value in row {idx}")
            continue

        try:
            first_digit_str = val[0]
            first_digit = int(first_digit_str)

            if not first_digit:
                raise ValueError("Invalid value.")

            if first_digit_str not in counts:
                counts[first_digit_str] = 0

            counts[first_digit_str] += 1
        except:
            errors.append(f"Invalid value {val} in row {idx}")

    count_tuples = sorted(list(counts.items()), key=lambda x: x[0])
    total_count = sum([t[1] for t in count_tuples])
    count_tuples = [(t[0], t[1], to_pct(t[1] / total_count)) for t in count_tuples]

    return count_tuples, errors


def parse_csv(file_path: str, csv_delimiter: str = ",") -> List[Dict[str, str]]:
    with open(file_path, "rt") as fin:
        reader = csv.DictReader(
            fin, skipinitialspace=True, strict=True, delimiter=csv_delimiter
        )
        return [row for row in reader]


def get_cols(parsed_csv: List[Dict[str, str]]):
    if len(parsed_csv) == 0:
        raise ValueError("Parsed CSV must include at least one row.")

    return list(parsed_csv[0].keys())
