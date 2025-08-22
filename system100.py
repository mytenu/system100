import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Define scope
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
@st.cache_resource
def init_connection():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPE
    )
    client = gspread.authorize(credentials)
    return client

# Initialize connection
CLIENT = init_connection()
SHEET = CLIENT.open("users101").sheet1

st.title("Araba Unisex Boutique")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    with st.form("Login"):
        users = SHEET.get_all_records()
        username = st.text_input("Enter Username").strip().lower()
        password = st.text_input("Enter password", type="password").strip()
        
        if st.form_submit_button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                found = False
                for user in users:
                    if str(user.get("username", "")).strip().lower() == username and str(user.get("password", "")).strip() == password:
                        found = True
                        st.success(f"Welcome, {username}!")
                        break
                
                if not found:
                    st.error("Invalid username or password")

with tab2:
    with st.form("Register"):
        username100 = st.text_input("Enter a username")
        password100 = st.text_input("Enter a password", type="password")
        email100 = st.text_input("Enter your email")
        first100 = st.text_input("Enter first name")
        last100 = st.text_input("Enter last name")
        Dob100 = st.text_input("Enter DoB")
        contact100 = st.text_input("Enter Contact")
        
        if st.form_submit_button("Register"):
            # Validate required fields
            if not all([username100, password100, email100, first100, last100]):
                st.error("Please fill in all required fields")
            else:
                try:
                    # Check if username already exists
                    users = SHEET.get_all_records()
                    existing_usernames = [str(user.get("username", "")).strip().lower() for user in users]
                    
                    if username100.strip().lower() in existing_usernames:
                        st.error("Username already exists. Please choose a different username.")
                    else:
                        SHEET.append_row([first100, last100, Dob100, contact100, email100, password100, username100])
                        st.success("Registration Successful!")
                        st.balloons()  # Fun celebration effect
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
