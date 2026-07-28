#---------------------------------------------------------------------------------
#                                   DocMind — AI Knowledge Base
#              Pixel-perfect match of React Ethereal Glass design
#              Light/Dark theme switching with glassmorphism
#---------------------------------------------------------------------------------
import time
import streamlit as st
from datetime import datetime
import os, sys
from api_client import APIClient


#---------------------------------------------------------------------------------
#                                   Page Config
#---------------------------------------------------------------------------------
st.set_page_config(
    page_title="DocMind — Your Private AI Knowledge Base",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


#---------------------------------------------------------------------------------
#                                   Theme Management
#---------------------------------------------------------------------------------

def get_theme():
    """Get current theme from session state, default to light."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    return st.session_state.theme


def toggle_theme():
    """Toggle between light and dark themes."""
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


THEME = get_theme()


#---------------------------------------------------------------------------------
#                                   CSS — Ethereal Glass Design
#---------------------------------------------------------------------------------

if THEME == "light":
    CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #FAFBFF;
    --surface: rgba(255,255,255,0.7);
    --surface-strong: rgba(255,255,255,0.85);
    --surface-glass: rgba(255,255,255,0.92);
    --border: rgba(0,0,0,0.06);
    --border-light: rgba(0,0,0,0.04);
    --accent: #4F46E5;
    --accent-rgb: 79,70,229;
    --cyan: #06B6D4;
    --cyan-rgb: 6,182,212;
    --violet: #8B5CF6;
    --violet-rgb: 139,92,246;
    --amber: #F59E0B;
    --green: #10B981;
    --red: #EF4444;
    --text: #1E293B;
    --text-light: #64748B;
    --text-muted: #94A3B8;
    --glass-shadow: 0 8px 32px rgba(79,70,229,0.06), 0 2px 8px rgba(0,0,0,0.04);
    --glass-hover-shadow: 0 12px 40px rgba(79,70,229,0.10), 0 4px 12px rgba(0,0,0,0.06);
    --orb-indigo: rgba(79,70,229,0.15);
    --orb-cyan: rgba(6,182,212,0.12);
    --orb-violet: rgba(139,92,246,0.10);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px;
}

/* ── Sidebar — Frosted Glass ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.88) !important;
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.02);
}

[data-testid="stSidebar"] .stSidebarContent {
    padding-top: 1rem !important;
}

/* ── Gradient Orbs (background decoration) ── */
.orb-indigo, .orb-cyan, .orb-violet {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    z-index: 0;
}

.orb-indigo {
    width: 600px; height: 600px;
    background: radial-gradient(circle, var(--orb-indigo) 0%, transparent 70%);
}

.orb-cyan {
    width: 500px; height: 500px;
    background: radial-gradient(circle, var(--orb-cyan) 0%, transparent 70%);
}

.orb-violet {
    width: 400px; height: 400px;
    background: radial-gradient(circle, var(--orb-violet) 0%, transparent 70%);
}

/* ── Glass Panels ── */
.glass {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--glass-shadow);
    transition: all 200ms cubic-bezier(0.23,1,0.32,1);
}

.glass:hover {
    box-shadow: var(--glass-hover-shadow);
    transform: translateY(-2px);
}

.glass-strong {
    background: var(--surface-strong) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
}

.glass-accent {
    border-left: 3px solid var(--accent);
}

/* ── Metric Tiles ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
    .metric-row { grid-template-columns: repeat(2, 1fr); }
}

.metric-tile {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 16px;
    padding: 1.25rem;
    text-align: left;
    box-shadow: var(--glass-shadow);
    transition: all 200ms cubic-bezier(0.23,1,0.32,1);
    position: relative;
    overflow: hidden;
}

.metric-tile:hover {
    box-shadow: var(--glass-hover-shadow);
    transform: translateY(-2px);
}

.metric-tile:nth-child(1)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(79,70,229,0.08), rgba(59,130,246,0.04));
}
.metric-tile:nth-child(2)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(6,182,212,0.08), rgba(20,184,166,0.04));
}
.metric-tile:nth-child(3)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(124,58,237,0.04));
}
.metric-tile:nth-child(4)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(249,115,22,0.04));
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
    letter-spacing: -0.02em;
    margin-top: 0.5rem;
}

.metric-label {
    font-size: 0.7rem;
    color: var(--text-light);
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

.metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

.metric-icon-indigo { background: linear-gradient(135deg, rgba(79,70,229,0.15), rgba(59,130,246,0.1)); }
.metric-icon-cyan   { background: linear-gradient(135deg, rgba(6,182,212,0.15), rgba(20,184,166,0.1)); }
.metric-icon-violet { background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(124,58,237,0.1)); }
.metric-icon-amber  { background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(249,115,22,0.1)); }

/* ── Chat Bubbles ── */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.6rem 0;
}

.chat-user .bubble {
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 6px 18px;
    max-width: 75%;
    font-size: 0.92rem;
    line-height: 1.5;
    box-shadow: 0 4px 16px rgba(79,70,229,0.2);
}

.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.6rem 0;
}

.chat-ai .bubble {
    background: var(--surface-strong) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    color: var(--text);
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 18px 6px;
    max-width: 80%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.chat-meta {
    font-size: 0.7rem;
    color: var(--text-light);
    margin-top: 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(0,0,0,0.05);
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

/* ── Source Chips ── */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(79,70,229,0.05);
    border: 1px solid rgba(79,70,229,0.1);
    color: var(--accent);
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Status Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
}

.badge-ready     { background: rgba(16,185,129,0.08); color: #059669; border: 1px solid rgba(16,185,129,0.2); }
.badge-processing { background: rgba(245,158,11,0.08); color: #D97706; border: 1px solid rgba(245,158,11,0.2); }
.badge-error     { background: rgba(239,68,68,0.08); color: #DC2626; border: 1px solid rgba(239,68,68,0.2); }

/* ── Logo ── */
.logo {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
}

.logo span { color: var(--accent); }

/* ── Logo Icon ── */
.logo-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(79,70,229,0.25);
    font-size: 1.4rem;
}

.logo-icon-sm {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(79,70,229,0.2);
    font-size: 1rem;
}

.logo-icon-xs {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(79,70,229,0.15);
    font-size: 0.85rem;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.5) !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.55rem 0.8rem !important;
    transition: all 200ms ease !important;
    height: 44px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(79,70,229,0.4) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.08) !important;
    background: rgba(255,255,255,0.9) !important;
}

/* ── Buttons ── */
.stButton button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.5rem 1.2rem !important;
    height: 44px !important;
    transition: all 150ms ease !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.2) !important;
}

.stButton button:hover {
    background: #4338CA !important;
    box-shadow: 0 4px 16px rgba(79,70,229,0.3) !important;
    transform: translateY(-1px);
}

.stButton button:active {
    transform: scale(0.97);
}

/* Secondary buttons */
.stButton > div[kind="secondary"] > button,
.stButton > div[kind="primary"] ~ div > button,
div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(79,70,229,0.06) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(79,70,229,0.15) !important;
    box-shadow: none !important;
}

.stButton > div[kind="secondary"] > button:hover {
    background: rgba(79,70,229,0.1) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.5) !important;
    border: 2px dashed rgba(0,0,0,0.08) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    transition: all 300ms ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(79,70,229,0.2) !important;
    background: rgba(79,70,229,0.02) !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,0,0,0.05) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.02) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-light) !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 2px !important;
    transition: all 200ms ease !important;
}

.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: white !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border-bottom: none !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.6) !important;
    border-color: rgba(0,0,0,0.06) !important;
    border-radius: 10px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 12px !important;
    box-shadow: var(--glass-shadow);
}

[data-testid="stExpander"] [data-testid="stExpanderContent"] {
    padding: 1rem;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}

/* ── Info/Success/Error ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ── Page Header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.25rem;
}

.page-header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.page-header-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(79,70,229,0.1), rgba(6,182,212,0.08));
    flex-shrink: 0;
}

.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
    color: var(--text);
}

.page-subtitle {
    color: var(--text-light);
    font-size: 0.85rem;
    margin-top: 0.15rem;
}

/* ── System Status Badge ── */
.system-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
    background: rgba(0,0,0,0.03);
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
}

/* ── Doc Row ── */
.doc-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    transition: all 150ms ease;
    margin-bottom: 0.5rem;
}

.doc-row:hover {
    background: rgba(0,0,0,0.02);
}

.doc-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(79,70,229,0.05), rgba(6,182,212,0.03));
    border: 1px solid rgba(79,70,229,0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 1rem;
}

/* ── Activity Item ── */
.activity-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.6rem;
    border-radius: 12px;
    transition: background 150ms ease;
}

.activity-item:hover {
    background: rgba(0,0,0,0.02);
}

.activity-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 0.85rem;
}

.activity-time {
    font-size: 0.7rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 3rem 1.5rem;
}

/* ── Suggestion Grid ── */
.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    max-width: 420px;
    margin: 1.5rem auto 0;
}

@media (max-width: 600px) {
    .suggestion-grid { grid-template-columns: 1fr; }
}

.suggestion-card {
    background: var(--surface);
    border: 1px solid rgba(0,0,0,0.04);
    border-radius: 12px;
    padding: 0.75rem;
    font-size: 0.82rem;
    color: var(--text-light);
    text-align: left;
    transition: all 150ms ease;
}

.suggestion-card:hover {
    background: rgba(255,255,255,0.9);
    border-color: rgba(79,70,229,0.15);
}

/* ── User Badge ── */
.user-badge {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.75rem;
    border-radius: 12px;
    background: rgba(79,70,229,0.04);
    border: 1px solid rgba(79,70,229,0.08);
    margin-bottom: 1rem;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 3px 8px rgba(79,70,229,0.2);
}

.user-info .name {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text);
}

.user-info .plan {
    font-size: 0.68rem;
    color: var(--accent);
    font-weight: 500;
}

/* ── Nav Buttons ── */
.nav-active {
    background: linear-gradient(135deg, rgba(79,70,229,0.08), rgba(6,182,212,0.04)) !important;
    border: 1px solid rgba(79,70,229,0.12) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}

/* ── Namespace Stats ── */
.ns-stat-label {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.68rem;
    color: var(--text-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.25rem;
}

.ns-stat-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
}

.plan-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(79,70,229,0.08), rgba(6,182,212,0.06));
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border: 1px solid rgba(79,70,229,0.1);
}

.ns-divider {
    margin-top: 1.25rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(0,0,0,0.05);
}

.ns-code {
    font-size: 0.72rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
}

.ns-code span {
    background: rgba(0,0,0,0.03);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    border: 1px solid rgba(0,0,0,0.06);
}

/* ── History Item ── */
.history-item {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
    border-radius: 14px;
    margin-bottom: 0.75rem;
    overflow: hidden;
    transition: all 200ms ease;
}

.history-item:hover {
    box-shadow: var(--glass-shadow);
}

/* ── Upload Zone ── */
.upload-zone {
    background: var(--surface-strong) !important;
    backdrop-filter: blur(30px) !important;
    border: 2px dashed rgba(0,0,0,0.08) !important;
    border-radius: 16px !important;
    padding: 2.5rem 1.5rem !important;
    text-align: center;
    transition: all 300ms ease !important;
}

.upload-zone:hover {
    border-color: rgba(79,70,229,0.2) !important;
    background: rgba(79,70,229,0.02) !important;
}

/* ── Hide Streamlit branding ── */
footer { visibility: hidden !important; }
footer:after { visibility: hidden !important; }

/* ── Smooth scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.08);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.15); }
</style>
"""

else:
    # ── DARK THEME ──
    CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0C0E1A;
    --surface: rgba(30,34,50,0.7);
    --surface-strong: rgba(30,34,50,0.85);
    --surface-glass: rgba(24,27,40,0.92);
    --border: rgba(255,255,255,0.06);
    --border-light: rgba(255,255,255,0.04);
    --accent: #818CF8;
    --accent-rgb: 129,140,248;
    --cyan: #22D3EE;
    --cyan-rgb: 34,211,238;
    --violet: #A78BFA;
    --violet-rgb: 167,139,250;
    --amber: #FBBF24;
    --green: #34D399;
    --red: #F87171;
    --text: #E2E8F0;
    --text-light: #94A3B8;
    --text-muted: #64748B;
    --glass-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 2px 8px rgba(0,0,0,0.2);
    --glass-hover-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 4px 12px rgba(0,0,0,0.3);
    --orb-indigo: rgba(99,102,241,0.2);
    --orb-cyan: rgba(6,182,212,0.15);
    --orb-violet: rgba(139,92,246,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(20,23,36,0.92) !important;
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.3);
}

