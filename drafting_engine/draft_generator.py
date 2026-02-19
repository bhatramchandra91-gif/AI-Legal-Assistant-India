import openai

def generate_draft(doc_type, court_type, details):

    prompt = f"""
    Create a {doc_type} as per latest {court_type} India format.

    Case Details:
    {details}

    Follow proper legal formatting, headings, clauses and court language.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response['choices'][0]['message']['content']

import streamlit as st
from drafting_engine.draft_generator import generate_draft

def drafting_ui():
    st.header("Drafting Engine")

    court = st.selectbox("Select Court",["Session Court","High Court","Supreme Court"])
    doc = st.selectbox("Document",["Legal Notice","Affidavit","Agreement","NDA"])
    details = st.text_area("Enter case details")

    if st.button("Generate Draft"):
        draft = generate_draft(doc,court,details)
        st.write(draft)
        st.download_button("Download",draft)

