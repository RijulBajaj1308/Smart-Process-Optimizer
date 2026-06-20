# -*- coding: utf-8 -*-
import streamlit as st
from supabase import create_client, Client
import json
from datetime import datetime

@st.cache_resource
def get_supabase_client():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        url = "https://xrohccbmvunplgvyzhcz.supabase.co"
        key = "sb_publishable_PYOnL43Surm8oiOpaIipsw_6nC8FImI"
    return create_client(url, key)

def sign_up(email, password, full_name):
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": full_name}}
        })
        if response.user:
            return True, "Account created successfully!"
        return False, "Sign up failed. Please try again."
    except Exception as e:
        return False, str(e)

def sign_in(email, password):
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response.user:
            st.session_state.user = response.user
            st.session_state.session = response.session
            return True, "Logged in successfully!"
        return False, "Invalid email or password."
    except Exception as e:
        return False, "Invalid email or password."

def sign_out():
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except:
        pass
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def get_current_user():
    return st.session_state.get("user", None)

def create_company(name, category, industry, business_model):
    try:
        supabase = get_supabase_client()
        user = get_current_user()
        if not user:
            return None
        response = supabase.table("companies").insert({
            "user_id": user.id,
            "name": name,
            "category": category,
            "industry": industry,
            "business_model": business_model,
        }).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error creating company: {e}")
        return None

def get_companies():
    try:
        supabase = get_supabase_client()
        user = get_current_user()
        if not user:
            return []
        response = supabase.table("companies").select("*").eq("user_id", user.id).order("updated_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        return []

def save_analysis(company_id, analysis_type, kpi_data, results, risk_score, risk_label):
    try:
        supabase = get_supabase_client()
        user = get_current_user()
        if not user:
            return None
        response = supabase.table("analyses").insert({
            "company_id": company_id,
            "user_id": user.id,
            "analysis_type": analysis_type,
            "kpi_data": json.dumps(kpi_data),
            "results": json.dumps(results),
            "risk_score": risk_score,
            "risk_label": risk_label,
        }).execute()
        # Update company updated_at
        supabase.table("companies").update({
            "updated_at": datetime.now().isoformat()
        }).eq("id", company_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        return None

def get_analyses(company_id):
    try:
        supabase = get_supabase_client()
        response = supabase.table("analyses").select("*").eq("company_id", company_id).order("created_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        return []

def delete_company(company_id):
    try:
        supabase = get_supabase_client()
        supabase.table("analyses").delete().eq("company_id", company_id).execute()
        supabase.table("companies").delete().eq("id", company_id).execute()
        return True
    except Exception as e:
        return False