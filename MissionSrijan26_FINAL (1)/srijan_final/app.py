import streamlit as st
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Tester Agent — Mission Srijan 26", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# ── Theme Toggle ───────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

DARK = {
    "bg": "#0a0f1e", "sidebar": "#0d1426", "card": "#111827",
    "text": "#f1f5f9", "subtext": "#94a3b8", "border": "#1e2d45",
    "accent": "#0ea5e9", "green": "#10b981", "red": "#f43f5e",
    "yellow": "#f59e0b", "code_bg": "#080d18",
    "hover": "rgba(255,255,255,0.04)", "shadow": "rgba(14,165,233,0.15)",
    "btn_bg": "#0ea5e9", "btn_text": "#ffffff", "btn_border": "#0ea5e9", "btn_hover": "#0284c7",
    "banner_bg": "#0d1426",
    "info_bg": "rgba(14,165,233,0.06)", "info_border": "rgba(14,165,233,0.2)",
    "tag_cyan_bg": "rgba(14,165,233,0.08)", "tag_cyan_border": "rgba(14,165,233,0.25)",
    "tag_red_bg": "rgba(244,63,94,0.08)", "tag_red_border": "rgba(244,63,94,0.25)",
    "tag_green_bg": "rgba(16,185,129,0.08)", "tag_green_border": "rgba(16,185,129,0.25)",
    "tag_yellow_bg": "rgba(245,158,11,0.08)", "tag_yellow_border": "rgba(245,158,11,0.25)",
    "tag_purple_bg": "rgba(129,140,248,0.08)",
}
LIGHT = {
    "bg": "#f8fafc", "sidebar": "#ffffff", "card": "#ffffff",
    "text": "#0f172a", "subtext": "#64748b", "border": "#e2e8f0",
    "accent": "#0284c7", "green": "#059669", "red": "#e11d48",
    "yellow": "#d97706", "code_bg": "#f1f5f9",
    "hover": "rgba(0,0,0,0.04)", "shadow": "rgba(2,132,199,0.12)",
    "btn_bg": "#0284c7", "btn_text": "#ffffff", "btn_border": "#0284c7", "btn_hover": "#0369a1",
    "banner_bg": "#f0f9ff",
    "info_bg": "rgba(2,132,199,0.05)", "info_border": "rgba(2,132,199,0.2)",
    "tag_cyan_bg": "rgba(2,132,199,0.08)", "tag_cyan_border": "rgba(2,132,199,0.25)",
    "tag_red_bg": "rgba(225,29,72,0.08)", "tag_red_border": "rgba(225,29,72,0.25)",
    "tag_green_bg": "rgba(5,150,105,0.08)", "tag_green_border": "rgba(5,150,105,0.25)",
    "tag_yellow_bg": "rgba(217,119,6,0.08)", "tag_yellow_border": "rgba(217,119,6,0.25)",
    "tag_purple_bg": "rgba(129,140,248,0.08)",
}
T = DARK if st.session_state.dark_mode else LIGHT

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
*, *::before, *::after {{ font-family: 'DM Sans', sans-serif !important; }}
code, pre, .mono {{ font-family: 'DM Mono', monospace !important; }}

/* ── Base ── */
.stApp {{ background: {T['bg']} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: {T['sidebar']} !important;
    border-right: 1px solid {T['border']} !important;
    width: 240px !important;
}}
section[data-testid="stSidebar"] > div {{
    background: {T['sidebar']} !important;
}}

/* ── Radio nav ── */
[data-testid="stSidebar"] .stRadio > div {{
    gap: 2px !important;
    background: transparent !important;
}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
    background: transparent !important;
}}
[data-testid="stSidebar"] .stRadio label {{
    background: transparent !important;
    color: {T['subtext']} !important;
    padding: 9px 14px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    border: none !important;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: {T['hover']} !important;
    color: {T['text']} !important;
}}
[data-testid="stSidebar"] .stRadio label[data-baseweb] {{
    background: transparent !important;
}}

/* ── Cards ── */
.corp-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    padding: 20px 24px;
    margin: 8px 0;
    transition: box-shadow 0.2s;
}}
.corp-card:hover {{
    box-shadow: 0 2px 12px {T['shadow']};
}}

/* ── Metric ── */
.metric-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.2s;
}}
.metric-card:hover {{
    border-color: {T['accent']};
    box-shadow: 0 2px 12px {T['shadow']};
}}
.metric-number {{ font-size: 32px; font-weight: 700; margin: 0; letter-spacing: -1px; }}
.metric-label {{ font-size: 11px; color: {T['subtext']}; margin: 6px 0 0; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; }}

