# Security

If you believe you've found a security issue in the SalvageAlert API or website, **please don't open a public issue.** Report it privately through [salvagealert.com/contact](https://salvagealert.com/contact) or email support@salvagealert.com with "Security" in the subject.

Please include:

- What you found and its impact
- Steps to reproduce, with any `request_id` values
- Your contact details for follow-up

We'll acknowledge your report, keep you updated while we fix it, and credit you if you'd like.

## If your API key leaks

Revoke it immediately with `DELETE /v1/api-keys/{id}`, or with **Rotate** at [salvagealert.com/app/api](https://salvagealert.com/app/api). Revoked keys stop working at once.
