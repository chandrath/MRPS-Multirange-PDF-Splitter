# ui_handler.py
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, scrolledtext, ttk
import os
import json
import webbrowser
from pdf_handler import parse_page_ranges, extract_and_save_pages

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MRPS - Multirange PDF Splitter")
        self.root.geometry("600x500")
        self.root.minsize(600, 500)

        FONT = ("Arial", 12)
        BUTTON_FONT = ("Arial", 12, "bold")

        self.config_file = "app_config.json"
        self.load_config()

        # Menu bar
        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=about_menu)

        # Input PDF
        tk.Label(root, text="Select Input PDF File:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.pdf_path_var = tk.StringVar()
        self.pdf_path_combobox = ttk.Combobox(root, width=55, font=FONT, textvariable=self.pdf_path_var,
                                              values=self.input_pdf_paths)
        self.pdf_path_combobox.pack(padx=10, pady=5)
        self.pdf_path_combobox.bind("<<ComboboxSelected>>", self.load_pdf_path)
        tk.Button(root, text="Browse", font=FONT, command=self.select_pdf).pack(pady=5)

        # Input format selection
        tk.Label(root, text="Select Input Format:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.input_format_var = tk.StringVar(value="simple")
        tk.Radiobutton(root, text="Simple Range Format [ e.g., 3-12, 49-66, 67-123... ]", font=FONT,
                       variable=self.input_format_var, value="simple").pack(anchor="w", padx=20, pady=2)
        tk.Radiobutton(root, text="Range with File Name [ e.g., 19-48 (My PDF 1), 49-66 (My PDF 2)... ]", font=FONT,
                       variable=self.input_format_var, value="descriptions").pack(anchor="w", padx=20, pady=2)

        # Page ranges input
        tk.Label(root, text="Enter Page Ranges:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.page_ranges_entry = scrolledtext.ScrolledText(root, height=4, width=60, font=FONT, wrap=tk.WORD)
        self.page_ranges_entry.pack(padx=10, pady=5, fill="x", expand=True)

        # Output folder
        tk.Label(root, text="Select Output Folder:", font=FONT).pack(anchor="w", padx=10, pady=5)
        self.output_dir_var = tk.StringVar()
        self.output_dir_combobox = ttk.Combobox(root, width=55, font=FONT, textvariable=self.output_dir_var,
                                                 values=self.output_dir_paths)
        self.output_dir_combobox.pack(padx=10, pady=5)
        self.output_dir_combobox.bind("<<ComboboxSelected>>", self.load_output_dir_path)
        tk.Button(root, text="Browse", font=FONT, command=self.select_output_folder).pack(pady=5)

        # Action buttons
        self.extract_button = tk.Button(root, text="Extract Pages", font=BUTTON_FONT, bg="#4CAF50", fg="white",
                                        padx=10, pady=5, command=self.extract_pages)
        self.extract_button.pack(pady=10)

        tk.Button(root, text="Exit", font=FONT, bg="#f44336", fg="white", command=root.quit).pack(pady=5)

    def load_config(self):
        """Loads saved paths from config file."""
        self.input_pdf_paths = []
        self.output_dir_paths = []

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.input_pdf_paths = config.get("input_pdf_paths", [])
                    self.output_dir_paths = config.get("output_dir_paths", [])
            except json.JSONDecodeError:
                pass  # Handle error if config file is corrupted

    def save_config(self):
        """Saves the last 5 paths to the config file."""
        config = {
            "input_pdf_paths": self.input_pdf_paths[:5],  # Store only the last 5 items
            "output_dir_paths": self.output_dir_paths[:5], # Store only the last 5 items
        }
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path_var.set(file_path)
            self.add_path_to_history(file_path, "pdf")
    
    def load_pdf_path(self, event):
        self.pdf_path_var.set(self.pdf_path_combobox.get())

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_dir_var.set(folder_path)
            self.add_path_to_history(folder_path, "dir")

    def load_output_dir_path(self, event):
       self.output_dir_var.set(self.output_dir_combobox.get())

    def add_path_to_history(self, path, path_type):
      """Add the path to history, save config and update the Combobox dropdown values."""
      if path_type == "pdf":
         if path in self.input_pdf_paths:
            self.input_pdf_paths.remove(path)
         self.input_pdf_paths.insert(0, path)
         self.pdf_path_combobox['values'] = self.input_pdf_paths
      elif path_type == "dir":
        if path in self.output_dir_paths:
           self.output_dir_paths.remove(path)
        self.output_dir_paths.insert(0, path)
        self.output_dir_combobox['values'] = self.output_dir_paths

      self.save_config()
    
    def extract_pages(self):
        pdf_path = self.pdf_path_var.get().strip()
        page_ranges_str = self.page_ranges_entry.get("1.0", tk.END).strip()
        output_dir = self.output_dir_var.get().strip()
        with_descriptions = self.input_format_var.get() == "descriptions"

        if not pdf_path or not page_ranges_str or not output_dir:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            page_ranges = parse_page_ranges(page_ranges_str, with_descriptions)
            os.makedirs(output_dir, exist_ok=True)
            extract_and_save_pages(pdf_path, output_dir, page_ranges, with_descriptions, compress=False)
            messagebox.showinfo("Success", "Pages extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("500x250")
        about_window.resizable(False, False)
        FONT = ("Arial", 12)
        
        about_text = "MRPS - Multirange PDF Splitter v0.2.0\n"
        tk.Label(about_window, text=about_text, font=FONT, justify="center").pack(pady=10)

        dev_text = "Developed by: Shree\n"
        tk.Label(about_window, text=dev_text, font=FONT, justify="center").pack()

        lic_text = "License: GPLv3\n"
        tk.Label(about_window, text=lic_text, font=FONT, justify="center").pack()


        github_link = "https://github.com/chandrath/MRPS-Multirange-PDF-Splitter"
        github_label = tk.Label(about_window, text=github_link, font=FONT, fg="blue", cursor="hand2", justify="center")
        github_label.pack(pady=10)
        github_label.bind("<Button-1>", lambda e: self.open_github_link(github_link))
    
    def open_github_link(self, url):
        """Opens the provided URL in the default web browser."""
        webbrowser.open_new(url)