# Metadata Cleaner

Metadata Cleaner is a Python tool that removes metadata from various file types, including images, PDFs, Office files, audio files, and videos. It helps you preserve privacy by eliminating sensitive information from your files.

## Supported File Types

- **Images**: JPEG, PNG, TIFF, BMP
- **PDFs**
- **Microsoft Office Files**:
  - **DOCX** (Word)
  - **XLSX** (Excel)
- **Audio Files**: MP3, FLAC, OGG, WAV
- **Videos**: MP4, MKV, MOV, AVI, FLV

## How to Use

### Example Commands

- **Remove all metadata from a DOCX file**:
  ```bash
  python metadata_cleaner.py input.docx --output output.docx
  ```

- **Remove specific metadata from an audio file**:
  ```bash
  python metadata_cleaner.py input.mp3 --attributes artist album
  ```

### Removing Specific Attributes

- **DOCX**: author, title, subject, comments
- **XLSX**: creator, title, subject, keywords, comments
- **Audio (MP3)**: artist, album, genre, etc.

### Command-Line Options

- `input`: The path to the input file.
- `--output`: The path for the output file (required for some file types).
- `--attributes`: A list of specific attributes to remove (supported file types only).

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/metadata_cleaner.git
   ```
2. Navigate into the project directory:
   ```bash
   cd metadata_cleaner
   ```
3. Install the dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Contact Information

- **Author**: Varol Cagdas Tok
- **Email**: [c.tok@campus.lmu.de](mailto:c.tok@campus.lmu.de)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
