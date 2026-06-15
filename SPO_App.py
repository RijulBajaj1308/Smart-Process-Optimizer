# -*- coding: utf-8 -*-
import streamlit as st
from manufacturing import show_manufacturing
from distribution import show_distribution
from supply_chain import show_supply_chain

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
}

.prog-node { display: flex; flex-direction: column; align-items: center; gap: 8px; }

.prog-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
}
.prog-dot.done { background: var(--red); color: #fff; }
.prog-dot.curr {
    background: var(--red-dim);
    border: 1.5px solid var(--red);
    color: var(--red);
    box-shadow: 0 0 12px var(--red-glow);
}
.prog-dot.todo {
    background: var(--surface2);
    border: 1.5px solid var(--border2);
    color: var(--text-muted);
}

.prog-lbl { font-size: 0.6rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; }
.prog-lbl.curr { color: var(--red); }

.prog-seg { width: 56px; height: 1px; margin: 0 8px 20px; }
.prog-seg.done { background: var(--red); }
.prog-seg.todo { background: var(--border2); }

.step-header { text-align: center; margin-bottom: 44px; }

.step-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--red);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -1px;
    margin-bottom: 8px;
}

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

.ind-grid div[data-testid="stButton"] > button {
    padding: 18px 12px !important;
    font-size: 0.8rem !important;
    border-radius: 8px !important;
}

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

.stNumberInput input, .stTextInput input {
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

.analysis-header {
    padding: 20px 0 24px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}

.analysis-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--red);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.analysis-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.5px;
}

.analysis-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
}

[data-testid="stMetricValue"] { color: var(--red) !important; }
p, li { color: #888888 !important; }
h1, h2, h3, h4 { color: var(--text) !important; font-family: 'Space Grotesk', sans-serif !important; }
hr { border-color: var(--border) !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--red); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

def init_session():
    for key, val in {
        "page": "landing",
        "category": None,
        "industry": None,
        "business_model": None,
        "currency_symbol": "$"
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

def show_progress(current):
    steps = [("01", "Category"), ("02", "Industry"), ("03", "Model")]
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
# LANDING
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
                <div class="h-metric">
                    <div class="h-metric-n">26</div>
                    <div class="h-metric-l">Industries</div>
                </div>
                <div class="h-metric">
                    <div class="h-metric-n">3</div>
                    <div class="h-metric-l">Categories</div>
                </div>
                <div class="h-metric">
                    <div class="h-metric-n">INR</div>
                    <div class="h-metric-l">India First</div>
                </div>
                <div class="h-metric">
                    <div class="h-metric-n">Free</div>
                    <div class="h-metric-l">Always</div>
                </div>
            </div>
            <div class="feat-row">
                <div class="feat-item">
                    <div class="feat-item-t">Benchmark Analysis</div>
                    <div class="feat-item-d">Real Indian industry standards</div>
                </div>
                <div class="feat-item">
                    <div class="feat-item-t">Root Cause Detection</div>
                    <div class="feat-item-d">Know exactly what is wrong</div>
                </div>
                <div class="feat-item">
                    <div class="feat-item-t">Financial Impact</div>
                    <div class="feat-item-d">See the money you are losing</div>
                </div>
                <div class="feat-item">
                    <div class="feat-item-t">Priority Actions</div>
                    <div class="feat-item-d">What to fix first</div>
                </div>
                <div class="feat-item">
                    <div class="feat-item-t">What-If Simulator</div>
                    <div class="feat-item-d">Project improvements before acting</div>
                </div>
                <div class="feat-item">
                    <div class="feat-item-t">Risk Score</div>
                    <div class="feat-item-d">Overall operational risk rating</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.8, 1, 1.8])
    with col2:
        st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# CATEGORY
