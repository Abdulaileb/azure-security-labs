# Lab 02: Storage Security and Blob Monitoring

**Status:** In progress

## Objective

Secure an Azure Storage account, route Blob resource logs to Log Analytics, generate authenticated data-plane activity, and use evidence to validate the control.

## Security questions

- Can anonymous or public Blob access be enabled accidentally?
- Are HTTPS and a modern TLS version enforced?
- Can the team distinguish Azure management-plane access from Blob data-plane access?
- Are Blob reads, writes, and deletes routed to a queryable log table?
- What happens when a storage key is exposed during troubleshooting?

## Architecture

```text
Azure Storage Account
  └── Blob service
        └── Diagnostic setting
              └── Log Analytics workspace
                    └── StorageBlobLogs
```

The account and workspace were placed in the same Azure region. The diagnostic setting collects `StorageRead`, `StorageWrite`, and `StorageDelete` as resource logs. DCR-based metrics export is a separate concern and is not required for this log path.

## Build and verify

Use placeholders when reproducing this lab. Do not commit real subscription IDs or keys.

```powershell
az login

$storageId = az storage account show `
  --name <storage-account-name> `
  --resource-group <lab-resource-group> `
  --query id `
  --output tsv

$blobServiceId = "$storageId/blobServices/default"

az monitor diagnostic-settings categories list `
  --resource $blobServiceId `
  --output table

python .\scripts\check_storage_security.py `
  --resource-group <lab-resource-group> `
  --storage-account <storage-account-name>
```

Expected log categories are `StorageRead`, `StorageWrite`, and `StorageDelete`.

## Generate activity without storage keys

Assign the smallest suitable Blob data role at the lab storage-account scope, wait for RBAC propagation, and use Entra authentication:

```powershell
az storage container create `
  --name evidence `
  --account-name <storage-account-name> `
  --auth-mode login `
  --public-access off

az storage blob list `
  --container-name evidence `
  --account-name <storage-account-name> `
  --auth-mode login `
  --output table
```

## KQL verification

Resource logs may take time to arrive after the first operation. Query the dedicated table in Log Analytics:

```kusto
StorageBlobLogs
| where TimeGenerated > ago(1h)
| project TimeGenerated, OperationName, StatusCode,
          AuthenticationType, CallerIpAddress, Uri
| order by TimeGenerated desc
```

Useful follow-up queries:

```kusto
StorageBlobLogs
| where TimeGenerated > ago(24h)
| summarize Requests=count() by AuthenticationType, OperationName
| order by Requests desc
```

```kusto
StorageBlobLogs
| where TimeGenerated > ago(24h)
| where AuthenticationType == "Anonymous"
| project TimeGenerated, OperationName, StatusCode, Uri, CallerIpAddress
```

## Current result

The diagnostic setting was created successfully and the three Blob log categories are enabled. The first Entra-authenticated test was blocked because the signed-in identity had subscription-level `Owner` access but no Blob data-plane role. A storage-account-scoped `Storage Blob Data Contributor` assignment was then created. Final KQL ingestion verification remains to be recorded after RBAC propagation.

## Lessons so far

- A valid Blob service resource ID must end with `/blobServices/default`.
- Management-plane `Owner` does not automatically grant Blob data-plane access.
- DCR language can refer to metrics export; it does not automatically mean Blob resource logs require a DCR.
- Storage keys must never be used as a default troubleshooting shortcut.
- Diagnostic settings and Log Analytics are controls that need verification, not assumptions.
