import streamlit as st
import pandas as pd
import joblib

# Load model and features
model = joblib.load("stroke_model.pkl")
features = joblib.load("features.pkl")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# User authentication
def authenticate(username, password):
    users = pd.read_csv("users.csv")
    return any((users["username"] == username) & (users["password"] == password))

# Health tips function
def get_health_tips(pred):
    if pred == 2:
        return {
            "label": "🔴 High Risk",
            "tips": [
                "💉 Monitor and control your blood pressure daily.",
                "🚭 Quit smoking immediately.",
                "🍲 Reduce salt and processed foods from your diet.",
                "🏃 Walk at least 30 minutes a day.",
                "⚖️ Maintain a healthy BMI through diet and exercise.",
                "🧘 Reduce stress using yoga or meditation.",
                "💊 Take medications as prescribed and never skip a dose.",
            ]
        }
    elif pred == 1:
        return {
            "label": "🟠 Medium Risk",
            "tips": [
                "🥗 Eat more fruits, vegetables, and whole grains.",
                "🩺 Get your glucose and cholesterol checked regularly.",
                "🚶 Stay physically active for at least 150 minutes/week.",
                "🧂 Watch your salt intake.",
                "🧘 Practice relaxation techniques daily.",
                "🧃 Avoid sugary drinks and alcohol.",
                "⏰ Maintain regular sleep schedule and avoid fatigue.",
            ]
        }
    else:
        return {
            "label": "🟢 Low Risk",
            "tips": [
                "🏋️ Continue regular physical activities.",
                "🥦 Maintain a balanced, nutritious diet.",
                "🩺 Do annual health checkups.",
                "🚭 Stay away from tobacco and secondhand smoke.",
                "🌞 Get sunlight and stay hydrated.",
                "😴 Get 7-9 hours of quality sleep per night.",
                "📚 Stay educated on healthy habits and follow them.",
            ]
        }

# Categorical label options
label_map = {
    "gender": ("Female", "Male", "Other"),
    "ever_married": ("No", "Yes"),
    "work_type": ("Private", "Self-employed", "Govt_job", "Children", "Never_worked"),
    "Residence_type": ("Urban", "Rural"),
    "smoking_status": ("Never smoked", "Formerly smoked", "Smokes", "Unknown"),
    "hypertension": ("No", "Yes"),
    "heart_disease": ("No", "Yes")
}

# UI
st.title("🧠 Stroke Risk Prediction App")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Navigation", menu)

# ------------------- LOGIN ------------------- #
if choice == "Login":
    if not st.session_state.logged_in:
        st.subheader("🔐 User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate(username, password):
                st.success(f"✅ Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("❌ Invalid username or password.")

    if st.session_state.logged_in:
        st.markdown("---")
        st.header("📋 Enter Your Health Details")

        with st.form("prediction_form"):
            user_input = {}
            for col in features:
                if col in ["age", "avg_glucose_level", "bmi"]:
                    user_input[col] = st.number_input(f"{col.replace('_', ' ').capitalize()}", min_value=0.0)
                elif col in label_map:
                    options = label_map[col]
                    selected = st.selectbox(f"{col.replace('_', ' ').capitalize()}", options)
                    user_input[col] = options.index(selected)
                else:
                    user_input[col] = st.selectbox(f"{col.replace('_', ' ').capitalize()} (0/1)", [0, 1])

            submit = st.form_submit_button("Predict Risk")

        if submit:
            df_input = pd.DataFrame([user_input])
            prediction = model.predict(df_input)[0]
            result = get_health_tips(prediction)

            st.markdown(f"### 🧾 Prediction Result: **{result['label']}**")
            st.markdown("#### 🩺 Personalized Healthcare Tips:")
            for tip in result["tips"]:
                st.markdown(f"- {tip}")

        st.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": ""}))

# ------------------- SIGN UP ------------------- #
elif choice == "Sign Up":
    st.subheader("🆕 Create New Account")
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        users = pd.read_csv("users.csv")
        if new_user in users["username"].values:
            st.warning("⚠️ Username already exists!")
        else:
            users.loc[len(users)] = [new_user, new_pass]
            users.to_csv("users.csv", index=False)
            st.success("🎉 Account created successfully! Please login.")
