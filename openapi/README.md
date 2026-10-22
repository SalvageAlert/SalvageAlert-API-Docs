# OpenAPI spec

`openapi.json` mirrors the live contract at **https://salvagealert.com/api/v1/openapi.json** (OpenAPI 3.0).

- **Postman / Insomnia / Bruno:** import the file directly, or use the ready-made [Postman collection](../postman).
- **Swagger UI:** `npx @redocly/cli preview-docs openapi/openapi.json`, or paste the URL into [editor.swagger.io](https://editor.swagger.io).
- **Typed clients:**

  ```bash
  npx @openapitools/openapi-generator-cli generate -i openapi/openapi.json -g typescript-fetch -o sdk/ts
  npx @openapitools/openapi-generator-cli generate -i openapi/openapi.json -g python -o sdk/python
  ```

The spec has three extensions worth reading: `x-conventions` (timestamp units, booleans, casing, money), `x-deprecation-policy` and `x-changelog`.
