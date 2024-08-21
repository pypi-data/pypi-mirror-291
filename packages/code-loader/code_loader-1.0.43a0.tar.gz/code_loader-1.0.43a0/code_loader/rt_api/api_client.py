
from dataclasses import dataclass
from typing import Dict, List, Optional
from code_loader.rt_api.types import ApiMetrics
from code_loader.rt_api.utils import join_url, to_dict_no_none
from .cli_config_utils import get_auth_config
import requests


@dataclass
class StartExperimentRequest:
    projectId: str
    experimentName: str
    description: str
    removeUntaggedUploadedModels: bool = True
    codeIntegrationVersionId: Optional[str] = None

@dataclass
class StartExperimentResponse:
    projectId: str
    versionId: str
    experimentId: str

@dataclass
class GetUploadModelSignedUrlRequest:
    epoch: int
    experimentId: str
    versionId: str
    projectId: str
    fileType: str
    origin: Optional[str] = None

@dataclass
class GetUploadModelSignedUrlResponse:
    url: str
    fileName: str

@dataclass
class AddExternalEpochDataRequest:
  projectId: str
  experimentId: str
  epoch: int
  metrics: ApiMetrics
  force: bool = False

@dataclass
class TagModelRequest:
  projectId: str
  experimentId: str
  epoch: int
  tags: List[str]

@dataclass
class SetExperimentNotesRequest:
    projectId: str
    experimentId: str
    notes: Dict[str, any] # type: ignore[valid-type]

class ApiClient:
    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        if url is None or token is None:
            configAuth = get_auth_config()
            if configAuth is None:
                raise Exception("No auth config found, either provide url and token or use `leap auth [url] [token]` to setup a config file")
            url = configAuth.api_url
            token = configAuth.api_key
        
        self.url = url
        self.token = token

    def __add_auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def __post(self, post_path: str, data: any, headers: Dict[str, str] = {})-> requests.Response: # type: ignore[valid-type]
        headers = self.__add_auth(headers)
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        url = join_url(self.url, post_path)
        json_data = to_dict_no_none(data)
        return requests.post(url, json=json_data, headers=headers)
    
    def __check_response(self, response: requests.Response)-> None:
        if response.status_code >= 400:
            raise Exception(f"Error: {response.status_code} {response.text}")
    
    def start_experiment(self, data: StartExperimentRequest) -> StartExperimentResponse:
        response = self.__post('/versions/startExperiment', data)
        self.__check_response(response)
        return StartExperimentResponse(**response.json())
    
    def get_attach_model_upload_signed_url(self, data: GetUploadModelSignedUrlRequest)-> GetUploadModelSignedUrlResponse:
        response = self.__post('/versions/getUploadModelSignedUrl', data)
        self.__check_response(response)
        return GetUploadModelSignedUrlResponse(**response.json())
    
    def add_external_epoch_data(self, data: AddExternalEpochDataRequest)-> None:
        response = self.__post('/externalepochdata/addExternalEpochData', data)
        self.__check_response(response)
    
    def tag_model(self, data: TagModelRequest)-> None:
        response = self.__post('/versions/tagModel', data)
        self.__check_response(response)

    def set_experiment_notes(self, data: SetExperimentNotesRequest)-> None:
        response = self.__post('/versions/setExperimentNotes', data)
        self.__check_response(response)