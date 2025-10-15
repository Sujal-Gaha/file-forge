from pathlib import Path
from typing import Optional


class VideoProcessor:
    def __init__(self, input_path: Path, output_path: Optional[Path] = None):
        self.input_path = input_path
        self.output_path = output_path

    def convert(self, output_format: str, quality: int = 95) -> Path:
        if self.output_path is None:
            self.output_path = self.input_path.with_suffix(f".{output_format}")

        return self.output_path
