import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import pathlib
import tempfile
import tkinter.font as tkfont

from src.excel.reading import read_excel_file
from src.API.trustedparts import request
from src.API.trustedparts.utilities import format
from src.excel.writing import add_data_to_bom

def switch_to_main_application():
    try:
        # Create the main application window
        home_window = tk.Tk()
        home_window.title("BOMSafe")
        home_window.geometry('700x300')
        home_window.configure(bg="#7A1C24")

        # holds the BOM we will edit until they download it
        processed_file = {"path": None}

        normal_font = tkfont.Font(family="Arial", size=14)

        def resize_fonts(event):
            scale = 1 + ((event.width / 700) - 1) * 0.35
            scale = max(1, min(scale, 1.5))
            normal_font.configure(size=int(14 * scale))

        frame = tk.Frame(home_window, bg="#7A1C24")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # The middle column expands when the window gets wider
        frame.columnconfigure(1, weight=1)

        # Upload row
        tk.Label(frame, text="Upload File Path:", bg="#7A1C24", fg="#FFFFFF", font=normal_font).grid(row=0, column=0, sticky="w", pady=10, padx=(0,10))

        upload_entry = tk.Entry(frame, font=normal_font)
        upload_entry.grid(row=0, column=1, sticky="ew", pady=10)

        tk.Button(frame, text="Browse & Upload", bg="#6C7054", fg="#FFFFFF", font=normal_font, command=lambda: upload_file(upload_entry, processed_file, download_entry)).grid(row=0, column=2, pady=10, padx=(10,0))

        # Download row
        tk.Label(frame, text="Download Save Path:", bg="#7A1C24", fg="#FFFFFF", font=normal_font).grid(row=1, column=0, sticky="w", pady=10, padx=(0,10))

        download_entry = tk.Entry(frame, font=normal_font)
        download_entry.grid(row=1, column=1, sticky="ew", pady=10)

        tk.Button(frame, text="Save / Download", bg="#6C7054", fg="#FFFFFF", font=normal_font, command=lambda: download_file(processed_file)).grid(row=1, column=2, pady=10, padx=(10,0))

        home_window.bind("<Configure>", resize_fonts)

        home_window.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise

def upload_file(upload_entry, processed_file, download_entry):
    try:
        file_path = filedialog.askopenfilename(title="Select File to Upload")
        if file_path:
            upload_entry.delete(0, tk.END)
            upload_entry.insert(0, file_path)
            messagebox.showinfo("Success", "File selected for upload!")
            # calling actual logic
        
            variables = read_excel_file(file_path)
            payload = request.create_get_request(variables, request.load_API_key(), request.load_Company_ID())
            data = request.send_get_request(payload)
            data = format.format_data(data, variables)

            file_path = pathlib.Path(file_path)
            output_path = pathlib.Path(tempfile.gettempdir()) / f"{file_path.stem}_BOMSafe.xlsx"

            shutil.copy2(file_path, output_path)
            add_data_to_bom(output_path, data)

            processed_file["path"] = output_path

            #update the download box with the new file name
            download_entry.delete(0, tk.END)
            download_entry.insert(0, output_path.name)
            messagebox.showinfo("Success", "Data added to BOM")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise

def download_file(processed_file):
    try:
        if processed_file["path"] is None:
            messagebox.showerror("Error", "Please upload and process a BOM first!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=processed_file["path"].name, title="Save Downloaded File As")
        if save_path:
            shutil.copy2(processed_file["path"], save_path)
            messagebox.showinfo("Success", f"File location set for download: {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")   
        raise