[data-testid="stSidebar"] .stSidebarContent {
    padding-top: 1rem !important;
}

/* ── Glass Panels ── */
.glass {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--glass-shadow);
    transition: all 200ms cubic-bezier(0.23,1,0.32,1);
}

.glass:hover {
    box-shadow: var(--glass-hover-shadow);
    transform: translateY(-2px);
}

.glass-strong {
    background: var(--surface-strong) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}

.glass-accent {
    border-left: 3px solid var(--accent);
}

/* ── Metric Tiles ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
    .metric-row { grid-template-columns: repeat(2, 1fr); }
}

.metric-tile {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 16px;
    padding: 1.25rem;
    text-align: left;
    box-shadow: var(--glass-shadow);
    transition: all 200ms cubic-bezier(0.23,1,0.32,1);
    position: relative;
    overflow: hidden;
}

.metric-tile:hover {
    box-shadow: var(--glass-hover-shadow);
    transform: translateY(-2px);
}

.metric-tile:nth-child(1)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(79,70,229,0.05));
}
.metric-tile:nth-child(2)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(20,184,166,0.05));
}
.metric-tile:nth-child(3)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(124,58,237,0.05));
}
.metric-tile:nth-child(4)::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    border-radius: 0 0 0 100%;
    background: linear-gradient(135deg, rgba(251,191,36,0.1), rgba(249,115,22,0.05));
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
    letter-spacing: -0.02em;
    margin-top: 0.5rem;
}

.metric-label {
    font-size: 0.7rem;
    color: var(--text-light);
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

.metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

.metric-icon-indigo { background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(79,70,229,0.1)); }
.metric-icon-cyan   { background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(20,184,166,0.1)); }
.metric-icon-violet { background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(124,58,237,0.1)); }
.metric-icon-amber  { background: linear-gradient(135deg, rgba(251,191,36,0.2), rgba(249,115,22,0.1)); }

/* ── Chat Bubbles ── */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.6rem 0;
}

