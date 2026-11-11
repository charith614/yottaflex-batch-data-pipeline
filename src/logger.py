
import logging
from pathlib import Path


def setup_logger():
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_folder / "pipeline.log"),
            logging.StreamHandler()
        ],
        force=True
    )

    return logging.getLogger("YottaFlexPipeline")
