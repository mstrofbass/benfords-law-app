from typing import Dict, List


def handle_upload():
    pass


def validate_file(file_data: str):
    pass


def parse_csv(file_data: str) -> List[Dict[str, str]]:
    pass


def get_cols(parsed_csv: List[Dict[str, str]]):
    if len(parsed_csv) == 0:
        raise ValueError("Parsed CSV must include at least one row.")

    return list(parsed_csv[0].keys())
