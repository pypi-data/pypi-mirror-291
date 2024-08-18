from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from gmctl.gmclient import GitmoxiClient
import json
import logging

logger = logging.getLogger(__name__)

class Commit(BaseModel):
    commit_hash: str = Field(..., min_length=1)
    repo_url: str = Field(..., min_length=1)
    branch: str = Field(..., min_length=1)
    receive_timestamp: str = Field(..., min_length=1)
    relevant_files: Optional[Dict[str, Any]] = {}
    commit_payload: Optional[Dict[str, Any]] = {}
    status_details: Optional[List[str]] = []
    status: Optional[str] = ""
    
    def __str__(self) -> str:
        return self.model_dump_json()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    def get_relevant_files(self) -> List[Dict[str, Any]]:
        if not self.relevant_files:
            return []
        return_list = []
        for k in self.relevant_files.keys():
            for file_prefix in self.relevant_files[k]:
                for f in self.relevant_files[k][file_prefix]:
                    return_list.append({"commit_hash": self.commit_hash, "repo_url": self.repo_url, 
                                        "branch": self.branch, "change_type": k, 
                                        "file_prefix": file_prefix, "file": f})
        return return_list
    
    def summary(self) -> str:
        summary_keys = ["commit_hash", "repo_url", "branch", "receive_timestamp", "status"]
        return {k: self.to_dict()[k] for k in summary_keys}
            
    @staticmethod
    def get(gmclient: GitmoxiClient, commit_hash: str, repo_url: str) -> List[Any]:
        resource_path = "/commits"
        conditions = []
        if commit_hash:
            conditions.append(f"commit_hash={commit_hash}")
        if repo_url:
            conditions.append(f"repo_url={repo_url}")
        if conditions:
            resource_path += "?" + "&".join(conditions)
        logger.info(f'Getting repository: {resource_path}')
        # make a GET call to the /repository/get endpoint with the repository URL
        commits = gmclient.get(resource_path)
        if not commits:
            logger.error(f'Failed to get repositories for: {resource_path}')
            commits = []
        return [Commit(**commit) for commit in commits]
    
    @staticmethod
    def delete(gmclient: GitmoxiClient, commit_hash: str) -> Optional[Dict[str, Any]]:
        if not commit_hash:
            logger.error(f'Commit hash is required for deletion')
            return None
        resource_path = f"/commits/{commit_hash}/delete"
        logger.info(f'Deleting commit: {resource_path}')
        # make a DELETE call to the /commits/{commit_hash} endpoint
        return gmclient.delete(resource_path)