import os
from typing import Dict, List

import requests


def _request(payload: Dict) -> Dict:
    response = requests.post(
        os.environ["GAS_WEB_APP_URL"],
        json={"secret": os.environ["GAS_SHARED_SECRET"], **payload},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Google Sheet request failed"))
    return result


def all_rows() -> List[Dict[str, str]]:
    return _request({"action": "list"})["rows"]


def update_row(row_number: int, changes: Dict[str, str]) -> None:
    _request({"action": "update", "row_number": row_number, "changes": changes})
