# fireblocks-cli

> **Disclaimer:** This project is an independent, unofficial command-line interface (CLI) for interacting with the Fireblocks API.
> It is not affiliated with or endorsed by Fireblocks Ltd.
> "Fireblocks" is a registered trademark of Fireblocks Ltd.
>
> This project is inspired by the design philosophy and usability of the AWS CLI.


##  Installation

You can install fireblocks-cli locally as a Python project:

```bash
git clone https://github.com/your-org/fireblocks-cli.git
cd fireblocks-cli
pip install .
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

---

##  Environment

This tool has been tested with:

- **Python 3.11 or newer**

Other versions are not officially supported.
Please ensure you are using Python 3.11+ before running or contributing to this project.

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

## 🤝 Contributing

Contributions are welcome!
Please make sure your commits are signed off (DCO) and that you run the following before pushing:

```bash
pre-commit run --all-files
```

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
