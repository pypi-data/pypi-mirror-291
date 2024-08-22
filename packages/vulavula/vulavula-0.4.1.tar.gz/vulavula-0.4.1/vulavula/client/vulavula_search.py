from typing import Union, Dict
from vulavula.common.response_handler import APIResponseHandler
from vulavula.config import settings
from vulavula.models.types import CreateKnowledgeBaseRequest, DeleteKnowledgeBaseRequest
import requests
import os
import logging
class VulavulaSearch:

    def __init__(self, client_token,  base_url=None, session=None):
        self.base_url = base_url if base_url else settings.BASE_URL
        self.headers = {
            "X-CLIENT-TOKEN": client_token,
            "accept": "application/json"
        }
        self.client_token= client_token
        self._handle_response = APIResponseHandler.handle_response
        self.session = session if session else requests.Session()
        self.session.headers.update(self.headers)
        self.collection = None
        self.logger = logging.getLogger("vulavulaSearch")

    def create_collection(self, data: Union[str, CreateKnowledgeBaseRequest]):

        payload = {
            "knowledgebase_name":data}

        url = f"{self.base_url}/search/knowledgebase"
        response = self.session.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def get_knowledgebases(self):
        url = f"{self.base_url}/search/knowledgebases"
        response = self.session.get(url, headers=self.headers)
        return self._handle_response(response)

    def delete_knowledgebase(self, id: Union[str,DeleteKnowledgeBaseRequest ]):
        data = id.knowledgebase_id if isinstance(id, DeleteKnowledgeBaseRequest) else id

        url = f"{self.base_url}/search/knowledgebase/{data}"
        response = self.session.delete(url, headers=self.headers)
        return self._handle_response(response)
    def delete_document(self, document_id:str):

        url = f"{self.base_url}/search/knowledgebase/document/{document_id}"
        response = self.session.delete(url, headers=self.headers)
        return self._handle_response(response)

    def upload_and_extract_text(self, file_path: str, knowledgebase_id: str) -> dict:
        upload_url = f"{self.base_url}/search/knowledgebase/{knowledgebase_id}/document"

        if not os.path.isfile(file_path):
            self.logger.info(f"File does not exist: {file_path}")
            return {"error": "File not found"}

        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                upload_response = requests.post(upload_url, headers=self.headers, files=files)
            if upload_response.status_code != 200:
                self.logger.info(
                    f"Failed to upload file. Status code: {upload_response.status_code}, Response: {upload_response.text}")
                return self._handle_response(upload_response)

            # Checking if the response has documents extracted
            documents = upload_response.json().get("documents", [])

            if documents:
                self.logger.info("Documents extracted successfully.")
            else:
                self.logger.info("No documents extracted.")

            return self._handle_response(upload_response)

        except Exception as e:
            self.logger.info(f"An error occurred: {e}")
            return {"error": str(e)}

    def get_documents(self, knowledgebase_id: str) -> dict:
        url = f"{self.base_url}/search/knowledgebase/{knowledgebase_id}/documents"

        try:
            response = self.session.get(url, headers=self.headers)

            if response.status_code == 200:
                self.logger.info("Documents retrieved successfully.")
                return response.json()
            else:
                self.logger.info(f"Failed to retrieve documents. Status code: {response.status_code}, Response: {response.text}")
                return self._handle_response(response.json())

        except Exception as e:
            self.logger.info(f"An error occurred while retrieving documents: {e}")
            return {"error": str(e)}

    def search_query(self,knowledgebase_id: str, query: str, language: str) -> dict:
        url = f"{self.base_url}/search/knowledgebase/{knowledgebase_id}/query"

        data = {
            "query": query,
            "language": language
        }

        try:
            response = self.session.post(url, headers=self.headers, json=data)
            return self._handle_response(response)
        except Exception as e:
            self.logger.info(f"An error occurred during the search query: {e}")
            return {"error": str(e)}
