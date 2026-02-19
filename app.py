import streamlit as st
from auth.login import login
from auth.signup import signup
from drafting_engine.draft_generator import generate_draft
from crm.crm_dashboard import crm_ui

st.set_page_config(page_title="AI Legal Assistant",layout="wide")

menu = st.sidebar.selectbox("Menu",[
"Login","Signup","Drafting Engine","OCR",
"ADR Mediator","Judgments","CRM","Improvements"
])

if menu=="Login":
    login()
elif menu=="Signup":
    signup()
elif menu=="CRM":
    crm_ui()
