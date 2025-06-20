from pathlib import Path
from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
from src.log import logging

logger = logging.getLogger(__name__)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    rclone_config: Optional[Path] = Path("~/.config/rclone/rclone.conf").expanduser()
    rclone_config_url: Optional[str] = None
    rclone_config_data: Optional[str] = None

    rclone_commands: Optional[Path] = Path("~/.config/rclone/commands.sh").expanduser()
    rclone_commands_url: Optional[str] = None
    rclone_commands_data: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:
        for url, path, data in [
            (self.rclone_config_url, self.rclone_config, self.rclone_config_data),
            (self.rclone_commands_url, self.rclone_commands, self.rclone_commands_data),
        ]:
            # Check if at least one source exists
            if not any([path.exists(), data, url]):
                raise FileNotFoundError(f"Neither file, URL, nor data provided for {path.name}")
            
            # Priority 1: If file exists, use that
            if path.exists():
                logger.info(f"Using existing {path.name} at {path}")
                continue
            
            # Priority 2: If data exists, write from data
            if data:
                logger.info(f"Writing {path.name} from data")
                self._write_file(path, data)
                continue
            
            # Priority 3: If URL exists, download from URL
            if url:
                logger.info(f"Downloading {path.name} from {url}")
                response = httpx.get(url)
                response.raise_for_status()
                
                self._write_file(path, response.text)
                
                logger.info(f"Downloaded {path.name} to {path}")
                continue

    def _write_file(self, path: Path, data: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        path.write_text(data)

config = Config()
