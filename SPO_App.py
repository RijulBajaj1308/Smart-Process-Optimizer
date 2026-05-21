import streamlit as st
from manufacturing import show_manufacturing
from distribution import show_distribution
from supply_chain import show_supply_chain

# Page configuration
st.set_page_config(
    page_title="Smart Process Optimizer",
    page_icon="🏭",
    layout="wide"
)

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Session state for onboarding
if "onboarded" not in st.session_state:
    st.session_state.onboarded = False
if "category" not in st.session_state:
    st.session_state.category = None
if "industry" not in st.session_state:
    st.session_state.industry = None
if "business_model" not in st.session_state:
    st.session_state.business_model = None

# Onboarding Screen
if not st.session_state.onboarded:
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="color: #CC0000; font-size: 3rem; font-weight: 900;">🏭 Smart Process Optimizer</h1>
            <p style="color: #cccccc; font-size: 1.2rem;">A Decision Support Tool for Manufacturing, Distribution and Supply Chain</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<h2 style='text-align: center; color: #ffffff;'>Let's get started — tell us about your business</h2>", unsafe_allow_html=True)
    st.write("")

    # Step 1 - Business Category
    st.subheader("Step 1 — What is your business category?")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏭 Manufacturing", use_container_width=True):
            st.session_state.category = "Manufacturing"

    with col2:
        if st.button("📦 Distribution", use_container_width=True):
            st.session_state.category = "Distribution"

    with col3:
        if st.button("🔗 Supply Chain", use_container_width=True):
            st.session_state.category = "Supply Chain"

    if st.session_state.category:
        st.success(f"Selected: {st.session_state.category}")
        st.write("")

        # Step 2 - Industry
        st.subheader("Step 2 — What is your industry?")

        if st.session_state.category == "Manufacturing":
            industries = ["Automotive", "Electronics", "Food and Beverage", "Textile and Apparel", "General Manufacturing"]
        elif st.session_state.category == "Distribution":
            industries = ["Warehouse and Distribution", "Cold Chain Distribution", "E-commerce Fulfillment"]
        else:
            industries = ["Automotive Supply Chain", "Food and Beverage Supply Chain", "Electronics Supply Chain", "General Supply Chain"]

        industry = st.selectbox("Select your industry", industries)
        st.session_state.industry = industry
        st.write("")

        # Step 3 - Business Model
        st.subheader("Step 3 — What is your business model?")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🏢 B2B", use_container_width=True):
                st.session_state.business_model = "B2B"
        with col2:
            if st.button("🛒 B2C", use_container_width=True):
                st.session_state.business_model = "B2C"
        with col3:
            if st.button("🔄 B2B2C", use_container_width=True):
                st.session_state.business_model = "B2B2C"

        if st.session_state.business_model:
            st.success(f"Selected: {st.session_state.business_model}")
            st.write("")

            # Start Button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Start Optimizing", use_container_width=True):
                    st.session_state.onboarded = True
                    st.rerun()

# Main App
else:
    # Header
    st.markdown(f"""
        <div style="padding: 20px 0;">
            <h1 style="color: #CC0000;">🏭 Smart Process Optimizer</h1>
            <p style="color: #cccccc;">Category: {st.session_state.category} | Industry: {st.session_state.industry} | Model: {st.session_state.business_model}</p>
        </div>
    """, unsafe_allow_html=True)

    # Reset button
    if st.sidebar.button("🔄 Start Over"):
        st.session_state.onboarded = False
        st.session_state.category = None
        st.session_state.industry = None
        st.session_state.business_model = None
        st.rerun()

    st.divider()

    # Load correct module
    if st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry)