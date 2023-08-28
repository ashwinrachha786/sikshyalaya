import streamlit as st
import requests

BACKEND_URL = "http://localhost:8080/api/v1"  # Please replace with your backend URL

def signup():
    st.subheader("Sign Up")
    email = st.text_input("Email")
    full_name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    address = st.text_input("Address")
    group_id = st.number_input("Group ID", format="%d")
    contact_number = st.text_input("Contact Number")
    dob = st.date_input("Date of Birth")
    join_year = st.number_input("Join Year", format="%d")

    if st.button("Sign Up"):
        response = requests.post(f"{BACKEND_URL}/auth/signup/", json={
            "email": email,
            "full_name": full_name,
            "address": address,
            "group_id": group_id,
            "contact_number": contact_number,
            "dob": str(dob),
            "join_year": join_year,
            "password": password
        }, timeout=30)
        if response.status_code == 200:
            st.success("Signed up successfully!")
        else:
            st.error("Failed to sign up!")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember_me = st.checkbox("Remember Me")

    if st.button("Login"):
        response = requests.post(f"{BACKEND_URL}/auth/web/", json={
            "username": username,
            "password": password,
            "remember_me": remember_me
        }, timeout=30)
        if response.status_code == 200 and response.json().get("msg") == "Logged in successfully!":
            st.success("Logged in successfully!")
        else:
            st.error("Failed to log in!")

def passwordless_login():
    st.subheader("Passwordless Login")
    if st.button("Generate Token"):
        response = requests.get(f"{BACKEND_URL}/auth/password-less/create", timeout=30)
        if response.status_code == 200:
            token = response.json().get("token")
            st.success(f"Token generated: {token}")
        else:
            st.error("Failed to generate token!")
    token = st.text_input("Enter Token")
    if st.button("Verify Token"):
        response = requests.post(f"{BACKEND_URL}/auth/password-less/verify", json={"token": token}, timeout=30)
        if response.status_code == 200:
            st.success("Token verified successfully!")
        else:
            st.error("Failed to verify token!")

def main():
    st.title("Gurukul Authentication Tester")
    tasks = ["Login", "Sign Up", "Passwordless Login"]
    choice = st.sidebar.selectbox("Choose Task", tasks)

    if choice == "Login":
        login()
    elif choice == "Sign Up":
        signup()
    elif choice == "Passwordless Login":
        passwordless_login()

if __name__ == "__main__":
    main()