.chat-user .bubble {
    background: linear-gradient(135deg, #4F46E5, #4338CA);
    color: white;
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 6px 18px;
    max-width: 75%;
    font-size: 0.92rem;
    line-height: 1.5;
    box-shadow: 0 4px 16px rgba(79,70,229,0.3);
}

.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin: 0.6rem 0;
}

.chat-ai .bubble {
    background: var(--surface-strong) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: var(--text);
    padding: 0.85rem 1.15rem;
    border-radius: 18px 18px 18px 6px;
    max-width: 80%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}

.chat-meta {
    font-size: 0.7rem;
    color: var(--text-light);
    margin-top: 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

/* ── Source Chips ── */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(129,140,248,0.08);
    border: 1px solid rgba(129,140,248,0.15);
    color: var(--accent);
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Status Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
}

.badge-ready     { background: rgba(52,211,153,0.1); color: #34D399; border: 1px solid rgba(52,211,153,0.2); }
.badge-processing { background: rgba(251,191,36,0.1); color: #FBBF24; border: 1px solid rgba(251,191,36,0.2); }
.badge-error     { background: rgba(248,113,113,0.1); color: #F87171; border: 1px solid rgba(248,113,113,0.2); }

/* ── Logo ── */
.logo {
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text);
}

.logo span { color: var(--accent); }

/* ── Logo Icon ── */
.logo-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 24px rgba(79,70,229,0.3);
    font-size: 1.4rem;
}

.logo-icon-sm {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(79,70,229,0.25);
    font-size: 1rem;
}

.logo-icon-xs {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(79,70,229,0.2);
    font-size: 0.85rem;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.55rem 0.8rem !important;
    transition: all 200ms ease !important;
    height: 44px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(129,140,248,0.4) !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.1) !important;
    background: rgba(255,255,255,0.08) !important;
}

