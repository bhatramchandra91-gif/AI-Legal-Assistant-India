import streamlit as st
import sqlite3

st.set_page_config(page_title="AI Legal Assistant", layout="wide")

# ---------- DATABASE ----------
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
conn.commit()

# ---------- LANGUAGE ----------
lang = st.sidebar.selectbox("🌐 Language", ["English","Hindi","Marathi"])

# ---------- LOGIN SYSTEM ----------
st.title("⚖️ AI Legal Assistant India")

menu_main = st.sidebar.selectbox("Menu",["Login","Signup","Enter App"])

if menu_main == "Signup":
    st.subheader("Create Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Signup"):
        cur.execute("INSERT INTO users VALUES(?,?)",(new_user,new_pass))
        conn.commit()
        st.success("Account created. Go to login.")

elif menu_main == "Login":
    st.subheader("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(user,pwd))
        data = cur.fetchone()
        if data:
            st.session_state.logged = True
            st.success("Login successful")
        else:
            st.error("Invalid login")

elif menu_main == "Enter App":
    if "logged" not in st.session_state:
        st.warning("Login first")
        st.stop()

    st.success("Welcome Lawyer 👨‍⚖️")

    dashboard = st.sidebar.selectbox("Dashboard",[
        "📜 AI Drafting",
        "⚖️ Judgment Search",
        "📁 Case CRM",
        "📄 OCR Scanner",
        "📊 Practice Improvements"
    ])


       if menu == "Drafting Engine":
        st.header("📜 Drafting Engine")

        court = st.selectbox("Select Court",[
            "Session Court",
            "High Court",
            "Supreme Court"
        ])

        doc_type = st.selectbox("Select Document",[
            "Legal Notice",
            "Affidavit",
            "Agreement",
            "NDA"
        ])

        details = st.text_area("Enter case details")

        if st.button("Generate Draft"):
            prompt = f"""
            Create a professional {doc_type} for {court} India.

            Case details:
            {details}

            Use latest Indian court format with proper headings,
            legal language and structure.
            """

            import openai
            import os

            openai.api_key = st.secrets["OPENAI_API_KEY"]

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )

            result = response.choices[0].message.content
            st.write(result)

            st.download_button("Download Draft", result)

    elif menu == "OCR Converter":
        st.header("OCR Converter")
        st.write("OCR module coming next...")

    elif menu == "ADR Mediator":
        st.header("ADR Mediator")
        st.write("Negotiation AI coming next...")

        elif menu == "Judgments":
        st.header("⚖️ Judgment & Precedent Search")

        case = st.text_input("Enter case type or section (example: cheque bounce 138)")

        if st.button("Search Judgments"):
            import requests
            from bs4 import BeautifulSoup

            url = f"https://indiankanoon.org/search/?formInput={case}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')

            results = soup.select(".result_title")[:5]

            for res in results:
                st.write(res.text)

        if dashboard == "📁 Case CRM":
        st.header("Client Case Manager")

        import sqlite3
        conn = sqlite3.connect("cases.db",check_same_thread=False)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cases(
            case_no TEXT, client TEXT, phone TEXT,
            case_type TEXT, hearing TEXT, fees TEXT)""")

        case_no = st.text_input("Case Number")
        client = st.text_input("Client Name")
        phone = st.text_input("Phone")
        case_type = st.text_input("Case Type")
        hearing = st.date_input("Next Hearing")
        fees = st.selectbox("Fees",["Paid","Pending","Partial"])

        if st.button("Save Case"):
            cur.execute("INSERT INTO cases VALUES(?,?,?,?,?,?)",
                        (case_no,client,phone,case_type,str(hearing),fees))
            conn.commit()
            st.success("Case saved")

        if st.button("Show All Cases"):
            rows = cur.execute("SELECT * FROM cases").fetchall()
            for r in rows:
                st.write(r)


    elif menu == "Improvements":
        st.header("System Improvements")
        st.write("AI improvement engine coming next...")
