import streamlit as st
import sqlite3
from openai import OpenAI

# ------------------ OPENAI ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Legal Assistant", layout="wide")

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
            "Session Court","High Court","Supreme Court"
        ])

        doc_type = st.selectbox("Select Document",[
            "Legal Notice","Affidavit","Agreement","NDA"
        ])

        details = st.text_area("Enter case details")

        if st.button("Generate Draft"):
            if details:
                with st.spinner("Generating draft..."):

                    prompt = f"""
                    Create a professional {doc_type} for {court} India.
                    Case details:
                    {details}
                    Use proper Indian legal format.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role":"system","content":"You are expert Indian lawyer"},
                            {"role":"user","content":prompt}
                        ]
                    )

                    result = response.choices[0].message.content

                    if lang != "English":
                        result = translate_text(result, lang)

                    st.success("Draft Ready")
                    st.write(result)
                    st.download_button("Download Draft", result)

            else:
                st.warning("Enter case details")

    # ================== JUDGMENT SEARCH ==================
elif dashboard == "⚖️ Judgment Search":

    st.header("📚 Case Summary by Case Number")

    case_number = st.text_input("Enter Case Number or Party Name")
    manual_text = st.text_area("OR paste full judgment text")

    if st.button("Get Case Summary"):

        if case_number or manual_text:

            with st.spinner("Fetching & summarizing..."):

                # ---------------- FETCH FROM INDIANKANOON ----------------
                if case_number and not manual_text:
                    import requests
                    from bs4 import BeautifulSoup

                    url = f"https://indiankanoon.org/search/?formInput={case_number}"
                    headers = {"User-Agent":"Mozilla/5.0"}
                    r = requests.get(url, headers=headers)

                    soup = BeautifulSoup(r.text,'html.parser')
                    link = soup.select_one(".result_title a")

                    if link:
                        case_url = "https://indiankanoon.org" + link.get("href")
                        r2 = requests.get(case_url, headers=headers)
                        soup2 = BeautifulSoup(r2.text,'html.parser')

                        judgment_text = soup2.get_text()[:12000]
                    else:
                        st.error("Case not found")
                        st.stop()
                else:
                    judgment_text = manual_text

                # ---------------- AI SUMMARY ----------------
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role":"system","content":
                        "You are senior Indian Supreme Court lawyer. Summarize judgment with: facts, issues, decision, legal points."},

                        {"role":"user","content": judgment_text}
                    ]
                )

                result = response.choices[0].message.content

                # -------- Translation --------
                if lang != "English":
                    result = translate_text(result, lang)

                st.success("Case Summary Ready")
                st.write(result)

                st.download_button("Download Summary", result)

        else:
            st.warning("Enter case number or paste judgment")


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

    # ================== PRACTICE IMPROVEMENTS ==================
    elif dashboard == "📊 Practice Improvements":
        st.header("AI Practice Growth Suggestions")

        text = st.text_area("Describe your practice problems")

        if st.button("Get Suggestions"):
            if text:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role":"user","content":f"Give law firm growth strategy: {text}"}]
                )
                st.write(response.choices[0].message.content)
            else:
                st.warning("Enter problem")
