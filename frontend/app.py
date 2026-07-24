#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------
import time 
import streamlit as st 
from datetime import datetime 
import os , sys 
from api_client import APIClient


# Setting up the page cofig for the first streamlit call
st.set_page_config(
    page_title="NeuraVault-Multi-Tenant-Enterprise-RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

#---------------------------------------------------------------------------------
#                                   CSS Style Statements
#---------------------------------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root theme ── */
:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2236;
    --border: #1e2d45;
    --accent: #3b82f6;
    --accent2: #6366f1;
    --green: #10b981;
    --amber: #f59e0b;
    --red: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Main area */
.main .block-container {
    padding-top: 1.5rem;
    max-width: 1100px;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.card-accent {
    border-left: 3px solid var(--accent);
}

/* ── Metric tiles ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

.metric-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.metric-tile .value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}

.metric-tile .label {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.badge-ready   { background: rgba(16,185,129,.15); color: #10b981; border: 1px solid #10b981; }
.badge-processing { background: rgba(245,158,11,.15); color: #f59e0b; border: 1px solid #f59e0b; }
.badge-error   { background: rgba(239,68,68,.15); color: #ef4444; border: 1px solid #ef4444; }

/* ── Chat bubbles ── */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.5rem 0;
}

.chat-user .bubble {
    background: var(--accent2);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 75%;
    font-size: 0.92rem;
}

.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.5rem 0;
}

.chat-ai .bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 16px 4px;
    max-width: 80%;
    font-size: 0.92rem;
    line-height: 1.6;
}

.chat-meta {
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.25rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Source chips ── */
.source-chip {
    display: inline-block;
    background: rgba(59,130,246,.1);
    border: 1px solid rgba(59,130,246,.3);
    color: var(--accent);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    margin: 2px 3px;
}

/* ── Logo ── */
.logo {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
}

.logo span { color: var(--accent); }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}

/* ── Buttons ── */
.stButton button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: opacity .15s;
}

.stButton button:hover { opacity: 0.88 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}
</style>
""", unsafe_allow_html=True)


#---------------------------------------------------------------------------------
#                                   Session State init
#---------------------------------------------------------------------------------

def init_session():
    """
        Init the session with all None values
    """

    # Creating dict with all necessary fields
    defaults = {
        "access_token" : None ,
        "username" : None,
        "user_id" : None,
        "chat_history" : [],
        "page" : "chat"
    }

    # now add this field to st.session_state
    for k , v in defaults.items():
        st.session_state[k] = v

# Calling init session
init_session()

def get_client() -> APIClient:
    """
        for getting the client class object inorder to process the auth and
        management.
        Returns:
            return object of class APIClient of the api_client.py file 
    """
    return APIClient(access_token=st.session_state.access_token)


#---------------------------------------------------------------------------------
#                                     Auth pages
#---------------------------------------------------------------------------------

def render_login():
    col1,col2,col3 = st.columns([1,1.4,1])

    with col2:
        st.markdown("""
            <div style='text-align:center; padding: 2rem 0 1.5rem;'>
                <div class='logo'>Doc<span>Mind</span></div>
                <p style='color:#64748b; font-size:.9rem; margin-top:.5rem;'>
                    Your Private AI Knowledge Base
                </p>
            </div>
        """ , unsafe_allow_html=True)

        tab_login , tab_register = st.tabs(['Sign In' , "Create Account"])

        with tab_login:
            st.markdown("<div class='card'>" , unsafe_allow_html=True)
            username = st.text_input("Username" , key="login_user" , placeholder="your username")
            password = st.text_input("Password" , type="password" , key="login_pass" , placeholder="*******")

            if st.button("Sign in" , use_container_width=True):
                if username and password:
                    client = APIClient()
                    data,code = client.login(username , password)
                    if code == 200:
                        st.session_state.access_token = data['access_token']
                        me , _ = APIClient(data['access_token']).me()
                        st.session_state.username = me.get("username" , username)
                        st.session_state.user_id = me.get("user_id" , "")
                        st.success("Signed in!")
                        # st.rerun()
                    else:
                        st.error(data.get("detail" , "Login failed"))
                else:
                    st.warning("Please fill in all fields")
            st.markdown("</div>" , unsafe_allow_html=True)


        with tab_register:
            st.markdown("<div class='card'>" , unsafe_allow_html=True)
            r_email = st.text_input("Email" , key="reg_email" , placeholder="you@example.come")
            r_username = st.text_input("Username" , key="reg_user" , placeholder="choose_username")
            r_password = st.text_input("Password" , key="reg_pass" , type="password" , placeholder="min 8 chars")

            if st.button("Create Account" , use_container_width=True , key="reg_btn"):
                if r_email and r_username and r_password:
                    client = APIClient()
                    data,code = client.register(r_email,r_username,r_password)
                    if code == 201:
                        st.success("Account created! Please log in.")
                    else:
                        st.error(data.get("detail" , "Registration failed"))
                else:
                    st.warning("All fields required")
            st.markdown("</div>" , unsafe_allow_html=True)



#---------------------------------------------------------------------------------
#                                   App Router
#---------------------------------------------------------------------------------

def main():
    if not st.session_state.access_token:
        render_login()

if __name__ == "__main__":
    main()