/* ── Section heading ── */
.sec-head {{
    font-size: 11px;
    font-weight: 600;
    color: {T['subtext']};
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 20px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid {T['border']};
}}

/* ── Status badge ── */
.status-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    color: {T['text']};
    margin: 3px 0;
}}
.status-row:hover {{ background: {T['hover']}; }}

/* ── Story card ── */
.story-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-left: 3px solid {T['accent']};
    border-radius: 8px;
    padding: 14px 16px;
    margin: 8px 0;
    transition: all 0.2s;
}}
.story-card:hover {{
    border-left-color: {T['accent']};
    box-shadow: 0 2px 8px {T['shadow']};
}}

/* ── BDD box ── */
.bdd-box {{
    background: {T['code_bg']};
    border-radius: 6px;
    padding: 12px;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px;
    line-height: 1.9;
    margin-top: 10px;
    border: 1px solid {T['border']};
}}
.given {{ color: #818cf8; }}
.when  {{ color: #38bdf8; }}
.then  {{ color: #34d399; }}

/* ── Test card ── */
.test-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0;
    transition: all 0.2s;
}}

/* ── Tags ── */
.tag {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.3px;
}}
.tag-cyan   {{ background: {T['tag_cyan_bg']};   color: {T['accent']};  border: 1px solid {T['tag_cyan_border']}; }}
.tag-red    {{ background: {T['tag_red_bg']};    color: {T['red']};     border: 1px solid {T['tag_red_border']}; }}
.tag-green  {{ background: {T['tag_green_bg']};  color: {T['green']};   border: 1px solid {T['tag_green_border']}; }}
.tag-yellow {{ background: {T['tag_yellow_bg']}; color: {T['yellow']};  border: 1px solid {T['tag_yellow_border']}; }}
.tag-purple {{ background: {T['tag_purple_bg']}; color: #818cf8;        border: 1px solid rgba(129,140,248,0.3); }}

/* ── HITL panel ── */
.hitl-panel {{
    background: {T['card']};
    border: 1px solid {T['red']};
    border-left: 4px solid {T['red']};
    border-radius: 10px;
    padding: 18px 20px;
    margin: 12px 0;
}}

/* ── Info box ── */
.info-box {{
    background: {T['info_bg']};
    border: 1px solid {T['info_border']};
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 12px;
    color: {T['subtext']};
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* ── RAG card ── */
.rag-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-left: 3px solid #818cf8;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    transition: all 0.2s;
}}
.rag-card:hover {{ box-shadow: 0 2px 8px {T['shadow']}; }}

/* ── Buttons ── */
.stButton > button {{
    background: {T['btn_bg']} !important;
    color: {T['btn_text']} !important;
    border: 1px solid {T['btn_border']} !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.15s !important;
    letter-spacing: 0.2px !important;
}}
.stButton > button:hover {{
    background: {T['btn_hover']} !important;
    border-color: {T['accent']} !important;
    box-shadow: 0 2px 8px {T['shadow']} !important;
}}

/* ── Progress ── */
.stProgress > div > div {{
    background: linear-gradient(90deg, {T['accent']}, {T['green']}) !important;
    border-radius: 4px !important;
}}

/* ── Selectbox Dropdown Fix ── */
div[data-baseweb="popover"] {{
    background: {T['card']} !important;
    border: 1px solid {T['accent']} !important;
    border-radius: 8px !important;
}}
div[data-baseweb="popover"] ul {{
    background: {T['card']} !important;
    padding: 4px !important;
}}
div[data-baseweb="popover"] li {{
    background: {T['card']} !important;
    color: {T['text']} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
}}
div[data-baseweb="popover"] li:hover {{
    background: {T['accent']} !important;
    color: #ffffff !important;
}}
div[data-baseweb="select"] span {{
    color: {T['text']} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}}
div[data-baseweb="select"] > div {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
}}
div[data-baseweb="select"] > div:focus-within {{
    border-color: {T['accent']} !important;
}}
/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 2px {T['shadow']} !important;
}}
.stSelectbox > div > div {{
    background: {T['card']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 8px !important;
}}

/* ── Report box ── */
.report-box {{
    background: {T['code_bg']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    padding: 18px;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px;
    color: {T['subtext']};
    line-height: 1.9;
}}

/* ── Banner ── */
.top-banner {{
    background: {T['banner_bg']};
    border: 1px solid {T['border']};
    border-top: 3px solid {T['accent']};
    border-radius: 10px;
    padding: 22px 28px;
    margin-bottom: 24px;
}}

/* ── Pipeline ── */
.pipe-node {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    padding: 14px 10px;
    text-align: center;
    flex: 1;
    transition: all 0.2s;
}}
.pipe-node:hover {{
    border-color: {T['accent']};
    transform: translateY(-2px);
    box-shadow: 0 4px 12px {T['shadow']};
}}

/* ── Alerts ── */
.stAlert {{ background: {T['card']} !important; border-radius: 8px !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T['border']}; border-radius: 2px; }}

/* ── General text ── */
.stMarkdown p {{ color: {T['text']}; }}
label {{ color: {T['subtext']} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────
for k, v in {"test_cases":[], "generated":False, "executed":False, "selected_story":None, "hitl_decisions":{}}.items():
    if k not in st.session_state:
        st.session_state[k] = v

api_key = os.getenv("GROQ_API_KEY", "")
api_ok = bool(api_key)

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:20px 16px 12px;'>
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>
            <div style='width:32px;height:32px;background:{T["accent"]};border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;'>🤖</div>
            <div>
                <div style='font-size:13px;font-weight:700;color:{T["text"]};'>AI Tester Agent</div>
                <div style='font-size:10px;color:{T["subtext"]};'>Mission Srijan 26</div>
            </div>
        </div>
    </div>
    <div style='height:1px;background:{T["border"]};margin:0 16px 8px;'></div>
    """, unsafe_allow_html=True)

    # Theme Toggle
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🌙", use_container_width=True):
            st.session_state.dark_mode = True
            st.rerun()
    with col_b:
        if st.button("☀️", use_container_width=True):
            st.session_state.dark_mode = False
            st.rerun()

    st.markdown(f"<div style='height:1px;background:{T['border']};margin:8px 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding:4px 16px 6px;font-size:10px;font-weight:600;color:{T['subtext']};text-transform:uppercase;letter-spacing:1px;'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("Nav", ["🏠 Dashboard","📋 Jira Stories","🤖 AI Test Generator","▶️ Test Executor","👤 HITL Review","🧠 RAG Memory","📊 Reports"], label_visibility="collapsed")
    st.markdown(f"<div style='height:1px;background:{T['border']};margin:8px 0;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding:4px 16px 6px;font-size:10px;font-weight:600;color:{T['subtext']};text-transform:uppercase;letter-spacing:1px;'>System Status</div>", unsafe_allow_html=True)
    api_dot = "🟢" if api_ok else "🔴"
    statuses = [
        (api_dot, "Gemini API", T['green'] if api_ok else T['red']),
        ("🟢", "LangChain", T['green']),
        ("🟢", "ChromaDB RAG", T['green']),
        ("🟢", "Playwright", T['green']),
        ("🟢", "Jira REST API", T['green']),
    ]
    for dot, label, color in statuses:
        st.markdown(f"""<div class='status-row'>
            <span style='font-size:8px;color:{color};'>●</span>
            <span style='font-size:12px;color:{T['text']};'>{label}</span>
        </div>""", unsafe_allow_html=True)

# ── BANNER ─────────────────────────────────────────────────
st.markdown(f"""<div class="top-banner">
<div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>
    <div>
        <div style='display:inline-flex;align-items:center;gap:6px;background:{T["info_bg"]};border:1px solid {T["info_border"]};color:{T["accent"]};padding:4px 12px;border-radius:6px;font-size:10px;font-weight:600;letter-spacing:1px;margin-bottom:10px;'>
            <span>●</span> SRIJAN 2026 — ATOS GLOBAL &nbsp;·&nbsp; AI-Agent Driven, Context-Aware Release Testing
        </div>
        <div style='font-size:22px;font-weight:700;color:{T["text"]};margin-bottom:6px;letter-spacing:-0.3px;'>AI-Agent Driven, Context-Aware Release Testing</div>
        <div style='display:flex;gap:8px;flex-wrap:wrap;'>
            <span style='font-size:11px;color:{T["subtext"]};background:{T["hover"]};padding:3px 10px;border-radius:4px;'>Gemini AI</span>
            <span style='font-size:11px;color:{T["subtext"]};'>·</span>
            <span style='font-size:11px;color:{T["subtext"]};background:{T["hover"]};padding:3px 10px;border-radius:4px;'>LangChain</span>
            <span style='font-size:11px;color:{T["subtext"]};'>·</span>
            <span style='font-size:11px;color:{T["subtext"]};background:{T["hover"]};padding:3px 10px;border-radius:4px;'>ChromaDB RAG</span>
            <span style='font-size:11px;color:{T["subtext"]};'>·</span>
            <span style='font-size:11px;color:{T["subtext"]};background:{T["hover"]};padding:3px 10px;border-radius:4px;'>Playwright</span>
            <span style='font-size:11px;color:{T["subtext"]};'>·</span>
            <span style='font-size:11px;color:{T["subtext"]};background:{T["hover"]};padding:3px 10px;border-radius:4px;'>HITL Governance</span>
        </div>
    </div>
</div>
</div>""", unsafe_allow_html=True)

if not api_ok:
    st.error("⚠️ Please set GROQ_API_KEY in CMD: set GROQ_API_KEY=your_key")
    st.code("set GROQ_API_KEY=gsk_...", language="bash")
    st.stop()

# ══════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════
if "Dashboard" in page:
    from agent import get_stories, seed_defects, PAST_DEFECTS, get_defect_count
    stories = get_stories()

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['accent']};">{len(stories)}</p><p class="metric-label">User Stories</p></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['green']};">{len(st.session_state.test_cases)}</p><p class="metric-label">Tests Generated</p></div>""", unsafe_allow_html=True)
    with c3:
        hp = len([t for t in st.session_state.test_cases if t.get("result")=="hitl"])
        st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['yellow']};">{hp}</p><p class="metric-label">HITL Pending</p></div>""", unsafe_allow_html=True)
    with c4:
        fp = len([t for t in st.session_state.test_cases if t.get("result")=="fail"])
        st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['red']};">{fp}</p><p class="metric-label">Defects Found</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cl, cr = st.columns([3,2])
    with cl:
        st.markdown('<p class="sec-head">Pipeline Flow</p>', unsafe_allow_html=True)
        st.markdown(f"""<div style='display:flex;align-items:center;gap:4px;'>
            <div style='background:{T['card']};border:1px solid #10b981;border-radius:8px;padding:12px;text-align:center;flex:1;'><div style='font-size:20px;'>📋</div><div style='font-size:9px;color:#10b981;font-weight:700;margin-top:4px;'>JIRA</div></div>
            <div style='color:{T['border']};font-size:16px;'>→</div>
            <div style='background:{T['card']};border:1px solid #7c3aed;border-radius:8px;padding:12px;text-align:center;flex:1;'><div style='font-size:20px;'>🧠</div><div style='font-size:9px;color:#a78bfa;font-weight:700;margin-top:4px;'>GEMINI</div></div>
            <div style='color:{T['border']};font-size:16px;'>→</div>
            <div style='background:{T['card']};border:1px solid #d97706;border-radius:8px;padding:12px;text-align:center;flex:1;'><div style='font-size:20px;'>🗄️</div><div style='font-size:9px;color:#f59e0b;font-weight:700;margin-top:4px;'>CHROMADB</div></div>
            <div style='color:{T['border']};font-size:16px;'>→</div>
            <div style='background:{T['card']};border:1px solid #059669;border-radius:8px;padding:12px;text-align:center;flex:1;'><div style='font-size:20px;'>▶️</div><div style='font-size:9px;color:#34d399;font-weight:700;margin-top:4px;'>PLAYWRIGHT</div></div>
            <div style='color:{T['border']};font-size:16px;'>→</div>
            <div style='background:{T['card']};border:1px solid {T['red']};border-radius:8px;padding:12px;text-align:center;flex:1;'><div style='font-size:20px;'>📊</div><div style='font-size:9px;color:{T['red']};font-weight:700;margin-top:4px;'>REPORTS</div></div>
        </div>
        <div style='margin-top:8px;padding:8px 14px;background:rgba(239,68,68,0.05);border:1px dashed rgba(239,68,68,0.2);border-radius:6px;font-size:10px;color:{T['red']};text-align:center;'>← HITL Loop: Low-confidence tests → Human Review →</div>""", unsafe_allow_html=True)
    with cr:
        st.markdown(f'<p class="sec-head">🧠 RAG Memory ({get_defect_count()} defects)</p>', unsafe_allow_html=True)
        for d in PAST_DEFECTS[:4]:
            sc = T['red'] if d["severity"]=="Critical" else T['yellow'] if d["severity"]=="High" else T['accent']
            st.markdown(f"""<div class='rag-card'><div style='font-size:10px;color:#a78bfa;font-weight:600;font-family:JetBrains Mono,monospace;'>{d['id']} · {d['sprint']} · <span style='color:{sc};'>{d['severity']}</span></div><div style='font-size:11px;color:{T['subtext']};margin-top:3px;'>{d['title']}</div></div>""", unsafe_allow_html=True)

    # Tech Stack
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sec-head">Tech Stack</p>', unsafe_allow_html=True)
    techs = [("🐍","Python 3.11","Core Language"),("🦜","LangChain","AI Orchestration"),("✨","Gemini API","LLM Engine"),("🗄️","ChromaDB","Vector DB / RAG"),("🎭","Playwright","Test Execution"),("📋","Jira REST API","Story Ingestion"),("🌐","Streamlit","Dashboard UI")]
    cols = st.columns(len(techs))
    for i,(icon,name,desc) in enumerate(techs):
        with cols[i]:
            st.markdown(f"""<div style='background:{T['card']};border:1px solid {T['border']};border-radius:8px;padding:10px;text-align:center;'><div style='font-size:22px;'>{icon}</div><div style='font-size:10px;font-weight:700;color:{T['accent']};margin-top:4px;'>{name}</div><div style='font-size:9px;color:{T['subtext']};margin-top:2px;'>{desc}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# JIRA STORIES
# ══════════════════════════════════════════════════
elif "Jira" in page:
    from agent import get_stories
    st.markdown('<p class="sec-head">📋 Jira REST API (Live) — Sprint 14 User Stories</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">🟢 Jira REST API (Connected) · anki8pandey.atlassian.net · Sprint 14 · Live stories loaded</div>', unsafe_allow_html=True)
    for s in get_stories():
        pc = T['red'] if s["priority"]=="Critical" else T['yellow'] if s["priority"]=="High" else T['accent']
        st.markdown(f"""<div class="story-card"><div style='font-size:10px;color:{T['accent']};font-family:JetBrains Mono,monospace;'>{s['id']} · {s['sprint']} · {s['component']}</div><div style='font-size:13px;font-weight:600;color:{T['text']};margin:5px 0;'>{s['title']}</div><div style='font-size:11px;color:{T['subtext']};'>{s['description']}</div><div style='margin-top:8px;display:flex;gap:6px;'><span style='background:rgba(8,145,178,0.1);border:1px solid rgba(8,145,178,0.2);color:{T['accent']};padding:2px 10px;border-radius:20px;font-size:9px;'>{s['component']}</span><span style='background:rgba(0,0,0,0.1);border:1px solid {pc}44;color:{pc};padding:2px 10px;border-radius:20px;font-size:9px;'>{s['priority']}</span></div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# AI TEST GENERATOR
# ══════════════════════════════════════════════════
elif "Generator" in page:
    from agent import get_stories, search_related_defects, generate_test_cases_with_ai
    st.markdown('<p class="sec-head">🤖 AI Test Generator — Gemini AI + LangChain + ChromaDB RAG</p>', unsafe_allow_html=True)
    stories = get_stories()
    smap = {f"{s['id']} — {s['title']}": s for s in stories}
    cl, cr = st.columns([2,3])
    with cl:
        sel_key = st.selectbox("Story", list(smap.keys()), label_visibility="collapsed")
        sel = smap[sel_key]
        st.markdown(f"""<div class="story-card"><div style='font-size:10px;color:{T['accent']};font-family:JetBrains Mono,monospace;'>{sel['id']} · {sel['component']}</div><div style='font-size:13px;font-weight:600;color:{T['text']};margin:5px 0;'>{sel['title']}</div><div style='font-size:11px;color:{T['subtext']};'>{sel['description']}</div></div>""", unsafe_allow_html=True)
        related = search_related_defects(sel['description'], sel['component'])
        if related:
            st.markdown(f"**🧠 RAG: Related Defects Found:**")
            for d in related:
                sc = T['red'] if d["severity"]=="Critical" else T['yellow']
                st.markdown(f"""<div class='rag-card'><div style='font-size:10px;color:#a78bfa;font-weight:600;font-family:JetBrains Mono,monospace;'>{d['id']} · {d['sprint']} · <span style='color:{sc};'>{d['severity']}</span></div><div style='font-size:11px;color:{T['subtext']};margin-top:3px;'>{d['title']}</div></div>""", unsafe_allow_html=True)
        if st.button("🤖 Generate with Gemini AI + LangChain", use_container_width=True):
            prog = st.progress(0, text="Reading Jira story...")
            time.sleep(0.3)
            prog.progress(25, text="LangChain orchestrating prompt...")
            time.sleep(0.3)
            prog.progress(50, text="Querying ChromaDB RAG...")
            rd = search_related_defects(sel['description'], sel['component'])
            time.sleep(0.3)
            prog.progress(75, text="Gemini generating BDD tests...")
            tcs = generate_test_cases_with_ai(sel, rd)
            prog.progress(100, text="Done!")
            st.session_state.selected_story = sel
            st.session_state.test_cases = tcs
            st.session_state.generated = True
            st.session_state.executed = False
            st.success(f"✅ {len(tcs)} tests generated by Gemini AI + LangChain!")
    with cr:
        if st.session_state.generated:
            st.markdown(f"**{len(st.session_state.test_cases)} Test Cases — {st.session_state.selected_story['id']}**")
            for tc in st.session_state.test_cases:
                conf = tc.get("confidence", 0)
                cc = T['green'] if conf>=80 else T['yellow'] if conf>=60 else T['red']
                ih = conf < 75
                st.markdown(f"""<div class="test-card" style="border-color:{'#ef4444' if ih else T['border']};"><div style='display:flex;justify-content:space-between;'><div><div style='font-size:9px;color:{T['subtext']};font-family:JetBrains Mono,monospace;'>{tc.get('id','TC')} · {tc.get('type','test')}</div><div style='font-size:13px;font-weight:600;color:{T['text']};margin:3px 0;'>{tc.get('name','')}</div></div><div style='color:{cc};font-size:11px;font-weight:700;font-family:JetBrains Mono,monospace;'>CONF: {conf}%</div></div><div class="bdd-box"><div class="given">GIVEN  {tc.get('given','')}</div><div class="when">WHEN   {tc.get('when','')}</div><div class="then">THEN   {tc.get('then','')}</div></div><div>{'<span class="hitl-tag">⚠️ HITL Required — Low Confidence</span>' if ih else f'<span class="why-tag">💡 {tc.get("why","")}</span>'}</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='text-align:center;padding:60px 20px;color:{T['subtext']};'><div style='font-size:48px;'>🤖</div><div style='font-size:15px;font-weight:600;margin-top:12px;'>Select a story and click Generate</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TEST EXECUTOR
# ══════════════════════════════════════════════════
elif "Executor" in page:
    st.markdown('<p class="sec-head">▶️ Playwright Test Executor</p>', unsafe_allow_html=True)
    if not st.session_state.generated:
        st.warning("⚠️ Please generate tests from AI Generator first!")
    else:
        from agent import run_playwright_tests
        cases = st.session_state.test_cases
        runnable = [t for t in cases if t.get("result") != "hitl" and t.get("confidence",0) >= 75]
        hitl_c = [t for t in cases if t.get("confidence",0) < 75]
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['accent']};">{len(cases)}</p><p class="metric-label">Total</p></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['green']};">{len(runnable)}</p><p class="metric-label">Auto Run</p></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['yellow']};">{len(hitl_c)}</p><p class="metric-label">HITL</p></div>""", unsafe_allow_html=True)
        if hitl_c:
            st.markdown(f"""<div class='hitl-panel'><div class='hitl-title'>⚠️ {len(hitl_c)} test(s) → HITL Review</div>{"".join([f"<div style='font-size:11px;color:{T['yellow']};margin:4px 0;'>• {t.get('id')}: {t.get('name')} ({t.get('confidence')}%)</div>" for t in hitl_c])}<div style='font-size:10px;color:{T['subtext']};margin-top:6px;'>→ Review and approve/reject in HITL Review tab</div></div>""", unsafe_allow_html=True)
        if st.button("▶️ Run All Tests with Playwright", use_container_width=True):
            prog = st.progress(0, text="Launching Playwright browser...")
            sb = st.empty()
            for i, tc in enumerate(runnable):
                prog.progress(int(i/max(len(runnable),1)*85), text=f"Running {tc.get('id')}: {tc.get('name','')[:35]}...")
                sb.markdown(f"""<div style='background:{T['code_bg']};border:1px solid {T['border']};border-radius:6px;padding:8px 12px;font-family:JetBrains Mono,monospace;font-size:11px;color:{T['subtext']};'>⚡ {tc.get('name','')}</div>""", unsafe_allow_html=True)
                time.sleep(0.3)
            results = run_playwright_tests(runnable)
            prog.progress(100, text="Complete!")
            sb.empty()
            rm = {t["id"]: t for t in results}
            st.session_state.test_cases = [rm.get(t["id"], t) for t in st.session_state.test_cases]
            st.session_state.executed = True
            st.success("✅ Playwright execution complete!")
        if st.session_state.executed:
            st.markdown('<p class="sec-head">Results</p>', unsafe_allow_html=True)
            for tc in st.session_state.test_cases:
                r = tc.get("result","pending")
                badge = f'<span class="badge-pass">✓ PASS</span>' if r=="pass" else f'<span class="badge-fail">✗ FAIL</span>' if r=="fail" else f'<span class="badge-hitl">⏳ HITL</span>'
                st.markdown(f"""<div style='background:{T['card']};border:1px solid {T['border']};border-radius:8px;padding:12px 16px;margin:5px 0;display:flex;justify-content:space-between;align-items:center;'><div><span style='font-family:JetBrains Mono,monospace;font-size:9px;color:{T['subtext']};'>{tc.get('id')}</span><span style='font-size:13px;color:{T['text']};font-weight:500;margin-left:10px;'>{tc.get('name','')}</span></div><div style='display:flex;align-items:center;gap:10px;'><span style='font-size:11px;color:{T['subtext']};'>{tc.get('duration','-')}</span>{badge}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# HITL REVIEW
# ══════════════════════════════════════════════════
elif "HITL" in page:
    st.markdown('<p class="sec-head">👤 Human-in-the-Loop Review Panel</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">🔒 Low confidence tests — Human expert review required before execution.</div>', unsafe_allow_html=True)
    if not st.session_state.generated:
        st.warning("⚠️ Please generate test cases first!")
    else:
        hc = [t for t in st.session_state.test_cases if t.get("confidence",100) < 75]
        if not hc:
            st.success("✅ No HITL tests pending — all clear!")
        for tc in hc:
            dec = st.session_state.hitl_decisions.get(tc["id"])
            bc = T['green'] if dec=="approve" else T['red'] if dec=="reject" else T['yellow']
            st.markdown(f"""<div class='hitl-panel' style='border-color:{bc};'><div class='hitl-title'>⚠️ {tc.get('id')}: {tc.get('name')}</div><div style='font-size:12px;color:{T['subtext']};margin-bottom:10px;'>Confidence: <b style='color:{T['red']};'>{tc.get('confidence')}%</b> · {tc.get('why','')}</div><div class='bdd-box'><div class='given'>GIVEN  {tc.get('given','')}</div><div class='when'>WHEN   {tc.get('when','')}</div><div class='then'>THEN   {tc.get('then','')}</div></div>""", unsafe_allow_html=True)
            ca,cr2,cm = st.columns(3)
            with ca:
                if st.button("✅ Approve", key=f"a_{tc['id']}", use_container_width=True):
                    st.session_state.hitl_decisions[tc["id"]] = "approve"; st.rerun()
            with cr2:
                if st.button("❌ Reject", key=f"r_{tc['id']}", use_container_width=True):
                    st.session_state.hitl_decisions[tc["id"]] = "reject"; st.rerun()
            with cm:
                if st.button("✏️ Modify", key=f"m_{tc['id']}", use_container_width=True):
                    st.session_state.hitl_decisions[tc["id"]] = "modify"; st.rerun()
            if dec:
                lbl = {"approve":"✅ APPROVED","reject":"❌ REJECTED","modify":"✏️ MODIFY"}[dec]
                clr = {"approve":T['green'],"reject":T['red'],"modify":T['yellow']}[dec]
                st.markdown(f"<div style='color:{clr};font-size:12px;font-weight:600;margin:6px 0 0 4px;'>{lbl}</div>", unsafe_allow_html=True)
            st.markdown("</div><br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# RAG MEMORY
# ══════════════════════════════════════════════════
elif "RAG" in page:
    from agent import seed_defects, PAST_DEFECTS, add_defect_to_memory, get_defect_count
    st.markdown('<p class="sec-head">🧠 ChromaDB RAG Memory</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">📚 ChromaDB vector DB — past defects stored as embeddings. Gets smarter every sprint via LangChain orchestration.</div>', unsafe_allow_html=True)
    cl, cr = st.columns([3,2])
    with cl:
        st.markdown(f"**Stored Defects ({get_defect_count()}):**")
        for d in PAST_DEFECTS:
            sc = T['red'] if d["severity"]=="Critical" else T['yellow'] if d["severity"]=="High" else T['accent']
            st.markdown(f"""<div style='background:{T['card']};border:1px solid #7c3aed;border-left:3px solid {sc};border-radius:8px;padding:12px 16px;margin:7px 0;'><div style='display:flex;justify-content:space-between;'><span style='font-family:JetBrains Mono,monospace;font-size:10px;color:#a78bfa;'>{d['id']}</span><span style='font-size:9px;color:{sc};border:1px solid {sc}44;padding:2px 8px;border-radius:10px;'>{d['severity']}</span></div><div style='font-size:13px;color:{T['text']};font-weight:500;margin:5px 0;'>{d['title']}</div><div style='font-size:11px;color:{T['subtext']};'>{d['sprint']} · {d['component']}</div></div>""", unsafe_allow_html=True)
    with cr:
        st.markdown("**➕ Add New Defect to ChromaDB:**")
        nt = st.text_input("Title")
        nd = st.text_area("Description", height=80)
        nc = st.selectbox("Component", ["Authentication","Search","Cart","Payment","Other"])
        ns = st.selectbox("Severity", ["Critical","High","Medium","Low"])
        nsp = st.text_input("Sprint", value="Sprint 14")
        if st.button("➕ Add to ChromaDB", use_container_width=True):
            if nt and nd:
                did = add_defect_to_memory(nt, nd, nc, ns, nsp)
                st.success(f"✅ {did} added! Will be used in future test generation.")
            else:
                st.error("Title and description are required!")

# ══════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════
elif "Reports" in page:
    st.markdown('<p class="sec-head">📊 Test Execution Report</p>', unsafe_allow_html=True)
    if not st.session_state.executed:
        st.warning("⚠️ Please run tests from Test Executor first!")
    else:
        cases = st.session_state.test_cases
        passed = [t for t in cases if t.get("result")=="pass"]
        failed = [t for t in cases if t.get("result")=="fail"]
        hitl   = [t for t in cases if t.get("result")=="hitl"]
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['accent']};">{len(cases)}</p><p class="metric-label">Total</p></div>""", unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['green']};">{len(passed)}</p><p class="metric-label">Passed</p></div>""", unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['red']};">{len(failed)}</p><p class="metric-label">Failed</p></div>""", unsafe_allow_html=True)
        with c4: st.markdown(f"""<div class="metric-card"><p class="metric-number" style="color:{T['yellow']};">{len(hitl)}</p><p class="metric-label">HITL</p></div>""", unsafe_allow_html=True)
        if failed:
            st.markdown(f'<p class="sec-head" style="color:{T["red"]};">❌ Defects Found</p>', unsafe_allow_html=True)
            for tc in failed:
                st.markdown(f"""<div style='background:{T['card']};border:1px solid {T['red']};border-radius:8px;padding:14px 16px;margin:8px 0;'><div style='display:flex;justify-content:space-between;'><span style='color:{T['red']};font-weight:600;'>{tc.get('id')}: {tc.get('name')}</span><span class='badge-fail'>✗ FAIL</span></div><div style='font-size:12px;color:{T['subtext']};margin-top:8px;'>🔍 {tc.get('why','')}</div><div style='font-size:11px;color:{T['subtext']};margin-top:4px;'>Duration: {tc.get('duration','-')} · Confidence: {tc.get('confidence')}%</div></div>""", unsafe_allow_html=True)
        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "story": st.session_state.selected_story["id"] if st.session_state.selected_story else "N/A",
            "ai_model": "Google Gemini AI",
            "orchestration": "LangChain",
            "rag_engine": "ChromaDB",
            "test_runner": "Playwright",
            "summary": {"total":len(cases),"passed":len(passed),"failed":len(failed),"hitl":len(hitl),"pass_rate":f"{int(len(passed)/max(len(passed)+len(failed),1)*100)}%"},
            "defects": [{"id":t["id"],"name":t["name"],"why":t.get("why","")} for t in failed],
            "hitl_pending": [{"id":t["id"],"confidence":t.get("confidence",0)} for t in hitl]
        }
        st.markdown('<p class="sec-head">📄 JSON Report</p>', unsafe_allow_html=True)
        st.markdown(f"""<div class='report-box'>{json.dumps(report, indent=2)}</div>""", unsafe_allow_html=True)
        st.download_button("⬇️ Download Report", json.dumps(report,indent=2), f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "application/json", use_container_width=True)
