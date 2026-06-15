# -*- coding: utf-8 -*-
import streamlit as st
from manufacturing import show_manufacturing
from distribution import show_distribution
from supply_chain import show_supply_chain

st.set_page_config(
    page_title="Smart Process Optimizer",
    page_icon="🏭",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #0a0a0a; }

    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 2px solid #CC0000;
    }

    /* Landing */
    .landing-hero {
        background: radial-gradient(ellipse at 50% 0%, #2a0000 0%, #0a0a0a 60%),
                    linear-gradient(180deg, #0a0a0a 0%, #050505 100%);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px;
        position: relative;
        overflow: hidden;
    }

    .landing-hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(circle at 20% 50%, rgba(204,0,0,0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(204,0,0,0.03) 0%, transparent 40%);
        pointer-events: none;
    }

    .grid-bg {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
    }

    .badge {
        background: rgba(204,0,0,0.12);
        border: 1px solid rgba(204,0,0,0.35);
        color: #CC0000;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 28px;
        display: inline-block;
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.05;
        margin-bottom: 20px;
        letter-spacing: -2px;
    }

    .hero-title .red { color: #CC0000; }

    .hero-sub {
        font-size: 1.15rem;
        color: #666666;
        margin-bottom: 48px;
        max-width: 550px;
        line-height: 1.7;
    }

    .stats-row {
        display: flex;
        gap: 48px;
        justify-content: center;
        margin-bottom: 56px;
        flex-wrap: wrap;
    }

    .stat { text-align: center; }
    .stat-n { font-size: 2.2rem; font-weight: 900; color: #CC0000; line-height: 1; }
    .stat-l { font-size: 0.75rem; color: #444444; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }

    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        max-width: 780px;
        margin: 0 auto 56px auto;
    }

    .feat {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 18px;
        text-align: left;
        transition: border-color 0.2s;
    }

    .feat:hover { border-color: rgba(204,0,0,0.3); }
    .feat-icon { font-size: 1.3rem; margin-bottom: 8px; }
    .feat-t { color: #ffffff; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
    .feat-d { color: #444444; font-size: 0.78rem; line-height: 1.5; }

    /* Progress */
    .prog-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin-bottom: 48px;
        padding: 24px 0 0 0;
    }

    .prog-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
    }

    .prog-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .prog-circle.done { background: #CC0000; color: white; }
    .prog-circle.curr { background: rgba(204,0,0,0.15); border: 2px solid #CC0000; color: #CC0000; }
    .prog-circle.todo { background: rgba(255,255,255,0.04); border: 2px solid rgba(255,255,255,0.08); color: #333; }

    .prog-label { font-size: 0.65rem; color: #444; text-transform: uppercase; letter-spacing: 1px; }

    .prog-line {
        width: 48px;
        height: 2px;
        margin: 0 4px;
        margin-bottom: 22px;
    }

    .prog-line.done { background: #CC0000; }
    .prog-line.todo { background: rgba(255,255,255,0.06); }

    /* Step pages */
    .step-hdr { text-align: center; padding: 0 0 40px 0; }
    .step-tag { color: #CC0000; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
    .step-ttl { color: #ffffff; font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
    .step-stl { color: #555; font-size: 0.95rem; }

    /* Category / option cards */
    .opt-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 36px 24px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        height: 100%;
    }

    .opt-card:hover {
        border-color: #CC0000;
        background: rgba(204,0,0,0.05);
        transform: translateY(-2px);
    }

    .opt-icon { font-size: 2.8rem; margin-bottom: 14px; }
    .opt-title { color: #ffffff; font-size: 1.05rem; font-weight: 700; margin-bottom: 8px; }
    .opt-desc { color: #555; font-size: 0.82rem; line-height: 1.55; }

    /* Buttons */
    .stButton button {
        background-color: #CC0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }

    .stButton button:hover {
        background-color: #ff0000 !important;
        transform: translateY(-1px) !important;
    }

    .back-btn button {
        background: transparent !important;
        border: 1px solid #222 !important;
        color: #555 !important;
    }

    .back-btn button:hover {
        border-color: #CC0000 !important;
        color: #CC0000 !important;
        transform: none !important;
    }

    /* Inputs */
    .stNumberInput input, .stTextInput input {
        background: #111 !important;
        border: 1px solid #222 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    .stSelectbox > div > div {
        background: #111 !important;
        border: 1px solid #222 !important;
        color: white !important;
    }

    [data-testid="stMetricValue"] { color: #CC0000 !important; }

    p, li { color: #cccccc !important; }
    h1, h2, h3 { color: #ffffff !important; }
    hr { border-color: #1a1a1a !important; }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #CC0000; border-radius: 3px; }
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
    html = '<div class="prog-wrap">'
    for i, (num, label) in enumerate(steps):
        n = i + 1
        if n < current:
            css = "done"
        elif n == current:
            css = "curr"
        else:
            css = "todo"
        html += f'''
        <div class="prog-step">
            <div class="prog-circle {css}">{num}</div>
            <div class="prog-label">{label}</div>
        </div>'''
        if i < len(steps) - 1:
            line_css = "done" if n < current else "todo"
            html += f'<div class="prog-line {line_css}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# LANDING PAGE
# ============================================================
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-hero">
        <div class="grid-bg"></div>
        <div class="badge">Decision Support Tool — Built for India</div>
        <div class="hero-title">Smart Process<br><span class="red">Optimizer</span></div>
        <div class="hero-sub">
            Enter your numbers. SPO tells you what is wrong, why it is wrong,
            and exactly what to do to fix it — compared against real Indian industry benchmarks.
        </div>
        <div class="stats-row">
            <div class="stat">
                <div class="stat-n">26</div>
                <div class="stat-l">Industries</div>
            </div>
            <div class="stat">
                <div class="stat-n">3</div>
                <div class="stat-l">Categories</div>
            </div>
            <div class="stat">
                <div class="stat-n">100%</div>
                <div class="stat-l">India Benchmarks</div>
            </div>
            <div class="stat">
                <div class="stat-n">Free</div>
                <div class="stat-l">Always</div>
            </div>
        </div>
        <div class="features">
            <div class="feat">
                <div class="feat-icon">📊</div>
                <div class="feat-t">Benchmark Analysis</div>
                <div class="feat-d">Compare against real Indian industry standards</div>
            </div>
            <div class="feat">
                <div class="feat-icon">🔍</div>
                <div class="feat-t">Root Cause Detection</div>
                <div class="feat-d">Understand exactly what is causing your gaps</div>
            </div>
            <div class="feat">
                <div class="feat-icon">💰</div>
                <div class="feat-t">Financial Impact</div>
                <div class="feat-d">See how much money you could save</div>
            </div>
            <div class="feat">
                <div class="feat-icon">🎯</div>
                <div class="feat-t">Priority Actions</div>
                <div class="feat-d">Know exactly what to fix first</div>
            </div>
            <div class="feat">
                <div class="feat-icon">🔮</div>
                <div class="feat-t">What-If Simulator</div>
                <div class="feat-d">See projected improvements before acting</div>
            </div>
            <div class="feat">
                <div class="feat-icon">⚠️</div>
                <div class="feat-t">Risk Assessment</div>
                <div class="feat-d">Get an overall risk score for your operations</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()

# ============================================================
# CATEGORY PAGE
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
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">🏭</div>
            <div class="opt-title">Manufacturing</div>
            <div class="opt-desc">Automotive, Electronics, Food, Textile, Pharma and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manufacturing", use_container_width=True):
            st.session_state.category = "Manufacturing"
            st.session_state.page = "industry"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">📦</div>
            <div class="opt-title">Distribution</div>
            <div class="opt-desc">Warehouse, Cold Chain, E-commerce, Pharma and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Distribution", use_container_width=True):
            st.session_state.category = "Distribution"
            st.session_state.page = "industry"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">🔗</div>
            <div class="opt-title">Supply Chain</div>
            <div class="opt-desc">Automotive, Food, Electronics, Pharma and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Supply Chain", use_container_width=True):
            st.session_state.category = "Supply Chain"
            st.session_state.page = "industry"
            st.rerun()

# ============================================================
# INDUSTRY PAGE
# ============================================================
elif st.session_state.page == "industry":
    show_progress(2)
    st.markdown(f"""
    <div class="step-hdr">
        <div class="step-tag">Step 2 of 3</div>
        <div class="step-ttl">What is your industry?</div>
        <div class="step-stl">Select the industry that best matches your business</div>
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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected = st.selectbox("", industries, label_visibility="collapsed")
        st.session_state.industry = selected
        st.write("")

        if st.button("Continue", use_container_width=True):
            st.session_state.page = "business_model"
            st.rerun()

        st.write("")
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BUSINESS MODEL PAGE
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
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">🏢</div>
            <div class="opt-title">B2B</div>
            <div class="opt-desc">You sell to other businesses</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("B2B", use_container_width=True):
            st.session_state.business_model = "B2B"
            st.session_state.page = "analysis"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">🛒</div>
            <div class="opt-title">B2C</div>
            <div class="opt-desc">You sell directly to consumers</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("B2C", use_container_width=True):
            st.session_state.business_model = "B2C"
            st.session_state.page = "analysis"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="opt-card">
            <div class="opt-icon">🔄</div>
            <div class="opt-title">B2B2C</div>
            <div class="opt-desc">You sell to businesses who sell to consumers</div>
        </div>
        """, unsafe_allow_html=True)
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
# ANALYSIS PAGE
# ============================================================
elif st.session_state.page == "analysis":
    st.markdown(f"""
    <div style="padding: 16px 0 20px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 24px;">
        <h1 style="color: #CC0000; margin: 0; font-size: 1.6rem; font-weight: 900;">Smart Process Optimizer</h1>
        <p style="color: #444; margin: 4px 0 0 0; font-size: 0.8rem;">
            {st.session_state.category} &nbsp;&nbsp;|&nbsp;&nbsp; {st.session_state.industry} &nbsp;&nbsp;|&nbsp;&nbsp; {st.session_state.business_model}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="padding: 12px; background: rgba(204,0,0,0.08); border: 1px solid rgba(204,0,0,0.25); border-radius: 8px; margin-bottom: 16px;">
        <p style="color: #CC0000; font-size: 0.7rem; font-weight: 700; margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 1px;">Current Session</p>
        <p style="color: #fff; font-size: 0.85rem; margin: 0; font-weight: 600;">{st.session_state.industry}</p>
        <p style="color: #666; font-size: 0.78rem; margin: 2px 0 0 0;">{st.session_state.category} &nbsp;|&nbsp; {st.session_state.business_model}</p>
    </div>
    """, unsafe_allow_html=True)

    # Currency selector in sidebar
    currency_options = {"USD ($)": "$", "INR (₹)": "₹", "GBP (£)": "£"}
    selected_currency = st.sidebar.selectbox(
        "Currency",
        list(currency_options.keys()),
        index=0
    )
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