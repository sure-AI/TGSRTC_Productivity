from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    #penalty: str #added for LR
    #solver: str  #added for LR
    #C: float     #added for LR
    #alpha: float
    #l1_ratio: float
    n_estimators: float         #added for rf       
    max_depth: float            #added for rf           
    min_samples_split: float    #added for rf    
    max_features: str           #added for rf
    random_state: float         #added for rf
    target_column: str          


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str
    
    
@dataclass(frozen=True)
class ModelPredictionConfig:
    model_path: Path
    data_path: Path