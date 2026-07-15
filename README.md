# Perth Property Market Social Automation

An approval-first weekly content system for **Jacky Chan | Exceptional Real Estate**.

It produces a weekly Facebook Group post for **Bentley, Wilson, Waterford WA House Market (Buy, Sell or Management)**. It can also publish the same approved content to a Facebook Page and Instagram through Meta's official APIs.

## Important platform limitation

Meta no longer supports reliable new Facebook Group publishing through its public Groups API. This project therefore creates an approved **Group-ready** post that you publish manually. Page and Instagram publishing are optional and use only official Meta APIs.

## How it works

1. Add a row of verified market information to Google Sheets.
2. Run the **Generate weekly draft** GitHub Action (or wait for Monday).
3. Review the generated caption and change `approval_status` to `APPROVED`.
4. Copy the finished Group-ready post into Facebook. The sheet records that it was published.
5. Optionally run the Page/Instagram publisher for an approved row.

The generator refuses to use a metric without a source URL, source date, metric label, and metric value. This protects your reputation and reduces incorrect market claims.

## Google Sheet columns

Create a sheet named `posts` with this exact header row:

```text
id,status,channel,topic,area,source_url,source_date,metric_label,metric_value,notes,caption,approval_status,published_at,published_url,error
```

Use these values:

- `status`: `READY_FOR_DRAFT`, `DRAFT_READY`, `PUBLISHED`, `ERROR`
- `channel`: `FACEBOOK_GROUP`, `FACEBOOK_PAGE`, `INSTAGRAM`
- `approval_status`: `PENDING`, `APPROVED`, `SKIPPED`

For group posts, set `channel` to `FACEBOOK_GROUP`. The workflow will create the caption but will not attempt an unsupported automatic Group post.

## Required GitHub Secrets

| Secret | Purpose |
|---|---|
| `OPENAI_API_KEY` | Generates the channel-specific draft. |
| `GAS_WEB_APP_URL` | Google Apps Script web-app URL. |
| `GAS_SHARED_SECRET` | A long, private passphrase used only between GitHub and Apps Script. |

Optional, only for Facebook Page publishing:

| Secret | Purpose |
|---|---|
| `META_PAGE_ID` | Your Facebook Page ID. |
| `META_PAGE_ACCESS_TOKEN` | Long-lived Page access token with publishing permission. |

Never put any of these values in a code file, Google Sheet, or Git commit. `GOOGLE_SHEET_ID` is configured in Apps Script; it does not need to be a GitHub secret.

## GitHub Actions

- **Generate weekly property draft** runs Monday at 7:05 am Perth time (23:05 UTC Sunday) and can also be run manually.
- **Publish approved Facebook Page post** is manual only. It will not publish unless the selected row is explicitly approved.

GitHub's scheduler may run a few minutes late. It is appropriate for content production, not time-critical notices.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...
export GAS_WEB_APP_URL=...
export GAS_SHARED_SECRET=...
python -m src.generate_draft
```

## Before publishing a market statistic

Confirm the geography and metric type. For example, do not treat a Perth dwelling-value index, a median house price, a unit median, or an advertised-listing figure as interchangeable.
