import streamlit as st
from pint import UnitRegistry
import requests
import json
import datetime
import pandas as pd
from googletrans import Translator

# Initialize unit registry and translator
ureg = UnitRegistry()
translator = Translator()

# Conversion history (Session state initialization)
if "conversion_history" not in st.session_state:
    st.session_state["conversion_history"] = []

# Supported languages
languages = {
    "English": "en",
    "Urdu (اردو)": "ur",
    "Arabic (العربية)": "ar",
    "French (Français)": "fr",
    "Spanish (Español)": "es",
    "Chinese (中文)": "zh-cn"
}

# Function to translate text
def translate_text(text, lang_code):
    if lang_code == "en":
        return text
    try:
        return translator.translate(text, dest=lang_code).text
    except Exception as e:
        return f"Translation Error: {e}"

# Function to handle unit conversion
def convert_units(category, from_unit, to_unit, value):
    try:
        if category == "Currency":
            return convert_currency(from_unit, to_unit, value)
        result = (value * ureg(from_unit)).to(to_unit).magnitude
        return round(result, 4)
    except Exception as e:
        return f"Error: {e}"

# Function to handle currency conversion
def convert_currency(from_currency, to_currency, amount):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url).json()
        rate = response["rates"].get(to_currency.upper())
        if rate:
            return round(amount * rate, 4)
        return "Invalid currency code"
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI Configuration
st.set_page_config(page_title="⚡ HG - Thunder Converter  ⚡", layout="wide", initial_sidebar_state="expanded")

# Custom styling
st.markdown("""
    <style>
    .footer {text-align: center; font-size: 16px; margin-top: 20px; color: #888;}
    </style>
""", unsafe_allow_html=True)

# Language selection
selected_language = st.sidebar.selectbox("🌎 Select Language", list(languages.keys()))
lang_code = languages[selected_language]

st.title(translate_text("⚡ HG - Thunder Converter  ⚡", lang_code))
st.write(translate_text("Convert between different units of measurement instantly with ease!", lang_code))
st.sidebar.image("currency.webp")
# Sidebar settings
st.sidebar.header(translate_text("⚙ Settings", lang_code))
st.sidebar.write(f" {translate_text('Current Date:', lang_code)} {datetime.date.today()}")
st.sidebar.date_input(translate_text("📆 Select a date", lang_code))

# Conversion categories
categories = {
    "Mass": ["milligram", "gram", "kilogram", "pound", "ounce"],
    "Length": ["millimeter", "centimeter", "meter", "kilometer", "mile", "yard", "foot", "inch"],
    "Time": ["second", "minute", "hour", "day"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Currency": ["USD", "EUR", "GBP", "INR", "PKR", "JPY", "CNY"]
}

# User input fields
category = st.selectbox(translate_text("Select Conversion Type", lang_code), list(categories.keys()))
from_unit = st.selectbox(translate_text("From Unit", lang_code), categories[category])
to_unit = st.selectbox(translate_text("To Unit", lang_code), categories[category])
value = st.number_input(translate_text("Enter Value", lang_code), min_value=0.0, format="%f")

# Convert button
if st.button(translate_text("🚀 Convert", lang_code)):
    st.success("✅ Successfully Convert")
    st.balloons()
    result = convert_units(category, from_unit, to_unit, value)
    if "Error" not in str(result):
        st.session_state["conversion_history"].append({
            "category": category,
            "from": from_unit,
            "to": to_unit,
            "value": value,
            "result": result,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    st.success(f"{translate_text('Result:', lang_code)} {result} {to_unit}")

# Sidebar - Conversion History
st.sidebar.subheader(translate_text("📜 Conversion History", lang_code))
if st.session_state["conversion_history"]:
    for record in reversed(st.session_state["conversion_history"]):
        st.sidebar.write(f"🕒 {record['timestamp']}")
        st.sidebar.write(f"🔹 {record['value']} {record['from']} → {record['result']} {record['to']}")
        st.sidebar.write(f"({record['category']})")
        st.sidebar.write("---")
else:
    st.sidebar.write(translate_text("No history available.", lang_code))

# Download history as CSV
if st.sidebar.button(translate_text("📥 Download History", lang_code)):
    df = pd.DataFrame(st.session_state["conversion_history"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(label=translate_text("Download CSV", lang_code), data=csv, file_name="conversion_history.csv", mime="text/csv")
    st.sidebar.success(translate_text("✅ Download successfully!", lang_code))
# Clear history button
if st.sidebar.button(translate_text("🗑 Clear History", lang_code)):
    st.session_state["conversion_history"] = []
    st.sidebar.success(translate_text("✅ History cleared!", lang_code))


# Footer
st.markdown(f'<p class="footer">{translate_text("💖 Created by Hadiqa Gohar", lang_code)}</p>', unsafe_allow_html=True)
