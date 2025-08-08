import requests

from ..config.environment import EnvironmentConfig

config = EnvironmentConfig()

headers = {
    "Authorization": f"Bearer {config.get_notion_token()}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def post_database_query(database_id, payload):
    url = f"{config.get_notion_base_url()}/v1/databases/{database_id}/query"
    response = requests.post(url, json=payload, headers=headers)
    return response


def patch_page(page_id, payload):
    url = f"{config.get_notion_base_url()}/v1/pages/{page_id}"
    response = requests.patch(url, json=payload, headers=headers)
    return response
