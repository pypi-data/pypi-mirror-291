import requests

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://localhost:5000" 

    def ingest_document(self, document_path: str, doc_type: str):
        url = f"{self.base_url}/ingest"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        files = {"file": open(document_path, "rb")}
        data = {"type": doc_type}

        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        return response.json()

    def search_text(self, query: str, similarity_type: str):
        url = f"{self.base_url}/search"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"query": query, "similarity_type": similarity_type}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
