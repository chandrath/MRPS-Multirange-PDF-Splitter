import tkinter as tk
from ui_handler import PDFExtractorApp
import sys
import os

def main():
    root = tk.Tk()
    app = PDFExtractorApp(root)

    # Determine the path to the icon file
    if getattr(sys, 'frozen', False):  # If bundled with PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))

    icon_path = os.path.join(base_path, "app_icon.ico")

    # Set the window icon
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)  # Title bar icon
    else:
        print("Warning: Icon file not found. Window icon will not be set.")

    root.mainloop()

if __name__ == "__main__":
    main()
