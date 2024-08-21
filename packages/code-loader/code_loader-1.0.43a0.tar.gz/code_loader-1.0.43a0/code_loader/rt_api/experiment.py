
from typing import Dict, List, Optional
from code_loader.rt_api import Epoch, ExperimentContext
from code_loader.rt_api.types import Metrics
from code_loader.rt_api.workingspace_config_utils import load_workspace_config
from .api_client import  SetExperimentNotesRequest, StartExperimentRequest, ApiClient

        
class Experiment:
    def __init__(self, ctx: ExperimentContext):
        self.ctx = ctx

    def start_epoch(self, epoch: int) -> Epoch:
        return Epoch(self.ctx, epoch)
    
    def add_epoch(self, epoch: int, metrics: Optional[Metrics] = None, model_path: Optional[str] = None, tags: List[str] = ['latest'])-> None:
        epoch_o = self.start_epoch(epoch)
        if metrics is not None:
            epoch_o.set_metrics(metrics)
        epoch_o.save(model_path, tags)

    def set_notes(self, notes: Dict[str, any])-> None: # type: ignore[valid-type]
        print(f"Setting experiment({self.ctx.experiment_id}) notes")
        self.ctx.client.set_experiment_notes(SetExperimentNotesRequest(
            experimentId=self.ctx.experiment_id,
            projectId=self.ctx.project_id,
            notes=notes
        ))
    
    @staticmethod
    def Start(experimentName: str, description: str, working_dir: Optional[str] = None, client: Optional[ApiClient] = None) -> 'Experiment':
        
        if client is None:
            client = ApiClient()
        
        workspace_config = load_workspace_config(working_dir)
        if workspace_config is None or workspace_config.projectId is None:
            raise Exception("No leap workspace config found or projectId is missing, make sure you are in a leap workspace directory or provide a working_dir")

        result = client.start_experiment(StartExperimentRequest(
            projectId=workspace_config.projectId,
            experimentName=experimentName,
            description=description,
            codeIntegrationVersionId=workspace_config.codeIntegrationId
        ))
        ctx = ExperimentContext(client, result.projectId, result.versionId, result.experimentId)
        return Experiment(ctx)
