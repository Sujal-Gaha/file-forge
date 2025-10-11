# file-forge 🔨

I just wanted to make my own file processor as I don't trust other services which may steal my data.

## Features

- **Image Processing**

  - Convert between formats (JPG, PNG, WEBP, GIF, BMP, TIFF)
  - Compress images with quality control
  - Resize images while maintaining aspect ratio
  - Batch processing support

- **Document Conversion**

  - PDF to TXT extraction
  - DOCX to TXT conversion
  - TXT to DOCX creation
  - PDF page extraction and merging

- **Privacy-First**
  - All processing happens locally on your machine
  - No data uploaded to external servers
  - No tracking or analytics
  - Open source and transparent

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/file-forge.git
cd file-forge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install file-forge
```

## Quick Start

```bash
# Check version
file-forge version

# Get file information
file-forge info image.jpg

# Convert image format
file-forge image convert input.png jpg

# Compress image
file-forge image compress photo.jpg --quality 85

# Resize image
file-forge image resize large.jpg --width 800

# Convert document
file-forge doc convert document.pdf txt
```

## Usage

### Image Commands

#### Convert Image Format

```bash
file-forge image convert INPUT_FILE OUTPUT_FORMAT [OPTIONS]

Options:
  -o, --output PATH       Output file path
  -q, --quality INTEGER   Image quality 1-100 (default: 95)
```

Example:

```bash
# Convert PNG to JPG
file-forge image convert photo.png jpg -q 90

# Convert with custom output path
file-forge image convert input.webp png -o output/result.png
```

#### Compress Image

```bash
file-forge image compress INPUT_FILE [OPTIONS]

Options:
  -q, --quality INTEGER    Compression quality 1-100 (default: 85)
  -o, --output PATH       Output file path
  --max-width INTEGER     Maximum width in pixels
  --max-height INTEGER    Maximum height in pixels
```

Example:

```bash
# Compress with quality 80
file-forge image compress large-photo.jpg -q 80

# Compress and resize
file-forge image compress photo.jpg --max-width 1920 --max-height 1080
```

#### Resize Image

```bash
file-forge image resize INPUT_FILE [OPTIONS]

Options:
  -w, --width INTEGER               Target width
  -h, --height INTEGER              Target height
  -o, --output PATH                 Output file path
  --maintain-aspect/--no-maintain-aspect  Maintain aspect ratio (default: True)
```

Example:

```bash
# Resize to specific width (height auto-calculated)
file-forge image resize photo.jpg -w 800

# Resize to exact dimensions without maintaining aspect
file-forge image resize photo.jpg -w 800 -h 600 --no-maintain-aspect
```

### Document Commands

#### Convert Document

```bash
file-forge doc convert INPUT_FILE OUTPUT_FORMAT [OPTIONS]

Options:
  -o, --output PATH       Output file path
```

Supported conversions:

- PDF → TXT
- DOCX → TXT
- TXT → DOCX

Example:

```bash
# Extract text from PDF
file-forge doc convert document.pdf txt

# Convert text to Word document
file-forge doc convert notes.txt docx
```

### File Information

```bash
file-forge info INPUT_FILE
```

Get detailed information about any file including size, dimensions (for images), and format.

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=file_forge

# Format code
black file_forge/

# Type checking
mypy file_forge/
```

## Dependencies

- **typer**: CLI framework
- **Pillow**: Image processing
- **PyPDF2**: PDF manipulation
- **python-docx**: Word document handling
- **rich**: Beautiful terminal output

## Roadmap

- [ ] Image format conversion
- [ ] Video format conversion
- [ ] Audio format conversion
- [ ] Batch processing for multiple files
- [ ] Progress bars for long operations
- [ ] Configuration file support
- [ ] Custom presets for common operations
- [ ] Image watermarking
- [ ] PDF encryption/decryption

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Privacy & Security

file-forge processes all files locally on your machine. No files are uploaded to external servers, and no usage data is collected. Your files remain private and secure.

## Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check the documentation
- Review existing issues for solutions

## Acknowledgments

Built with modern Python tools and libraries to provide a trustworthy, privacy-focused alternative to online file conversion services.
