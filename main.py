from pathlib import Path
from src.config import config
import logging
import subprocess

logger = logging.getLogger(__name__)

PROCESS_CODES = {
    0: "SUCCESS",
    1: "FAILURE",
    2: "WARNING",
    3: "ERROR",
    4: "CRITICAL",
    5: "FATAL",
    6: "UNKNOWN",
}

def load_commands(path: Path) -> list[str]:
    return path.read_text().splitlines()

def main():
    logger.info("Starting rclone-sync")
    commands = load_commands(config.rclone_commands)

    for command in commands:
        logger.info(f"Running command: {command}")
        result = subprocess.run(command, shell=True, check=True)
        logger.info(f"Command result: {PROCESS_CODES[result.returncode]}")

    logger.info("All commands completed")

if __name__ == "__main__":
    main()
