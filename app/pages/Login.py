import streamlit as st

class Node:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.next = None

# Head of the linked list
head = None
# def signip_function(): pass
# def login_function(): pass
# Function to insert username and password into linked list
def insert(name, password):
    global head
    new_node = Node(name, password)
    new_node.next = head
    head = new_node

# Function to check login details
def sign_in(name, password):
    global head
    temp = head
    # Traverse the linked list
    while temp is not None:
        if temp.username == name and temp.password == password:
            return True
        temp = temp.next
    return False

# Function to sign up
def sign_up(name, password):
    insert(name, password)

def signup_function():
    st.subheader("Create New Admin Account")
    username = st.text_input("Choose Username", key="signup_username")
    password = st.text_input("Choose Password", type='password', key="signup_password")
    button = st.button("Sign Up", key="signup_button")
    
    if button:
        if username and password:
            sign_up(username, password)
            st.success(f"Account created for {username}!")
        else:
            st.warning("Please fill in all fields")

def login_function(): 
    st.subheader("Admin Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type='password', key="login_password")
    button = st.button("Login", key="login_button")
    sign_up("admin", "admin123")  # Pre-populate with a default admin account for testing
    if button:
        if sign_in(username, password):
            st.success(f"Logged In as {username}")
            # ...
            st.session_state.logged_in = True  # This is the correct way
            st.session_state.current_user = username
            st.rerun()
        else:
            st.warning("Incorrect Username/Password")
        
# signup_function()
# login_function()
