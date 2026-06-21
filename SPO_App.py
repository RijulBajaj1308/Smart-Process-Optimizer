# -*- coding: utf-8 -*-
import streamlit as st
from manufacturing import show_manufacturing
from distribution import show_distribution
from supply_chain import show_supply_chain
from manufacturing_deep import show_manufacturing_deep
from distribution_deep import show_distribution_deep
from supply_chain_deep import show_supply_chain_deep
from auth import sign_in, sign_up, sign_out, get_current_user, get_companies, create_company, get_analyses, delete_company
from cross_analysis import show_cross_analysis

st.set_page_config(
    page_title="Smart Process Optimizer",
    page_icon="SPO",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --red: #E8001D;
    --red-dim: rgba(232,0,29,0.12);
    --red-glow: rgba(232,0,29,0.25);
    --bg: #070708;
    --surface: #0E0E10;
    --surface2: #141416;
    --border: #1C1C1F;
    --border2: #242428;
    --text: #F0F0F0;
    --text-dim: #5A5A60;
    --text-muted: #2C2C30;
}

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: var(--bg) !important; }
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

.hero-wrap {
    min-height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 80px 32px 100px;
    overflow: hidden;
    background: var(--bg);
}

.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 48px 48px;
    opacity: 0.4;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(232,0,29,0.15) 0%, transparent 70%);
    pointer-events: none;
}

.scan-line {
    position: absolute;
    left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    animation: scan 4s ease-in-out infinite;
    opacity: 0.5;
    pointer-events: none;
    z-index: 1;
}

@keyframes scan {
    0% { top: 0%; opacity: 0; }
    10% { opacity: 0.5; }
    90% { opacity: 0.5; }
    100% { top: 100%; opacity: 0; }
}

.corner {
    position: absolute;
    width: 40px; height: 40px;
    border-color: var(--red);
    border-style: solid;
    opacity: 0.4;
    z-index: 1;
}
.corner-tl { top: 24px; left: 24px; border-width: 2px 0 0 2px; }
.corner-tr { top: 24px; right: 24px; border-width: 2px 2px 0 0; }
.corner-bl { bottom: 24px; left: 24px; border-width: 0 0 2px 2px; }
.corner-br { bottom: 24px; right: 24px; border-width: 0 2px 2px 0; }

.hero-content { position: relative; z-index: 2; }

.system-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(232,0,29,0.06);
    border: 1px solid rgba(232,0,29,0.2);
    color: var(--red);
    padding: 6px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 36px;
}

.blink {
    width: 7px; height: 7px;
    background: var(--red);
    border-radius: 50%;
    animation: blink 1.2s step-end infinite;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 5.5rem;
    font-weight: 700;
    color: var(--text);
    line-height: 0.95;
    letter-spacing: -4px;
    margin-bottom: 28px;
}

.hero-title .accent {
    display: block;
    color: var(--red);
    font-weight: 300;
    letter-spacing: -2px;
    font-size: 4.5rem;
}

.hero-body {
    font-size: 1rem;
    color: var(--text-dim);
    max-width: 480px;
    line-height: 1.75;
    margin: 0 auto 52px;
}

.hero-metrics {
    display: flex;
    gap: 0;
    border: 1px solid var(--border2);
    border-radius: 8px;
    overflow: hidden;
    margin: 0 auto 60px;
    max-width: 480px;
}

.h-metric {
    flex: 1;
    padding: 18px 0;
    border-right: 1px solid var(--border2);
    text-align: center;
}
.h-metric:last-child { border-right: none; }
.h-metric-n {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.h-metric-l {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
}

.feat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    max-width: 660px;
    margin: 0 auto 60px;
}

.feat-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px 16px;
    text-align: left;
}

.feat-item-t { color: var(--text); font-size: 0.78rem; font-weight: 600; margin-bottom: 3px; }
.feat-item-d { color: var(--text-muted); font-size: 0.71rem; line-height: 1.4; }

.prog-track {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 36px 0 52px;
    flex-wrap: wrap;
    gap: 0;
}

.prog-node { display: flex; flex-direction: column; align-items: center; gap: 8px; }

