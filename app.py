import streamlit as st
import hmac
import json
import re
from enum import Enum
from typing import Dict, Tuple, Optional

# Define user roles
class UserRole(str, Enum):
    SUPERUSER = "superuser"
    USER = "user"

# Use a JSON file to store users
USERS_FILE = "users.json"

def load_users() -> Dict:
    """Load users from JSON file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_users(users: Dict) -> None:
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def is_valid_username(username: str) -> bool:
    """Check if username meets requirements"""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password: str) -> bool:
    """Check if password meets requirements"""
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))

def create_user(username: str, password: str, role: UserRole = UserRole.USER) -> Tuple[bool, str]:
    """Create a new user with specified role"""
    try:
        users = load_users()
        
        if username in users['users']:
            return False, "Username already exists"
        
        if not is_valid_username(username):
            return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores"
        
        if not is_valid_password(password):
            return False, "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number"
        
        users['users'][username] = {
            "password": password,
            "role": role
        }
        save_users(users)
        
        return True, "User created successfully"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_credentials(username: str, password: str) -> Tuple[bool, Optional[UserRole]]:
    """Verify user credentials and return role if successful"""
    users = load_users()
    if username in users['users']:
        user_data = users['users'][username]
        if hmac.compare_digest(password, user_data['password']):
            return True, UserRole(user_data['role'])
    return False, None

def init_session_state():
    """Initialize session state variables"""
    if 'login_successful' not in st.session_state:
        st.session_state.login_successful = False
    if 'current_username' not in st.session_state:
        st.session_state.current_username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

def handle_logout():
    """Handle logout"""
    st.session_state.login_successful = False
    st.session_state.current_username = None
    st.session_state.user_role = None
    st.rerun()

def login_page():
    """Display login and registration page"""
    st.markdown("### Login or Create Account")
    
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                success, role = verify_credentials(username, password)
                if success:
                    st.session_state.login_successful = True
                    st.session_state.current_username = username
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("create_account"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            st.markdown("##### Password Requirements:")
            st.markdown("- At least 8 characters long")
            st.markdown("- At least one uppercase letter")
            st.markdown("- At least one lowercase letter")
            st.markdown("- At least one number")
            
            submit = st.form_submit_button("Create Account")
            if submit:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    success, message = create_user(new_username, new_password, UserRole.USER)
                    if success:
                        st.success(message)
                        st.session_state.login_successful = True
                        st.session_state.current_username = new_username
                        st.session_state.user_role = UserRole.USER
                        st.rerun()
                    else:
                        st.error(message)

def render_dashboard():
    """Render the dashboard tab content"""
    st.header("Dashboard")
    st.write("This is your secure dashboard content")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
    with col2:
        st.metric(label="Humidity", value="45%", delta="-2%")
    with col3:
        st.metric(label="Pressure", value="1013 hPa", delta="0.5 hPa")

def render_settings():
    """Render the settings tab content"""
    st.header("Settings")
    st.subheader("User Preferences")
    theme = st.selectbox("Theme", ["Light", "Dark", "System"])
    notifications = st.toggle("Enable Notifications")
    email_updates = st.toggle("Receive Email Updates")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def render_admin_panel():
    """Render the admin panel tab content"""
    st.header("Admin Panel")
    st.subheader("User Management")
    
    users = load_users()
    
    # Display users table
    st.dataframe(
        {
            "Username": [username for username in users['users'].keys()],
            "Role": [user_data['role'] for user_data in users['users'].values()]
        }
    )
    
    # Add new user form
    with st.form("add_user_form"):
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", [UserRole.USER, UserRole.SUPERUSER])
        
        if st.form_submit_button("Add User"):
            success, message = create_user(username, password, role)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def render_profile():
    """Render the profile tab content"""
    st.header("Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Personal Information")
        st.text_input("Username", value=st.session_state.current_username, disabled=True)
        st.text_input("Role", value=st.session_state.user_role, disabled=True)
        
        with st.expander("Change Password"):
            with st.form("change_password"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_new_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    success, _ = verify_credentials(st.session_state.current_username, current_password)
                    if not success:
                        st.error("Current password is incorrect!")
                    elif new_password != confirm_new_password:
                        st.error("New passwords don't match!")
                    elif not is_valid_password(new_password):
                        st.error("New password doesn't meet requirements!")
                    else:
                        users = load_users()
                        users['users'][st.session_state.current_username]["password"] = new_password
                        save_users(users)
                        st.success("Password updated successfully!")

def main():
    st.set_page_config(
        page_title="Secure Streamlit App",
        page_icon="🔒",
        layout="wide"
    )
    
    init_session_state()

    if not st.session_state.login_successful:
        login_page()
        st.stop()

    # Main application content after successful login
    st.sidebar.title(f'Welcome {st.session_state.current_username}')
    st.sidebar.text(f'Role: {st.session_state.user_role}')
    st.sidebar.button('Logout', on_click=handle_logout)

    st.title('Secure Dashboard')
    
    # Define available tabs based on user role
    if st.session_state.user_role == UserRole.SUPERUSER:
        tabs = st.tabs(["Dashboard", "Settings", "Admin Panel", "Profile"])
        tab1, tab2, tab3, tab4 = tabs
    else:
        tabs = st.tabs(["Dashboard", "Profile"])
        tab1, tab4 = tabs
    
    with tab1:
        render_dashboard()
    
    if st.session_state.user_role == UserRole.SUPERUSER:
        with tab2:
            render_settings()
        with tab3:
            render_admin_panel()
    
    with tab4:
        render_profile()

if __name__ == '__main__':
    main()