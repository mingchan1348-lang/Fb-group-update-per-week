"""Manual-only publisher for an explicitly approved Facebook Page row."""
import os
from datetime import datetime, timezone

import requests

from src.sheets import all_rows, update_row


def main():
    target_id = os.environ["POST_ID"]
    row_number, row = next(
        ((n, row) for n, row in enumerate(all_rows(), start=2) if str(row.get("id")) == target_id),
        (None, None),
    )
    if not row:
        raise ValueError(f"Post id {target_id} was not found.")
    if row.get("channel") != "FACEBOOK_PAGE" or row.get("approval_status") != "APPROVED":
        raise ValueError("Only an explicitly APPROVED FACEBOOK_PAGE row can publish.")
    if not row.get("caption"):
        raise ValueError("The post has no caption.")

    endpoint = f"https://graph.facebook.com/v23.0/{os.environ['META_PAGE_ID']}/feed"
    response = requests.post(endpoint, data={
        "message": row["caption"],
        "access_token": os.environ["META_PAGE_ACCESS_TOKEN"],
    }, timeout=30)
    response.raise_for_status()
    result = response.json()
    update_row(row_number, {
        "status": "PUBLISHED",
        "published_at": datetime.now(timezone.utc).isoformat(),
        "published_url": f"https://www.facebook.com/{result['id']}",
        "error": "",
    })
    print(result["id"])


if __name__ == "__main__":
    main()