/* ── Buttons ── */
.stButton button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.5rem 1.2rem !important;
    height: 44px !important;
    transition: all 150ms ease !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.2) !important;
}

.stButton button:hover {
    background: #6366F1 !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
    transform: translateY(-1px);
}

.stButton button:active {
    transform: scale(0.97);
}

.stButton > div[kind="secondary"] > button {
    background: rgba(129,140,248,0.08) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(129,140,248,0.2) !important;
    box-shadow: none !important;
}

.stButton > div[kind="secondary"] > button:hover {
    background: rgba(129,140,248,0.14) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 2px dashed rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    transition: all 300ms ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(129,140,248,0.25) !important;
    background: rgba(129,140,248,0.03) !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-light) !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 2px !important;
    transition: all 200ms ease !important;
}

.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: rgba(30,34,50,0.9) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2) !important;
    border-bottom: none !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    box-shadow: var(--glass-shadow);
}

[data-testid="stExpander"] [data-testid="stExpanderContent"] {
    padding: 1rem;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}

/* ── Info/Success/Error ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ── Page Header ── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.25rem;
}

.page-header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.page-header-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(129,140,248,0.12), rgba(34,211,238,0.08));
    flex-shrink: 0;
}

.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0;
    color: var(--text);
}

.page-subtitle {
    color: var(--text-light);
    font-size: 0.85rem;
    margin-top: 0.15rem;
}

/* ── System Status Badge ── */
.system-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
    background: rgba(255,255,255,0.04);
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
}

/* ── Doc Row ── */
.doc-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    transition: all 150ms ease;
    margin-bottom: 0.5rem;
}

.doc-row:hover {
    background: rgba(255,255,255,0.03);
}

.doc-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(129,140,248,0.08), rgba(34,211,238,0.04));
    border: 1px solid rgba(129,140,248,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 1rem;
}

/* ── Activity Item ── */
.activity-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.6rem;
    border-radius: 12px;
    transition: background 150ms ease;
}

.activity-item:hover {
    background: rgba(255,255,255,0.03);
}

.activity-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 0.85rem;
}

.activity-time {
    font-size: 0.7rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 3rem 1.5rem;
}

/* ── Suggestion Grid ── */
.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    max-width: 420px;
    margin: 1.5rem auto 0;
}

@media (max-width: 600px) {
    .suggestion-grid { grid-template-columns: 1fr; }
}

.suggestion-card {
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 0.75rem;
    font-size: 0.82rem;
    color: var(--text-light);
    text-align: left;
    transition: all 150ms ease;
}

.suggestion-card:hover {
    background: rgba(255,255,255,0.06);
    border-color: rgba(129,140,248,0.2);
}

/* ── User Badge ── */
.user-badge {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.75rem;
    border-radius: 12px;
    background: rgba(129,140,248,0.06);
    border: 1px solid rgba(129,140,248,0.1);
    margin-bottom: 1rem;
}

.user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F46E5, #06B6D4);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 3px 8px rgba(79,70,229,0.25);
}

.user-info .name {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text);
}

.user-info .plan {
    font-size: 0.68rem;
    color: var(--accent);
    font-weight: 500;
}

/* ── Nav Buttons ── */
.nav-active {
    background: linear-gradient(135deg, rgba(129,140,248,0.1), rgba(34,211,238,0.05)) !important;
    border: 1px solid rgba(129,140,248,0.15) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}

