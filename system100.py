import streamlit as st
import sys
import subprocess

# Debug: Check if packages are available
st.title("Debug: Secrets and Packages")

try:
    import gspread
    st.success("✅ gspread imported successfully")
    st.write(f"gspread version: {gspread.__version__}")
except ImportError as e:
    st.error(f"❌ gspread import failed: {e}")
    st.stop()

try:
    from google.oauth2.service_account import Credentials
    st.success("✅ google.oauth2.service_account imported successfully")
except ImportError as e:
    st.error(f"❌ google.oauth2.service_account import failed: {e}")
    st.stop()

# Debug: Check secrets
st.write("### Secrets Debug:")
st.write("Available secrets keys:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets object")

if "gcp_service_account" in st.secrets:
    st.success("✅ gcp_service_account found in secrets")
    st.write("Keys in gcp_service_account:", list(st.secrets["gcp_service_account"].keys()))
else:
    st.error("❌ gcp_service_account NOT found in secrets")
    st.write("All available secret keys:", list(st.secrets.keys()) if hasattr(st, 'secrets') and st.secrets else "None")
    
    # Show what secrets are actually available
    try:
        st.write("### All secrets structure:")
        for key in st.secrets.keys():
            st.write(f"- {key}: {type(st.secrets[key])}")
    except Exception as e:
        st.write(f"Error accessing secrets: {e}")
    
    st.stop()

# If we get here, secrets are working
st.success("🎉 All imports and secrets successful! Loading main app...")

# Your actual app code here
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def init_connection():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPE
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

CLIENT = init_connection()

if CLIENT is None:
    st.error("Failed to connect to Google Sheets. Please check your secrets configuration.")
    st.stop()

try:
    SHEET = CLIENT.open("users101").sheet1
    st.success("✅ Connected to Google Sheets successfully")
except Exception as e:
    st.error(f"Error opening spreadsheet: {e}")
    st.stop()

st.title("Araba Unisex Boutique")

tab1, tab2 =st.tabs(["Login", "Register"])
with tab1:
    with st.form("Login"):
        users = SHEET.get_all_records()
        username = st.text_input("Enter Username").strip().lower()
        password = st.text_input("Enter password", type="password").strip() # mask password input
        if st.form_submit_button("Login"):
            found = False
            for user in users:
            	#sheet_username = str(user["username"]).strip().lower()
            	#print("username", sheet_username)
            	#sheet_password = str(user["password"]).strip()
            	if str(user["username"]) == username and str(user["password"]) == password:
                    found = True  # ✅ assignment, not comparison
                    st.success(f"Welcome, {username}!")
                    break  # ✅ stop checking once a match is found

            # ✅ only runs after loop is done
            if not found:
                st.error("Invalid username or password")
	
with tab2:
	with st.form("Register"):
		users=SHEET.get_all_records()
		username100=st.text_input("Enter a username")
		password100=st.text_input("Enter a password")
		email100=st.text_input("Enter your email")
		first100=st.text_input("Enter first name")
		last100=st.text_input("Enter last name")
		Dob100=st.text_input("Enter DoB")
		contact100=st.text_input("Enter Contact")
		if st.form_submit_button("Register"):
			SHEET.append_row([first100, last100, Dob100, contact100,email100, password100, username100])
			st.success("Registration Successful")
