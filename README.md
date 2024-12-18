<!-- Cover Icon -->
<p align="center">
  <img src="Cover Icon.png" alt="MRPS - Multirange PDF Splitter Icon" width="200" height="200">
</p>

<h1 align="center">MRPS - Multirange PDF Splitter</h1>

<p align="center">
  🚀 A powerful tool to extract specific page ranges from a PDF file and save them as individual PDF files.
</p>

---

## Features

- ✅ **Simple GUI:** Easy-to-use interface for non-technical users.
- ✅ **Multi-Range Support:** Extract multiple custom page ranges from a PDF file at once.
- ✅ **Flexible Page Range Input:** Supports both simple range formats (e.g., "3-12, 25-34") and ranges with descriptions (e.g., "19-48 (Chapter 1)").
- ✅ **Lossless Output Quality:** Maintains original PDF formatting and quality when extracting pages.
- ✅ **Fast and Lightweight:** Handles large PDFs efficiently.
- ✅ **Path History:** Remembers the last 5 used input PDF file paths and output directories for easy access.

---

## Screenshots

### Simple User Interface

![PDF Extractor UI](https://i.imgur.com/BNBfmIw.png)

---

## Getting Started

### Prerequisites

To build or run the program:

- Python 3.8+ installed (if running from source).
- Dependencies listed in `requirements.txt`.

### Installation

#### **Run as Executable (Recommended)**

1. Download the latest release from the [Releases Page](https://github.com/chandrath/MRPS-Multirange-PDF-Splitter/releases).
2. Run the **`PDF Page Extractor.exe`** file.

#### **Run from Source**

1. Clone this repository:
   ```bash
   git clone https://github.com/chandrath/MRPS-Multirange-PDF-Splitter.git
   cd mrps-multirange-pdf-splitter
   ```
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application:
   python main.py

## Usage

### Input PDF:

- Select the PDF file you want to extract pages from.

### Enter Page Ranges:

- Use the format `3-12, 25-34, 47-56, ...` for multiple ranges.

### Select Output Folder:

- Choose where you want the extracted PDFs to be saved.

### Extract:

- Click on the "Extract Pages" button, and the program will save each range as a separate PDF file.

## Roadmap

- Include a progress bar for large PDF operations.
- Add drag-and-drop support for input files.

## License

- "MRPS - Multirange PDF Splitter" uses the GPLv3 license

Feel free to open an issue to suggest more features or report bugs!
