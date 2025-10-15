from pathlib import Path
from typing import Optional, Any

from PIL import Image


class ImageProcessor:
    def __init__(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
    ) -> None:
        """
        Initialize ImageProcessor

        Args:
            input_path: Path to input image
            output_path: Optional output path

        Returns:
            None
        """
        self.input_path = input_path
        self.output_path = output_path
        self.input_path_suffix = input_path.suffix.lower()

    def _resize_with_aspect_ratio(
        self,
        img: Image.Image,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> Image.Image:
        """
        Resize image while maintaining aspect ratio

        Args:
            img: PIL Image object
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels

        Returns:
            Resized PIL Image object
        """
        original_width, original_height = img.size

        if max_width and max_height:
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height

            ratio = min(width_ratio, height_ratio)

            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        elif max_width:
            ratio = max_width / original_width
            new_width = max_width
            new_height = int(original_height * ratio)
        elif max_height:
            ratio = max_height / original_height
            new_width = int(original_width * ratio)
            new_height = max_height
        else:
            return img

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _generate_output_path(
        self,
        output_format: Optional[str],
        angle: Optional[int],
        dimension_str: Optional[str],
    ) -> Path:
        stem = self.input_path.stem
        suffix = self.input_path.suffix

        if output_format:
            return self.input_path.with_suffix(f".{output_format}")
        elif dimension_str:
            return self.input_path.parent / f"{stem}_resized_{dimension_str}{suffix}"
        elif angle:
            return self.input_path.parent / f"{stem}_rotated_{angle}{suffix}"
        else:
            return self.input_path.parent / f"{stem}_compressed{suffix}"

    def convert(self, output_format: str, quality: int = 95) -> Path:
        """
        Convert image to a different format

        Args:
            output_path: Optional output path (ex: jpg, png, webp, etc.)
            quality: Image quality (1-100) (default: 95)

        Returns:
            Path to converted image
        """
        output_format = output_format.lower().replace(".", "")

        if self.output_path is None:
            self.output_path = self._generate_output_path(output_format, None, None)

        with Image.open(self.input_path) as img:
            if output_format in ["jpg", "jpeg"] and img.mode in ["RGBA", "LA", "P"]:
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                rgb_img.paste(
                    img, mask=img.split()[-1] if img.mode in ["RGBA", "LA"] else None
                )
                img = rgb_img

            if img.mode == "P" and output_format not in ["png", "gif"]:
                img = img.convert("RGB")

            save_kwargs: dict[str, Any] = {"quality": quality, "optimize": True}

            if output_format in ["jpg", "jpeg"]:
                save_kwargs["format"] = "JPEG"
            elif output_format == "png":
                save_kwargs["format"] = ("PNG",)
                save_kwargs.pop("quality")
            elif output_format == "webp":
                save_kwargs["format"] = "WEBP"
            elif output_format == "gif":
                save_kwargs["format"] = "GIF"
                save_kwargs.pop("quality")
            else:
                save_kwargs["format"] = output_format.upper()

            img.save(self.output_path, **save_kwargs)

        return self.output_path

    def compress(
        self,
        quality: int = 85,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> Path:
        """
        Compress image file

        Args:
            quality: Compression quality (1-100) (default: 85)
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels

        Returns:
            Path to compressed image
        """
        if self.output_path is None:
            self.output_path = self._generate_output_path(None, None, None)

        with Image.open(self.input_path) as img:
            if max_width or max_height:
                img = self._resize_with_aspect_ratio(img, max_width, max_height)

            save_kwargs: dict[str, Any] = {"optimize": True}

            if self.input_path_suffix in [".jpg", ".jpeg"]:
                save_kwargs["quality"] = quality
                save_kwargs["format"] = "JPEG"
            elif self.input_path_suffix == ".png":
                save_kwargs["format"] = "PNG"
                save_kwargs["compress_level"] = 9
            elif self.input_path_suffix == ".webp":
                save_kwargs["quality"] = quality
                save_kwargs["format"] = "WEBP"
            else:
                save_kwargs["quality"] = quality

            img.save(self.output_path, **save_kwargs)

        return self.output_path

    def resize(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
    ) -> Path:
        """
        Resize image to specified dimensions

        Args:
            width: Target width in pixels
            height: Target height in pixels
            maintain_aspect: Whether to maintain aspect ratio

        Returns:
            Path to resized image
        """

        if self.output_path is None:
            dimension_str = f"{width or 'auto'}x{height or 'auto'}"
            self.output_path = self._generate_output_path(None, None, dimension_str)

        with Image.open(self.input_path) as img:
            if maintain_aspect:
                img = self._resize_with_aspect_ratio(img, width, height)
            else:
                if width and height:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    raise ValueError(
                        "Both width and height must be specified when not maintaining aspect ratio"
                    )

            save_kwargs: dict[str, Any] = {"optimize": True}
            if self.input_path_suffix in [".jpg", ".jpeg"]:
                save_kwargs["quality"] = 95

            img.save(self.output_path, **save_kwargs)

        return self.output_path

    def rotate_image(self, angle: int, expand: bool = True) -> Path:
        """
        Rotate image by specified angle

        Args:
            input_path: Path to input image
            angle: Rotation angle in degrees (positive = counter-clockwise)
            output_path: Optional output path
            expand: Whether to expand image to fit rotated content

        Returns:
            Path to rotated image
        """

        if self.output_path is None:
            self.output_path = self._generate_output_path(None, angle, None)

        with Image.open(self.input_path) as img:
            rotated = img.rotate(angle, expand=expand, fillcolor="white")
            rotated.save(self.output_path, optimize=True)

        return self.output_path
