"""
Image conversion and compression utilities
"""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageOps


def convert_image(
    input_path: Path,
    output_format: str,
    output_path: Optional[Path] = None,
    quality: int = 95,
) -> Path:
    """
    Convert image to a different format

    Args:
        input_path: Path to input image
        output_format: Target format (jpg, png, webp, etc.)
        output_path: Optional output path
        quality: Image quality (1-100)

    Returns:
        Path to converted image
    """
    # Normalize format
    output_format = output_format.lower().replace(".", "")

    # Generate output path if not provided
    if output_path is None:
        output_path = input_path.with_suffix(f".{output_format}")

    # Open and convert image
    with Image.open(input_path) as img:
        # Convert RGBA to RGB for formats that don't support transparency
        if output_format in ["jpg", "jpeg"] and img.mode in ["RGBA", "LA", "P"]:
            # Create a white background
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            rgb_img.paste(
                img, mask=img.split()[-1] if img.mode in ["RGBA", "LA"] else None
            )
            img = rgb_img

        # Handle palette mode images
        if img.mode == "P" and output_format not in ["png", "gif"]:
            img = img.convert("RGB")

        # Save with appropriate parameters
        from typing import Any

        save_kwargs: dict[str, Any] = {"quality": quality, "optimize": True}

        if output_format in ["jpg", "jpeg"]:
            save_kwargs["format"] = "JPEG"
        elif output_format == "png":
            save_kwargs["format"] = "PNG"
            save_kwargs.pop("quality")  # PNG doesn't use quality parameter
        elif output_format == "webp":
            save_kwargs["format"] = "WEBP"
        elif output_format == "gif":
            save_kwargs["format"] = "GIF"
            save_kwargs.pop("quality")
        else:
            save_kwargs["format"] = output_format.upper()

        img.save(output_path, **save_kwargs)

    return output_path


def compress_image(
    input_path: Path,
    quality: int = 85,
    output_path: Optional[Path] = None,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
) -> Path:
    """
    Compress image file

    Args:
        input_path: Path to input image
        quality: Compression quality (1-100)
        output_path: Optional output path
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels

    Returns:
        Path to compressed image
    """
    # Generate output path if not provided
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_compressed{suffix}"

    with Image.open(input_path) as img:
        # Resize if max dimensions are specified
        if max_width or max_height:
            img = _resize_with_aspect_ratio(img, max_width, max_height)

        # Optimize and compress
        from typing import Any

        save_kwargs: dict[str, Any] = {"optimize": True}

        # Format-specific settings
        if input_path.suffix.lower() in [".jpg", ".jpeg"]:
            save_kwargs["quality"] = quality
            save_kwargs["format"] = "JPEG"
        elif input_path.suffix.lower() == ".png":
            # PNG compression is lossless, so we use optimization
            save_kwargs["format"] = "PNG"
            save_kwargs["compress_level"] = 9
        elif input_path.suffix.lower() == ".webp":
            save_kwargs["quality"] = quality
            save_kwargs["format"] = "WEBP"
        else:
            save_kwargs["quality"] = quality

        img.save(output_path, **save_kwargs)

    return output_path


def resize_image(
    input_path: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
    output_path: Optional[Path] = None,
    maintain_aspect: bool = True,
) -> Path:
    """
    Resize image to specified dimensions

    Args:
        input_path: Path to input image
        width: Target width in pixels
        height: Target height in pixels
        output_path: Optional output path
        maintain_aspect: Whether to maintain aspect ratio

    Returns:
        Path to resized image
    """
    # Generate output path if not provided
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        dimension_str = f"{width or 'auto'}x{height or 'auto'}"
        output_path = input_path.parent / f"{stem}_resized_{dimension_str}{suffix}"

    with Image.open(input_path) as img:
        if maintain_aspect:
            img = _resize_with_aspect_ratio(img, width, height)
        else:
            if width and height:
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            else:
                raise ValueError(
                    "Both width and height must be specified when not maintaining aspect ratio"
                )

        # Save with original format settings
        from typing import Any

        save_kwargs: dict[str, Any] = {"optimize": True}
        if input_path.suffix.lower() in [".jpg", ".jpeg"]:
            save_kwargs["quality"] = 95

        img.save(output_path, **save_kwargs)

    return output_path


def _resize_with_aspect_ratio(
    img: Image.Image, max_width: Optional[int] = None, max_height: Optional[int] = None
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
        # Calculate scaling factors
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height
        # Use the smaller ratio to ensure image fits within bounds
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


def rotate_image(
    input_path: Path,
    angle: int,
    output_path: Optional[Path] = None,
    expand: bool = True,
) -> Path:
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
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_rotated_{angle}{suffix}"

    with Image.open(input_path) as img:
        rotated = img.rotate(angle, expand=expand, fillcolor="white")
        rotated.save(output_path, optimize=True)

    return output_path
