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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #080808; }
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        border-right: 1px solid #1a1a1a;
    }

    /* ---- LANDING ---- */
    .hero {
        min-height: 95vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 24px;
        background:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(204,0,0,0.12) 0%, transparent 60%),
            linear-gradient(180deg, #080808 0%, #050505 100%);
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
        background-size: 64px 64px;
    }

    .hero::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 120px;
        background: linear-gradient(to top, #080808, transparent);
    }

    .hero > * { position: relative; z-index: 1; }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(204,0,0,0.08);
        border: 1px solid rgba(204,0,0,0.25);
        color: #CC0000;
        padding: 5px 14px;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 32px;
    }

    .badge-dot {
        width: 6px; height: 6px;
        background: #CC0000;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        letter-spacing: -3px;
        margin-bottom: 24px;
    }

    .hero-title .red {
        color: transparent;
        background: linear-gradient(135deg, #CC0000, #ff4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        font-size: 1.1rem;
        color: #555;
        max-width: 520px;
        line-height: 1.75;
        margin-bottom: 56px;
        font-weight: 400;
    }

    .stats {
        display: flex;
        gap: 56px;
        justify-content: center;
        margin-bottom: 64px;
        flex-wrap: wrap;
    }

    .stat { text-align: center; }
    .stat-n { font-size: 2rem; font-weight: 900; color: #fff; letter-spacing: -1px; }
    .stat-l { font-size: 0.7rem; color: #333; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }

    .feat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 720px;
        margin: 0 auto 64px;
    }

    .feat {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 16px;
        text-align: left;
    }

    .feat-t { color: #fff; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px; }
    .feat-d { color: #383838; font-size: 0.76rem; line-height: 1.5; }

    /* ---- PROGRESS ---- */
    .prog {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        padding: 32px 0 48px;
    }

    .ps {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }

    .pc {
        width: 34px; height: 34px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.78rem; font-weight: 700;
    }

    .pc.done { background: #CC0000; color: #fff; }
    .pc.curr { background: rgba(204,0,0,0.1); border: 1.5px solid #CC0000; color: #CC0000; }
    .pc.todo { background: rgba(255,255,255,0.03); border: 1.5px solid #1a1a1a; color: #2a2a2a; }
    .pl { font-size: 0.62rem; color: #2a2a2a; text-transform: uppercase; letter-spacing: 1px; }
    .pl.curr { color: #CC0000; }

    .pline {
        width: 52px; height: 1px;
        margin: 0 6px 20px;
    }
    .pline.done { background: #CC0000; }
    .pline.todo { background: #1a1a1a; }

    /* ---- STEP HEADER ---- */
    .step-hdr { text-align: center; margin-bottom: 40px; }
    .step-tag { color: #CC0000; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
    .step-ttl { color: #fff; font-size: 1.9rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px; }
    .step-stl { color: #333; font-size: 0.9rem; }

    /* ---- OPTION CARDS ---- */
    .card-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 32px; }
    .card-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 32px; }
    .card-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 32px; }

    .opt {
        background: rgba(255,255,255,0.02);
        border: 1px solid #1a1a1a;
        border-radius: 12px;
        padding: 28px 20px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s ease;
    }

    .opt:hover {
        border-color: #CC0000;
        background: rgba(204,0,0,0.04);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(204,0,0,0.08);
    }

    .opt-title { color: #fff; font-size: 1rem; font-weight: 700; margin-bottom: 6px; }
    .opt-desc { color: #333; font-size: 0.78rem; line-height: 1.5; }

    .opt-sm {
        background: rgba(255,255,255,0.02);
        border: 1px solid #1a1a1a;
        border-radius: 10px;
        padding: 18px 14px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s ease;
    }

    .opt-sm:hover {
        border-color: #CC0000;
        background: rgba(204,0,0,0.04);
        transform: translateY(-1px);
    }

    .opt-sm-title { color: #fff; font-size: 0.85rem; font-weight: 600; }

    /* ---- BUTTONS ---- */
    .stButton button {
        background: #CC0000 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 10px 24px !important;
        transition: all 0.15s !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
    }

    .stButton button:hover {
        background: #e60000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(204,0,0,0.3) !important;
    }

    .back-btn button {
        background: transparent !important;
        border: 1px solid #1a1a1a !important;
        color: #333 !important;
        box-shadow: none !important;
    }

    .back-btn button:hover {
        border-color: #333 !important;
        color: #666 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* ---- INPUTS ---- */
    .stNumberInput input, .stTextInput input {
        background: #0f0f0f !important;
        border: 1px solid #1a1a1a !important;
        color: #fff !important;
        border-radius: 8px !important;
    }

    .stSelectbox > div > div {
        background: #0f0f0f !important;
        border: 1px solid #1a1a1a !important;
        color: #fff !important;
        border-radius: 8px !important;
    }

    /* ---- MISC ---- */
    [data-testid="stMetricValue"] { color: #CC0000 !important; }
    p, li { color: #aaaaaa !important; }
    h1, h2, h3 { color: #ffffff !important; }
    hr { border-color: #111 !important; }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #080808; }
    ::-webkit-scrollbar-thumb { background: #CC0000; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# Session State
def init_session():
    defaults = {
        "page": "landing",
        "category": None,
        "industry": None,
        "business_model": None,
        "currency_symbol": "$"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# Progress Bar
def show_progress(current):
    steps = [("1", "Category"), ("2", "Industry"), ("3", "Model")]
    html = '<div class="prog">'
    for i, (num, label) in enumerate(steps):
        n = i + 1
        if n < current:
            pc = "done"
            pl = ""
        elif n == current:
            pc = "curr"
            pl = "curr"
        else:
            pc = "todo"
            pl = ""
        html += f'<div class="ps"><div class="pc {pc}">{num}</div><div class="pl {pl}">{label}</div></div>'
        if i < len(steps) - 1:
            lc = "done" if n < current else "todo"
            html += f'<div class="pline {lc}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# LANDING
# ============================================================
if st.session_state.page == "landing":

    st.markdown("""
    <div class="hero">
        <div class="badge"><div class="badge-dot"></div>Decision Support Tool for India</div>
        <div class="hero-title">Smart Process<br><span class="red">Optimizer</span></div>
        <div class="hero-sub">
            Enter your numbers. SPO tells you what is wrong, why it is wrong,
            and exactly what to do — compared against real Indian industry benchmarks.
        </div>
        <div class="stats">
            <div class="stat"><div class="stat-n">26</div><div class="stat-l">Industries</div></div>
            <div class="stat"><div class="stat-n">3</div><div class="stat-l">Categories</div></div>
            <div class="stat"><div class="stat-n">3</div><div class="stat-l">Currencies</div></div>
            <div class="stat"><div class="stat-n">Free</div><div class="stat-l">Always</div></div>
        </div>
        <div class="feat-grid">
            <div class="feat"><div class="feat-t">Benchmark Analysis</div><div class="feat-d">Compare against real Indian industry standards</div></div>
            <div class="feat"><div class="feat-t">Root Cause Detection</div><div class="feat-d">Understand exactly what is causing your gaps</div></div>
            <div class="feat"><div class="feat-t">Financial Impact</div><div class="feat-d">See how much money you could save</div></div>
            <div class="feat"><div class="feat-t">Priority Actions</div><div class="feat-d">Know exactly what to fix first</div></div>
            <div class="feat"><div class="feat-t">What-If Simulator</div><div class="feat-d">See projected improvements before acting</div></div>
            <div class="feat"><div class="feat-t">Risk Assessment</div><div class="feat-d">Get an overall risk score for your operations</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()

# ============================================================
# CATEGORY
# ============================================================
elif st.session_state.page == "category":
    show_progress(1)
    st.markdown("""
    <div class="step-hdr">
        <div class="step-tag">Step 1 of 3</div>
        <div class="step-ttl">What type of business are you?</div>
        <div class="step-stl">Select the category that best describes your operations</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="opt">', unsafe_allow_html=True)
        st.markdown('<div class="opt-title">Manufacturing</div><div class="opt-desc">Automotive, Electronics, Food, Textile, Pharma and more</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Manufacturing", use_container_width=True):
            st.session_state.category = "Manufacturing"
            st.session_state.page = "industry"
            st.rerun()

    with col2:
        st.markdown('<div class="opt">', unsafe_allow_html=True)
        st.markdown('<div class="opt-title">Distribution</div><div class="opt-desc">Warehouse, Cold Chain, E-commerce, Pharma and more</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Distribution", use_container_width=True):
            st.session_state.category = "Distribution"
            st.session_state.page = "industry"
            st.rerun()

    with col3:
        st.markdown('<div class="opt">', unsafe_allow_html=True)
        st.markdown('<div class="opt-title">Supply Chain</div><div class="opt-desc">Automotive, Food, Electronics, Pharma and more</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Supply Chain", use_container_width=True):
            st.session_state.category = "Supply Chain"
            st.session_state.page = "industry"
            st.rerun()

# ============================================================
# INDUSTRY
# ============================================================
elif st.session_state.page == "industry":
    show_progress(2)
    st.markdown(f"""
    <div class="step-hdr">
        <div class="step-tag">Step 2 of 3</div>
        <div class="step-ttl">What is your industry?</div>
        <div class="step-stl">Select the industry that best matches your {st.session_state.category} business</div>
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

    # Render industry cards in rows of 4
    for i in range(0, len(industries), 4):
        row = industries[i:i+4]
        cols = st.columns(len(row))
        for j, ind in enumerate(row):
            with cols[j]:
                st.markdown(f'<div class="opt-sm"><div class="opt-sm-title">{ind}</div></div>', unsafe_allow_html=True)
                if st.button(ind, key=f"ind_{i}_{j}", use_container_width=True):
                    st.session_state.industry = ind
                    st.session_state.page = "business_model"
                    st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BUSINESS MODEL
# ============================================================
elif st.session_state.page == "business_model":
    show_progress(3)
    st.markdown("""
    <div class="step-hdr">
        <div class="step-tag">Step 3 of 3</div>
        <div class="step-ttl">What is your business model?</div>
        <div class="step-stl">How do you sell your products or services?</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="opt"><div class="opt-title">B2B</div><div class="opt-desc">You sell to other businesses</div></div>', unsafe_allow_html=True)
        if st.button("B2B", use_container_width=True):
            st.session_state.business_model = "B2B"
            st.session_state.page = "analysis"
            st.rerun()

    with col2:
        st.markdown('<div class="opt"><div class="opt-title">B2C</div><div class="opt-desc">You sell directly to consumers</div></div>', unsafe_allow_html=True)
        if st.button("B2C", use_container_width=True):
            st.session_state.business_model = "B2C"
            st.session_state.page = "analysis"
            st.rerun()

    with col3:
        st.markdown('<div class="opt"><div class="opt-title">B2B2C</div><div class="opt-desc">You sell to businesses who sell to consumers</div></div>', unsafe_allow_html=True)
        if st.button("B2B2C", use_container_width=True):
            st.session_state.business_model = "B2B2C"
            st.session_state.page = "analysis"
            st.rerun()

    st.write("")
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "industry"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ANALYSIS
# ============================================================
elif st.session_state.page == "analysis":
    st.markdown(f"""
    <div style="padding: 16px 0 20px; border-bottom: 1px solid #111; margin-bottom: 28px;">
        <div style="font-size: 0.7rem; color: #CC0000; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">Smart Process Optimizer</div>
        <div style="font-size: 1.4rem; color: #fff; font-weight: 800; letter-spacing: -0.5px;">{st.session_state.industry}</div>
        <div style="font-size: 0.78rem; color: #333; margin-top: 2px;">{st.session_state.category} &nbsp;|&nbsp; {st.session_state.business_model}</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar session info
    st.sidebar.markdown(f"""
    <div style="padding: 14px; background: rgba(204,0,0,0.06); border: 1px solid rgba(204,0,0,0.15); border-radius: 10px; margin-bottom: 16px;">
        <div style="color: #CC0000; font-size: 0.65rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">Session</div>
        <div style="color: #fff; font-size: 0.9rem; font-weight: 600;">{st.session_state.industry}</div>
        <div style="color: #444; font-size: 0.78rem; margin-top: 2px;">{st.session_state.category}</div>
        <div style="color: #444; font-size: 0.78rem;">{st.session_state.business_model}</div>
    </div>
    """, unsafe_allow_html=True)

    # Currency selector
    currency_options = {"USD ($)": "$", "INR (₹)": "₹", "GBP (£)": "£"}
    selected_currency = st.sidebar.selectbox("Currency", list(currency_options.keys()), index=0)
    st.session_state.currency_symbol = currency_options[selected_currency]

    st.sidebar.divider()

    if st.sidebar.button("Start Over"):
        for key in ["page", "category", "industry", "business_model", "currency_symbol"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # Load module
    if st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry, st.session_state.currency_symbol)