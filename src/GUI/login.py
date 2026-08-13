import tkinter as tk
from tkinter import messagebox
from src.API.trustedparts import request
import tkinter.font as tkfont

def login_page():
    try:
        global login_success
        login_success = False

        login_window = tk.Tk()
        login_window.title("Login")
        login_window.geometry('500x300')
        login_window.configure(bg="#7A1C24")

        normal_font = tkfont.Font(family="Arial", size=16)
        title_font = tkfont.Font(family="Arial", size=30)

        def resize_fonts(event):
            scale = 1 + ((event.width / 500) - 1) * 0.35
            scale = max(1, min(scale, 1.5))

            normal_font.configure(size=int(16 * scale))
            title_font.configure(size=int(30 * scale))

        frame = tk.Frame(login_window, bg="#7A1C24")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Entry column expands with the window
        frame.columnconfigure(1, weight=1)

        #making widgets(buttons)
        login_label = tk.Label(frame, text="Login", bg="#7A1C24", fg="#6C7054", font=title_font)
        company_ID_label = tk.Label(frame, text="API Company ID", bg="#7A1C24", fg="#FFFFFF", font=normal_font)
        company_ID_entry = tk.Entry(frame, font=normal_font)
        API_key_label = tk.Label(frame, text="API Key", bg="#7A1C24", fg="#FFFFFF", font=normal_font)
        API_key_entry = tk.Entry(frame, show="*", font=normal_font)
        login_button = tk.Button(frame, text="Login", bg="#6C7054", fg="#FFFFFF", font=normal_font, command=lambda: login(login_window, company_ID_entry.get(), API_key_entry.get()))

        #placing widgets on window
        login_label.grid(row=0, column=0, columnspan=2, pady=(0,30))

        company_ID_label.grid(row=1, column=0, sticky="w", pady=10, padx=(0,10))
        company_ID_entry.grid(row=1, column=1, sticky="ew", pady=10)

        API_key_label.grid(row=2, column=0, sticky="w", pady=10, padx=(0,10))
        API_key_entry.grid(row=2, column=1, sticky="ew", pady=10)

        login_button.grid(row=3, column=0, columnspan=2, pady=30)

        login_window.bind("<Configure>", resize_fonts)

        login_window.mainloop()

        return login_success
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise

def login(window, company_id, api_key):
    try:
        if not company_id or not api_key:
            messagebox.showerror("Error", "Please enter both Company ID and API Key.")
            return

        if not create_company_ID_and_API_Key(company_id, api_key):
            return
        
        messagebox.showinfo("Success", "Login successful!")

        #if success return true to trigger window switch to home
        global login_success
        login_success = True
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise

def create_company_ID_and_API_Key(ID: str, Key: str) -> bool:
    try:
        # Check the credentials
        if not request.check_credentials(ID, Key):
            messagebox.showerror("Error", "Invalid Company ID or API Key.")
            return False
        with open(".env", "w") as f:
                # Brand new file creation
                f.write(f"MY_SECRET_API_KEY={Key}\n")
                f.write(f"MY_SECRET_COMPANY_ID={ID}\n")

        return True
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise