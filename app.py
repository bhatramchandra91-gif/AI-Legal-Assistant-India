import streamlit as st
import sqlite3
import openai
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Legal Assistant", layout="wide")

# ------------------ OPENAI KEY ------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ------------------ USER DATABASE ------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
conn.commit()

# ------------------ LANGUAGE ------------------
lang = st.sidebar.selectbox("🌐 Language", ["English","Hindi","Marathi"])
def translate_text(text, lang):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":f"Translate into {lang} legal language"},
            {"role":"user","content":text}
        ]
    )
    return response.choices[0].message.content


st.title("⚖️ AI Legal Assistant India")

# ------------------ LOGIN MENU ------------------
menu_main = st.sidebar.selectbox("Menu",["Login","Signup","Enter App"])

# ------------------ SIGNUP ------------------
if menu_main == "Signup":
    st.subheader("Create Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Signup"):
        cur.execute("INSERT INTO users VALUES(?,?)",(new_user,new_pass))
        conn.commit()
        st.success("Account created. Go to login.")

# ------------------ LOGIN ------------------
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

# ------------------ MAIN APP ------------------
elif menu_main == "Enter App":

    if "logged" not in st.session_state:
        st.warning("Login first")
        st.stop()

    st.success("Welcome Lawyer 👨‍⚖️")

    dashboard = st.sidebar.selectbox("Dashboard",[
        "📜 AI Drafting",
        "⚖️ Judgment Search",
        "📁 Case CRM",
        "📊 Practice Improvements"
    ])

    # ================== AI DRAFTING ==================
    if dashboard == "📜 AI Drafting":
        st.header("📜 AI Legal Drafting")

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

        if user_input:
            with st.spinner("Generating..."):

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role":"system","content":"You are expert Indian lawyer"},
                        {"role":"user","content":user_input}
                    ]
                )

                result = response.choices[0].message.content

                # Translation
                if lang != "English":
                    result = translate_text(result, lang)

                st.success("Draft Ready")
                st.write(result)

        else:
            st.warning("Enter case details")

    # ================== JUDGMENT SEARCH ==================
elif menu == "Judgments":
    st.subheader("📚 Indian Judgment AI Search")

    query = st.text_input("Enter case type (ex: cheque bounce, divorce, bail)")

    if st.button("Search Judgments"):
        if query:

            with st.spinner("Finding relevant judgments..."):

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                        "role":"system",
                        "content":"You are an expert Indian Supreme Court legal researcher. Give real Indian case references with summary."
                        },
                        {
                        "role":"user",
                        "content":f"Give top Indian court judgments for: {query} with summary and legal points"
                        }
                    ]
                )

                result = response.choices[0].message.content
                st.success("Judgments Found")
                st.write(result)
        else:
            st.warning("Enter case topic")

    # ================== CRM ==================
    elif dashboard == "📁 Case CRM":
        st.header("Client Case Manager")

        conn2 = sqlite3.connect("cases.db",check_same_thread=False)
        cur2 = conn2.cursor()
        cur2.execute("""CREATE TABLE IF NOT EXISTS cases(
            case_no TEXT, client TEXT, phone TEXT,
            case_type TEXT, hearing TEXT, fees TEXT)""")

        case_no = st.text_input("Case Number")
        client = st.text_input("Client Name")
        phone = st.text_input("Phone")
        case_type = st.text_input("Case Type")
        hearing = st.date_input("Next Hearing")
        fees = st.selectbox("Fees",["Paid","Pending","Partial"])

        if st.button("Save Case"):
            cur2.execute("INSERT INTO cases VALUES(?,?,?,?,?,?)",
                        (case_no,client,phone,case_type,str(hearing),fees))
            conn2.commit()
            st.success("Case saved")

        if st.button("Show All Cases"):
            rows = cur2.execute("SELECT * FROM cases").fetchall()
            for r in rows:
                st.write(r)

    # ================== IMPROVEMENTS ==================
    elif dashboard == "📊 Practice Improvements":
        st.header("AI Practice Growth Suggestions")

        text = st.text_area("Describe your practice issues")

        if st.button("Get Suggestions"):
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":f"Give business growth advice for lawyer: {text}"}]
            )
            st.write(response.choices[0].message.content)
