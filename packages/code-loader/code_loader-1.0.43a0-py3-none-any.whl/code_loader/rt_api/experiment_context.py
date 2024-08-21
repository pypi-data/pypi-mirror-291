from dataclasses import dataclass
from code_loader.rt_api.api_client import ApiClient


@dataclass
class ExperimentContext:
    client: ApiClient
    project_id: str
    version_id: str
    experiment_id: str