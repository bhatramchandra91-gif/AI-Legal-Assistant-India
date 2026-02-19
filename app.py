import streamlit as st

st.set_page_config(page_title="AI Legal Assistant", layout="wide")

st.title("⚖️ AI Legal Assistant India")

menu = st.sidebar.selectbox("Select Module",[
"Home",
"Drafting Engine",
"OCR Converter",
"ADR Mediator",
"Judgments",
"CRM Dashboard",
"Improvements"
])

if menu == "Home":
    st.write("Welcome to AI Legal Assistant")

elif menu == "Drafting Engine":
    st.write("Drafting module loading...")

elif menu == "OCR Converter":
    st.write("OCR module loading...")

elif menu == "ADR Mediator":
    st.write("ADR module loading...")

elif menu == "Judgments":
    st.write("Judgment scraper loading...")

elif menu == "CRM Dashboard":
    st.write("CRM loading...")

elif menu == "Improvements":
    st.write("Improvement AI loading...")
