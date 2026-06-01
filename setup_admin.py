from modules.controller.auth_controller import setup_default_users

if __name__ == "__main__":
    setup_default_users()
    print("Admin users ready:")
    print("  Username: admin     Password: admin123")
    print("  Username: manager1  Password: manager123")
    print("")
    print("Now run: python main.py")
