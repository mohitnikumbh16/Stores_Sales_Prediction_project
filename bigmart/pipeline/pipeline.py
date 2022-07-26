from collections import namedtuple
from datetime import datetime
import uuid
from bigmart.config.configuration import Configuartion
from bigmart.logger import logging, get_log_file_name
from bigmart.exception import BigmartException, HousingException
from threading import Thread
from typing import List

from multiprocessing import Process
from bigmart.entity.artifact_entity import ModelPusherArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from bigmart.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from bigmart.entity.config_entity import DataIngestionConfig, ModelEvaluationConfig
from bigmart.component.data_ingestion import DataIngestion
from bigmart.component.data_validation import DataValidation
from bigmart.component.data_transformation import DataTransformation
from bigmart.component.model_trainer import ModelTrainer
from bigmart.component.model_evaluation import ModelEvaluation
from bigmart.component.model_pusher import ModelPusher
import os, sys
from collections import namedtuple
from datetime import datetime
import pandas as pd
from bigmart.constant import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME


Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                        "running_status", "start_time", "stop_time", "execution_time", "message",
                                        "experiment_file_path", "accuracy", "is_model_accepted"])





class Pipeline(Thread):
    experiment: Experiment = Experiment(*([None] * 11))
    experiment_file_path = None

    def __init__(self, config: Configuartion ) -> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
            Pipeline.experiment_file_path=os.path.join(config.training_pipeline_config.artifact_dir,EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME)
            super().__init__(daemon=False, name="pipeline")
            self.config = config
        except Exception as e:
            raise BigmartException(e, sys) from e