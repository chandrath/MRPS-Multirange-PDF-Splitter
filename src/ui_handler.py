import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pdf_handler import parse_page_ranges, extract_and_save_pages

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Page Extractor")
        self.root.geometry("500x300")

        # Input PDF file selection
        tk.Label(root, text="Select Input PDF File:").pack(anchor="w", pady=5)
        self.pdf_path_entry = tk.Entry(root, width=50)
        self.pdf_path_entry.pack(padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_pdf).pack(pady=5)

        # Page ranges input
        tk.Label(root, text="Enter Page Ranges (e.g., 3-12, 25-34):").pack(anchor="w", pady=5)
        self.page_ranges_entry = tk.Entry(root, width=50)
        self.page_ranges_entry.pack(padx=10, pady=5)

        # Output folder selection
        tk.Label(root, text="Select Output Folder:").pack(anchor="w", pady=5)
        self.output_dir_entry = tk.Entry(root, width=50)
        self.output_dir_entry.pack(padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_output_folder).pack(pady=5)

        # Action buttons
        tk.Button(root, text="Extract Pages", command=self.extract_pages).pack(pady=10)
        tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path_entry.delete(0, tk.END)
            self.pdf_path_entry.insert(0, file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, folder_path)

    def extract_pages(self):
        pdf_path = self.pdf_path_entry.get().strip()
        page_ranges_str = self.page_ranges_entry.get().strip()
        output_dir = self.output_dir_entry.get().strip()

        if not pdf_path or not page_ranges_str or not output_dir:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            page_ranges = parse_page_ranges(page_ranges_str)
            os.makedirs(output_dir, exist_ok=True)
            extract_and_save_pages(pdf_path, output_dir, page_ranges)
            messagebox.showinfo("Success", "Pages extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
