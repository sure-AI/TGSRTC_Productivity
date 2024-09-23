from TGSRTC_Productivity import logger
from TGSRTC_Productivity.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
#from TGSRTC_Productivity.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
#from TGSRTC_Productivity.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
#from TGSRTC_Productivity.pipeline.stage_04_model_trainer  import ModelTrainerTrainingPipeline
#from TGSRTC_Productivity.pipeline.stage_05_model_evaluation import ModelEvaluationTrainingPipeline


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e
