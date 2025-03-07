import re
import streamlit as st
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    return score, feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="wide")
st.markdown("""
    <style>
    body {background-color: #f4f4f4;}
    .main { padding: 30px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
    .footer {position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 100%; text-align: center; padding: 10px; background: #zzzz; font-size: 14px; color: white; box-shadow: 0px -2px 5px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Meter & Generator")
st.write("Easily check the strength of your password or generate a secure one!")

# Sidebar for saved passwords
st.sidebar.title("🔑 Saved Passwords")
if "saved_passwords" not in st.session_state:
    st.session_state["saved_passwords"] = []

with st.sidebar:
    for idx, saved_pw in enumerate(st.session_state["saved_passwords"], start=1):
        st.write(f"{idx}. `{saved_pw}`")
    
option = st.radio("Choose an option:", ("Check Password Strength", "Generate Strong Password"))

st.markdown("---")

if option == "Check Password Strength":
    with st.container():
        password = st.text_input("Enter your password:", type="password")
        if st.button("🔍 Check Strength", use_container_width=True):
            if password:
                score, feedback = check_password_strength(password)
                
                if score == 4:
                    st.success("✅ Strong Password!")
                    if password not in st.session_state["saved_passwords"]:
                        st.session_state["saved_passwords"].append(password)
                elif score == 3:
                    st.warning("⚠️ Moderate Password - Consider adding more security features.")
                    if password not in st.session_state["saved_passwords"]:
                        st.session_state["saved_passwords"].append(password)
                else:
                    st.error("❌ Weak Password - Improve it using the suggestions below.")
                
                for tip in feedback:
                    st.write("- " + tip)
            else:
                st.error("Please enter a password.")

elif option == "Generate Strong Password":
    with st.container():
        length = st.slider("Select Password Length", 8, 20, 12)
        if st.button("⚡ Generate Password", use_container_width=True):
            strong_password = generate_strong_password(length)
            st.success(f"🔑 Your Strong Password: `{strong_password}`")
            
            st.balloons() 
            # Save generated password to session state
            if strong_password not in st.session_state["saved_passwords"]:
                st.session_state["saved_passwords"].append(strong_password)
                

# Footer
st.markdown('<div class="footer">Made by Moiz Ahmed Shaikh</div>', unsafe_allow_html=True)