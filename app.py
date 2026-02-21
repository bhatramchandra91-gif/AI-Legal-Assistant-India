import streamlit as st
import sqlite3
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

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
    if lang == "English":
        return text

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
        "🤝 ADR Negotiator",
        "📚 Precedents for Argument",
        "📄 OCR PDF/Image Converter",
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
                    Use latest Indian legal format with headings.
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role":"system","content":"You are expert Indian lawyer"},
                            {"role":"user","content":prompt}
                        ]
                    )

                    result = response.choices[0].message.content
                    result = translate_text(result, lang)

                    st.success("Draft Ready")
                    st.write(result)
                    st.download_button("Download Draft", result)
            else:
                st.warning("Enter case details")

    # ================== JUDGMENT SEARCH ==================
    elif dashboard == "⚖️ Judgment Search":

        st.header("📚 Case Summary by Case Number")

        case_number = st.text_input("Enter Case Number / Party Name")
        manual_text = st.text_area("OR paste full judgment")

        if st.button("Get Case Summary"):

            if case_number or manual_text:

                with st.spinner("Fetching & summarizing..."):

                    if case_number and not manual_text:
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

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role":"system","content":
                             "Summarize this Indian judgment into facts, issues, decision, legal points."},
                            {"role":"user","content": judgment_text}
                        ]
                    )

                    result = response.choices[0].message.content
                    result = translate_text(result, lang)

                    st.success("Case Summary Ready")
                    st.write(result)
                    st.download_button("Download Summary", result)
            else:
                st.warning("Enter case number or paste judgment")

    # ================== ADR NEGOTIATOR ==================
    elif dashboard == "🤝 ADR Negotiator":

        st.header("🤝 Interactive AI Mediation Courtroom")

        if "adr_stage" not in st.session_state:
            st.session_state.adr_stage = 1
            st.session_state.case_data = {}
            st.session_state.score = 50

        if st.session_state.adr_stage == 1:
            st.subheader("Step 1: Enter Case")

            dispute = st.selectbox("Dispute type",[
                "Cheque Bounce","Property","Divorce","Business","Employment","Other"
            ])
            facts = st.text_area("Case facts")
            your_role = st.selectbox("Your role",[
                "Petitioner","Respondent","Accused","Complainant"
            ])

            if st.button("Start Mock Trial"):
                if facts:
                    st.session_state.case_data = {
                        "dispute":dispute,
                        "facts":facts,
                        "role":your_role
                    }
                    st.session_state.adr_stage = 2
                    st.rerun()
                else:
                    st.warning("Enter case facts")

        elif st.session_state.adr_stage == 2:

            st.subheader("Step 2: AI Judge Scenario")
            case = st.session_state.case_data

            if "scenario" not in st.session_state:
                prompt = f"""
                Create a realistic Indian court mediation scenario.

                Case: {case['dispute']}
                Facts: {case['facts']}
                User role: {case['role']}

                Give:
                - Opponent argument
                - Judge observation
                - 3 possible actions user can choose
                - Winning probability for each option (in %)
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role":"user","content":prompt}]
                )
                st.session_state.scenario = response.choices[0].message.content

            st.write(st.session_state.scenario)

            choice = st.radio("Choose your action:",[
                "Strong legal argument",
                "Settlement negotiation",
                "Aggressive litigation"
            ])

            if st.button("Submit Decision"):

                prompt2 = f"""
                User selected: {choice}
                Based on Indian legal practice:
                Update winning probability
                Give judge reaction
                Give next move options
                """

                response2 = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role":"user","content":prompt2}]
                )

                result = response2.choices[0].message.content
                result = translate_text(result, lang)

                st.write(result)

                import random
                change = random.randint(-10,15)
                st.session_state.score += change
                st.progress(min(max(st.session_state.score,0),100))
                st.write(f"### 🧠 Case Winning Probability: {st.session_state.score}%")

                st.session_state.adr_stage = 3

        elif st.session_state.adr_stage == 3:

            st.subheader("Step 3: Final Verdict / Settlement")

            if st.button("Generate Final Outcome"):

                prompt3 = f"""
                Generate final mediation result.

                Winning probability: {st.session_state.score}%

                If above 60% → user likely wins  
                If below 40% → suggest settlement  
                Provide final judge style decision
                """

                response3 = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role":"user","content":prompt3}]
                )

                result = response3.choices[0].message.content
                result = translate_text(result, lang)

                st.success("🏛 Final Mediation Result")
                st.write(result)

            if st.button("Start New Case"):
                st.session_state.adr_stage = 1
                st.session_state.score = 50
                st.session_state.scenario = ""
                st.rerun()

    # ================== PRECEDENTS ==================
    elif dashboard == "📚 Precedents for Argument":

        st.header("📚 AI Precedent Finder for Court Arguments")

        case_topic = st.text_input("Enter case topic")
        your_side = st.selectbox("Which side?",["Petitioner","Respondent","Accused","Complainant"])
        facts = st.text_area("Enter brief case facts")

        if st.button("Find Strong Precedents"):

            if case_topic:

                with st.spinner("Finding best court precedents..."):

                    prompt = f"""
                    You are senior Supreme Court legal researcher.

                    Case topic: {case_topic}
                    My side: {your_side}
                    Case facts: {facts}

                    Provide:
                    - 5 strongest Indian precedents
                    - Court name
                    - Year
                    - Legal principle
                    - How to use in argument
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role":"user","content":prompt}]
                    )

                    result = response.choices[0].message.content
                    result = translate_text(result, lang)

                    st.success("Top Precedents for Argument")
                    st.write(result)
                    st.download_button("Download Precedents", result)
            else:
                st.warning("Enter case topic")

        # ================== OCR PDF / IMAGE CONVERTER ==================
        elif dashboard == "📄 OCR PDF/Image Converter":

            st.header("📄 OCR Converter – PDF/Image to Searchable Text")

            uploaded_file = st.file_uploader(
               "Upload scanned PDF or image",
                type=["pdf","png","jpg","jpeg"]
        )

        if uploaded_file:

            st.success("File uploaded successfully")

            if st.button("Extract Text using OCR"):

                with st.spinner("Performing OCR..."):

                    text_output = ""

                    try:
                        # ---- IF PDF ----
                        if uploaded_file.type == "application/pdf":
                            pages = convert_from_bytes(uploaded_file.read())
                            for page in pages:
                                text_output += pytesseract.image_to_string(page)

                        # ---- IF IMAGE ----
                        else:
                            image = Image.open(uploaded_file)
                            text_output = pytesseract.image_to_string(image)

                        if text_output.strip():

                            text_output = translate_text(text_output, lang)

                            st.success("OCR Extraction Completed")
                            st.text_area("Extracted Text", text_output, height=400)
                            st.download_button("Download Text File", text_output)

                        else:
                            st.warning("No readable text detected.")

                    except Exception as e:
                        st.error("OCR failed. Make sure Tesseract is installed.")

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

    # ================== PRACTICE ==================
    elif dashboard == "📊 Practice Improvements":
        st.header("AI Practice Growth Suggestions")

        text = st.text_area("Describe your practice problems")

        if st.button("Get Suggestions"):
            if text:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role":"user","content":f"Law firm growth strategy: {text}"}]
                )
                result = response.choices[0].message.content
                result = translate_text(result, lang)
                st.write(result)
            else:
                st.warning("Enter problem")
