import requests
from typing import List
from .const import API_URL, USER_AGENT
from .lock import Lock

class GlueClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Api-Key {self.api_key}',
            'User-Agent': USER_AGENT
        })

    def get_all_locks(self) -> List[Lock]:
        response = self.session.get(f'{API_URL}/v1/locks')
        response.raise_for_status()
        return [Lock.from_json(self.api_key, lock_data) for lock_data in response.json()]

    def get_lock(self, lock_id: str) -> Lock:
        response = self.session.get(f'{API_URL}/v1/locks/{lock_id}')
        response.raise_for_status()
        return Lock.from_json(self.api_key, response.json())

    def get_locks(self, lock_ids: List[str]) -> List[Lock]:
        return [self.get_lock(lock_id) for lock_id in lock_ids]
