# varsync/cli.py

import sys
from .varsync import register, login

def main():
    if len(sys.argv) < 2:
        print("Usage: varsync [command] [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "register":
        if len(sys.argv) != 5:
            print("Usage: varsync register <username> <password> <confirm_password>")
            sys.exit(1)
        username, password, confirm_password = sys.argv[2], sys.argv[3], sys.argv[4]
        register(username, password, confirm_password)
        print(f"User {username} registered successfully.")
    
    elif command == "login":
        if len(sys.argv) != 4:
            print("Usage: varsync login <username> <password>")
            sys.exit(1)
        username, password = sys.argv[2], sys.argv[3]
        session = login(username, password)
        print(f"User {username} logged in successfully.")

    elif command == "get":
        if len(sys.argv) != 4:
            print("Usage: varsync get <var_name>")
            sys.exit(1)
        username, password = sys.argv[2], sys.argv[3]
        session = login(username, password)
        var_name = sys.argv[3]
        print(session.get(var_name))
    
    else:
        print("Unknown command")
        sys.exit(1)

if __name__ == "__main__":
    main()
