import logging
from pathlib import Path

def setup_file_logging(log_path: str = "/notebooks/ML/Flight Delay Prediction Project/logs/pipeline.log", level=logging.WARNING):
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)

    # keep noisy Spark bridge loggers quieter than your own app logs
    logging.getLogger("py4j").setLevel(logging.ERROR)
    logging.getLogger("pyspark").setLevel(logging.WARNING)