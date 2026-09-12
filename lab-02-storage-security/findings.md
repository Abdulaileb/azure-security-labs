# Findings: Lab 02 Storage Security

**Status:** In progress

## Finding 1: Malformed Blob service resource ID

- **Symptom:** Azure returned `ParentResourceNotFound` while listing diagnostic categories.
- **Evidence:** The resource path was missing the full storage account name or the `/blobServices/default` child resource.
- **Root cause:** Azure Monitor diagnostic settings are attached to the Blob service resource, not an invented or truncated path.
- **Fix:** Derived the account ID with Azure CLI and appended `/blobServices/default`.
- **Lesson:** Derive resource IDs from Azure instead of typing long IDs manually.

## Finding 2: Shell state preserved a variable typo

- **Symptom:** A corrected command continued using an old value.
- **Evidence:** `ST0RAGE_ID` used a zero, while later commands referenced `STORAGE_ID`.
- **Root cause:** The shell retained the earlier variable and the typo was not cleared.
- **Fix:** Recomputed the values from Azure and printed the complete strings for comparison.
- **Lesson:** Validate both variable names and values when debugging CLI automation.

## Finding 3: DCR message was not blocking Blob resource logs

- **Symptom:** The portal reported that Storage Accounts in `francecentral` require DCR.
- **Evidence:** Azure exposed `StorageRead`, `StorageWrite`, and `StorageDelete` as log categories, and the classic diagnostic setting was created successfully.
- **Root cause:** The message applied to a different monitoring path, most likely metrics export or a portal flow, rather than these Blob resource logs.
- **Fix:** Created a resource-specific diagnostic setting for logs only and omitted metrics.
- **Lesson:** Identify the exact data source before changing collection architecture.

## Finding 4: Management-plane access was not data-plane access

- **Symptom:** Blob operations using `--auth-mode login` were denied.
- **Evidence:** The signed-in identity had subscription-level `Owner` but no Blob data role at the storage account.
- **Root cause:** Azure RBAC separates resource management permissions from Storage data permissions.
- **Fix:** Assigned `Storage Blob Data Contributor` at the storage-account scope for this lab.
- **Residual risk:** The role is broader than a read-only test role. Remove it after the lab or reduce it to `Storage Blob Data Reader` when writes are no longer needed.

## Finding 5: Storage key exposure during troubleshooting

- **Symptom:** A key value appeared in terminal output during key rotation verification.
- **Root cause:** The CLI command returned key material because the output was not restricted to a non-secret field.
- **Fix:** Rotated both storage keys again with secret output suppressed. The lab uses Entra authentication instead of account keys.
- **Residual risk:** Any system that may have captured the earlier value must be treated as untrusted until the rotated keys have propagated.

## Pending evidence

- Confirm RBAC propagation.
- Generate authenticated Blob activity.
- Confirm records arrive in `StorageBlobLogs`.
- Add sanitized query output or a screenshot with identifiers removed.
- Remove or reduce the temporary Blob data role after verification.
