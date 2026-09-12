# Azure Security Labs

A practical cloud-security portfolio built while preparing for AZ-900 and progressing toward Azure security, DevSecOps, Kubernetes, infrastructure, AI/ML, and GRC engineering.

The operating loop for every lab is:

**Build -> Verify -> Break -> Detect -> Fix -> Automate -> Document -> Rebuild from memory**

This repository is evidence of hands-on work, not a collection of copied tutorials.

## Labs

| Lab | Focus | Status |
| --- | --- | --- |
| [Lab 01: Resource Groups](lab-01-resource-groups/) | Azure resource organization, scope, and lifecycle | Planned |
| [Lab 02: Storage Security](lab-02-storage-security/) | Blob access, Azure Monitor logs, RBAC, KQL, and key rotation | In progress |

Future labs will cover identity and RBAC, networking, Key Vault, secure infrastructure as code, Defender for Cloud, Kubernetes security, and policy/GRC controls.

## Repository structure

```text
azure-security-labs/
├── lab-01-resource-groups/
│   ├── README.md
│   ├── findings.md
│   └── scripts/
├── lab-02-storage-security/
│   ├── README.md
│   ├── findings.md
│   └── scripts/
├── templates/
│   └── lab-template/
├── linkedin/
│   └── lab-02-storage-security.md
└── README.md
```

Each lab contains:

- `README.md`: objective, architecture, commands, verification, and lessons learned.
- `scripts/`: repeatable Bash, PowerShell, or Python checks.
- `findings.md`: what failed, what was detected, the root cause, and the fix.

## Prerequisites

- An Azure subscription intended for learning and experimentation.
- Azure CLI with an interactive login: `az login`.
- Python 3.11 or newer for the Python checks.
- A Log Analytics workspace for monitoring labs.
- Permission to create and inspect the resources used by a lab.

Run Azure CLI commands only against a lab resource group. Do not place subscription IDs, tenant IDs, access keys, SAS tokens, passwords, or private IP addresses in committed files.

## Reproduce the checks

From a lab folder:

```powershell
az login
python .\scripts\check_storage_security.py `
  --resource-group <lab-resource-group> `
  --storage-account <storage-account-name>
```

The scripts use Azure CLI authentication and intentionally do not accept storage keys.

## Evidence standard

A lab is complete when the repository contains:

1. A clear objective and threat or control model.
2. The commands or code used to build and verify the environment.
3. A controlled failure or misconfiguration, where safe and appropriate.
4. Detection evidence such as a CLI result, KQL query, alert, or screenshot with secrets removed.
5. A remediation and an automated check.
6. A short explanation of what was learned and what remains uncertain.

## Public-repository safety

Before pushing changes:

```powershell
git diff --check
git status
```

Review every diff for secrets and identifying data. Rotate any credential that was exposed during a lab, even if it was later deleted from the working tree. Keep raw exports and screenshots with sensitive values outside the repository.

## Suggested GitHub repository metadata

- **Name:** `azure-security-labs`
- **Description:** `Hands-on Azure security labs documenting build, break, detect, fix, automate, and verification workflows.`
- **Topics:** `azure`, `cloud-security`, `devsecops`, `az-900`, `kql`, `log-analytics`, `rbac`, `infrastructure-as-code`, `security-automation`