.prog-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; flex-shrink: 0;
}
.prog-dot.done { background: var(--red); color: #fff; }
.prog-dot.curr { background: var(--red-dim); border: 2px solid var(--red); color: var(--red); box-shadow: 0 0 12px var(--red-glow); }
.prog-dot.todo { background: var(--surface2); border: 2px solid var(--border2); color: var(--text-muted); }

.prog-lbl { font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }
.prog-lbl.curr { color: var(--red); }

.prog-seg { width: 40px; height: 1px; margin: 0 4px 20px; flex-shrink: 0; }
.prog-seg.done { background: var(--red); }
.prog-seg.todo { background: var(--border2); }

.step-header { text-align: center; margin-bottom: 44px; }
.step-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--red); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px; }
.step-title { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--text); letter-spacing: -1px; margin-bottom: 8px; }
.step-sub { font-size: 0.88rem; color: var(--text-muted); }

div[data-testid="stButton"] > button {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 32px 20px !important;
    width: 100% !important;
    height: auto !important;
    white-space: pre-line !important;
    line-height: 1.5 !important;
    transition: all 0.18s ease !important;
    text-align: center !important;
    cursor: pointer !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: var(--red) !important;
    background: rgba(232,0,29,0.04) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(232,0,29,0.1), 0 0 0 1px var(--red) !important;
    color: #fff !important;
}

.ind-grid div[data-testid="stButton"] > button { padding: 18px 12px !important; font-size: 0.8rem !important; border-radius: 8px !important; }

.cta-btn div[data-testid="stButton"] > button {
    background: var(--red) !important;
    border-color: var(--red) !important;
    border-radius: 6px !important;
    padding: 14px 36px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(232,0,29,0.3) !important;
}

.cta-btn div[data-testid="stButton"] > button:hover {
    background: #ff0020 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(232,0,29,0.4) !important;
}

.back-btn div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
    padding: 10px 20px !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
}

.back-btn div[data-testid="stButton"] > button:hover {
    border-color: var(--border2) !important;
    color: var(--text-dim) !important;
    transform: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.sidebar-btn div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-dim) !important;
    padding: 9px 16px !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
}

.sidebar-btn div[data-testid="stButton"] > button:hover {
    border-color: var(--red) !important;
    color: var(--red) !important;
    transform: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.stNumberInput input, .stTextInput input, .stTextInput textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

.analysis-header { padding: 20px 0 24px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
.analysis-label { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--red); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
.analysis-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 700; color: var(--text); letter-spacing: -0.5px; }
.analysis-meta { font-size: 0.75rem; color: var(--text-muted); margin-top: 3px; font-family: 'JetBrains Mono', monospace; }

/* Auth page */
.auth-wrap {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 24px;
    background: var(--bg);
    position: relative;
}

.auth-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 48px 48px;
    opacity: 0.3;
}

.auth-box {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 16px;
    padding: 40px;
    width: 100%;
    max-width: 420px;
    position: relative;
    z-index: 1;
}

.auth-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: -0.5px;
    margin-bottom: 8px;
    text-align: center;
}

.auth-tagline {
    font-size: 0.82rem;
    color: var(--text-muted);
    text-align: center;
    margin-bottom: 32px;
}

/* Company cards */
.company-card {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.15s;
}

