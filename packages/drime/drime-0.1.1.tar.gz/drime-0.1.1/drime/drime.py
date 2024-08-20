import requests

class DrimeAPI:
    def __init__(self, token: str, base_url: str = "https://app.drime.cloud"):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def upload_file(self, file_path: str):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self._request("POST", "/uploads", files=files)

    def register(self, email: str, password: str):
        data = {"email": email, "password": password}
        return self._request("POST", "/auth/register", json=data)

    def login(self, email: str, password: str):
        data = {"email": email, "password": password}
        response = self._request("POST", "/auth/login", json=data)
        self.headers["Authorization"] = f"Bearer {response['token']}"
        return response

    def get_file_entries(self):
        return self._request("GET", "/drive/file-entries")

    def delete_file_entries(self, entry_ids: list, permanent: bool = False):
        data = {"entryIds": entry_ids, "permanent": permanent}
        return self._request("DELETE", "/file-entries", json=data)

    def update_file_entry(self, entry_id: str, new_name: str):
        data = {"name": new_name}
        return self._request("PUT", f"/file-entries/{entry_id}", json=data)

    def create_folder(self, name: str, parent_id: str = None):
        data = {"name": name, "parentId": parent_id}
        return self._request("POST", "/folders", json=data)

    def move_file_entries(self, entry_ids: list, target_folder_id: str):
        data = {"entryIds": entry_ids, "targetFolderId": target_folder_id}
        return self._request("POST", "/file-entries/move", json=data)

    def duplicate_file_entries(self, entry_ids: list):
        data = {"entryIds": entry_ids}
        return self._request("POST", "/file-entries/duplicate", json=data)

    def restore_file_entries(self, entry_ids: list):
        data = {"entryIds": entry_ids}
        return self._request("POST", "/file-entries/restore", json=data)

    def share_file_entry(self, entry_id: str, user_email: str):
        data = {"userEmail": user_email}
        return self._request("POST", f"/file-entries/{entry_id}/share", json=data)

    def change_permissions(self, entry_id: str, user_email: str, permissions: str):
        data = {"userEmail": user_email, "permissions": permissions}
        return self._request("PUT", f"/file-entries/{entry_id}/change-permissions", json=data)

    def unshare_file_entry(self, entry_id: str, user_email: str):
        data = {"userEmail": user_email}
        return self._request("DELETE", f"/file-entries/{entry_id}/unshare", json=data)

    def star_file_entries(self, entry_ids: list):
        data = {"entryIds": entry_ids}
        return self._request("POST", "/file-entries/star", json=data)

    def unstar_file_entries(self, entry_ids: list):
        data = {"entryIds": entry_ids}
        return self._request("POST", "/file-entries/unstar", json=data)

    def get_shareable_link(self, entry_id: str):
        return self._request("GET", f"/file-entries/{entry_id}/shareable-link")

    def create_shareable_link(self, entry_id: str):
        return self._request("POST", f"/file-entries/{entry_id}/shareable-link")

    def update_shareable_link(self, entry_id: str, link_id: str, **kwargs):
        return self._request("PUT", f"/file_entries/{entry_id}/shareable-link", json=kwargs)

    def delete_shareable_link(self, entry_id: str, link_id: str):
        return self._request("DELETE", f"/file_entries/{entry_id}/shareable-link")