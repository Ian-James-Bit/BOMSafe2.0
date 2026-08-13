import tkinter as tk
from tkinter import messagebox
from src.API.trustedparts import request

def login_page():
    try:
        global login_success
        login_success = False
        login_window = tk.Tk()
        login_window.title("Login Screen")
        login_window.geometry('340x440')
        login_window.configure(bg="#7A1C24")
        frame = tk.Frame(login_window, bg ="#7A1C24")

        #making widgets(buttons)
        login_label = tk.Label(frame, text="Login", bg ="#7A1C24", fg="#6C7054", font=("Arial", 30))
        company_ID_label = tk.Label(frame, text="API Company ID", bg ="#7A1C24", fg="#FFFFFF", font=("Arial", 16))
        company_ID_entry = tk.Entry(frame, font=("Arial", 16))
        API_key_label = tk.Label(frame, text="API Key", bg ="#7A1C24", fg="#FFFFFF", font=("Arial", 16))
        API_key_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        login_button = tk.Button(frame, text="Login", bg ="#6C7054", fg="#FFFFFF", font=("Arial", 16), command=lambda: login(login_window, company_ID_entry.get(),API_key_entry.get()))

        #placing widgets on window
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        company_ID_label.grid(row=1, column=0)
        company_ID_entry.grid(row=1, column=1, pady=20)
        API_key_label.grid(row=2, column=0)
        API_key_entry.grid(row=2, column=1, pady=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)

        frame.pack()

        login_window.mainloop()

        return login_success  # Return True to indicate successful login
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

def create_company_ID_and_API_Key(ID: str, Key: str) -> None:
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