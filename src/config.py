from pathlib import Path
from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
import logging

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
            if data:
                path.write_text(data)
            elif url:
                logger.info(f"Downloading {path.name} from {url}")

                response = httpx.get(url)
                response.raise_for_status()

                data = response.text
                path.write_text(data)

                logger.info(f"Downloaded {path.name} to {path}")
            elif not path.exists():
                raise FileNotFoundError(f"{path.name} file not found at {path}")


config = Config()
