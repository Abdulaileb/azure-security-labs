#!/usr/bin/env python3
"""Check baseline Azure Storage security controls using Azure CLI authentication."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

REQUIRED_LOG_CATEGORIES = {"StorageRead", "StorageWrite", "StorageDelete"}


def run_az(*arguments: str) -> Any:
    result = subprocess.run(
        ["az", *arguments, "--output", "json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Azure CLI command failed")
    return json.loads(result.stdout or "null")


def report(control: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "REVIEW"
    print(f"[{status}] {control}: {detail}")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--storage-account", required=True)
    args = parser.parse_args()

    try:
        account = run_az(
            "storage",
            "account",
            "show",
            "--name",
            args.storage_account,
            "--resource-group",
            args.resource_group,
        )
        storage_id = account["id"]
        blob_service_id = f"{storage_id}/blobServices/default"
        diagnostic_settings = run_az(
            "monitor",
            "diagnostic-settings",
            "list",
            "--resource",
            blob_service_id,
        )
    except (FileNotFoundError, KeyError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    checks = [
        report(
            "HTTPS-only traffic",
            account.get("supportsHttpsTrafficOnly") is True,
            str(account.get("supportsHttpsTrafficOnly")),
        ),
        report(
            "Minimum TLS version",
            account.get("minimumTlsVersion") == "TLS1_2",
            str(account.get("minimumTlsVersion")),
        ),
        report(
            "Public Blob access disabled",
            account.get("allowBlobPublicAccess") is False,
            str(account.get("allowBlobPublicAccess")),
        ),
    ]

    enabled_categories: set[str] = set()
    for setting in diagnostic_settings or []:
        for log in setting.get("logs", []):
            if log.get("enabled"):
                enabled_categories.add(log.get("category", ""))

    missing_categories = REQUIRED_LOG_CATEGORIES - enabled_categories
    checks.append(
        report(
            "Blob audit logs",
            not missing_categories,
            "enabled: " + ", ".join(sorted(enabled_categories))
            if not missing_categories
            else "missing: " + ", ".join(sorted(missing_categories)),
        )
    )

    print(f"Checked account: {args.storage_account}")
    print(f"Diagnostic settings found: {len(diagnostic_settings or [])}")
    return 0 if all(checks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
