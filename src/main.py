from src.GUI import login, home
        
def main():
    if login.login_page():
        home.switch_to_main_application()

if __name__ == "__main__":
    main()