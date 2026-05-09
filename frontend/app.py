import streamlit as st
import requests

# The URL where your FastAPI server is running
API_URL = "https://healthsidekick.onrender.com"

st.set_page_config(page_title="HealthSideKick", page_icon="🩺")

# --- SESSION STATE ---
# We use this to store the JWT token so the user stays logged in
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# --- HELPER FUNCTIONS ---
def get_headers():
    """Attaches the VIP Wristband (JWT) to our API requests."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}

# --- PAGE LAYOUT: LOGIN / SIGNUP ---
if st.session_state["access_token"] is None:
    st.title("🩺 Welcome to HealthSideKick")
    st.subheader("Please Log In or Sign Up")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        login_email = st.text_input("Email (Login)")
        login_password = st.text_input("Password (Login)", type="password")
        if st.button("Login"):
            # Send data to FastAPI using Form Data format
            response = requests.post(f"{API_URL}/login", data={"username": login_email, "password": login_password})
            if response.status_code == 200:
                st.session_state["access_token"] = response.json().get("access_token")
                st.success("Logged in successfully!")
                st.rerun() # Refresh the page to show the chat UI
            else:
                st.error("Invalid email or password.")
                
    with tab2:
        signup_username = st.text_input("Username")
        signup_email = st.text_input("Email (Sign Up)")
        signup_password = st.text_input("Password (Sign Up)", type="password")
        if st.button("Sign Up"):
            payload = {"username": signup_username, "email": signup_email, "password": signup_password}
            response = requests.post(f"{API_URL}/signup", json=payload)
            
            # FastAPI often defaults to 200 instead of 201, so we check for both!
            if response.status_code in [200, 201]:
                st.success("Account created! You can now log in.")
            else:
                # Safely try to read the JSON. If it's an HTML/Text error, catch it!
                try:
                    error_msg = response.json().get('detail', 'Unknown error')
                except Exception:
                    # If it's not JSON, just grab the raw text Render sent us
                    error_msg = f"Server returned {response.status_code}: {response.text}"
                
                st.error(f"Sign up failed: {error_msg}")
# --- PAGE LAYOUT: MAIN APP ---
else:
    # Sidebar for File Uploads and Logout
    with st.sidebar:
        st.header("📂 Your Documents")
        uploaded_file = st.file_uploader("Upload a Medical PDF", type=["pdf"])
        
        if uploaded_file:
            if st.button("Process Document"):
                with st.spinner("Uploading and analyzing to Pinecone..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    # Notice we pass get_headers() to prove who we are!
                    response = requests.post(f"{API_URL}/upload-pdf/", files=files, headers=get_headers())
                    
                    if response.status_code == 200:
                        st.success("Document securely uploaded!")
                    else:
                        st.error("Failed to upload document.")
                        
        st.divider()
        if st.button("Logout"):
            st.session_state["access_token"] = None
            st.session_state["chat_history"] = []
            st.rerun()

    # Main Chat Area
    st.title("💬 HealthSideKick AI")
    st.markdown("Ask questions about your uploaded medical documents.")

    # Display past chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input Box
    if prompt := st.chat_input("What is the recommended dosage?"):
        # 1. Show the user's message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        
        # 2. Send the question to FastAPI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                payload = {"question": prompt}
                response = requests.post(f"{API_URL}/ask/", json=payload, headers=get_headers())
                
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    st.markdown(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                else:
                    st.error("Authentication expired or error occurred. Please log in again.")