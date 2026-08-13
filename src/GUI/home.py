import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import pathlib
import tempfile

from src.excel.reading import read_excel_file
from src.API.trustedparts import request
from src.API.trustedparts.utilities import format
from src.excel.writing import add_data_to_bom

def switch_to_main_application():
    try:
        # Create the main application window
        home_window = tk.Tk()
        home_window.title("BOM Home")
        home_window.geometry('340x440')
        home_window.configure(bg="#7A1C24")

        # holds the BOM we will edit until they download it
        processed_file = {"path": None}

        # Build the new window content in place
        home_window.title("BOM Home")
        lbl = tk.Label(home_window, text="Welcome to the Home Screen!", font=("Arial", 16))
        lbl.pack(pady=50)

        # create upload section
        tk.Label(home_window, text="Upload File Path:").pack(pady=5)
        upload_entry = tk.Entry(home_window, width=50)
        upload_entry.pack(pady=5)
        tk.Button(home_window, text="Browse & Upload", command=lambda: upload_file(upload_entry, processed_file, download_entry)).pack(pady=5)

        # create download section
        tk.Label(home_window, text="Download Save Path:").pack(pady=5)
        download_entry = tk.Entry(home_window, width=50)
        download_entry.pack(pady=5)
        tk.Button(home_window, text="Save / Download", command=lambda: download_file(processed_file)).pack(pady=5)

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