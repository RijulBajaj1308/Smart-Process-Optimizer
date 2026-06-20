# -*- coding: utf-8 -*-
import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from reportlab.platypus import Image as RLImage
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from datetime import datetime
import io


def make_bar_chart(x_labels, y_values, colors_list, title, ylabel="", benchmark=None):
    fig, ax = plt.subplots(figsize=(8, 3.2))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f9f9f9")
    bars = ax.bar(x_labels, y_values, color=colors_list, alpha=0.9)
    for bar, val in zip(bars, y_values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                f"{val:.1f}", ha="center", va="bottom", fontsize=8)
    if benchmark:
        ax.axhline(y=benchmark, color="#000000", linestyle="--", linewidth=1.5, label=f"Target: {benchmark}")
        ax.legend(fontsize=8)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=15, ha="right", fontsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    plt.close()
    return buf


def make_pie_chart(labels, values, colors_list, title):
    fig, ax = plt.subplots(figsize=(5, 3.2))
    fig.patch.set_facecolor("#ffffff")
    non_zero = [(l, v, c) for l, v, c in zip(labels, values, colors_list) if v > 0]
    if non_zero:
        lbls, vals, clrs = zip(*non_zero)
        ax.pie(vals, labels=lbls, colors=clrs, autopct="%1.1f%%", startangle=90,
               textprops={"fontsize": 8})
    ax.set_title(title, fontsize=10, fontweight="bold")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    plt.close()
    return buf


