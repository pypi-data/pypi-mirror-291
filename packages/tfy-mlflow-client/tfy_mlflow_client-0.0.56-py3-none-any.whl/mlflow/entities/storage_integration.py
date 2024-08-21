import re
from enum import Enum
from typing import Any, Dict, Optional, TypeVar, Union

from typing_extensions import Annotated, Literal

from mlflow.exceptions import MlflowException
from mlflow.pydantic_v1 import BaseModel, Field, parse_obj_as, root_validator


class IntegrationType(str, Enum):
    STORAGE_INTEGRATION = "blob-storage"


class IntegrationProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class BaseCredentials(BaseModel):
    class Config:
        extra = "allow"


class GCSCredentials(BaseCredentials):
    key_file_content: Dict[str, Any]


class AWSS3Credentials(BaseCredentials):
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    region: Optional[str] = None
    assumed_role_arn: Optional[str] = None


class AzureBlobCredentials(BaseCredentials):
    connection_string: str


class BaseStorageIntegration(BaseModel):
    id: str
    name: str
    fqn: str
    type: IntegrationType
    integrationProvider: IntegrationProvider
    manifest: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    @root_validator(pre=True)
    def check_empty_auth_data(cls, values):
        if not values.get("authData"):
            values["authData"] = None
        return values

    def get_storage_root(self) -> str:
        if self.integrationProvider == IntegrationProvider.AZURE:
            storageRoot = (
                self.manifest["storage_root"]
                if self.manifest["storage_root"].endswith("/")
                else self.manifest["storage_root"] + "/"
            )
            match = re.match(
                r"https://(?P<storage_account>[^.]+)\.blob\.core\.windows\.net/(?P<container_name>[^/]+)/(?P<path>.*)",
                storageRoot,
            )
            if not match:
                raise MlflowException(
                    "Invalid Azure Blob Storage URI: {}, for storage integration: {}".format(
                        storageRoot, self.fqn
                    )
                )
            container_name = match.group("container_name")
            storage_account_name = match.group("storage_account")
            path = match.group("path") or ""
            return f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/{path}"
        return self.manifest["storage_root"]


class AWSStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.AWS] = IntegrationProvider.AWS
    authData: Optional[AWSS3Credentials] = None


class GCSStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.GCP] = IntegrationProvider.GCP
    authData: Optional[GCSCredentials] = None


class AzureBlobStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.AZURE] = IntegrationProvider.AZURE
    authData: Optional[AzureBlobCredentials] = None


_StorageIntegration = Annotated[
    Union[AWSStorageIntegration, GCSStorageIntegration, AzureBlobStorageIntegration],
    Field(..., discriminator="integrationProvider"),
]

StorageIntegration = TypeVar("StorageIntegration", bound=BaseStorageIntegration)


def storage_integration_from_dict(dct: Dict[str, Any]) -> StorageIntegration:
    """
    {
        id: str
        name: str
        fqn: str
        type: str
        providerAccount: {
            provider: str
        }
        manifest: {
            authData: Dict[str, Any]
            region: Optional[str]
        }
        metadata: Optional[Dict[str, Any]]
    }
    """
    # TODO (chiragjn): Refactor this for clarity
    raw_object = dct.copy()
    provider_account = raw_object["providerAccount"]
    raw_object["integrationProvider"] = provider_account["provider"]
    raw_object["authData"] = raw_object["manifest"].get("auth_data", {}) or {}
    if raw_object["integrationProvider"] == IntegrationProvider.AWS:
        raw_object["authData"]["region"] = raw_object["manifest"].get("region")
    if raw_object["integrationProvider"] == IntegrationProvider.GCP:
        if not raw_object["authData"] or not raw_object["authData"].get("key_file_content"):
            raw_object["authData"] = None
    return parse_obj_as(_StorageIntegration, raw_object)
