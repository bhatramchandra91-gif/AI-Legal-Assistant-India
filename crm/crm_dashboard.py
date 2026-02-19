import sqlite3
import streamlit as st

def crm_ui():
    st.header("CRM Dashboard")

    case_no = st.text_input("Case Number")
    client = st.text_input("Client Name")
    aadhaar = st.text_input("Aadhaar")
    phone = st.text_input("Phone")
    details = st.text_area("Case details")
    payment = st.selectbox("Payment",["Paid","Pending","Partial"])

    if st.button("Save"):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cases(
            case_no TEXT, client TEXT, aadhaar TEXT,
            phone TEXT, details TEXT, payment TEXT)""")
        cur.execute("INSERT INTO cases VALUES(?,?,?,?,?,?)",
                    (case_no,client,aadhaar,phone,details,payment))
        conn.commit()
        st.success("Saved")
