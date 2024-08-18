from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from gmctl.gmclient import GitmoxiClient
import hashlib
import logging

logger = logging.getLogger(__name__)

class ECSDeployment(BaseModel):
    repo_url: str = Field(..., min_length=1)
    commit_hash: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    service: str = Field(..., min_length=1)
    cluster: str = Field(..., min_length=1)
    create_timestamp: Optional[str] = None
    status_details: Optional[List[str]] = None
    status: Optional[str] = ""
    id: Optional[str] = None
    file_prefix: Optional[str] = None
    
    def __str__(self) -> str:
        return self.model_dump_json()

    def set_create_timestamp(self, timestamp: str) -> None:
        self.create_timestamp = timestamp   

    def generate_id(self) -> str:
        data_string = f'{self.repo_url}#{self.commit_hash}#{self.account_id}#{self.service}#{self.cluster}'
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def summary(self) -> str:
        summary_keys = ["repo_url", "commit_hash", "account_id", "service", 
                        "cluster", "create_timestamp", "status", "file_prefix"]
        return {k: self.to_dict()[k] for k in summary_keys}

    @staticmethod
    def get(gmclient: GitmoxiClient, repo_url: str, commit_hash: str,
            cluster: str, service: str, account_id: str) -> List[Any]:
        resource_path = "/deployments/ecs"
        conditions = []
        if repo_url:
            conditions.append(f"repo_url={repo_url}")
        if commit_hash:
            conditions.append(f"commit_hash={commit_hash}")
        if cluster:
            conditions.append(f"cluster={cluster}")
        if service:
            conditions.append(f"service={service}")
        if account_id:
            conditions.append(f"account_id={account_id}")
        if conditions:
            resource_path += "?" + "&".join(conditions)
        logger.info(f'Getting ECS deployments: {resource_path}')
        # make a GET call to the /deployments/ecs endpoint with the repository URL
        response = gmclient.get(resource_path)
        if response is None:
            logger.error(f'Failed to get ECS deployments for: {resource_path}')
            return []
        if response and len(response) <= 0:
            logger.warning(f'Did not get any ECS deployments for: {resource_path}')
        return [ECSDeployment(**deployment) for deployment in response]