# ════════════════════════════════════════
elif st.session_state.page == "category":
    show_progress(1)
    st.markdown("""
    <div class="step-header">
        <div class="step-eyebrow">Step 01 of 03</div>
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

# ════════════════════════════════════════
# INDUSTRY
# ════════════════════════════════════════
elif st.session_state.page == "industry":
    show_progress(2)
    st.markdown(f"""
    <div class="step-header">
        <div class="step-eyebrow">Step 02 of 03 &nbsp;·&nbsp; {st.session_state.category}</div>
        <div class="step-title">Select your industry</div>
        <div class="step-sub">Click a card to continue</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.category == "Manufacturing":
        industries = [
            "Automotive", "Electronics", "Food and Beverage",
            "Textile and Apparel", "General Manufacturing",
            "Eco Friendly Packaging", "Pulp and Paper Manufacturing",
            "Pharmaceutical Manufacturing"
        ]
    elif st.session_state.category == "Distribution":
        industries = [
            "Warehouse and Distribution", "Cold Chain Distribution",
            "E-commerce Fulfillment", "Pharmaceutical Distribution",
            "Automotive Parts Distribution", "Electronics Distribution",
            "Food and Beverage Distribution", "Textile and Apparel Distribution",
            "Eco Friendly Packaging Distribution", "Pulp and Paper Distribution"
        ]
    else:
        industries = [
            "Automotive Supply Chain", "Food and Beverage Supply Chain",
            "Electronics Supply Chain", "General Supply Chain",
            "Pharmaceutical Supply Chain", "Textile and Apparel Supply Chain",
            "Eco Friendly Packaging Supply Chain", "Pulp and Paper Supply Chain"
        ]

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
        <div class="step-eyebrow">Step 03 of 03 &nbsp;·&nbsp; {st.session_state.industry}</div>
        <div class="step-title">What is your business model?</div>
        <div class="step-sub">Click a card to begin your analysis</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("B2B\n\nYou sell to other businesses", use_container_width=True):
            st.session_state.business_model = "B2B"
            st.session_state.page = "analysis"
            st.rerun()
    with col2:
        if st.button("B2C\n\nYou sell directly to consumers", use_container_width=True):
            st.session_state.business_model = "B2C"
            st.session_state.page = "analysis"
            st.rerun()
    with col3:
        if st.button("B2B2C\n\nYou sell to businesses who sell to consumers", use_container_width=True):
            st.session_state.business_model = "B2B2C"
            st.session_state.page = "analysis"
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
# ANALYSIS
# ════════════════════════════════════════
elif st.session_state.page == "analysis":
    st.markdown(f"""
    <div class="analysis-header">
        <div class="analysis-label">Smart Process Optimizer &nbsp;|&nbsp; Active Session</div>
        <div class="analysis-title">{st.session_state.industry}</div>
        <div class="analysis-meta">{st.session_state.category} &nbsp;/&nbsp; {st.session_state.business_model}</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div style="padding:16px;background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.12);border-radius:8px;margin-bottom:20px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#E8001D;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">Active Session</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:0.95rem;font-weight:600;color:#F0F0F0;">{st.session_state.industry}</div>
        <div style="font-size:0.75rem;color:#3a3a3e;margin-top:4px;font-family:'JetBrains Mono',monospace;">{st.session_state.category}</div>
        <div style="font-size:0.75rem;color:#3a3a3e;font-family:'JetBrains Mono',monospace;">{st.session_state.business_model}</div>
    </div>
    """, unsafe_allow_html=True)

    currency_options = {"USD ($)": "$", "INR (₹)": "₹", "GBP (£)": "£"}
    selected_currency = st.sidebar.selectbox("Currency", list(currency_options.keys()), index=0)
    st.session_state.currency_symbol = currency_options[selected_currency]

    st.sidebar.divider()

    st.markdown('<div class="sidebar-btn">', unsafe_allow_html=True)
    if st.sidebar.button("Start Over", use_container_width=True):
        for key in ["page", "category", "industry", "business_model", "currency_symbol"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry, st.session_state.currency_symbol)