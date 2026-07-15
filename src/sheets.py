import json
import os
from typing import Dict, List

import gspread
from google.oauth2.service_account import Credentials


SHEET_NAME = "posts"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def worksheet():
    raw_credentials = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    credentials = Credentials.from_service_account_info(
        json.loads(raw_credentials), scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client.open_by_key(os.environ["GOOGLE_SHEET_ID"]).worksheet(SHEET_NAME)


def all_rows() -> List[Dict[str, str]]:
    return worksheet().get_all_records()


def update_row(row_number: int, changes: Dict[str, str]) -> None:
    sheet = worksheet()
    headers = sheet.row_values(1)
    updates = []
    for field, value in changes.items():
        if field not in headers:
            raise ValueError(f"Missing required column: {field}")
        column = headers.index(field) + 1
        updates.append({"range": gspread.utils.rowcol_to_a1(row_number, column), "values": [[value]]})
    sheet.batch_update(updates)
