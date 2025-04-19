<!--
SPDX-FileCopyrightText: 2025 Ethersecurity Inc.

SPDX-License-Identifier: MPL-2.0
-->

<!-- Author: Shohei KAMON <cameong@stir.network> -->

# fireblocks-cli: `configure` Command Specification (Extended)

This document outlines the behavior and structure of the `configure` subcommand group in the `fireblocks-cli` tool, including extended specifications and validation behavior.

---

## ✅ General Behavior

- The `api_secret_key` field uses `value` instead of `path` regardless of its type.
- The config file follows TOML format located at `~/.config/fireblocks-cli/config.toml`.

---

## `configure init`

- Recursively creates `~/.config/fireblocks-cli/keys` if not present.
- Generates a minimal `~/.config/fireblocks-cli/config.toml` template if not found:

```toml
[default]
api_id = ""
api_secret_key = { type = "file", value = "" }

# [example]
# api_id = "abcd-1234-api-key"
# api_secret_key = { type = "file", value = "~/.config/fireblocks-cli/keys/abcd.key" }
```

- If `[default]` section does not contain both `api_id` and `api_secret_key`, falls back to `~/.config/fireblocks-cli/credentials`.

---

## `configure gen-key`

- Creates a new private key under `~/.config/fireblocks-cli/keys`.
- Supported algorithms: `rsa2048`, `rsa4096`, `ed25519` (default).
- Key names:
  - 12-character base32 string (lowercase alphanumerics only)
  - Files:
    - `{key_name}.key`
    - `{key_name}.csr`
- Prevents key name collision.
- Prompts for organization (O=...) for CSR subject.
- CSR subject fields are extendable via CLI options.
- Optional: key name can be provided; collision causes error.
- Files are saved with permission mode `0600`.

---

## `configure list`

- Validates both `config.toml` and `credentials` files before proceeding.
- Displays all available `[profile]` names from:
  - `~/.config/fireblocks-cli/credentials`
  - `~/.config/fireblocks-cli/config.toml`
- Each profile includes a source tag:
  ```
  default (from credentials)
  example (from config)
  ```
- Secret keys or key names are **not** shown.

---

## `configure edit`

- Opens `~/.config/fireblocks-cli/config.toml` using the system's `$EDITOR`.

---

## `configure validate`

- Performs TOML syntax check on both `config.toml` and `credentials`.
- Does not require `api_id` or `api_secret_key` to be present.
- If either exists:
  - `api_id` must be a string.
  - `api_secret_key` must contain both:
    - `type` as a string
    - `value` as a string
- Key file paths listed in `value` must have file permission `0600`, or validation fails.
- Duplicate profile names across config and credentials raise an error, except for `default` (credentials takes precedence).
- Logs will indicate exact error fields and line numbers.
- Validation logic is modular and designed for extensibility.

---

## `configure add`

- Adds a new API profile to `~/.config/fireblocks-cli/config.toml`.
- Arguments:
  - `name` (profile name)
  - `api_id`
- Internally calls `gen-key` and generates both `.key` and `.csr` files.
- Displays paths to key and CSR.
- Appends profile to the **end of config file** without reformatting.

```toml
[{name}]
api_id = "{api_id}"
api_secret_key = { type = "file", value = "{path}" }
```

- Will not overwrite existing profiles.


---

## 🔄 Additional Clarification Based on Unit Test Design

### `configure list` (clarification)
- Profile names listed from both config and credentials.
- Source shown explicitly: `example (from config)` or `default (from credentials)`.
- Profiles are printed in order of:
  1. credentials file
  2. config file
- `key_name` values are not shown.

### `configure validate` (clarification)
- Outputs errors with line numbers and specific field issues.
- If `api_secret_key.value` points to a file, that file must have `0600` permissions.
- Extensible to support new `type` formats like `vault`, `env`.

### `configure gen-key` (clarification)
- Generated key names must be lowercase alphanumerics only.
- Key and CSR files must be saved with `chmod 600`.
- Algorithm defaults to `ed25519`.

### `configure add` (clarification)
- Profile is added to the bottom of `~/.config/fireblocks-cli/config.toml`.
- Will not reorder or format the file.
- Fails if a profile of the same name already exists.
