from typing import Dict, List

from tenyks_sdk.sdk.client import Client


class Workspace:
    def __init__(
        self,
        client: Client,
        id: str,
        name: str,
        key: str,
        created_by: str,
        created_at: str,
        updated_by: str,
        updated_at: str,
    ) -> "Workspace":
        self.client = client
        self.id = id
        self.name = name
        self.key = key
        self.created_by = created_by
        self.created_at = created_at
        self.updated_by = updated_by
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self.id)}, "
            f"name={repr(self.name)}, "
            f"key={repr(self.key)}, "
            f"created_by={repr(self.created_by)}, "
            f"created_at={repr(self.created_at)}, "
            f"updated_by={repr(self.updated_by)}, "
            f"updated_at={repr(self.updated_at)})"
        )

    def get_users(self, page: int = 1, page_size: int = 10) -> List[Dict]:
        endpoint = f"/workspaces/{self.id}/users"
        params = {"page": page, "page_size": page_size}
        users_response = self.client.get(endpoint, params=params)
        return users_response.get("data")

    def add_user(
        self,
        name: str,
        sub: str,
        email: str,
        providers: List[str],
    ) -> None:
        endpoint = f"/workspaces/{self.id}/users"
        payload = {
            "name": name,
            "sub": sub,
            "email": email,
            "providers": providers,
        }
        self.client.post(endpoint, body=payload)
        self.client.logger.info(f"User {name} added to workspace '{self.name}'.")

    def delete_users(self, subs: List[str]) -> None:
        endpoint = f"/workspaces/{self.id}/users"
        query_params = {"subs": subs}
        self.client.delete(endpoint, params=query_params)
        self.client.logger.info(f"Users {subs} deleted from workspace '{self.name}'.")
