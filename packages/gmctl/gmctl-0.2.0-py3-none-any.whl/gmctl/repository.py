from gmctl.gmclient import GitmoxiClient
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
logger = logging.getLogger(__name__)

class Repository(BaseModel):
    repo_url: str = Field(..., min_length=1)
    branches: List[str] = Field(..., min_items=1)
    access_token_arn: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.model_dump_json()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    def add(self, gmclient: GitmoxiClient) -> bool:
        logger.info(f'Adding repository: {self.repo_url}')
        # make a POST call to the /repository/add endpoint with the repository details
        # gmclient has the endpoint url, access token, and api version
        resource_path = "/repositories/add"
        response = gmclient.post(resource_path, self.to_dict())
        if not response:
            logger.error(f'Failed to add repository: {self.repo_url}')
            return False
        logger.info(f'Repository added: {self.repo_url}')
        return True

    @staticmethod
    def get(gmclient: GitmoxiClient, repo_url: str = "") -> List[Any]:

        resource_path = "/repositories"
        if repo_url:
            resource_path += f"?repo_url={repo_url}"
        logger.info(f'Getting repository: {resource_path}')
        # make a GET call to the /repository/get endpoint with the repository URL
        response = gmclient.get(resource_path)
        if not response:
            logger.error(f'Failed to get repositories for: {resource_path}')
        return [Repository(**repo) for repo in response]
    
    @staticmethod
    def delete(gmclient: GitmoxiClient, repo_url: str) -> Optional[Dict[str, Any]]:
        if not repo_url:
            logger.error('Repository URL is required to delete a repository')
            return None
        logger.info(f'Deleting repository: {repo_url}')
        # make a DELETE call to the /repository/delete endpoint with the repository URL
        resource_path = f"/repositories/delete?repo_url={repo_url}"
        logger.info(f'Deleting repository: {resource_path}')
        return gmclient.delete(resource_path)