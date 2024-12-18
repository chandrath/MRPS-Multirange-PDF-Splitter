# pdf_handler.py
import os
import re
from pikepdf import Pdf, PdfError, PdfImage

def sanitize_filename(filename):
    """
    Removes or replaces characters that are not allowed in file names.
    """
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, "_", filename)
    return sanitized.strip()

def parse_page_ranges(page_ranges_str, with_descriptions=False):
    """
    Parses a page ranges string into a list of tuples.
    If with_descriptions is True, handles ranges with descriptions.
    """
    ranges = []
    try:
        for part in page_ranges_str.split(","):
            part = part.strip()
            if with_descriptions:
                # Handle format like "19-48 (Introduction to Computer Science)"
                if "(" in part and ")" in part:
                    range_part, description = part.split("(", 1)
                    description = description.strip(")")
                    start, end = map(int, range_part.split("-"))
                    if start <= end:
                        sanitized_description = sanitize_filename(description)
                        ranges.append((start, end, sanitized_description))
                    else:
                        raise ValueError(f"Invalid range: {range_part}")
                else:
                    raise ValueError(f"Invalid range format with description: {part}")
            else:
                # Handle simple ranges like "19-48"
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    if start <= end:
                        ranges.append((start, end))
                    else:
                         raise ValueError(f"Invalid range: {part}")
                elif part.isdigit():
                    page = int(part)
                    ranges.append((int(part), int(part)))
                else:
                    raise ValueError(f"Invalid range format: {part}")
    except Exception as e:
        raise ValueError(f"Error parsing ranges: {e}")
    
    return ranges

def extract_and_save_pages(input_pdf, output_dir, page_ranges, with_descriptions=False, compress=False):
    """
    Extracts the specified page ranges from the input PDF and saves each range as a new PDF.
    Uses pikepdf to potentially compress the output.
    """
    if not os.path.exists(input_pdf):
        raise FileNotFoundError("Input PDF file does not exist.")

    try:
        pdf = Pdf.open(input_pdf)
        total_pages = len(pdf.pages)
        counter = 1  # Counter for numbered file naming

        for range_info in page_ranges:
            if with_descriptions:
                start, end, description = range_info
                file_name = f"{counter}- {description}.pdf"
                counter += 1
            else:
                start, end = range_info
                file_name = f"pages_{start}-{end}.pdf"

            if start < 1 or end > total_pages:
                raise ValueError(f"Page range {start}-{end} is out of bounds. PDF has {total_pages} pages.")
            
            output_pdf = Pdf.new()
            for page_num in range(start - 1, end):
                output_pdf.pages.append(pdf.pages[page_num])
            
            output_file = os.path.join(output_dir, sanitize_filename(file_name))

            try:
                output_pdf.save(output_file)
                print(f"Saved: {output_file}")
            except PdfError as e:
                raise RuntimeError(f"Failed to save output PDF: {e}")

    except Exception as e:
        raise RuntimeError(f"Failed to extract pages: {e}")