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

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False
if "category" not in st.session_state:
    st.session_state.category = None
if "industry" not in st.session_state:
    st.session_state.industry = None
if "business_model" not in st.session_state:
    st.session_state.business_model = None
if "currency_symbol" not in st.session_state:
    st.session_state.currency_symbol = "$"

if not st.session_state.onboarded:
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="color: #CC0000; font-size: 3rem; font-weight: 900;">Smart Process Optimizer</h1>
            <p style="color: #cccccc; font-size: 1.2rem;">A Decision Support Tool for Manufacturing, Distribution and Supply Chain</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>Let us get started — tell us about your business</h2>", unsafe_allow_html=True)
    st.write("")

    st.subheader("Step 1 — What is your business category?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Manufacturing", use_container_width=True):
            st.session_state.category = "Manufacturing"
    with col2:
        if st.button("Distribution", use_container_width=True):
            st.session_state.category = "Distribution"
    with col3:
        if st.button("Supply Chain", use_container_width=True):
            st.session_state.category = "Supply Chain"

    if st.session_state.category:
        st.success(f"Selected: {st.session_state.category}")
        st.write("")

        st.subheader("Step 2 — What is your industry?")

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

        industry = st.selectbox("Select your industry", industries)
        st.session_state.industry = industry
        st.write("")

        st.subheader("Step 3 — What is your business model?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("B2B", use_container_width=True):
                st.session_state.business_model = "B2B"
        with col2:
            if st.button("B2C", use_container_width=True):
                st.session_state.business_model = "B2C"
        with col3:
            if st.button("B2B2C", use_container_width=True):
                st.session_state.business_model = "B2B2C"

        if st.session_state.business_model:
            st.success(f"Selected: {st.session_state.business_model}")
            st.write("")

            st.subheader("Step 4 — Select your currency")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("USD ($)", use_container_width=True):
                    st.session_state.currency_symbol = "$"
            with col2:
                if st.button("INR (₹)", use_container_width=True):
                    st.session_state.currency_symbol = "₹"
            with col3:
                if st.button("GBP (£)", use_container_width=True):
                    st.session_state.currency_symbol = "£"

            if st.session_state.currency_symbol:
                st.success(f"Selected: {st.session_state.currency_symbol}")
                st.write("")

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Start Optimizing", use_container_width=True):
                        st.session_state.onboarded = True
                        st.rerun()

else:
    st.markdown(f"""
        <div style="padding: 20px 0;">
            <h1 style="color: #CC0000;">Smart Process Optimizer</h1>
            <p style="color: #cccccc;">Category: {st.session_state.category} | Industry: {st.session_state.industry} | Model: {st.session_state.business_model} | Currency: {st.session_state.currency_symbol}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("Start Over"):
        st.session_state.onboarded = False
        st.session_state.category = None
        st.session_state.industry = None
        st.session_state.business_model = None
        st.session_state.currency_symbol = "$"
        st.rerun()

    st.divider()

    if st.session_state.category == "Manufacturing":
        show_manufacturing(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Distribution":
        show_distribution(st.session_state.industry, st.session_state.currency_symbol)
    elif st.session_state.category == "Supply Chain":
        show_supply_chain(st.session_state.industry, st.session_state.currency_symbol)