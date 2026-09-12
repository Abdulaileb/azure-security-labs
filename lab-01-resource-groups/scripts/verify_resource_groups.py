#!/usr/bin/env python3
"""List Azure resource groups and their provisioning state using Azure CLI auth."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


def run_az(*arguments: str) -> Any:
    result = subprocess.run(
        ["az.cmd" if sys.platform == "win32" else "az", *arguments, "--output", "json"],
        #["az", *arguments, "--output", "json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Azure CLI command failed")
    return json.loads(result.stdout or "null")


def main() -> int:
    try:
        groups = run_az(
            "group",
            "list",
            "--query",
            "[].{name:name,location:location,state:properties.provisioningState,tags:tags}",
        )
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(json.dumps(groups, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
