import os
from PyPDF2 import PdfReader, PdfWriter

def parse_page_ranges(page_ranges_str):
    """
    Parses a page ranges string like "3-12, 25-34" into a list of (start, end) tuples.
    """
    ranges = []
    try:
        for part in page_ranges_str.split(","):
            part = part.strip()
            if "-" in part:
                start, end = map(int, part.split("-"))
                if start <= end:
                    ranges.append((start, end))
                else:
                    raise ValueError(f"Invalid range: {part}")
            elif part.isdigit():
                page = int(part)
                ranges.append((page, page))
            else:
                raise ValueError(f"Invalid range format: {part}")
    except Exception as e:
        raise ValueError(f"Error parsing ranges: {e}")
    
    return ranges

def extract_and_save_pages(input_pdf, output_dir, page_ranges):
    """
    Extracts the specified page ranges from the input PDF and saves each range as a new PDF.
    """
    if not os.path.exists(input_pdf):
        raise FileNotFoundError("Input PDF file does not exist.")

    try:
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)
        for start, end in page_ranges:
            if start < 1 or end > total_pages:
                raise ValueError(f"Page range {start}-{end} is out of bounds. PDF has {total_pages} pages.")
            
            writer = PdfWriter()
            for page_num in range(start - 1, end):  # PdfReader is zero-based
                writer.add_page(reader.pages[page_num])
            
            output_file = os.path.join(output_dir, f"pages_{start}-{end}.pdf")
            with open(output_file, "wb") as out_pdf:
                writer.write(out_pdf)
            print(f"Saved: {output_file}")
    
    except Exception as e:
        raise RuntimeError(f"Failed to extract pages: {e}")
