import streamlit as st
import sqlite3

def login():
    st.title("AI Legal Assistant Login")

    lang = st.selectbox("Choose Language", ["English","Hindi","Marathi"])
    st.session_state.lang = lang

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cur.fetchone()

        if user:
            st.success("Login successful")
            st.session_state.user = username
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")
