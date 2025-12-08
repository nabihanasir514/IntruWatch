import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFFF; 
    }
    .stSidebar {
        background-color: #483490; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

def user_login():
    st.title("User Login")
    menu = ["Login", "Register","Public Portal"," Admin Dshboard"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

    elif choice == "Register":
            st.subheader("Create New Account")

            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type='password')

user_login()
st.write("Welcome to the User Login App!")
button=st.button("Login")

if button:
     st.success("Logged In ")
    
     
