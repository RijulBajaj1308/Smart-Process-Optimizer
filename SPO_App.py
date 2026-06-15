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

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0a0a0a;
    }

    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 2px solid #CC0000;
    }

    /* Landing Page */
    .landing-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 60px 20px;
        background: radial-gradient(ellipse at top, #1a0000 0%, #0a0a0a 50%, #000510 100%);
    }

    .landing-badge {
        background: rgba(204, 0, 0, 0.15);
        border: 1px solid rgba(204, 0, 0, 0.4);
        color: #CC0000;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        display: inline-block;
    }

    .landing-title {
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .landing-title span {
        color: #CC0000;
    }

    .landing-subtitle {
        font-size: 1.3rem;
        color: #888888;
        margin-bottom: 16px;
        font-weight: 300;
    }

    .landing-description {
        font-size: 1rem;
        color: #555555;
        max-width: 600px;
        margin: 0 auto 48px auto;
        line-height: 1.8;
    }

    .stat-grid {
        display: flex;
        gap: 40px;
        justify-content: center;
        margin-bottom: 48px;
        flex-wrap: wrap;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 900;
        color: #CC0000;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #555555;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        max-width: 800px;
        margin: 0 auto 48px auto;
    }

    .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 20px;
        text-align: left;
    }

    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
    }

    .feature-title {
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .feature-desc {
        color: #555555;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    /* Progress Bar */
    .progress-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 40px;
        justify-content: center;
    }

    .progress-step {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .progress-step.completed {
        background: #CC0000;
        color: white;
    }

    .progress-step.active {
        background: rgba(204,0,0,0.2);
        border: 2px solid #CC0000;
        color: #CC0000;
    }

    .progress-step.inactive {
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(255,255,255,0.1);
        color: #444444;
    }

    .progress-line {
        height: 2px;
        width: 40px;
        background: rgba(255,255,255,0.1);
    }

    .progress-line.completed {
        background: #CC0000;
    }

    /* Step Pages */
    .step-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 40px 20px;
        text-align: center;
    }

    .step-label {
        color: #CC0000;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .step-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .step-subtitle {
        color: #666666;
        font-size: 1rem;
        margin-bottom: 40px;
    }

    /* Option Cards */
    .option-grid {
        display: grid;
        gap: 12px;
        margin-bottom: 32px;
    }

    .option-grid-3 {
        grid-template-columns: repeat(3, 1fr);
    }

    .option-grid-2 {
        grid-template-columns: repeat(2, 1fr);
    }

    /* Selected State */
    .selected-pill {
        background: rgba(204,0,0,0.15);
        border: 1px solid #CC0000;
        color: #CC0000;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 24px;
    }

    /* Buttons */
    .stButton button {
        background-color: #CC0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 12px 24px !important;
        transition: all 0.2s !important;
    }

    .stButton button:hover {
        background-color: #ff0000 !important;
        transform: translateY(-1px) !important;
    }

    /* Input styling */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Divider */
    hr {
        border-color: #1a1a1a !important;
    }

    /* Text */
    p, li {
        color: #cccccc !important;
    }

    h1, h2, h3 {
        color: #ffffff !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        color: white !important;
    }

    /* Metric */
    [data-testid="stMetricValue"] {
        color: #CC0000 !important;
    }

    /* Caption */
    .stCaption {
        color: #555555 !important;
    }

    /* Back button style */
    .back-btn button {
        background-color: transparent !important;
        border: 1px solid #333333 !important;
        color: #666666 !important;
    }

    .back-btn button:hover {
        border-color: #CC0000 !important;
        color: #CC0000 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    ::-webkit-scrollbar-thumb {
        background: #CC0000;
        border-radius: 3px;
    }
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

# Progress Bar Component
def show_progress(current_step, total_steps=5):
    steps = ["Category", "Industry", "Model", "Currency", "Analysis"]
    html = '<div class="progress-container">'
    for i, step in enumerate(steps):
        step_num = i + 1
        if step_num < current_step:
            css = "completed"
        elif step_num == current_step:
            css = "active"
        else:
            css = "inactive"

        html += f'<div class="progress-step {css}">{step_num}</div>'
        if i < len(steps) - 1:
            line_css = "completed" if step_num < current_step else ""
            html += f'<div class="progress-line {line_css}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# PAGE 1: LANDING
# ============================================================
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-container">
        <div class="landing-badge">AI-Powered Decision Support</div>
        <div class="landing-title">Smart Process<br><span>Optimizer</span></div>
        <div class="landing-subtitle">Know what is wrong. Know what to do. See the numbers.</div>
        <div class="landing-description">
            Enter your business performance numbers and SPO instantly tells you where you stand against
            industry benchmarks, what is causing your problems, and exactly what to do to fix them.
            Built for Manufacturing, Distribution and Supply Chain businesses in India.
        </div>
        <div class="stat-grid">
            <div class="stat-item">
                <div class="stat-number">26</div>
                <div class="stat-label">Industries Covered</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">Business Categories</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">Currencies Supported</div>
            </div>
        </div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Benchmark Analysis</div>
                <div class="feature-desc">Compare your numbers against real Indian industry standards</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Root Cause Detection</div>
                <div class="feature-desc">Understand exactly what is causing your performance gaps</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💰</div>
                <div class="feature-title">Financial Impact</div>
                <div class="feature-desc">See how much money you could save by fixing each problem</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Priority Actions</div>
                <div class="feature-desc">Know exactly what to fix first for maximum impact</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔮</div>
                <div class="feature-title">What-If Simulator</div>
                <div class="feature-desc">Play with numbers to see projected improvements before acting</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚠️</div>
                <div class="feature-title">Risk Assessment</div>
                <div class="feature-desc">Get an overall risk score for your operations</div>
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
# PAGE 2: CATEGORY
# ============================================================
elif st.session_state.page == "category":
    show_progress(1)
    st.markdown("""
    <div class="step-container">
        <div class="step-label">Step 1 of 4</div>
        <div class="step-title">What type of business are you?</div>
        <div class="step-subtitle">Select the category that best describes your operations</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🏭</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">Manufacturing</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">Automotive, Electronics, Food and Beverage, Textile, Pharma and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Manufacturing", use_container_width=True):
            st.session_state.category = "Manufacturing"
            st.session_state.page = "industry"
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📦</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">Distribution</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">Warehouse, Cold Chain, E-commerce, Pharma Distribution and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Distribution", use_container_width=True):
            st.session_state.category = "Distribution"
            st.session_state.page = "industry"
            st.rerun()

    with col3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🔗</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">Supply Chain</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">Automotive, Food, Electronics, Pharma Supply Chain and more</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Supply Chain", use_container_width=True):
            st.session_state.category = "Supply Chain"
            st.session_state.page = "industry"
            st.rerun()

# ============================================================
# PAGE 3: INDUSTRY
# ============================================================
elif st.session_state.page == "industry":
    show_progress(2)
    st.markdown(f"""
    <div class="step-container">
        <div class="step-label">Step 2 of 4</div>
        <div class="step-title">What is your industry?</div>
        <div class="step-subtitle">Select the industry that best matches your business</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.category == "Manufacturing":
        industries = [
            "Automotive",
            "Electronics",
            "Food and Beverage",
            "Textile and Apparel",
            "General Manufacturing",
            "Eco Friendly Packaging",
            "Pulp and Paper Manufacturing",
            "Pharmaceutical Manufacturing"
        ]
    elif st.session_state.category == "Distribution":
        industries = [
            "Warehouse and Distribution",
            "Cold Chain Distribution",
            "E-commerce Fulfillment",
            "Pharmaceutical Distribution",
            "Automotive Parts Distribution",
            "Electronics Distribution",
            "Food and Beverage Distribution",
            "Textile and Apparel Distribution",
            "Eco Friendly Packaging Distribution",
            "Pulp and Paper Distribution"
        ]
    else:
        industries = [
            "Automotive Supply Chain",
            "Food and Beverage Supply Chain",
            "Electronics Supply Chain",
            "General Supply Chain",
            "Pharmaceutical Supply Chain",
            "Textile and Apparel Supply Chain",
            "Eco Friendly Packaging Supply Chain",
            "Pulp and Paper Supply Chain"
        ]

    selected = st.selectbox("Select your industry", industries)
    st.session_state.industry = selected
    st.write("")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("Back", use_container_width=True):
            st.session_state.page = "category"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Continue", use_container_width=True):
            st.session_state.page = "business_model"
            st.rerun()

# ============================================================
# PAGE 4: BUSINESS MODEL
# ============================================================
elif st.session_state.page == "business_model":
    show_progress(3)
    st.markdown("""
    <div class="step-container">
        <div class="step-label">Step 3 of 4</div>
        <div class="step-title">What is your business model?</div>
        <div class="step-subtitle">How do you sell your products or services?</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🏢</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">B2B</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">You sell to other businesses</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select B2B", use_container_width=True):
            st.session_state.business_model = "B2B"
            st.session_state.page = "currency"
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🛒</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">B2C</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">You sell directly to consumers</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select B2C", use_container_width=True):
            st.session_state.business_model = "B2C"
            st.session_state.page = "currency"
            st.rerun()

    with col3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🔄</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">B2B2C</div>
            <div style="color: #555555; font-size: 0.85rem; line-height: 1.5;">You sell to businesses who sell to consumers</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select B2B2C", use_container_width=True):
            st.session_state.business_model = "B2B2C"
            st.session_state.page = "currency"
            st.rerun()

    st.write("")
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state.page = "industry"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE 5: CURRENCY
# ============================================================
elif st.session_state.page == "currency":
    show_progress(4)
    st.markdown("""
    <div class="step-container">
        <div class="step-label">Step 4 of 4</div>
        <div class="step-title">Select your currency</div>
        <div class="step-subtitle">All financial calculations will use this currency</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🇺🇸</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">USD</div>
            <div style="color: #555555; font-size: 0.85rem;">US Dollar ($)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select USD", use_container_width=True):
            st.session_state.currency_symbol = "$"
            st.session_state.page = "analysis"
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🇮🇳</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">INR</div>
            <div style="color: #555555; font-size: 0.85rem;">Indian Rupee (₹)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select INR", use_container_width=True):
            st.session_state.currency_symbol = "₹"
            st.session_state.page = "analysis"
            st.rerun()

    with col3:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 32px 20px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🇬🇧</div>
            <div style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">GBP</div>
            <div style="color: #555555; font-size: 0.85rem;">British Pound (£)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select GBP", use_container_width=True):
            st.session_state.currency_symbol = "£"
            st.session_state.page = "analysis"
            st.rerun()

    st.write("")
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state.page = "business_model"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE 6: ANALYSIS
# ============================================================
elif st.session_state.page == "analysis":
    # Header
    st.markdown(f"""
    <div style="padding: 20px 0 10px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h1 style="color: #CC0000; margin: 0; font-size: 1.8rem; font-weight: 900;">Smart Process Optimizer</h1>
                <p style="color: #444444; margin: 4px 0 0 0; font-size: 0.85rem;">
                    {st.session_state.category} &nbsp;|&nbsp; {st.session_state.industry} &nbsp;|&nbsp; {st.session_state.business_model} &nbsp;|&nbsp; {st.session_state.currency_symbol}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Start Over button in sidebar
    if st.sidebar.button("Start Over"):
        for key in ["page", "category", "industry", "business_model", "currency_symbol"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.sidebar.markdown(f"""
    <div style="padding: 12px; background: rgba(204,0,0,0.1); border: 1px solid rgba(204,0,0,0.3); border-radius: 8px; margin-bottom: 16px;">
        <p style="color: #CC0000; font-size: 0.75rem; font-weight: 600; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 1px;">Your Session</p>
        <p style="color: #ffffff; font-size: 0.85rem; margin: 0;">{st.session_state.category}</p>
        <p style="color: #888888; font-size: 0.8rem; margin: 0;">{st.session_state.industry}</p>
        <p style="color: #888888; font-size: 0.8rem; margin: 0;">{st.session_state.business_model} &nbsp;|&nbsp; {st.session_state.currency_symbol}</p>
    </div>
    """, unsafe_allow_html=True)

    # Load correct module
    if st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry, st.session_state.currency_symbol)