from typing import List, Optional, Union

from requests.exceptions import HTTPError

from tenyks_sdk.sdk.client import Client
from tenyks_sdk.sdk.cloud import AWSLocation, AzureLocation, GCSLocation
from tenyks_sdk.sdk.dataset.dataset import Dataset
from tenyks_sdk.sdk.exceptions import ClientError
from tenyks_sdk.sdk.workspace import Workspace


class Tenyks:

    def __init__(
        self,
        client: Client,
        workspace_name: Optional[str] = None,
    ):
        self.client = client
        self.set_workspace(workspace_name, verbose=False)

    @classmethod
    def authenticate_with_api_key(
        cls,
        api_base_url: str,
        api_key: str,
        api_secret: str,
        workspace_name: str,
    ):
        try:
            client = Client.authenticate_with_api_key(api_base_url, api_key, api_secret)
            client.logger.info("Successfully authenticated to the Tenyks API.")
            return cls(client, workspace_name)
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ClientError(
                    "Failed to authenticate to the Tenyks API. Credentials are invalid or expired."
                )
            else:
                raise e

    @classmethod
    def authenticate_with_login(
        cls,
        api_base_url: str,
        username: str,
        password: str,
        workspace_name: str,
    ):
        try:
            client = Client.authenticate_with_login(api_base_url, username, password)
            client.logger.info("Successfully authenticated to the Tenyks API.")
            return cls(client, workspace_name)
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ClientError(
                    "Failed to authenticate to the Tenyks API. Credentials are invalid."
                )
            else:
                raise e

    def set_workspace(self, workspace_key: str, verbose: Optional[bool] = True) -> None:
        if not workspace_key:
            raise ValueError("Workspace name cannot be empty.")

        workspaces = self.get_workspaces()

        # Check if the provided workspace_name is in the list of workspaces
        matching_workspace = None
        for workspace in workspaces:
            if workspace.key == workspace_key:
                matching_workspace = workspace
                break

        if matching_workspace:
            self.workspace_name = matching_workspace.key
            if verbose:
                self.client.logger.info(f"Workspace set to '{workspace_key}'.")
        else:
            raise ValueError(
                f"Workspace '{workspace_key}' is not accessible or does not exist."
            )

    def get_datasets(self) -> List[Dataset]:
        endpoint = f"/workspaces/{self.workspace_name}/datasets"
        datasets_response = self.client.get(endpoint)
        return [
            Dataset.from_dataset_response(
                {**dataset}, client=self.client, workspace_name=self.workspace_name
            )
            for dataset in datasets_response
        ]

    def get_dataset_names(self) -> List[str]:
        datasets = self.get_datasets()
        return [dataset.name for dataset in datasets]

    def get_dataset(self, key: str) -> Dataset:
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{key}"
        dataset_response = self.client.get(endpoint)
        return Dataset.from_dataset_response(
            {**dataset_response}, client=self.client, workspace_name=self.workspace_name
        )

    def create_dataset(
        self,
        name: str,
        images_location: Optional[
            Union[AWSLocation, GCSLocation, AzureLocation]
        ] = None,
        metadata_location: Optional[
            Union[AWSLocation, GCSLocation, AzureLocation]
        ] = None,
    ) -> Dataset:
        endpoint = f"/workspaces/{self.workspace_name}/datasets"
        payload = {
            "key": name.lower(),
            "display_name": name,
        }

        if images_location:
            payload["images_location"] = images_location.model_dump()
        if metadata_location:
            payload["metadata_location"] = metadata_location.model_dump()

        dataset_response = self.client.post(endpoint, body=payload)
        dataset = Dataset.from_dataset_response(
            {**dataset_response}, client=self.client, workspace_name=self.workspace_name
        )
        self.client.logger.info(
            f"Dataset '{name}' created successfully with key {dataset.key}."
        )
        return dataset

    def delete_dataset(self, key: str) -> None:
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{key}"
        self.client.delete(endpoint)
        self.client.logger.info(f"Dataset {key} deleted successfully.")

    def get_workspaces(self, page: int = 1, page_size: int = 10) -> List[Workspace]:
        endpoint = "/workspaces"
        params = {"page": page, "page_size": page_size}
        workspaces_response = self.client.get(endpoint, params=params)
        workspaces_list = workspaces_response.get("data")
        return [Workspace(self.client, **workspace) for workspace in workspaces_list]

    def get_workspace(self, id: str) -> Workspace:
        endpoint = f"/workspaces/{id}"
        workspace_response = self.client.get(endpoint)
        return Workspace(self.client, **workspace_response)

    def create_workspace(self, name: str) -> Workspace:
        endpoint = "/workspaces"
        payload = {"name": name}
        workspace_response = self.client.post(endpoint, body=payload)
        return Workspace(self.client, **workspace_response)
