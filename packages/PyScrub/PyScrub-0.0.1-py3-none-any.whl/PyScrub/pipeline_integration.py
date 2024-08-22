# pipeline_integration.py

import logging
import time
from collections import deque


class DataPipeline:
    def __init__(self):
        self.steps = deque()
        self.logger = logging.getLogger(__name__)

    def add_step(self, func, *args, **kwargs):
        """
        Add a processing step to the pipeline.

        Args:
            func (callable): The function to execute as a step in the pipeline.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """
        self.steps.append((func, args, kwargs))
        self.logger.info(f"Added step: {func.__name__}")

    def execute(self, data):
        """
        Execute the pipeline on the given dataset.

        Args:
            data (DataFrame): The input dataset.

        Returns:
            DataFrame: The processed dataset after all pipeline steps.
        """
        self.logger.info("Starting pipeline execution")
        for step, args, kwargs in self.steps:
            self.logger.info(f"Executing step: {step.__name__}")
            data = step(data, *args, **kwargs)
            self.logger.info(f"Step {step.__name__} completed")
        self.logger.info("Pipeline execution finished")
        return data

    def reset(self):
        """
        Reset the pipeline by clearing all steps.
        """
        self.steps.clear()
        self.logger.info("Pipeline reset")

    def save_pipeline(self, filepath):
        """
        Save the pipeline configuration to a file for reuse.

        Args:
            filepath (str): The file path to save the pipeline configuration.
        """
        with open(filepath, 'w') as file:
            for step, args, kwargs in self.steps:
                file.write(f"{step.__name__} {args} {kwargs}\n")
        self.logger.info(f"Pipeline saved to {filepath}")

    def load_pipeline(self, filepath, function_map):
        """
        Load a pipeline configuration from a file.

        Args:
            filepath (str): The file path to load the pipeline configuration from.
            function_map (dict): A dictionary mapping function names to function objects.
        """
        self.reset()
        with open(filepath, 'r') as file:
            for line in file:
                step_name, args_str, kwargs_str = line.split(' ', 2)
                step_func = function_map[step_name]
                args = eval(args_str)
                kwargs = eval(kwargs_str)
                self.add_step(step_func, *args, **kwargs)
        self.logger.info(f"Pipeline loaded from {filepath}")


def setup_logging(log_file='pipeline.log'):
    """
    Setup logging for the pipeline.

    Args:
        log_file (str): The name of the log file to write to.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


class PipelineMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def monitor(self, pipeline, data):
        """
        Monitor the execution of the pipeline.

        Args:
            pipeline (DataPipeline): The data pipeline to monitor.
            data (DataFrame): The dataset to process.

        Returns:
            DataFrame: The processed dataset after pipeline execution.
        """
        start_time = time.time()
        self.logger.info("Starting monitoring of the pipeline")

        result = pipeline.execute(data)

        end_time = time.time()
        duration = end_time - start_time
        self.logger.info(f"Pipeline execution time: {duration:.2f} seconds")

        return result
