<!--
SPDX-FileCopyrightText: 2025 Ethersecurity Inc.

SPDX-License-Identifier: MPL-2.0
-->
<!-- Author: Shohei KAMON <cameong@stir.network> -->

# Release Workflow for fireblocks-cli

This document outlines the release process for the **fireblocks-cli** project, covering both **PyPI** and **Homebrew** releases, and how they are handled through GitHub Actions.

## Overview

When a tag (e.g., `v0.1.8`) is pushed, the following actions are triggered:

1. **PyPI release**: The Python package is built and uploaded to **PyPI** (source tar.gz and wheel).

## Workflow Steps

1. **Trigger**: A tag is pushed (e.g., `v0.1.8`) to GitHub.
2. **GitHub Actions**:
   - **publish-pypi.yml**: This workflow builds the Python package and uploads it to PyPI.


# Additional Notes

- The process can be automated completely, minimizing manual steps for each release.
- This workflow is designed for seamless integration with both **Homebrew** and **PyPI**, making it easy for developers and users alike to install the tool.

---

# Future Improvements

- Add version management for Homebrew (automatic update of version on Homebrew tap).
- Enhance testing and validation steps for both PyPI and Homebrew releases.
