from pathlib import Path
from typing import Any, Optional
from moviepy import VideoFileClip


class VideoProcessor:
    def __init__(self, input_path: Path, output_path: Optional[Path] = None):
        self.input_path = input_path
        self.output_path = output_path

    def convert(self, output_format: str, quality: int = 95) -> Path:
        output_format = output_format.lower().replace(".", "")

        if self.output_path is None:
            self.output_path = self.input_path.with_suffix(f".{output_format}")

        self.output_path = self.output_path.resolve()

        with VideoFileClip(filename=self.input_path) as clip:
            clip.write_videofile(
                filename=self.output_path,
                codec="libx264" if output_format == "mp4" else None,
                bitrate="5000k",
                preset="veryslow",
                audio_codec="aac",
                audio_bitrate="192k",
                logger=None,
            )

        return self.output_path
