import tkinter as tk
from tkinter import filedialog, messagebox, Menu, scrolledtext
import os
from pdf_handler import parse_page_ranges, extract_and_save_pages

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MultiRange PDF Splitter")
        self.root.geometry("600x400")  # Slightly larger window
        self.root.minsize(600, 400)  # Minimum size to prevent awkward resizing

        # Styling and padding
        FONT = ("Arial", 12)
        BUTTON_FONT = ("Arial", 12, "bold")

        # Menu bar
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=about_menu)

        # Input PDF file selection
        tk.Label(root, text="Select Input PDF File:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.pdf_path_entry = tk.Entry(root, width=60, font=FONT)
        self.pdf_path_entry.pack(padx=10, pady=5)
        tk.Button(root, text="Browse", font=FONT, command=self.select_pdf).pack(pady=5)

        # Page ranges input
        tk.Label(root, text="Enter Page Ranges (e.g., 3-12, 25-34):", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.page_ranges_entry = scrolledtext.ScrolledText(root, height=4, width=60, font=FONT, wrap=tk.WORD)
        self.page_ranges_entry.pack(padx=10, pady=5, fill="x", expand=True)

        # Output folder selection
        tk.Label(root, text="Select Output Folder:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.output_dir_entry = tk.Entry(root, width=60, font=FONT)
        self.output_dir_entry.pack(padx=10, pady=5)
        tk.Button(root, text="Browse", font=FONT, command=self.select_output_folder).pack(pady=5)

        # Action buttons
        self.extract_button = tk.Button(root, text="Extract Pages", font=BUTTON_FONT, bg="#4CAF50", fg="white",
                                        padx=10, pady=5, command=self.extract_pages)
        self.extract_button.pack(pady=10)

        tk.Button(root, text="Exit", font=FONT, bg="#f44336", fg="white", command=root.quit).pack(pady=5)

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
        page_ranges_str = self.page_ranges_entry.get("1.0", tk.END).strip()
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

    def show_about(self):
        about_text = (
            "MultiRange PDF Splitter v0.1.1\n"
            "A tool to extract specific page ranges from a PDF file and save them as separate files.\n\n"
            "Developed by: Shree (https://github.com/chandrath)\n"
            "License: MIT License\n\n"
            
        )
        messagebox.showinfo("About PDF Page Extractor", about_text)
