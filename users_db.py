"""
User Database Module
Stores usernames and passwords for authentication
In a production environment, use a proper database and hash passwords
"""

import hashlib
import json
import os

# File to store user data
USERS_FILE = "users_data.json"

def hash_password(password):
    """Hash a password for storing"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return get_default_users()
    return get_default_users()

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def get_default_users():
    """Get default users (admin account)"""
    return {
        "admin": {
            "password": hash_password("password"),
            "email": "admin@example.com",
            "full_name": "Administrator"
        }
    }

def add_user(username, password, email, full_name):
    """Add a new user to the database"""
    users = load_users()
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists"
    
    # Add new user
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": full_name
    }
    
    # Save to file
    if save_users(users):
        return True, "User created successfully"
    else:
        return False, "Error saving user data"

def verify_user(username, password):
    """Verify user credentials"""
    users = load_users()
    
    if username not in users:
        return False
    
    hashed_password = hash_password(password)
    return users[username]["password"] == hashed_password

def get_user_info(username):
    """Get user information"""
    users = load_users()
    
    if username in users:
        return {
            "username": username,
            "email": users[username].get("email", ""),
            "full_name": users[username].get("full_name", "")
        }
    return None

def user_exists(username):
    """Check if a username exists"""
    users = load_users()
    return username in users

def get_all_usernames():
    """Get list of all usernames"""
    users = load_users()
    return list(users.keys())

def delete_user(username):
    """Delete a user from the database"""
    users = load_users()
    
    if username in users:
        del users[username]
        return save_users(users)
    return False

def update_password(username, old_password, new_password):
    """Update user password"""
    users = load_users()
    
    if username not in users:
        return False, "User not found"
    
    # Verify old password
    if users[username]["password"] != hash_password(old_password):
        return False, "Incorrect old password"
    
    # Update password
    users[username]["password"] = hash_password(new_password)
    
    if save_users(users):
        return True, "Password updated successfully"
    else:
        return False, "Error updating password"
