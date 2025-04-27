# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0
# Author: Shohei KAMON <cameong@stir.network>

import tomllib
import requests
import hashlib
import os
import re

FORMULA_TEMPLATE = """class {formula_class_name} < Formula
  include Language::Python::Virtualenv

  desc "{desc}"
  homepage "{homepage}"
  url "{sdist_url}"
  sha256 "{sdist_sha256}"
  license "{license}"

  depends_on "python@3.11"

{resources}
  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{{bin}}/{command_name}", "--version"
  end
end
"""

# 手動で追加したいパッケージ一覧
extra_packages = [
    "requests",
    "urllib3",
    "fireblocks_sdk",
    "idna",
    "certifi",
    "PyJWT",
    "chardet",
]


def get_pypi_metadata(package_name):
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    response.raise_for_status()
    return response.json()


def get_sdist_info(pypi_data, package_name="(unknown)"):
    for file in pypi_data["urls"]:
        if file["packagetype"] == "sdist":
            return file["url"], file["digests"]["sha256"]
    print(f"Warning: No sdist found for {package_name}, skipping.")
    return None, None


def get_sha256_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


def generate_resource_block(package_name):
    data = get_pypi_metadata(package_name)
    sdist_info = get_sdist_info(data, package_name)
    if sdist_info == (None, None):
        return ""  # resourceを生成しない
    sdist_url, sdist_sha256 = sdist_info
    return f"""  resource "{package_name}" do\n    url "{sdist_url}"\n    sha256 "{sdist_sha256}"\n  end\n"""


def sanitize_formula_class_name(name):
    parts = re.split(r"[-_]", name)
    return "".join(part.capitalize() for part in parts)


def normalize_package_name(dep_string):
    return re.split(r"[<>=\[]", dep_string)[0]


def extract_extras(dep_string):
    match = re.search(r"\[([^\]]+)\]", dep_string)
    if match:
        extras = match.group(1)
        return [e.strip() for e in extras.split(",")]
    return []


def extract_dependencies_with_extras(project_name, extras=[]):
    data = get_pypi_metadata(project_name)
    requires_dist = data["info"].get("requires_dist", [])
    result = []

    for dep in requires_dist:
        if "; extra ==" in dep:
            extra_match = re.search(r"extra == [\'\"]([^\'\"]+)[\'\"]", dep)
            if extra_match and extra_match.group(1) in extras:
                result.append(dep.split(";")[0].strip())
        else:
            result.append(dep.split(";")[0].strip())

    return result


def main():
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    project = pyproject["project"]
    project_name = project["name"]
    version = project["version"]
    homepage = project.get("urls", {}).get(
        "Homepage", "https://github.com/stirnetwork/fireblocks-cli"
    )
    license_name = project.get("license", {}).get("text", "MPL-2.0")
    desc = project.get("description", f"{project_name} CLI tool")

    pypi_data = get_pypi_metadata(project_name)
    sdist_url, sdist_sha256 = get_sdist_info(pypi_data)

    dependencies = []
    for dep in project.get("dependencies", []):
        dep_name = normalize_package_name(dep)
        extras = extract_extras(dep)
        dependencies.append((dep_name, extras))

    for extra in extra_packages:
        dependencies.append((extra, []))

    resources = ""
    seen = set()
    for dep_name, extras in dependencies:
        if dep_name in seen:
            continue
        seen.add(dep_name)
        resources += generate_resource_block(dep_name)

        if extras:
            for sub_dep in extract_dependencies_with_extras(dep_name, extras):
                sub_dep_name = normalize_package_name(sub_dep)
                if sub_dep_name not in seen:
                    seen.add(sub_dep_name)
                    resources += generate_resource_block(sub_dep_name)

    if not resources:
        raise ValueError("No resources generated. Check dependency parsing.")

    formula_content = FORMULA_TEMPLATE.format(
        formula_class_name=sanitize_formula_class_name(project_name),
        desc=desc,
        homepage=homepage,
        sdist_url=sdist_url,
        sdist_sha256=sdist_sha256,
        license=license_name,
        resources=resources,
        command_name=project_name,
    )

    formula_filename = f"{project_name}.rb"
    with open(formula_filename, "w") as f:
        f.write(formula_content)

    print(f"Formula generated: {formula_filename}")


if __name__ == "__main__":
    main()