/* ── Namespace Stats ── */
.ns-stat-label {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.68rem;
    color: var(--text-light);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.25rem;
}

.ns-stat-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
}

.plan-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    background: linear-gradient(135deg, rgba(129,140,248,0.1), rgba(34,211,238,0.06));
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border: 1px solid rgba(129,140,248,0.15);
}

.ns-divider {
    margin-top: 1.25rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.ns-code {
    font-size: 0.72rem;
    color: var(--text-light);
    font-family: 'JetBrains Mono', monospace;
}

.ns-code span {
    background: rgba(255,255,255,0.04);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ── History Item ── */
.history-item {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px;
    margin-bottom: 0.75rem;
    overflow: hidden;
    transition: all 200ms ease;
}

.history-item:hover {
    box-shadow: var(--glass-shadow);
}

/* ── Hide Streamlit branding ── */
footer { visibility: hidden !important; }
footer:after { visibility: hidden !important; }

/* ── Smooth scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


#---------------------------------------------------------------------------------
#                                   Session State init
#---------------------------------------------------------------------------------

def init_session():
    defaults = {
        "access_token": None,
        "username": None,
        "user_id": None,
        "chat_history": [],
        "page": "chat",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


def get_client() -> APIClient:
    return APIClient(access_token=st.session_state.access_token)


#---------------------------------------------------------------------------------
#                                   Auth Page
#---------------------------------------------------------------------------------

def render_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.15, 1])

    with col2:
        # ── Centered Header ──
        st.markdown(f"""
            <div style='text-align:center; margin-bottom:2rem;'>
                <div class='logo-icon' style='margin-bottom:1rem;'>
                    <span>🧠</span>
                </div>
                <h1 style='font-size:1.5rem; font-weight:700; letter-spacing:-0.02em; color:var(--text); margin-bottom:0.25rem;'>
                    Doc<span style='color:var(--accent)'>Mind</span>
                </h1>
                <p style='color:var(--text-light); font-size:0.85rem;'>Your Private AI Knowledge Base</p>
            </div>
        """, unsafe_allow_html=True)

        # ── Glass Card with Tabs ──
        st.markdown("<div class='glass-strong' style='padding:2rem;'>", unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("<div style='padding: 0.5rem 0;''>", unsafe_allow_html=True)

            username = st.text_input(
                "Username",
                key="login_user",
                placeholder="your_username",
            )
            password = st.text_input(
                "Password",
                type="password",
                key="login_pass",
                placeholder="••••••••",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In", use_container_width=True, type="primary"):
                if username and password:
                    client = APIClient()
                    data, code = client.login(username, password)
                    if code == 200:
                        st.session_state.access_token = data['access_token']
                        me, _ = APIClient(data['access_token']).me()
                        st.session_state.username = me.get("username", username)
                        st.session_state.user_id = me.get("user_id", "")
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Login failed"))
                else:
                    st.warning("Please fill in all fields")

            st.markdown("</div>", unsafe_allow_html=True)

        with tab_register:
            st.markdown("<div style='padding: 0.5rem 0;''>", unsafe_allow_html=True)

            r_email = st.text_input(
                "Email",
                key="reg_email",
                placeholder="you@example.com",
            )
            r_username = st.text_input(
                "Username",
                key="reg_user",
                placeholder="choose_username",
            )
            r_password = st.text_input(
                "Password",
                key="reg_pass",
                type="password",
                placeholder="Min 8 characters",
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account", use_container_width=True, type="primary", key="reg_btn"):
                if r_email and r_username and r_password:
                    if len(r_password) < 8:
                        st.error("Password must be at least 8 characters")
                    else:
                        client = APIClient()
                        data, code = client.register(r_email, r_username, r_password)
                        if code == 201:
                            st.success("Account created! Please sign in.")
                        else:
                            st.error(data.get("detail", "Registration failed"))
                else:
                    st.warning("All fields are required")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <p style='text-align:center; font-size:0.72rem; color:var(--text-muted); margin-top:1.25rem;'>
                By continuing, you agree to our Terms of Service and Privacy Policy.
            </p>
        """, unsafe_allow_html=True)


#---------------------------------------------------------------------------------
#                                   Sidebar
#---------------------------------------------------------------------------------

def render_sidebar():
    with st.sidebar:
        # ── Logo ──
        st.markdown("""
            <div style='display:flex; align-items:center; gap:0.6rem; padding:0.5rem 0 0.75rem;'>
                <div class='logo-icon-sm'><span>🧠</span></div>
                <div class='logo'>Doc<span>Mind</span></div>
            </div>
        """, unsafe_allow_html=True)

        # ── User Badge ──
        initial = st.session_state.username[0].upper() if st.session_state.username else "U"
        st.markdown(f"""
            <div class='user-badge'>
                <div class='user-avatar'>{initial}</div>
                <div class='user-info'>
                    <div class='name'>{st.session_state.username}</div>
                    <div class='plan'>Pro Plan</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Navigation ──
        pages = {
            "💬 Chat": "chat",
            "📄 Documents": "documents",
            "📊 Dashboard": "dashboard",
            "📜 History": "history",
        }

        for label, key in pages.items():
            active = st.session_state.page == key
            btn_type = "primary" if active else "secondary"
            custom_class = "nav-active" if active else ""

            st.markdown(f"<div style='margin-bottom:0.25rem;'>", unsafe_allow_html=True)
            if st.button(label, use_container_width=True, key=f"nav_{key}", type=btn_type):
                st.session_state.page = key
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # ── Theme Toggle ──
        theme_icon = "☀️" if THEME == "dark" else "🌙"
        theme_label = "Switch to Dark" if THEME == "light" else "Switch to Light"
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True, key="theme_toggle"):
            toggle_theme()
            st.rerun()

        # ── Logout ──
        st.divider()
        if st.button("Sign Out", use_container_width=True, key="logout_btn"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


#---------------------------------------------------------------------------------
#                                   Documents Page
#---------------------------------------------------------------------------------

def render_documents():
    st.markdown("""
        <div class='page-header'>
            <div class='page-header-left'>
                <div class='page-header-icon'>📄</div>
                <div>
                    <h1 class='page-title'>Document Library</h1>
                    <div class='page-subtitle'>Upload and manage your knowledge base files</div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Get doc count for badge (we'll fetch after API call)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Upload Zone ──
    st.markdown("<div class='glass-strong upload-zone' style='margin-top:0.5rem;'>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your files here",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        st.markdown(f"<span style='font-size:0.82rem; color:var(--text-light); margin-top:0.5rem; display:block;'>📎 {len(uploaded)} file(s) selected</span>", unsafe_allow_html=True)

        if st.button(f"Upload {len(uploaded)} file(s)", use_container_width=True, type="primary"):
            client = get_client()
            for f in uploaded:
                with st.spinner(f"Uploading {f.name}..."):
                    data, code = client.upload_document(f.read(), f.name)
                if code == 202:
                    st.success(f"✔ {f.name} queued for processing")
                elif code == 429:
                    st.warning("Daily upload limit reached")
                    break
                else:
                    st.error(f"❌ {f.name}: {data.get('detail', 'Upload failed')}")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Document List ──
    client = get_client()
    docs, code = client.list_documents()

    if code != 200:
        st.error("Failed to load documents")
        return

    if not docs:
        st.markdown("""
            <div class='glass' style='text-align:center; padding:3rem 1.5rem;'>
                <div style='display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:18px; background:linear-gradient(135deg, rgba(79,70,229,0.1), rgba(6,182,212,0.08)); margin-bottom:1rem;'>
                    <span style='font-size:1.8rem;'>📄</span>
                </div>
                <h3 style='font-size:1.1rem; font-weight:600; margin-bottom:0.25rem;'>No documents yet</h3>
                <p style='color:var(--text-light); font-size:0.85rem;'>Upload your first file to get started</p>
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"<div style='font-size:0.88rem; font-weight:600; margin:1.25rem 0 0.75rem;'>{len(docs)} document(s) indexed</div>", unsafe_allow_html=True)

    for doc in docs:
        status = doc.get("status", "unknown")
        badge_cls = {
            "ready": "badge-ready",
            "processing": "badge-processing",
            "error": "badge-error",
        }.get(status, "badge-processing")

        file_type = doc.get("file_type", "")
        icon_map = {"pdf": "📑", "docx": "📄", "txt": "📃"}
        icon = icon_map.get(file_type, "📑")

        status_label = {"ready": "✔ Ready", "processing": "⏳ Processing", "error": "✖ Error"}.get(status, status)

        st.markdown(f"""
            <div class='doc-row glass'>
                <div class='doc-icon'>{icon}</div>
                <div style='flex:1; min-width:0;'>
                    <div style='font-size:0.88rem; font-weight:600; margin-bottom:0.25rem;'>{doc['filename']}</div>
                    <div style='display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;'>
                        <span class='badge {badge_cls}'>{status_label}</span>
                        <span style='color:var(--text-light); font-size:0.75rem; font-family:JetBrains Mono,monospace;'>{doc.get("chunk_count", 0)} chunks</span>
                        <span style='color:var(--text-muted); font-size:0.7rem; font-family:JetBrains Mono,monospace; text-transform:uppercase;'>.{file_type}</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        if st.button("🗑", key=f"del_{doc['doc_id']}", help="Delete Document"):
            code = client.delete_document(doc['doc_id'])
            if code == 204:
                st.success("Deleted")
                st.rerun()
            else:
                st.error("Delete failed")

        st.markdown("</div>", unsafe_allow_html=True)


#---------------------------------------------------------------------------------
#                                   Dashboard Page
#---------------------------------------------------------------------------------

def render_dashboard():
    st.markdown("""
        <div class='page-header'>
            <div class='page-header-left'>
                <div class='page-header-icon'>📊</div>
                <div>
                    <h1 class='page-title'>Knowledge Overview</h1>
                    <div class='page-subtitle'>Monitor your document intelligence and performance</div>
                </div>
            </div>
            <div class='system-badge'>
                <span style='color:var(--accent);'>⚡</span> All systems operational
            </div>
        </div>
    """, unsafe_allow_html=True)

    client = get_client()
    stats, s_code = client.get_stats()
    ns_stats, n_code = client.get_namespace_stats()

    # ── Metric Tiles ──
    if s_code == 200:
        st.markdown(f"""
            <div class='metric-row'>
                <div class='metric-tile'>
                    <div class='metric-icon metric-icon-indigo'>📄</div>
                    <div class='metric-value'>{stats.get('document_count', 0)}</div>
                    <div class='metric-label'>Documents</div>
                </div>
                <div class='metric-tile'>
                    <div class='metric-icon metric-icon-cyan'>💬</div>
                    <div class='metric-value'>{stats.get('queries_today', 0)}</div>
                    <div class='metric-label'>Queries Today</div>
                </div>
                <div class='metric-tile'>
                    <div class='metric-icon metric-icon-violet'>📈</div>
                    <div class='metric-value'>{stats.get('total_queries', 0)}</div>
                    <div class='metric-label'>Total Queries</div>
                </div>
                <div class='metric-tile'>
                    <div class='metric-icon metric-icon-amber'>📤</div>
                    <div class='metric-value'>{stats.get('total_uploads', 0)}</div>
                    <div class='metric-label'>Total Uploads</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── Namespace + Activity ──
    if n_code == 200:
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown("<div class='glass-strong'>", unsafe_allow_html=True)

            st.markdown("""
                <div style='display:flex; align-items:center; gap:0.6rem; margin-bottom:1.25rem;'>
                    <div class='logo-icon-xs'>🗄️</div>
                    <div>
                        <div style='font-size:0.95rem; font-weight:600;'>Pinecone Namespace</div>
                        <div style='font-size:0.75rem; color:var(--text-light);'>Vector database status</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div>
                        <div class='ns-stat-label'>🗄 VECTORS</div>
                        <div class='ns-stat-value'>{ns_stats.get("vector_count", 0):,}</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div>
                        <div class='ns-stat-label'>⏱ QUOTA</div>
                        <div class='ns-stat-value'>{ns_stats.get("queries_remaining_this_minute", "?")}</div>
                        <div style='font-size:0.68rem; color:var(--text-muted);'>queries/minute</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div>
                        <div class='ns-stat-label'>🛡 PLAN</div>
                        <div class='plan-badge'>{ns_stats.get("plan", "free").upper()}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class='ns-divider'>
                    <span class='ns-code'>Namespace: <span>{ns_stats.get('namespace', '')}</span></span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='glass-strong'>", unsafe_allow_html=True)

            st.markdown("""
                <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;'>
                    <span style='color:var(--accent);'>📈</span>
                    <span style='font-size:0.95rem; font-weight:600;'>Recent Activity</span>
                </div>
            """, unsafe_allow_html=True)

            activities = [
                ("📤", "Document uploaded", "Annual_Report_2024.pdf", "2h ago"),
                ("💬", "Query completed", '"What are the key findings?"', "1h ago"),
                ("📄", "Document processed", "Product_Specs.docx — 23 chunks", "3h ago"),
                ("💬", "Query completed", '"Summarize the specs"', "4h ago"),
            ]

            for icon, action, detail, time in activities:
                st.markdown(f"""
                    <div class='activity-item'>
                        <div class='activity-icon'>{icon}</div>
                        <div style='flex:1; min-width:0;'>
                            <div style='font-size:0.82rem; font-weight:500;'>{action}</div>
                            <div style='font-size:0.72rem; color:var(--text-light); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>{detail}</div>
                        </div>
                        <div class='activity-time'>{time}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


#---------------------------------------------------------------------------------
#                                   Chat Page
#---------------------------------------------------------------------------------

def render_chat():
    st.markdown("""
        <div class='page-header'>
            <div class='page-header-left'>
                <div class='page-header-icon'>💬</div>
                <div>
                    <h1 class='page-title'>Ask Your Documents</h1>
                    <div class='page-subtitle'>Natural language queries across your entire knowledge base</div>
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🗑 Clear", key="clear_chat_btn"):
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Settings ──
    with st.expander("⚙ Generation Settings", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            top_k = st.slider("Retrieved Chunks (top_k)", 1, 10, 5)
        with col_b:
            temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.3, 0.05)

    # ── Chat Messages ──
    if not st.session_state.chat_history:
        st.markdown("""
            <div class='glass' style='text-align:center; padding:3rem 1.5rem; margin-top:0.5rem;'>
                <div style='display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:18px; background:linear-gradient(135deg, #4F46E5, #06B6D4); box-shadow:0 8px 24px rgba(79,70,229,0.2); margin-bottom:1rem;'>
                    <span style='font-size:1.8rem;'>🧠</span>
                </div>
                <h3 style='font-size:1.15rem; font-weight:700; margin-bottom:0.4rem;'>Ask your documents anything</h3>
                <p style='color:var(--text-light); font-size:0.85rem; max-width:380px; margin:0 auto 1rem; line-height:1.5;'>
                    Upload files in the <span style='color:var(--accent); font-weight:500;'>Documents</span> section, then ask questions in natural language.
                </p>
                <div class='suggestion-grid'>
                    <div class='suggestion-card'>✨ Summarize the key findings</div>
                    <div class='suggestion-card'>✨ What are the main topics?</div>
                    <div class='suggestion-card'>✨ Compare the two reports</div>
                    <div class='suggestion-card'>✨ Extract key metrics</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg['role'] == "user":
                st.markdown(f"""
                    <div class='chat-user'>
                        <div class='bubble'>{msg['content']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                sources_html = "".join(
                    f'<span class="source-chip">📄 {s}</span>'
                    for s in msg.get("meta", {}).get("sources", [])
                )
                meta = msg.get("meta", {})

                st.markdown(f"""
                    <div class='chat-ai'>
                        <div>
                            <div class='bubble'>{msg['content']}</div>
                            <div class='chat-meta'>
                                <span>⚡ {meta.get('latency_ms', '?')}ms</span>
                                <span>🔢 {meta.get('tokens_used', '?')} tokens</span>
                                {sources_html}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ── Input ──
    st.divider()

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            key="chat_input",
            placeholder="Ask about your documents...",
            label_visibility="collapsed",
        )
    with col_btn:
        send = st.button("Send", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
        })

        with st.spinner("Analyzing your documents..."):
            client = get_client()
            tk = top_k if 'top_k' in dir() else 5
            temp = temperature if 'temperature' in dir() else 0.3
            data, code = client.query(user_input, top_k=tk, temperature=temp)

        if code == 200:
            st.session_state.chat_history.append({
                "role": "ai",
                "content": data['answer'],
                "meta": {
                    "sources": data.get("sources", []),
                    "latency_ms": data.get("latency_ms", 0),
                    "tokens_used": data.get("tokens_used", 0),
                },
            })
        elif code == 429:
            st.warning(data.get("detail", "Rate limit hit. Please wait."))
        else:
            st.error(data.get("detail", "Query failed"))

        st.rerun()


#---------------------------------------------------------------------------------
#                                   History Page
#---------------------------------------------------------------------------------

def render_history():
    st.markdown("""
        <div class='page-header'>
            <div class='page-header-left'>
                <div class='page-header-icon'>📜</div>
                <div>
                    <h1 class='page-title'>Query History</h1>
                    <div class='page-subtitle'>Review your past conversations and answers</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    client = get_client()
    history, code = client.qurey_history(limit=50)

    if code != 200:
        st.error("Failed to load history")
        return

    if not history:
        st.markdown("""
            <div class='glass' style='text-align:center; padding:3rem 1.5rem;'>
                <div style='display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:18px; background:linear-gradient(135deg, rgba(79,70,229,0.1), rgba(6,182,212,0.08)); margin-bottom:1rem;'>
                    <span style='font-size:1.8rem;'>📜</span>
                </div>
                <h3 style='font-size:1.1rem; font-weight:600; margin-bottom:0.25rem;'>No query history yet</h3>
                <p style='color:var(--text-light); font-size:0.85rem;'>Start chatting to see your history here</p>
            </div>
        """, unsafe_allow_html=True)
        return

    for item in history:
        with st.expander(f"🔬 {item['query'][:80]}{'...' if len(item['query']) > 80 else ''}", expanded=False):
            st.markdown(f"**Answer:** {item['answer']}")

            if item.get("sources"):
                sources_html = "".join(
                    f'<span class="source-chip">📄 {s}</span>' for s in item['sources']
                )
                st.markdown(f"<div style='margin-top:0.75rem;'>**Sources:** {sources_html}</div>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div style='margin-top:0.75rem; display:flex; align-items:center; gap:0.75rem; flex-wrap:wrap;'>
                    <span style='font-size:0.72rem; color:var(--text-light); font-family:JetBrains Mono,monospace;'>⚡ {item['latency_ms']}ms</span>
                    <span style='font-size:0.72rem; color:var(--text-light); font-family:JetBrains Mono,monospace;'>🔢 {item['token_used']} tokens</span>
                    <span style='font-size:0.72rem; color:var(--text-light); font-family:JetBrains Mono,monospace;'>🕐 {item['created_at'][:16].replace('T', ' ')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


#---------------------------------------------------------------------------------
#                                   App Router
#---------------------------------------------------------------------------------

def main():
    if not st.session_state.access_token:
        render_login()
    else:
        render_sidebar()
        page = st.session_state.page
        if page == "documents":
            render_documents()
        elif page == "dashboard":
            render_dashboard()
        elif page == "chat":
            render_chat()
        elif page == "history":
            render_history()


if __name__ == "__main__":
    main()
