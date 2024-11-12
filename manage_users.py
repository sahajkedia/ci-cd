import json
import argparse
from enum import Enum

class UserRole(str, Enum):
    SUPERUSER = "superuser"
    USER = "user"

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def add_user(username, password, role):
    users = load_users()
    if username in users['users']:
        print(f"Error: User {username} already exists!")
        return
    
    users['users'][username] = {
        "password": password,
        "role": role
    }
    save_users(users)
    print(f"User {username} added successfully with role {role}!")

def delete_user(username):
    users = load_users()
    if username not in users['users']:
        print(f"Error: User {username} not found!")
        return
    
    del users['users'][username]
    save_users(users)
    print(f"User {username} deleted successfully!")

def list_users():
    users = load_users()
    if not users['users']:
        print("No users found!")
        return
    
    print("\nRegistered Users:")
    print("-" * 50)
    print(f"{'Username':<20} {'Role':<15}")
    print("-" * 50)
    for username, user_data in users['users'].items():
        print(f"{username:<20} {user_data['role']:<15}")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description='User Management Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add user command
    add_parser = subparsers.add_parser('add', help='Add a new user')
    add_parser.add_argument('username', help='Username')
    add_parser.add_argument('password', help='Password')
    add_parser.add_argument('--role', choices=['user', 'superuser'], default='user', help='User role')
    
    # Delete user command
    delete_parser = subparsers.add_parser('delete', help='Delete a user')
    delete_parser.add_argument('username', help='Username to delete')
    
    # List users command
    subparsers.add_parser('list', help='List all users')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_user(args.username, args.password, args.role)
    elif args.command == 'delete':
        delete_user(args.username)
    elif args.command == 'list':
        list_users()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()