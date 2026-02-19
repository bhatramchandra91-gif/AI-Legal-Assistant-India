import streamlit as st
import sqlite3

def signup():
    st.title("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
        cur.execute("INSERT INTO users VALUES(?,?)",(username,password))
        conn.commit()
        st.success("Account created")
