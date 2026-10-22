# Contributing

Thanks for helping improve these docs.

- **Found a mistake in a guide or example?** [Open an issue](../../issues/new/choose) or send a pull request.
- **Problem with your account, billing or a specific API call?** Don't open an issue. Contact [support](https://salvagealert.com/contact) and include the `request_id`.
- **Want an example in another language?** PRs are welcome. Keep it dependency-free where you can, read the key from `SALVAGEALERT_KEY`, and add it to the table in [`examples/README.md`](examples/README.md).

## Never commit a key

Use `sa_live_xxxxxxxx…` placeholders. If you leak a real key, revoke it at once at [salvagealert.com/app/api](https://salvagealert.com/app/api).

## Spec

`openapi/openapi.json` is a mirror of the live spec. Don't edit it by hand. Run `scripts/sync-openapi.sh` to refresh it, along with the Postman collection and `CHANGELOG.md`.
