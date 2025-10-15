from PIL import Image
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from file_forge.converters.image import ImageProcessor
from file_forge.converters.document import DocumentProcessor
from file_forge.converters.video import VideoProcessor

app = typer.Typer(
    name="file-forge",
    help="A trustworthy CLI tool for file format conversion and image compression",
    add_completion=False,
)
console = Console()

image_app = typer.Typer(help="Image processing and conversion commands")
app.add_typer(image_app, name="image")

doc_app = typer.Typer(help="Document conversion commands")
app.add_typer(doc_app, name="doc")

video_app = typer.Typer(help="Video processing and conversion commands")
app.add_typer(video_app, name="video")


@app.command()
def version():
    """Show file-forge version"""
    console.print(
        Panel.fit(
            "[bold cyan]file-forge[/bold cyan] [green]v0.1.0[/green]\n"
            "A trustworthy, local file processing tool",
            border_style="cyan",
        )
    )


@image_app.command("convert")
def convert_image(
    input_file: Path = typer.Argument(..., help="Input image file path"),
    output_format: str = typer.Argument(
        ..., help="Output format (jpg, png, webp, etc.)"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    quality: int = typer.Option(
        95, "--quality", "-q", help="Image quality (1-100)", min=1, max=100
    ),
):
    """Convert image to different format"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Converting image...", total=None)
            image = ImageProcessor(input_file, output_file)

            result_path = image.convert_image(output_format, quality)

        console.print(f"[green]✓[/green] Image converted successfully: {result_path}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@image_app.command("compress")
def compress_image(
    input_file: Path = typer.Argument(..., help="Input image file path"),
    quality: int = typer.Option(
        85, "--quality", "-q", help="Compression quality (1-100)", min=1, max=100
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    max_width: Optional[int] = typer.Option(
        None, "--max-width", help="Maximum width in pixels"
    ),
    max_height: Optional[int] = typer.Option(
        None, "--max-height", help="Maximum height in pixels"
    ),
):
    """Compress image file"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        original_size = input_file.stat().st_size

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Compressing image...", total=None)
            image = ImageProcessor(input_file, output_file)

            result_path = image.compress_image(quality, max_width, max_height)

        compressed_size = result_path.stat().st_size
        reduction = ((original_size - compressed_size) / original_size) * 100

        console.print(f"[green]✓[/green] Image compressed successfully: {result_path}")
        console.print(f"Original size: {original_size / 1024:.2f} KB")
        console.print(f"Compressed size: {compressed_size / 1024:.2f} KB")
        console.print(f"Size reduction: {reduction:.2f}%")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@image_app.command("resize")
def resize_image(
    input_file: Path = typer.Argument(..., help="Input image file path"),
    width: Optional[int] = typer.Option(
        None, "--width", "-w", help="Target width in pixels"
    ),
    height: Optional[int] = typer.Option(
        None, "--height", "-h", help="Target height in pixels"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    maintain_aspect: bool = typer.Option(
        True, "--maintain-aspect/--no-maintain-aspect", help="Maintain aspect ratio"
    ),
):
    """Resize image to specified dimensions"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        if width is None and height is None:
            console.print(
                "[red]Error:[/red] At least one of --width or --height must be specified"
            )
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Resizing image...", total=None)
            image = ImageProcessor(input_file, output_file)

            result_path = image.resize_image(width, height, maintain_aspect)

        console.print(f"[green]✓[/green] Image resized successfully: {result_path}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@doc_app.command("convert")
def convert_document(
    input_file: Path = typer.Argument(..., help="Input document file path"),
    output_format: str = typer.Argument(..., help="Output format (pdf, txt, docx)"),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
):
    """Convert document to different format"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Converting document...", total=None)
            document = DocumentProcessor(input_file, output_file)

            result_path = document.convert_document(output_format)

        console.print(
            f"[green]✓[/green] Document converted successfully: {result_path}"
        )

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@video_app.command("convert")
def convert_video(
    input_file: Path = typer.Argument(..., help="Input video file path"),
    output_format: str = typer.Argument(
        ..., help="Output format (mkv, mp4, mov, etc.)"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
    quality: int = typer.Option(
        95, "--quality", "-q", help="Video quality (1-100)", min=1, max=100
    ),
):
    """Convert video to different format"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Converting video...", total=None)
            video = VideoProcessor(input_file, output_file)

            result_path = video.convert(output_format, quality)

        console.print(f"[green]✓[green] Video converted successfully: {result_path}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command("info")
def file_info(
    input_file: Path = typer.Argument(..., help="File to get information about"),
):
    """Get detailed information about a file"""
    try:
        if not input_file.exists():
            console.print(f"[red]Error:[/red] File '{input_file}' not found")
            raise typer.Exit(1)

        file_stat = input_file.stat()
        file_size = file_stat.st_size

        info_text = f"""[cyan]File:[/cyan] {input_file.name}
[cyan]Path:[/cyan] {input_file.absolute()}
[cyan]Size:[/cyan] {file_size:,} bytes ({file_size / 1024:.2f} KB)
[cyan]Type:[/cyan] {input_file.suffix}"""

        if input_file.suffix.lower() in [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
        ]:
            with Image.open(input_file) as img:
                info_text += (
                    f"\n[cyan]Dimensions:[/cyan] {img.width} x {img.height} pixels"
                )
                info_text += f"\n[cyan]Format:[/cyan] {img.format}"
                info_text += f"\n[cyan]Mode:[/cyan] {img.mode}"

        console.print(Panel(info_text, title="File Information", border_style="cyan"))

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
