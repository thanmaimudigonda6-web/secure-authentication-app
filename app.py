# 🔐 Multi-Factor Authentication System (FINAL WORKING)

import streamlit as st
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Secure Authentication System", page_icon="🔐")

st.title("🔐 Secure Authentication System")

# ------------------ ML DATA ------------------
data = pd.DataFrame({
    "time": [0,0,1,1,0,1,0,1],
    "location": [0,1,0,1,0,1,1,0],
    "device": [0,0,1,1,0,1,0,1],
    "result": [1,1,0,0,1,0,1,0]
})

X = data[["time","location","device"]]
y = data["result"]

model = LogisticRegression()
model.fit(X, y)

# ------------------ USER PASSWORD ------------------
USER_PASSWORD = "admin123"

# ------------------ SESSION STATE ------------------
if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# ------------------ PASSWORD LOGIN ------------------
st.subheader("Step 1: Password Verification")

password = st.text_input("Enter Password", type="password")

if st.button("Login"):
    if password != USER_PASSWORD:
        st.session_state.attempts += 1
        st.error(f"Wrong Password ❌ (Attempts: {st.session_state.attempts})")

        if st.session_state.attempts >= 3:
            st.error("Too many attempts! Access blocked 🚫")
    else:
        st.success("Password Verified ✅")
        otp = random.randint(1000, 9999)
        st.session_state.otp = otp
        st.session_state.otp_verified = False
        st.info("OTP sent to registered device 📲")
        st.write(f"(Demo OTP: {otp})")  # demo only

# ------------------ OTP VERIFICATION ------------------
if st.session_state.otp is not None:
    st.subheader("Step 2: OTP Verification")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if str(user_otp) == str(st.session_state.otp):
            st.success("OTP Verified ✅")
            st.session_state.otp_verified = True
        else:
            st.error("Invalid OTP ❌")

# ------------------ ML SECURITY CHECK ------------------
if st.session_state.otp_verified:

    st.subheader("Step 3: ML Security Check")

    time = st.selectbox("Login Time", ["Normal", "Odd"])
    location = st.selectbox("Location", ["Same", "New"])
    device = st.selectbox("Device", ["Known", "New"])

    time_val = 0 if time == "Normal" else 1
    loc_val = 0 if location == "Same" else 1
    dev_val = 0 if device == "Known" else 1

    if st.button("Final Verification"):

        prediction = model.predict([[time_val, loc_val, dev_val]])
        prob = model.predict_proba([[time_val, loc_val, dev_val]])[0][1]

        st.write(f"🔍 Security Score: {round(prob*100,2)}%")

        if prediction[0] == 1:
            st.success("Login Successful ✅ (Safe User)")
        else:
            st.error("Suspicious Login ❌ (Access Denied)")

# ------------------ RESET BUTTON ------------------
st.markdown("---")

if st.button("Reset 🔄"):
    st.session_state.clear()
    st.rerun()

# ------------------ LOGOUT BUTTON ------------------
if st.button("Logout 🚪"):
    st.session_state.clear()
    st.rerun()