# fireblocks-cli

> **Disclaimer:** This project is an independent, unofficial command-line interface (CLI) for interacting with the Fireblocks API.
> It is not affiliated with or endorsed by Fireblocks Ltd.
> "Fireblocks" is a registered trademark of Fireblocks Ltd.
>
> This project is inspired by the design philosophy and usability of the AWS CLI.

---

##  Environment

This tool has been tested with:

- **Python 3.11 or newer**

Other versions are not officially supported.
Please ensure you are using Python 3.11+ before running or contributing to this project.

---

##  Installation

You can install fireblocks-cli locally as a Python project:

```bash
git clone https://github.com/your-org/fireblocks-cli.git
cd fireblocks-cli
pip install .
```

You can use pip.

```
pip install fireblocks-cli
```

> For development, use:

```bash
pip install -e .[dev]
```

---

##  Usage

```bash
fireblocks-cli [COMMAND] [OPTIONS]
```

Examples:

```bash
fireblocks-cli configure init
fireblocks-cli configure list
```

To see all available commands:

```bash
fireblocks-cli --help
```

# fireblocks-cli configure Subcommand List

| Subcommand        | Status          | Description                                                    | Notes                                                                 |
|-------------------|------------------|----------------------------------------------------------------|-----------------------------------------------------------------------|
| `init`            | Not implemented  | Initialize the default configuration files                     | Creates `~/.fireblocks/config.toml` and `~/.fireblocks/keys/`         |
| `gen-keys`        | ✅ Implemented    | Generate Fireblocks-compatible private key and CSR            | Outputs to `.fireblocks/keys/{name}.csr`, etc.                    |
| `list`            | Not implemented  | List all configured profiles                                   | Displays `[profile]` sections from `config.toml`                      |
| `edit`            | Not implemented  | Open the config file in your default `$EDITOR`                 | Falls back to `vi` or `nano` if `$EDITOR` is not set                  |
| `validate`        | Not implemented  | Validate the structure and contents of the config file         | Checks for invalid or missing keys and values                         |
| `add`    | Not implemented  | Append a new profile to the configuration file                 | Will add to the bottom of the file without auto-formatting            |
| `remove` | Not implemented  | Remove a profile from the configuration                        | Deletes the corresponding section from `config.toml`                  |


---

## Directory Structure (XDG Base Directory Specification)

This CLI follows the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html):

- Configuration: `$XDG_CONFIG_HOME/fireblocks-cli/config.toml` (default: `~/.config/fireblocks-cli/config.toml`)
- Data: `$XDG_DATA_HOME/fireblocks-cli/` (default: `~/.local/share/fireblocks-cli/`)
- Cache: `$XDG_CACHE_HOME/fireblocks-cli/` (default: `~/.cache/fireblocks-cli/`)

---

#  For Developers

This section explains how to contribute and work on the project.

---

## 🛠️ Developer Setup

Install development dependencies:

```bash
make install-dev
```

Run tests:

```bash
make test
```

Run linter:

```bash
make lint-license
```

Run all pre-commit hooks:

```bash
make pre-commit-refresh
```

---

##  Build a binary (optional)

To build an executable for distribution:

```bash
./build.sh patch  # or 'minor' or 'major'
```

The binary will be generated in the `dist/` directory, compressed using UPX (if available).

---

##  Code Licensing & Attribution

- Licensed under **MPL-2.0**.
- Files include SPDX headers and author metadata.

- Please use the following before committing:

```bash
make annotate-SPD
make add-author
```

---

### Changing the Copyright Holder

To change the copyright holder name inserted into source files:

1. Create a file named `COPYRIGHT_HOLDER` in the root of the repository, and write your name or your organization’s name in it.
   For example:

   ```bash
   echo "Your Name or Organization" > COPYRIGHT_HOLDER
   ```

   > ⚠️ Note: This file is `.gitignore`'d and should not be committed.

2. Run `make annotate-SPD` (or the relevant pre-commit hook) to re-annotate modified source files with the new copyright holder name.

   - This target internally calls `reuse annotate` to update SPDX headers.
   - Only `.py` and `.sh` files tracked by git are affected.

   ```bash
   make annotate-SPD
   ```

> **Important**: The value in `COPYRIGHT_HOLDER` must be under 50 characters.

---

## 🤝 Contributing

Contributions are welcome!

Please make sure your commits are signed off (DCO) and that you run the following before pushing:

```bash
pre-commit run --all-files
```

### 🖋 What is "signed off (DCO)"?

By signing off your commits, you certify that you wrote the code or have the right to submit it under the project's license.

To sign off a commit, use the `-s` flag when committing:

```bash
git commit -s -m "Your commit message"
or
git commit -sm "Your commit message"
```

This will append a line like the following to your commit message:

```
Signed-off-by: Your Name <your.email@example.com>
```

For more details, see the [Developer Certificate of Origin](https://developercertificate.org/).

---

## 🧾 Contributors

This project is developed with support from multiple contributors.
See [CONTRIBUTORS.md](./CONTRIBUTORS.md) for a full list.

---

## 📄 License

This project is licensed under the [Mozilla Public License 2.0](./LICENSE).

---

## 📬 Contact

Maintained by [Shohei Kamon](mailto:cameong@stir.network).
Feel free to reach out for collaboration or questions!
