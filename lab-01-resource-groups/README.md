# Lab 01: Resource Groups

**Status:** Planned

## Objective

Build a small Azure resource-group layout and understand how resource groups provide a management, access-control, tagging, and lifecycle boundary.

## Learning goals

- Explain the difference between a subscription, resource group, resource, and region.
- Create a resource group in a deliberate region.
- Apply ownership and environment tags.
- Inspect provisioning state and resource membership with Azure CLI.
- Delete a disposable resource group and verify that its resources are removed.

## Planned workflow

1. Create a disposable resource group.
2. Add tags such as `environment=lab` and `owner=personal`.
3. Deploy one small test resource into it.
4. Verify the resource group and resource inventory.
5. Delete the resource group.
6. Confirm the resource and group are gone.

## Verification commands

```powershell
az group create `
  --name <lab-resource-group> `
  --location <azure-region> `
  --tags environment=lab owner=personal

az resource list `
  --resource-group <lab-resource-group> `
  --output table

az group show `
  --name <lab-resource-group> `
  --query "{name:name,location:location,state:properties.provisioningState,tags:tags}" `
  --output json
```

## What will count as evidence

- Sanitized CLI output showing the group, region, tags, and resource inventory.
- A short explanation of why the group is a useful operational and access boundary.
- A deletion verification showing the disposable environment was cleaned up.
