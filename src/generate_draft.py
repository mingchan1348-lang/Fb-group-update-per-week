"""Create one factual, community-led weekly post from a verified Sheet row."""
import json
from datetime import date

from openai import OpenAI

from src.sheets import all_rows, update_row


REQUIRED_EVIDENCE = ("source_url", "source_date", "metric_label", "metric_value")


def row_is_ready(row):
    return row.get("status") == "READY_FOR_DRAFT" and row.get("channel") == "FACEBOOK_GROUP"


def validate(row):
    missing = [field for field in REQUIRED_EVIDENCE if not str(row.get(field, "")).strip()]
    if missing:
        raise ValueError("Missing verified evidence: " + ", ".join(missing))


def draft(row):
    prompt = f"""Write one English Facebook Group post for Bentley, Wilson, Waterford WA House Market (Buy, Sell or Management).

Brand: Jacky Chan, Exceptional Real Estate.
Audience: local owners, buyers, and investors.
Tone: professional, factual, friendly, community-led, not pushy, no emojis.
Do not add any number or claim that is not supplied below. Make clear the date and metric exactly as supplied. Use one gentle question to encourage comments. Finish with: 'Message Jacky from Exceptional Real Estate if you would like a complimentary local price update.'

Verified information:
Topic: {row['topic']}
Area: {row['area']}
Metric: {row['metric_label']}
Value: {row['metric_value']}
Source date: {row['source_date']}
Source: {row['source_url']}
Context: {row.get('notes', '')}

Return only the final post text, including 3-5 relevant hashtags."""
    response = OpenAI().responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text.strip()


def main():
    for index, row in enumerate(all_rows(), start=2):
        if not row_is_ready(row):
            continue
        try:
            validate(row)
            update_row(index, {
                "caption": draft(row),
                "status": "DRAFT_READY",
                "approval_status": "PENDING",
                "error": "",
            })
            print(f"Draft created for row {index} ({row.get('id', 'no id')}).")
        except Exception as exc:
            update_row(index, {"status": "ERROR", "error": str(exc)})
            raise
        return
    print("No READY_FOR_DRAFT Facebook Group rows found.")


if __name__ == "__main__":
    main()
