# MkDocs Placeholder Plugin

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-encrypt-source-plugin)](https://pypi.org/project/mkdocs-encrypt-source-plugin/)
![License](https://img.shields.io/pypi/l/mkdocs-encrypt-source-plugin)
![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-encrypt-source-plugin)

This plugin allows you to store sensitive information in encrypted form it the source code.
When you build the site, it is decrypted using a key you pass as an enviroment variable.
This means only people with the key or access to the deployed website can access the information.
It also prevents code scanning tools from checking the data you store encrypted.

## Installation and usage

Installation and usage is described in more detail in [docs/usage.md](https://mkdocs-encrypt-source-plugin.six-two.dev/usage/).

The quick summary is:

1. Install it with pip:
    ```bash
    mkdocs-encrypt-source-plugin
    ```
2. Add `encrypt-source` to the `plugins` list in `mkdocs.yml`.
3. Generate an encryption/decryption key:
    ```bash
    echo -n | mkdocs-encrypt-source-cli -e -k "" >/dev/null
    ```
    And export the generated key as environment variable:
    ```bash
    export MKDOCS_ENCRYPT_SOURCE_KEY='WCFY7FJ2TlpXIG0nEqpSltXTAYB9gO3Ob6tS-psY9-s='
    ```
4. Encrypt all values you want to encrypt with:
    ```bash
    echo -n "Value to encrypt" | mkdocs-encrypt-source-cli -e
    ```
    and put the output in your Markdown source files.
5. Build the page with `mkdocs serve` and check that all encrypted values are correctly decrypted.

