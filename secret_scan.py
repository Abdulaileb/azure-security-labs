### This file helps to automate the monitoring of my azure resource.


import sys
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import resources
from azure.mgmt.storage import StorageManagementClient


def check_client_storage() -> int:
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    #client = StorageManagementClient(subscription_id, credential)
    client = StorageManagementClient(credential, subscription_id)

    failure = []

    for cred in client.storage_accounts.list():
        properties = cred.encryption
        https_only = getattr(cred, "enable_https_traffic_only", None)
        tls_version = getattr(cred, "minimum_tls_version", None)
        public_blob_access = getattr(cred, "allow_blob_public_access", None)

        print(f"\n Storgae Account : {cred.name}")
        print(f"\n Https_Only : {https_only}")
        print(f"\n tls_Version : {tls_version}")
        print(f"\n public Access : {public_blob_access}")

        if https_only is not True:
            print(" FAIL: Https-only is not enable ")
            failure.append({
                "name": cred.name,
                "check": "https_only",
                "status": "failed",
                "messgae": "Https-Only is not enabled",
            })

        if tls_version is not True:
            failure.append({
                "name": cred.name,
                "check": "tls_version",
                "status": "failed",
                "messgae": f"TLS version is too old {tls_version}",
            })

        if public_blob_access is not False:
            failure.append({
                "name": cred.name,
                "check": "public blob access",
                "status": "failed",
                "messgae": "the publiv blob is accessed publicy",
            })

    return failure

if __name__ == "__main__":
    sys.exit(check_client_storage())