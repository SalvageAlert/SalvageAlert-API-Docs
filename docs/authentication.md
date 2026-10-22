# Authentication and keys

Every `/v1` request carries a key in the `Authorization` header:

```
Authorization: Bearer sa_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keys are stored hashed. We can't show you a key again after it's issued, so a lost key gets revoked and replaced.

## Managing keys

You can manage keys in the [dashboard](https://salvagealert.com/app/api) or over the API. All of these calls are free.

| Call | Effect |
|---|---|
| `GET /api-keys` | List your keys (prefix, label, created, last used) |
| `POST /api-keys` | Mint an additional key. The secret is in the response **once** |
| `DELETE /api-keys/{id}` | Revoke one key |
| `POST /api-keys/rotate` | Revoke **every** key on the account and issue one new key |

`rotate` affects the whole account. If you run several services, give each one its own key with `POST /api-keys`, and revoke a single key when it leaks.

## Project URL

Each account must name the project its keys are used for, on the dashboard. If one is missing, every response carries an `X-Salvagealert-Warning` header ahead of the deadline. A key revoked for this reason answers `401 key_revoked_missing_project_url`. Set the URL, then rotate.

## Authentication errors

| Code | Status | Meaning |
|---|:-:|---|
| `missing_credentials` | 401 | No `Authorization` header, or it's malformed |
| `invalid_credentials` | 401 | The key is unknown or has been revoked |
| `account_inactive` | 401 | The key is valid but the account isn't. Rotating won't help, so contact support |
| `api_disabled` | 403 | The account isn't enrolled for API access |

## Good practice

- Keep keys on your server. Never ship one in a browser bundle or a mobile app binary.
- Use one key per environment (dev, staging, prod) so you can revoke one without the others.
- Log the `X-Request-Id` of every failed call.