def generate_pdf(company_name, industry, tool_name, data_rows, insights, currency_symbol, chart_buf=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.7*inch, rightMargin=0.7*inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle('T', parent=styles['Title'], textColor=colors.HexColor('#CC0000'), fontSize=20, spaceAfter=2)
    sub_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#555555'), spaceAfter=14)
    heading_style = ParagraphStyle('H', parent=styles['Heading2'], textColor=colors.HexColor('#CC0000'), fontSize=13, spaceBefore=16, spaceAfter=8)
    body_style = ParagraphStyle('B', parent=styles['Normal'], fontSize=9.5, leading=14, spaceAfter=8, alignment=TA_LEFT)
    footer_style = ParagraphStyle('F', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#999999'))

    elements.append(Paragraph("Smart Process Optimizer", title_style))
    elements.append(Paragraph(f"Deep Analysis Report — {tool_name}", sub_style))

    meta = [
        ["Company / Facility", company_name],
        ["Industry", industry],
        ["Analysis Tool", tool_name],
        ["Report Date", datetime.now().strftime("%B %d, %Y")],
    ]
    meta_table = Table(meta, colWidths=[1.7*inch, 4.3*inch])
    meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#CC0000')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 4))
    elements.append(Table([['']], colWidths=[6*inch], style=[('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#CC0000'))]))

    if chart_buf:
        elements.append(Paragraph("Analysis Chart", heading_style))
        elements.append(RLImage(chart_buf, width=6.5*inch, height=3*inch))
        elements.append(Spacer(1, 8))

    if data_rows:
        elements.append(Paragraph("Analysis Data", heading_style))
        t = Table(data_rows, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t)

    if insights:
        elements.append(Paragraph("Key Insights and Recommendations", heading_style))
        for insight in insights:
            elements.append(Paragraph(f"&bull; {insight}", body_style))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Generated by Smart Process Optimizer (SPO) - smart-process-optimizer.streamlit.app", footer_style))
    doc.build(elements)
    buffer.seek(0)
    return buffer


def show_distribution_deep(industry, currency_symbol="$"):
    st.markdown("""
    <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;">
        <p style="color: #E8001D; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 4px 0;">Deep Analysis Mode</p>
        <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Enter detailed operational data to pinpoint exactly where your distribution is losing time and money.</p>
    </div>
    """, unsafe_allow_html=True)

    tool = st.selectbox(
        "Select a Deep Analysis Tool",
        [
            "Delivery Route Efficiency",
            "Order Picking Time Analysis",
            "Warehouse Slotting Analysis",
            "Returns Root Cause Analysis"
        ]
    )

    company_name = st.text_input("Company / Facility Name", placeholder="e.g. Delhivery Hub - Noida")
    st.divider()

    # ════════════════════════════════════════
    # TOOL 1: DELIVERY ROUTE EFFICIENCY
    # ════════════════════════════════════════
    if tool == "Delivery Route Efficiency":
        st.header("Delivery Route Efficiency")
        st.write("Analyze how efficiently your delivery routes are being used. Find which routes are costing you the most per delivery.")

        col1, col2 = st.columns(2)
        with col1:
            num_routes = st.number_input("Number of Delivery Routes", min_value=2, max_value=15, value=5, step=1)
            vehicle_capacity = st.number_input("Vehicle Capacity (max orders per trip)", min_value=1, max_value=200, value=50, step=1)
        with col2:
            fuel_cost_per_km = st.number_input(f"Fuel Cost per KM ({currency_symbol})", min_value=0.1, max_value=100.0, value=8.0, step=0.1, format="%.1f")
            driver_cost_per_day = st.number_input(f"Driver Cost per Day ({currency_symbol})", min_value=0.0, value=800.0, step=50.0)

        st.write("")
        st.subheader("Enter Route Data")

        routes = []
        for i in range(int(num_routes)):
            with st.expander(f"Route {i+1}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    name = st.text_input("Route Name", value=f"Route {i+1}", key=f"rname_{i}")
                with col2:
                    distance = st.number_input("Distance (KM)", min_value=1.0, value=float(20 + i*10), step=1.0, key=f"rdist_{i}")
                with col3:
                    orders = st.number_input("Orders Delivered", min_value=1, value=max(5, 40 - i*5), step=1, key=f"rorders_{i}")
                with col4:
                    on_time = st.number_input("On Time Deliveries", min_value=0, value=max(4, orders-2), step=1, key=f"rontime_{i}")
                routes.append({"name": name, "distance": distance, "orders": orders, "on_time": on_time})

        if routes:
            st.divider()
            st.header("Route Efficiency Results")

            total_orders = sum(r["orders"] for r in routes)
            total_distance = sum(r["distance"] for r in routes)
            total_on_time = sum(r["on_time"] for r in routes)
            overall_otd = (total_on_time / total_orders * 100) if total_orders > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #ffffff;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Total Orders</p>
                    <p style="color:#ffffff;font-size:2rem;font-weight:900;margin:8px 0;">{total_orders}</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #ffffff;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Total Distance</p>
                    <p style="color:#ffffff;font-size:2rem;font-weight:900;margin:8px 0;">{total_distance:.0f} KM</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                otd_color = "#00CC00" if overall_otd >= 92 else "#FFD700" if overall_otd >= 80 else "#CC0000"
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {otd_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Overall OTD</p>
                    <p style="color:{otd_color};font-size:2rem;font-weight:900;margin:8px 0;">{overall_otd:.1f}%</p>
                </div>""", unsafe_allow_html=True)
            with col4:
                total_fuel = total_distance * fuel_cost_per_km
                total_cost = total_fuel + (driver_cost_per_day * num_routes)
                cost_per_order = total_cost / total_orders if total_orders > 0 else 0
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #FFD700;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Cost per Order</p>
                    <p style="color:#FFD700;font-size:2rem;font-weight:900;margin:8px 0;">{currency_symbol}{cost_per_order:.0f}</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            route_data = []
            insights = []
            data_rows = [["Route", "Orders", "OTD %"]]
            for r in routes:
                utilization = (r["orders"] / vehicle_capacity) * 100
                otd_pct = (r["on_time"] / r["orders"] * 100) if r["orders"] > 0 else 0
                route_cost = (r["distance"] * fuel_cost_per_km) + driver_cost_per_day
                cpo = route_cost / r["orders"] if r["orders"] > 0 else 0
                route_data.append({
                    "name": r["name"],
                    "orders": r["orders"],
                    "utilization": utilization,
                    "otd": otd_pct,
                    "cpo": cpo
                })
                data_rows.append([r["name"], str(r["orders"]), f"{otd_pct:.1f}%"])

            worst_utilization = min(route_data, key=lambda x: x["utilization"])
            worst_otd = min(route_data, key=lambda x: x["otd"])
            most_expensive = max(route_data, key=lambda x: x["cpo"])

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Vehicle Utilization %",
                x=[r["name"] for r in route_data],
                y=[r["utilization"] for r in route_data],
                marker_color=["#CC0000" if r["utilization"] < 60 else "#FFD700" if r["utilization"] < 80 else "#00CC00" for r in route_data],
                text=[f"{r['utilization']:.0f}%" for r in route_data],
                textposition="outside"
            ))
            fig.add_hline(y=80, line_dash="dash", line_color="#ffffff",
                         annotation_text="80% Utilization Target",
                         annotation_position="top right")
            fig.update_layout(
                title="Vehicle Utilization by Route",
                yaxis_title="Utilization (%)",
                yaxis_range=[0, 120],
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Route by Route Breakdown")
            for r in route_data:
                util_color = "#CC0000" if r["utilization"] < 60 else "#FFD700" if r["utilization"] < 80 else "#00CC00"
                otd_color = "#CC0000" if r["otd"] < 80 else "#FFD700" if r["otd"] < 92 else "#00CC00"
                st.markdown(f"""
                <div style="background:#1a1a1a;border-left:4px solid {util_color};padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                    <span style="color:#ffffff;font-weight:700;">{r['name']}</span>
                    <span style="color:#888;margin-left:12px;font-size:0.82rem;">Orders: {r['orders']} | Utilization: <span style="color:{util_color}">{r['utilization']:.0f}%</span> | OTD: <span style="color:{otd_color}">{r['otd']:.1f}%</span> | Cost per Order: {currency_symbol}{r['cpo']:.0f}</span>
                </div>
                """, unsafe_allow_html=True)

            if worst_utilization["utilization"] < 60:
                insights.append(f"{worst_utilization['name']} has only {worst_utilization['utilization']:.0f}% vehicle utilization — you are paying for a full vehicle run but only using {worst_utilization['utilization']:.0f}% of its capacity. Consolidate this route with an adjacent one or increase order density before dispatching.")
            if worst_otd["otd"] < 85:
                insights.append(f"{worst_otd['name']} has the lowest on time delivery rate at {worst_otd['otd']:.1f}%. Investigate whether this is a traffic, scheduling or capacity issue on this specific route.")
            insights.append(f"Your most expensive route is {most_expensive['name']} at {currency_symbol}{most_expensive['cpo']:.0f} per order. Review if orders on this route can be batched more efficiently.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    [r["name"] for r in route_data],
                    [r["utilization"] for r in route_data],
                    ["#CC0000" if r["utilization"] < 60 else "#FFD700" if r["utilization"] < 80 else "#00CC00" for r in route_data],
                    "Vehicle Utilization by Route (%)",
                    ylabel="Utilization (%)",
                    benchmark=80
                )
                pdf = generate_pdf(
                    company_name or "Unnamed Company",
                    industry, tool, data_rows, insights, currency_symbol, chart_buf=chart
                )
                st.download_button(
                    label="Download PDF Report",
                    data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    # ════════════════════════════════════════
    # TOOL 2: ORDER PICKING TIME ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Order Picking Time Analysis":
        st.header("Order Picking Time Analysis")
        st.write("Analyze how long it takes to pick different order types and identify where your picking process is losing time.")

        col1, col2 = st.columns(2)
        with col1:
            shift_hours = st.number_input("Shift Hours", min_value=1.0, max_value=12.0, value=8.0, step=0.5)
            num_pickers = st.number_input("Number of Pickers", min_value=1, max_value=50, value=10, step=1)
            target_orders_per_hour = st.number_input("Target Orders per Picker per Hour", min_value=1.0, max_value=100.0, value=15.0, step=1.0)
        with col2:
            travel_time_pct = st.number_input("% of Time Spent Travelling in Warehouse", min_value=0.0, max_value=100.0, value=35.0, step=1.0)
            search_time_pct = st.number_input("% of Time Spent Searching for Items", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
            actual_pick_time_pct = st.number_input("% of Time Actually Picking", min_value=0.0, max_value=100.0, value=45.0, step=1.0)

        num_order_types = st.number_input("Number of Order Types to Analyze", min_value=1, max_value=8, value=3, step=1)

        order_types = []
        cols = st.columns(3)
        for i in range(int(num_order_types)):
            col = cols[i % 3]
            with col:
                name = st.text_input(f"Order Type {i+1}", value=f"Type {i+1}", key=f"otname_{i}")
                avg_time = st.number_input(f"Avg Pick Time (mins)", min_value=0.1, max_value=60.0, value=float(3 + i*2), step=0.1, format="%.1f", key=f"ottime_{i}")
                volume = st.number_input(f"Daily Volume", min_value=1, max_value=5000, value=max(50, 200-i*50), step=1, key=f"otvol_{i}")
                order_types.append({"name": name, "avg_time": avg_time, "volume": volume})

        if order_types:
            st.divider()
            st.header("Picking Analysis Results")

            available_mins = shift_hours * 60 * num_pickers
            productive_mins = available_mins * (actual_pick_time_pct / 100)
            total_pick_demand = sum(ot["avg_time"] * ot["volume"] for ot in order_types)
            picking_efficiency = (productive_mins / total_pick_demand * 100) if total_pick_demand > 0 else 0
            picking_efficiency = min(picking_efficiency, 100)
            total_volume = sum(ot["volume"] for ot in order_types)
            actual_orders_per_picker_hour = (total_volume / num_pickers) / shift_hours

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                eff_color = "#00CC00" if picking_efficiency >= 80 else "#FFD700" if picking_efficiency >= 60 else "#CC0000"
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {eff_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Picking Efficiency</p>
                    <p style="color:{eff_color};font-size:2rem;font-weight:900;margin:8px 0;">{picking_efficiency:.1f}%</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #ffffff;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Total Daily Orders</p>
                    <p style="color:#ffffff;font-size:2rem;font-weight:900;margin:8px 0;">{total_volume:,}</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                rate_color = "#00CC00" if actual_orders_per_picker_hour >= target_orders_per_hour else "#CC0000"
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {rate_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Orders/Picker/Hour</p>
                    <p style="color:{rate_color};font-size:2rem;font-weight:900;margin:8px 0;">{actual_orders_per_picker_hour:.1f}</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">Target: {target_orders_per_hour:.0f}</p>
                </div>""", unsafe_allow_html=True)
            with col4:
                wasted_pct = travel_time_pct + search_time_pct
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #CC0000;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Non-Productive Time</p>
                    <p style="color:#CC0000;font-size:2rem;font-weight:900;margin:8px 0;">{wasted_pct:.0f}%</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">Travel + Search</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            fig = go.Figure(go.Pie(
                labels=["Actually Picking", "Travelling", "Searching"],
                values=[actual_pick_time_pct, travel_time_pct, search_time_pct],
                marker_colors=["#00CC00", "#FFD700", "#CC0000"],
                hole=0.4
            ))
            fig.update_layout(
                title="How Pickers Spend Their Time",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            insights = []
            data_rows = [["Order Type", "Avg Time (mins)", "Daily Volume"]]
            for ot in order_types:
                data_rows.append([ot["name"], f"{ot['avg_time']:.1f}", str(ot["volume"])])

            if travel_time_pct > 30:
                insights.append(f"Your pickers are spending {travel_time_pct:.0f}% of their time just travelling around the warehouse. This is your biggest opportunity — implement zone picking or batch picking to reduce travel distance by up to 40%.")
            if search_time_pct > 15:
                insights.append(f"Pickers are spending {search_time_pct:.0f}% of their time searching for items. This points to poor bin labeling or incorrect stock locations. Implement a proper location system and cycle counting to keep locations accurate.")
            if actual_orders_per_picker_hour < target_orders_per_hour:
                gap = target_orders_per_hour - actual_orders_per_picker_hour
                insights.append(f"You are {gap:.1f} orders per picker per hour below your target. At your current volume this means you need approximately {(total_pick_demand / productive_mins * num_pickers - num_pickers):.0f} additional pickers to meet demand — or you need to improve productivity.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_pie_chart(
                    ["Actually Picking", "Travelling", "Searching"],
                    [actual_pick_time_pct, travel_time_pct, search_time_pct],
                    ["#00CC00", "#FFD700", "#CC0000"],
                    "How Pickers Spend Their Time"
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

    # ════════════════════════════════════════
    # TOOL 3: WAREHOUSE SLOTTING ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Warehouse Slotting Analysis":
        st.header("Warehouse Slotting Analysis")
        st.write("Are your fastest moving products in the most accessible locations? Bad slotting is one of the biggest hidden costs in warehousing.")

        col1, col2 = st.columns(2)
        with col1:
            total_skus = st.number_input("Total Number of SKUs", min_value=10, max_value=100000, value=500, step=10)
            warehouse_zones = st.number_input("Number of Warehouse Zones", min_value=2, max_value=10, value=3, step=1)
        with col2:
            prime_zone_pct = st.number_input("% of Space in Prime Zone (closest to dispatch)", min_value=5.0, max_value=50.0, value=20.0, step=1.0)
            avg_pick_travel_time = st.number_input("Average Travel Time per Pick (mins)", min_value=0.1, max_value=30.0, value=3.5, step=0.1, format="%.1f")

        st.subheader("SKU Velocity Distribution")
        st.write("How many of your SKUs fall into each velocity category?")

        col1, col2, col3 = st.columns(3)
        with col1:
            fast_skus = st.number_input("Fast Movers (A) — picked daily", min_value=0, max_value=10000, value=50, step=5)
            fast_in_prime = st.number_input("Of these, how many are IN the prime zone?", min_value=0, max_value=int(fast_skus), value=30, step=1, key="fip")
        with col2:
            medium_skus = st.number_input("Medium Movers (B) — picked weekly", min_value=0, max_value=10000, value=150, step=5)
            medium_in_prime = st.number_input("Of these, how many are IN the prime zone?", min_value=0, max_value=int(medium_skus), value=40, step=1, key="mip")
        with col3:
            slow_skus = st.number_input("Slow Movers (C) — picked monthly or less", min_value=0, max_value=100000, value=300, step=10)
            slow_in_prime = st.number_input("Of these, how many are IN the prime zone?", min_value=0, max_value=int(slow_skus), value=50, step=1, key="sip")

        if fast_skus > 0 or medium_skus > 0 or slow_skus > 0:
            st.divider()
            st.header("Slotting Analysis Results")

            total_in_prime = fast_in_prime + medium_in_prime + slow_in_prime
            fast_coverage = (fast_in_prime / fast_skus * 100) if fast_skus > 0 else 0
            slotting_score = fast_coverage * 0.7 + (1 - slow_in_prime / max(total_in_prime, 1)) * 30

            score_color = "#00CC00" if slotting_score >= 80 else "#FFD700" if slotting_score >= 60 else "#CC0000"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {score_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Slotting Score</p>
                    <p style="color:{score_color};font-size:2.5rem;font-weight:900;margin:8px 0;">{slotting_score:.0f}/100</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #{'00CC00' if fast_coverage >= 80 else 'CC0000'};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Fast Movers in Prime Zone</p>
                    <p style="color:#{'00CC00' if fast_coverage >= 80 else 'CC0000'};font-size:2.5rem;font-weight:900;margin:8px 0;">{fast_coverage:.0f}%</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">Target: 80%+</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                misplaced_slow = slow_in_prime
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #{'CC0000' if misplaced_slow > 10 else '00CC00'};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Slow Movers Wasting Prime Space</p>
                    <p style="color:#{'CC0000' if misplaced_slow > 10 else '00CC00'};font-size:2.5rem;font-weight:900;margin:8px 0;">{misplaced_slow}</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">SKUs to relocate</p>
                </div>""", unsafe_allow_html=True)

            fig = go.Figure(go.Bar(
                x=["Fast Movers (A)", "Medium Movers (B)", "Slow Movers (C)"],
                y=[fast_in_prime, medium_in_prime, slow_in_prime],
                marker_color=["#00CC00", "#FFD700", "#CC0000"],
                text=[f"{fast_in_prime}", f"{medium_in_prime}", f"{slow_in_prime}"],
                textposition="outside",
                name="SKUs in Prime Zone"
            ))
            fig.update_layout(
                title="SKUs in Prime Zone by Velocity Category (Ideal: High A, Low C)",
                yaxis_title="Number of SKUs",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            insights = []
            data_rows = [
                ["Category", "Total SKUs", "In Prime Zone"],
                ["Fast Movers (A)", str(fast_skus), str(fast_in_prime)],
                ["Medium Movers (B)", str(medium_skus), str(medium_in_prime)],
                ["Slow Movers (C)", str(slow_skus), str(slow_in_prime)],
            ]

            if fast_coverage < 80:
                missing = fast_skus - fast_in_prime
                insights.append(f"{missing} of your fast moving SKUs are NOT in the prime zone. Every time a picker has to walk to the back of the warehouse for a fast moving item you are wasting time that multiplies across hundreds of picks per day. Move these {missing} SKUs to prime zone first.")
            if slow_in_prime > 10:
                insights.append(f"{slow_in_prime} slow moving SKUs are occupying prime zone space. These items are picked rarely but taking up your most valuable picking real estate. Move them to the back and free up prime space for your fast movers.")
            time_saved_per_pick = avg_pick_travel_time * 0.2
            daily_picks_estimate = fast_skus * 3
            annual_time_saved = time_saved_per_pick * daily_picks_estimate * 250 / 60
            insights.append(f"Optimizing your slotting could save approximately {time_saved_per_pick:.1f} mins per pick on fast movers. Across an estimated {daily_picks_estimate} daily picks that is {annual_time_saved:,.0f} hours per year saved.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    ["Fast Movers (A)", "Medium Movers (B)", "Slow Movers (C)"],
                    [fast_in_prime, medium_in_prime, slow_in_prime],
                    ["#00CC00", "#FFD700", "#CC0000"],
                    "SKUs in Prime Zone by Velocity Category",
                    ylabel="Number of SKUs"
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

    # ════════════════════════════════════════
    # TOOL 4: RETURNS ROOT CAUSE ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Returns Root Cause Analysis":
        st.header("Returns Root Cause Analysis")
        st.write("Understand exactly why customers are returning products so you can fix the root cause instead of just processing returns.")

        col1, col2 = st.columns(2)
        with col1:
            total_returns = st.number_input("Total Returns Last Month", min_value=1, max_value=100000, value=500, step=10)
            total_orders_sent = st.number_input("Total Orders Sent Last Month", min_value=1, max_value=1000000, value=10000, step=100)
            cost_per_return = st.number_input(f"Cost to Process Each Return ({currency_symbol})", min_value=0.0, value=150.0, step=10.0)
        with col2:
            st.write("")

        return_rate = (total_returns / total_orders_sent * 100) if total_orders_sent > 0 else 0

        st.subheader("Return Reasons Breakdown")
        st.write("Enter how many returns fall into each category:")

        col1, col2 = st.columns(2)
        with col1:
            wrong_item = st.number_input("Wrong Item Sent", min_value=0, value=int(total_returns*0.25), step=1)
            damaged = st.number_input("Damaged in Transit", min_value=0, value=int(total_returns*0.20), step=1)
            quality = st.number_input("Quality Not as Expected", min_value=0, value=int(total_returns*0.20), step=1)
            late = st.number_input("Delivered Too Late", min_value=0, value=int(total_returns*0.15), step=1)
        with col2:
            wrong_address = st.number_input("Wrong Address / Not Delivered", min_value=0, value=int(total_returns*0.10), step=1)
            changed_mind = st.number_input("Customer Changed Mind", min_value=0, value=int(total_returns*0.05), step=1)
            other = st.number_input("Other Reasons", min_value=0, value=int(total_returns*0.05), step=1)

        reasons = [
            ("Wrong Item Sent", wrong_item),
            ("Damaged in Transit", damaged),
            ("Quality Not as Expected", quality),
            ("Delivered Too Late", late),
            ("Wrong Address / Not Delivered", wrong_address),
            ("Customer Changed Mind", changed_mind),
            ("Other", other)
        ]
        reasons_sorted = sorted([(r, v) for r, v in reasons if v > 0], key=lambda x: x[1], reverse=True)

        if reasons_sorted:
            st.divider()
            st.header("Returns Analysis Results")

            total_cost = total_returns * cost_per_return
            rate_color = "#00CC00" if return_rate < 2 else "#FFD700" if return_rate < 5 else "#CC0000"

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {rate_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Return Rate</p>
                    <p style="color:{rate_color};font-size:2rem;font-weight:900;margin:8px 0;">{return_rate:.2f}%</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">Benchmark: below 2%</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #CC0000;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Monthly Returns Cost</p>
                    <p style="color:#CC0000;font-size:2rem;font-weight:900;margin:8px 0;">{currency_symbol}{total_cost:,.0f}</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                annual_cost = total_cost * 12
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #CC0000;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Annual Returns Cost</p>
                    <p style="color:#CC0000;font-size:2rem;font-weight:900;margin:8px 0;">{currency_symbol}{annual_cost:,.0f}</p>
                </div>""", unsafe_allow_html=True)

            total_categorized = sum(v for _, v in reasons_sorted)
            labels = [r for r, v in reasons_sorted]
            values = [v for r, v in reasons_sorted]

            fig = go.Figure(go.Pie(
                labels=labels,
                values=values,
                marker_colors=["#CC0000", "#FF6B00", "#FFD700", "#888888", "#444444", "#222222", "#111111"],
                hole=0.4
            ))
            fig.update_layout(
                title="Return Reasons Breakdown",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Priority Return Reasons to Fix")
            insights = []
            data_rows = [["Return Reason", "Count", "% of Returns"]]
            cumulative = 0
            for reason, count in reasons_sorted:
                pct = (count / total_categorized * 100) if total_categorized > 0 else 0
                cumulative += pct
                data_rows.append([reason, str(count), f"{pct:.1f}%"])
                cost_of_reason = count * cost_per_return
                st.markdown(f"""
                <div style="background:#1a1a1a;border-left:4px solid #CC0000;padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                    <span style="color:#ffffff;font-weight:700;">{reason}</span>
                    <span style="color:#888;margin-left:12px;font-size:0.82rem;">{count} returns ({pct:.1f}%) — costing {currency_symbol}{cost_of_reason:,.0f}/month</span>
                </div>
                """, unsafe_allow_html=True)

            top_reason = reasons_sorted[0]
            insights.append(f"Your biggest return reason is '{top_reason[0]}' accounting for {top_reason[1]} returns per month at a cost of {currency_symbol}{top_reason[1]*cost_per_return:,.0f}. Fix this one reason alone and you will reduce your return costs by {top_reason[1]/total_returns*100:.0f}%.")
            if wrong_item > 0:
                insights.append(f"Wrong items sent ({wrong_item} returns) is a picking accuracy problem. Implement barcode scanning at packing to eliminate this category entirely.")
            if damaged > 0:
                insights.append(f"Transit damage ({damaged} returns) points to packaging inadequacy. Review your packaging standards for your most commonly damaged product types.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_pie_chart(
                    [r for r, v in reasons_sorted],
                    [v for r, v in reasons_sorted],
                    ["#CC0000", "#FF6B00", "#FFD700", "#888888", "#444444", "#222222", "#111111"][:len(reasons_sorted)],
                    "Return Reasons Breakdown"
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)