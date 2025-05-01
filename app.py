import streamlit as st
import pandas as pd
import joblib

# Load the trained model and feature columns
model = joblib.load("stroke_model.pkl")        # Make sure this model outputs 0, 1, 2
features = joblib.load("features.pkl")         # List of input features

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------- Utility Functions ---------------------- #

# Authenticate user credentials
def authenticate(username, password):
    users = pd.read_csv("users.csv")
    return any((users['username'] == username) & (users['password'] == password))

# Generate personalized tips based on risk level
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

# ---------------------- Streamlit UI ---------------------- #

st.title("🧠 Stroke Risk Prediction App")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Login":
    st.subheader("🔐 User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"✅ Welcome {username}!")
            st.markdown("---")
            st.header("📋 Enter Your Health Details")

            user_input = {}
            for col in features:
                if col in ["age", "avg_glucose_level", "bmi"]:
                    user_input[col] = st.number_input(f"{col.replace('_', ' ').capitalize()}", min_value=0.0)
                else:
                    user_input[col] = st.selectbox(f"{col.replace('_', ' ').capitalize()} (0 = No / 1 = Yes)", [0, 1])

            if st.button("Predict Risk"):
                df_input = pd.DataFrame([user_input])
                prediction = model.predict(df_input)[0]
                result = get_health_tips(prediction)

                st.markdown(f"### 🧾 Prediction Result: **{result['label']}**")
                st.markdown("#### 🩺 Personalized Healthcare Tips:")
                for tip in result["tips"]:
                    st.markdown(f"- {tip}")

        else:
            st.error("❌ Invalid username or password.")

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
