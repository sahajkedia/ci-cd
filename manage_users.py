import toml
from pathlib import Path
import argparse

def load_secrets():
    secrets_path = Path('.streamlit/secrets.toml')
    if secrets_path.exists():
        with open(secrets_path, 'r') as f:
            return toml.load(f)
    return {'passwords': {}, 'cookies': {'key': 'your-secret-key', 'expiry_days': 30}}

def save_secrets(secrets):
    secrets_path = Path('.streamlit/secrets.toml')
    secrets_path.parent.mkdir(exist_ok=True)
    with open(secrets_path, 'w') as f:
        toml.dump(secrets, f)

def add_user(username, password):
    secrets = load_secrets()
    secrets['passwords'][username] = password
    save_secrets(secrets)
    print(f"User {username} added successfully!")

def delete_user(username):
    secrets = load_secrets()
    if username not in secrets['passwords']:
        print(f"User {username} not found!")
        return
    del secrets['passwords'][username]
    save_secrets(secrets)
    print(f"User {username} deleted successfully!")

def list_users():
    secrets = load_secrets()
    users = secrets.get('passwords', {})
    if not users:
        print("No users found!")
        return
    
    print("\nRegistered Users:")
    print("-" * 30)
    for username in users:
        print(f"Username: {username}")
    print("-" * 30)

def main():
    parser = argparse.ArgumentParser(description='User Management Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add user command
    add_parser = subparsers.add_parser('add', help='Add a new user')
    add_parser.add_argument('username', help='Username')
    add_parser.add_argument('password', help='Password')
    
    # Delete user command
    delete_parser = subparsers.add_parser('delete', help='Delete a user')
    delete_parser.add_argument('username', help='Username to delete')
    
    # List users command
    subparsers.add_parser('list', help='List all users')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_user(args.username, args.password)
    elif args.command == 'delete':
        delete_user(args.username)
    elif args.command == 'list':
        list_users()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()