.company-card:hover { border-color: var(--red); }
.company-name { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.company-meta { font-size: 0.78rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; }
.company-risk { font-size: 0.82rem; font-weight: 600; }

[data-testid="stMetricValue"] { color: var(--red) !important; }
p, li { color: #888888 !important; }
h1, h2, h3, h4 { color: var(--text) !important; font-family: 'Space Grotesk', sans-serif !important; }
hr { border-color: var(--border) !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--red); border-radius: 2px; }

    /* ══════════════════════════════════════
       MOBILE RESPONSIVE
    ══════════════════════════════════════ */
    @media (max-width: 768px) {

        /* Hero */
        .hero-title {
            font-size: 3rem !important;
            letter-spacing: -2px !important;
        }

        .hero-title .accent {
            font-size: 2.5rem !important;
        }

        .hero-body {
            font-size: 0.9rem !important;
        }

        .hero-metrics {
            max-width: 100% !important;
        }

        .h-metric-n {
            font-size: 1.2rem !important;
        }

        .feat-row {
            grid-template-columns: repeat(2, 1fr) !important;
            max-width: 100% !important;
        }

        /* Corner brackets hidden on mobile */
        .corner { display: none !important; }

        /* Step header */
        .step-title {
            font-size: 1.4rem !important;
        }

        /* Cards — full width on mobile */
        div[data-testid="stButton"] > button {
            padding: 20px 16px !important;
            font-size: 0.88rem !important;
        }

        /* Progress bar — smaller */
        .prog-dot {
            width: 28px !important;
            height: 28px !important;
            font-size: 0.72rem !important;
        }

        .prog-seg {
            width: 24px !important;
        }

        .prog-lbl {
            font-size: 0.52rem !important;
        }

        /* Analysis header */
        .analysis-title {
            font-size: 1.1rem !important;
        }

        /* Auth box */
        .auth-box {
            padding: 24px 20px !important;
        }

        /* Dashboard company cards */
        .company-name {
            font-size: 0.95rem !important;
        }

        .company-meta {
            font-size: 0.7rem !important;
        }

        /* Hero metrics strip */
        .h-metric {
            padding: 12px 0 !important;
        }

        /* Sidebar notice on mobile */
        [data-testid="stSidebar"] {
            display: none !important;
        }
    }

    @media (max-width: 480px) {
        .hero-title {
            font-size: 2.4rem !important;
            letter-spacing: -1px !important;
        }

        .hero-title .accent {
            font-size: 2rem !important;
        }

        .feat-row {
            grid-template-columns: 1fr !important;
        }

        .hero-metrics {
            flex-wrap: wrap !important;
        }

        .h-metric {
            flex: 0 0 50% !important;
            border-bottom: 1px solid var(--border2) !important;
        }
    }

</style>
""", unsafe_allow_html=True)

# ── Session State ──
def init_session():
    for key, val in {
        "page": "landing",
        "category": None,
        "industry": None,
        "business_model": None,
        "currency_symbol": "$",
        "analysis_type": None,
        "user": None,
        "session": None,
        "current_company": None,
        "auth_mode": "login"
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ── Progress Bar ──
def show_progress(current):
    steps = [("1", "Category"), ("2", "Industry"), ("3", "Model"), ("4", "Analysis")]
    html = '<div class="prog-track">'
    for i, (num, label) in enumerate(steps):
        n = i + 1
        if n < current:
            dc, lc = "done", ""
        elif n == current:
            dc, lc = "curr", "curr"
        else:
            dc, lc = "todo", ""
        html += f'<div class="prog-node"><div class="prog-dot {dc}">{num}</div><div class="prog-lbl {lc}">{label}</div></div>'
        if i < len(steps) - 1:
            sc = "done" if n < current else "todo"
            html += f'<div class="prog-seg {sc}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ════════════════════════════════════════
# AUTH PAGE — Login / Signup
# ════════════════════════════════════════
def show_auth():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="auth-box">
            <div class="auth-logo">Smart Process Optimizer</div>
            <div class="auth-tagline">Decision Support Tool for India</div>
        </div>
        """, unsafe_allow_html=True)

        mode = st.radio("", ["Login", "Sign Up"], horizontal=True,
                       index=0 if st.session_state.auth_mode == "login" else 1,
                       label_visibility="collapsed")
        st.session_state.auth_mode = "login" if mode == "Login" else "signup"

        if mode == "Login":
            email = st.text_input("Email", placeholder="you@company.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            st.write("")
            st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
            if st.button("Login", use_container_width=True):
                if email and password:
                    with st.spinner("Logging in..."):
                        success, message = sign_in(email, password)
                    if success:
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter your email and password.")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            full_name = st.text_input("Full Name", placeholder="Rijul Bajaj", key="signup_name")
            email = st.text_input("Email", placeholder="you@company.com", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="signup_pass")
            st.write("")
            st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True):
                if full_name and email and password:
                    if len(password) < 8:
                        st.error("Password must be at least 8 characters.")
                    else:
                        with st.spinner("Creating account..."):
                            success, message = sign_up(email, password, full_name)
                        if success:
                            st.success("Account created! Please check your email to verify, then login.")
                        else:
                            st.error(message)
                else:
                    st.error("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="text-align: center; font-size: 0.75rem; color: #2C2C30; margin-top: 24px;">
            By using SPO you agree to our terms of service
        </p>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Continue as Guest", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align: center; font-size: 0.72rem; color: #2C2C30; margin-top: 8px;">
            Guest mode — analysis will not be saved
        </p>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# DASHBOARD — Company Selection
# ════════════════════════════════════════
def show_dashboard():
    user = get_current_user()
    name = user.user_metadata.get("full_name", "there") if user and user.user_metadata else "there"

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="padding:16px;background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.12);border-radius:8px;margin-bottom:20px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#E8001D;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Logged In As</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:0.95rem;font-weight:600;color:#F0F0F0;">{name}</div>
        <div style="font-size:0.75rem;color:#3a3a3e;font-family:'JetBrains Mono',monospace;">{user.email if user else ""}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-btn">', unsafe_allow_html=True)
    if st.sidebar.button("Sign Out", use_container_width=True):
        sign_out()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div style="padding: 20px 0 32px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#E8001D;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Smart Process Optimizer</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:700;color:#F0F0F0;letter-spacing:-1px;">Welcome back, {name}</div>
        <div style="font-size:0.85rem;color:#2C2C30;margin-top:4px;">Select a company to continue or add a new one</div>
    </div>
    """, unsafe_allow_html=True)

    # Get companies
    companies = get_companies()

    if companies:
        st.subheader(f"Your Companies ({len(companies)})")
        st.write("")

        for company in companies:
            analyses = get_analyses(company["id"])
            last_analysis = analyses[0] if analyses else None
            risk_score = last_analysis["risk_score"] if last_analysis else None
            risk_label = last_analysis["risk_label"] if last_analysis else None
            analysis_count = len(analyses)

            if risk_score is not None:
                if risk_score >= 80:
                    risk_color = "#00CC00"
                elif risk_score >= 50:
                    risk_color = "#FFD700"
                else:
                    risk_color = "#CC0000"
            else:
                risk_color = "#444444"

            # Company card header
            st.markdown(f"""
            <div class="company-card">
                <div class="company-name">{company['name']}</div>
                <div class="company-meta">{company['category']} &nbsp;/&nbsp; {company['industry']} &nbsp;/&nbsp; {company['business_model']}</div>
                <div class="company-risk" style="color:{risk_color}">
                    {"Risk Score: " + str(risk_score) + " — " + risk_label if risk_score else "No analysis yet"}
                    &nbsp;&nbsp; <span style="color:#2C2C30;font-weight:400;">{analysis_count} analysis record{"s" if analysis_count != 1 else ""}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tabs for each company
            tab1, tab2, tab3 = st.tabs(["Overview", "Cross Analysis", "History"])

            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Continue Analysis", key=f"cont_{company['id']}", use_container_width=True):
                        st.session_state.current_company = company
                        st.session_state.category = company["category"]
                        st.session_state.industry = company["industry"]
                        st.session_state.business_model = company["business_model"]
                        st.session_state.page = "analysis_type"
                        st.rerun()
                with col2:
                    if st.button("Delete Company", key=f"del_{company['id']}", use_container_width=True):
                        delete_company(company["id"])
                        st.rerun()

            with tab2:
                show_cross_analysis(company, analyses)

            with tab3:
                if analyses:
                    for a in analyses:
                        a_type = a.get("analysis_type", "Unknown")
                        a_date = a.get("created_at", "")[:10]
                        a_risk = a.get("risk_score", "N/A")
                        a_label = a.get("risk_label", "")
                        color = "#CC0000" if a_type == "Quick" else "#FFD700"
                        st.markdown(f"""
                        <div style="background:#1a1a1a;border-left:3px solid {color};padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;">
                            <span style="color:{color};font-weight:700;font-size:0.8rem;">{a_type} Analysis</span>
                            <span style="color:#888;margin-left:10px;font-size:0.78rem;">{a_date} &nbsp;|&nbsp; Risk Score: {a_risk}/100 — {a_label}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No analysis history yet.")

        st.divider()

    # Add new company
    st.subheader("Add New Company")
    st.write("Start a fresh analysis for a new company or client")
    st.write("")

    st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
    if st.button("Start New Analysis", use_container_width=True):
        st.session_state.current_company = None
        st.session_state.category = None
        st.session_state.industry = None
        st.session_state.business_model = None
        st.session_state.analysis_type = None
        st.session_state.page = "category"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="hero-wrap">
        <div class="scan-line"></div>
        <div class="corner corner-tl"></div>
        <div class="corner corner-tr"></div>
        <div class="corner corner-bl"></div>
        <div class="corner corner-br"></div>
        <div class="hero-content">
            <div class="system-tag">
                <div class="blink"></div>
                System Online &nbsp;|&nbsp; India Benchmark Database
            </div>
            <div class="hero-title">
                Smart Process
                <span class="accent">Optimizer</span>
            </div>
            <div class="hero-body">
                Enter your numbers. SPO compares them against real Indian industry benchmarks,
                identifies what is wrong, and tells you exactly what to fix.
            </div>
            <div class="hero-metrics">
                <div class="h-metric"><div class="h-metric-n">26</div><div class="h-metric-l">Industries</div></div>
                <div class="h-metric"><div class="h-metric-n">3</div><div class="h-metric-l">Categories</div></div>
                <div class="h-metric"><div class="h-metric-n">INR</div><div class="h-metric-l">India First</div></div>
                <div class="h-metric"><div class="h-metric-n">Free</div><div class="h-metric-l">Always</div></div>
            </div>
            <div class="feat-row">
                <div class="feat-item"><div class="feat-item-t">Benchmark Analysis</div><div class="feat-item-d">Real Indian industry standards</div></div>
                <div class="feat-item"><div class="feat-item-t">Root Cause Detection</div><div class="feat-item-d">Know exactly what is wrong</div></div>
                <div class="feat-item"><div class="feat-item-t">Financial Impact</div><div class="feat-item-d">See the money you are losing</div></div>
                <div class="feat-item"><div class="feat-item-t">Deep Analysis</div><div class="feat-item-d">Bottleneck, OEE, Pareto, Manpower</div></div>
                <div class="feat-item"><div class="feat-item-t">30 Day Action Plan</div><div class="feat-item-d">Structured plan to fix problems</div></div>
                <div class="feat-item"><div class="feat-item-t">PDF Report</div><div class="feat-item-d">Download and share your analysis</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.8, 1, 1.8])
    with col2:
        st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "auth"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# AUTH PAGE
# ════════════════════════════════════════
elif st.session_state.page == "auth":
    show_auth()

# ════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════
elif st.session_state.page == "dashboard":
    user = get_current_user()
    if not user:
        st.session_state.page = "auth"
        st.rerun()
    else:
        show_dashboard()

# ════════════════════════════════════════
# CATEGORY
# ════════════════════════════════════════
elif st.session_state.page == "category":
    show_progress(1)
    st.markdown("""
    <div class="step-header">
        <div class="step-eyebrow">Step 1 of 4</div>
        <div class="step-title">What type of business are you?</div>
        <div class="step-sub">Click a card to continue</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Manufacturing\n\nAutomotive · Electronics · Food · Textile · Pharma · Packaging", use_container_width=True):
            st.session_state.category = "Manufacturing"
            st.session_state.page = "industry"
            st.rerun()
    with col2:
        if st.button("Distribution\n\nWarehouse · Cold Chain · E-commerce · Pharma · Automotive Parts", use_container_width=True):
            st.session_state.category = "Distribution"
            st.session_state.page = "industry"
            st.rerun()
    with col3:
        if st.button("Supply Chain\n\nAutomotive · Food · Electronics · Pharma · Textile · Packaging", use_container_width=True):
            st.session_state.category = "Supply Chain"
            st.session_state.page = "industry"
            st.rerun()

    st.write("")
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        if st.button("Back", use_container_width=True, key="back_cat"):
            if get_current_user():
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "auth"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# INDUSTRY
# ════════════════════════════════════════
elif st.session_state.page == "industry":
    show_progress(2)
    st.markdown(f"""
    <div class="step-header">
        <div class="step-eyebrow">Step 2 of 4 &nbsp;·&nbsp; {st.session_state.category}</div>
        <div class="step-title">Select your industry</div>
        <div class="step-sub">Click a card to continue</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.category == "Manufacturing":
        industries = ["Automotive", "Electronics", "Food and Beverage", "Textile and Apparel",
                     "General Manufacturing", "Eco Friendly Packaging", "Pulp and Paper Manufacturing",
                     "Pharmaceutical Manufacturing"]
    elif st.session_state.category == "Distribution":
        industries = ["Warehouse and Distribution", "Cold Chain Distribution", "E-commerce Fulfillment",
                     "Pharmaceutical Distribution", "Automotive Parts Distribution", "Electronics Distribution",
                     "Food and Beverage Distribution", "Textile and Apparel Distribution",
                     "Eco Friendly Packaging Distribution", "Pulp and Paper Distribution"]
    else:
        industries = ["Automotive Supply Chain", "Food and Beverage Supply Chain", "Electronics Supply Chain",
                     "General Supply Chain", "Pharmaceutical Supply Chain", "Textile and Apparel Supply Chain",
                     "Eco Friendly Packaging Supply Chain", "Pulp and Paper Supply Chain"]

    st.markdown('''<div class="ind-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
    <style>@media(max-width:768px){.ind-grid{grid-template-columns:repeat(2,1fr) !important;}}</style>
    </div>''', unsafe_allow_html=True)
    st.markdown('<div class="ind-grid">', unsafe_allow_html=True)
    for i in range(0, len(industries), 4):
        row = industries[i:i+4]
        cols = st.columns(len(row))
        for j, ind in enumerate(row):
            with cols[j]:
                if st.button(ind, key=f"ind_{i}_{j}", use_container_width=True):
                    st.session_state.industry = ind
                    st.session_state.page = "business_model"
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# BUSINESS MODEL
# ════════════════════════════════════════
elif st.session_state.page == "business_model":
    show_progress(3)
    st.markdown(f"""
    <div class="step-header">
        <div class="step-eyebrow">Step 3 of 4 &nbsp;·&nbsp; {st.session_state.industry}</div>
        <div class="step-title">What is your business model?</div>
        <div class="step-sub">Click a card to continue</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("B2B\n\nYou sell to other businesses", use_container_width=True):
            st.session_state.business_model = "B2B"
            st.session_state.page = "analysis_type"
            st.rerun()
    with col2:
        if st.button("B2C\n\nYou sell directly to consumers", use_container_width=True):
            st.session_state.business_model = "B2C"
            st.session_state.page = "analysis_type"
            st.rerun()
    with col3:
        if st.button("B2B2C\n\nYou sell to businesses who sell to consumers", use_container_width=True):
            st.session_state.business_model = "B2B2C"
            st.session_state.page = "analysis_type"
            st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "industry"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# ANALYSIS TYPE
# ════════════════════════════════════════
elif st.session_state.page == "analysis_type":
    show_progress(4)
    st.markdown(f"""
    <div class="step-header">
        <div class="step-eyebrow">Step 4 of 4 &nbsp;·&nbsp; {st.session_state.industry}</div>
        <div class="step-title">Choose your analysis type</div>
        <div class="step-sub">Quick Analysis for an overview — Deep Analysis to pinpoint exact problems</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Quick Analysis\n\nEnter summary performance numbers and get benchmark comparison, root causes, 30 day action plan and PDF report", use_container_width=True):
            st.session_state.analysis_type = "Quick"
            # Create company in database if logged in
            if get_current_user() and not st.session_state.current_company:
                company = create_company(
                    "New Company",
                    st.session_state.category,
                    st.session_state.industry,
                    st.session_state.business_model
                )
                st.session_state.current_company = company
            st.session_state.page = "analysis"
            st.rerun()
    with col2:
        if st.session_state.category == "Manufacturing":
            if st.button("Deep Analysis\n\nEnter detailed process data — identify your exact bottleneck, calculate OEE, run Defect Pareto and plan manpower", use_container_width=True):
                st.session_state.analysis_type = "Deep"
                if get_current_user() and not st.session_state.current_company:
                    company = create_company(
                        "New Company",
                        st.session_state.category,
                        st.session_state.industry,
                        st.session_state.business_model
                    )
                    st.session_state.current_company = company
                st.session_state.page = "analysis"
                st.rerun()
        elif st.session_state.category == "Distribution":
            if st.button("Deep Analysis\n\nRoute efficiency, picking time analysis, warehouse slotting and returns root cause analysis", use_container_width=True):
                st.session_state.analysis_type = "Deep"
                if get_current_user() and not st.session_state.current_company:
                    company = create_company(
                        "New Company",
                        st.session_state.category,
                        st.session_state.industry,
                        st.session_state.business_model
                    )
                    st.session_state.current_company = company
                st.session_state.page = "analysis"
                st.rerun()
        else:
            if st.button("Deep Analysis\n\nSupplier scorecard, inventory ABC analysis, lead time breakdown and supply chain risk assessment", use_container_width=True):
                st.session_state.analysis_type = "Deep"
                if get_current_user() and not st.session_state.current_company:
                    company = create_company(
                        "New Company",
                        st.session_state.category,
                        st.session_state.industry,
                        st.session_state.business_model
                    )
                    st.session_state.current_company = company
                st.session_state.page = "analysis"
                st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "business_model"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# ANALYSIS
# ════════════════════════════════════════
elif st.session_state.page == "analysis":
    analysis_mode = st.session_state.get("analysis_type", "Quick")
    company = st.session_state.get("current_company")
    company_name = company["name"] if company else "Analysis"

    st.markdown(f"""
    <div class="analysis-header">
        <div class="analysis-label">Smart Process Optimizer &nbsp;|&nbsp; {analysis_mode} Analysis</div>
        <div class="analysis-title">{st.session_state.industry}</div>
        <div class="analysis-meta">{st.session_state.category} &nbsp;/&nbsp; {st.session_state.business_model}</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    user = get_current_user()
    if user:
        name = user.user_metadata.get("full_name", "") if user.user_metadata else ""
        st.sidebar.markdown(f"""
        <div style="padding:14px;background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.12);border-radius:8px;margin-bottom:16px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#E8001D;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Session</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:0.9rem;font-weight:600;color:#F0F0F0;">{st.session_state.industry}</div>
            <div style="font-size:0.75rem;color:#3a3a3e;font-family:'JetBrains Mono',monospace;">{st.session_state.category} / {analysis_mode}</div>
            <div style="font-size:0.75rem;color:#3a3a3e;font-family:'JetBrains Mono',monospace;margin-top:4px;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

    currency_options = {"USD ($)": "$", "INR (₹)": "₹", "GBP (£)": "£"}
    selected_currency = st.sidebar.selectbox("Currency", list(currency_options.keys()), index=0)
    st.session_state.currency_symbol = currency_options[selected_currency]

    st.markdown("""
    <div style="background:rgba(232,0,29,0.08);border:1px solid rgba(232,0,29,0.2);border-radius:8px;padding:12px 16px;margin-bottom:16px;">
        <p style="color:#E8001D;font-size:0.78rem;font-weight:700;margin:0 0 4px 0;">How to Enter Your Numbers</p>
        <p style="color:#888;font-size:0.75rem;margin:0;">Tap the <b style="color:#E8001D;">&gt;</b> arrow at the top left of your screen to open the sidebar and enter your KPI numbers.</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    st.markdown('<div class="sidebar-btn">', unsafe_allow_html=True)
    if get_current_user():
        if st.sidebar.button("Back to Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    if st.sidebar.button("Start Over", use_container_width=True):
        if get_current_user():
            st.session_state.current_company = None
            st.session_state.page = "dashboard"
        else:
            st.session_state.page = "category"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Load module
    if st.session_state.analysis_type == "Deep" and st.session_state.category == "Manufacturing":
        show_manufacturing_deep(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.analysis_type == "Deep" and st.session_state.category == "Distribution":
        show_distribution_deep(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.analysis_type == "Deep" and st.session_state.category == "Supply Chain":
        show_supply_chain_deep(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry, st.session_state.currency_symbol)