# -*- coding: utf-8 -*-
import streamlit as st
try:
    from auth import save_analysis
except ImportError:
    def save_analysis(*args, **kwargs): return None
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from reportlab.platypus import Image as RLImage
import plotly.graph_objects as go
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
        ["Company / Organization", company_name],
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

    if data_rows:
        elements.append(Paragraph("Analysis Data", heading_style))
        t = Table(data_rows, colWidths=[2.0*inch, 1.5*inch, 1.5*inch, 1.0*inch])
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


def show_supply_chain_deep(industry, currency_symbol="$"):
    st.markdown("""
    <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;">
        <p style="color: #E8001D; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 4px 0;">Deep Analysis Mode</p>
        <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Enter detailed supply chain data to pinpoint exactly where your supply chain is creating risk and cost.</p>
    </div>
    """, unsafe_allow_html=True)

    tool = st.selectbox(
        "Select a Deep Analysis Tool",
        [
            "Supplier Performance Scorecard",
            "Inventory ABC Analysis",
            "Lead Time Analysis",
            "Supply Chain Risk Assessment"
        ]
    )

    company_name = st.text_input("Company / Organization Name", placeholder="e.g. Tata Motors Supply Chain")
    st.divider()

    # ════════════════════════════════════════
    # TOOL 1: SUPPLIER PERFORMANCE SCORECARD
    # ════════════════════════════════════════
    if tool == "Supplier Performance Scorecard":
        st.header("Supplier Performance Scorecard")
        st.write("Rate each of your key suppliers across quality, delivery and cost. SPO will rank them and identify which ones need urgent attention.")

        num_suppliers = st.number_input("Number of Key Suppliers to Score", min_value=2, max_value=15, value=5, step=1)

        suppliers = []
        for i in range(int(num_suppliers)):
            with st.expander(f"Supplier {i+1}"):
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    name = st.text_input("Supplier Name", value=f"Supplier {i+1}", key=f"supname_{i}")
                with col2:
                    otd = st.number_input("On Time Delivery %", min_value=0.0, max_value=100.0, value=float(max(70, 95-i*5)), step=0.1, format="%.1f", key=f"suplotd_{i}")
                with col3:
                    quality = st.number_input("Quality Rate %", min_value=0.0, max_value=100.0, value=float(max(80, 98-i*3)), step=0.1, format="%.1f", key=f"supqual_{i}")
                with col4:
                    response = st.number_input("Response Time Score (1-10)", min_value=1.0, max_value=10.0, value=float(max(4, 9-i)), step=0.5, format="%.1f", key=f"supresp_{i}")
                with col5:
                    spend = st.number_input(f"Annual Spend ({currency_symbol})", min_value=0.0, value=float(100000 - i*15000), step=1000.0, key=f"supspend_{i}")
                single_source = st.checkbox(f"Single Source (no backup supplier)", key=f"supss_{i}")
                suppliers.append({"name": name, "otd": otd, "quality": quality, "response": response, "spend": spend, "single_source": single_source})

        if suppliers:
            st.divider()
            st.header("Supplier Scorecard Results")

            scored = []
            for s in suppliers:
                score = (s["otd"] * 0.4) + (s["quality"] * 0.4) + (s["response"] * 10 * 0.2)
                if s["single_source"]:
                    risk = "High Risk"
                    risk_color = "#CC0000"
                elif score < 70:
                    risk = "Medium Risk"
                    risk_color = "#FFD700"
                else:
                    risk = "Low Risk"
                    risk_color = "#00CC00"
                scored.append({**s, "score": score, "risk": risk, "risk_color": risk_color})

            scored_sorted = sorted(scored, key=lambda x: x["score"])

            fig = go.Figure(go.Bar(
                x=[s["name"] for s in scored_sorted],
                y=[s["score"] for s in scored_sorted],
                marker_color=[s["risk_color"] for s in scored_sorted],
                text=[f"{s['score']:.0f}" for s in scored_sorted],
                textposition="outside"
            ))
            fig.add_hline(y=80, line_dash="dash", line_color="#ffffff",
                         annotation_text="Target Score: 80",
                         annotation_position="top right")
            fig.update_layout(
                title="Supplier Performance Scores (Lower = More Urgent Attention Needed)",
                yaxis_title="Score (0-100)",
                yaxis_range=[0, 115],
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            insights = []
            data_rows = [["Supplier", "OTD %", "Quality %", "Score", "Risk"]]
            for s in scored_sorted:
                data_rows.append([s["name"], f"{s['otd']:.1f}%", f"{s['quality']:.1f}%", f"{s['score']:.0f}", s["risk"]])
                st.markdown(f"""
                <div style="background:#1a1a1a;border-left:4px solid {s['risk_color']};padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                    <span style="color:{s['risk_color']};font-weight:800;">{s['risk']}</span>
                    <span style="color:#ffffff;margin-left:10px;font-weight:600;">{s['name']}</span>
                    <span style="color:#888;margin-left:10px;font-size:0.82rem;">Score: {s['score']:.0f}/100 | OTD: {s['otd']:.1f}% | Quality: {s['quality']:.1f}% | Spend: {currency_symbol}{s['spend']:,.0f}</span>
                    {"<span style='color:#CC0000;margin-left:8px;font-size:0.8rem;font-weight:700;'>⚠️ SINGLE SOURCE</span>" if s['single_source'] else ""}
                </div>
                """, unsafe_allow_html=True)

            worst = scored_sorted[0]
            single_sources = [s for s in scored if s["single_source"]]
            total_spend = sum(s["spend"] for s in scored)
            risky_spend = sum(s["spend"] for s in scored if s["risk"] != "Low Risk")

            insights.append(f"Your worst performing supplier is {worst['name']} with a score of {worst['score']:.0f}/100. Their OTD is {worst['otd']:.1f}% and quality rate is {worst['quality']:.1f}%. Have an urgent performance review with them and set clear improvement targets with a 30 day deadline.")
            if single_sources:
                ss_names = ", ".join([s["name"] for s in single_sources])
                ss_spend = sum(s["spend"] for s in single_sources)
                insights.append(f"You have {len(single_sources)} single source supplier(s): {ss_names}. This represents {currency_symbol}{ss_spend:,.0f} in annual spend with no backup. If any of these suppliers fails you have no alternative. Start qualifying backup suppliers immediately.")
            if risky_spend > 0:
                insights.append(f"{currency_symbol}{risky_spend:,.0f} ({risky_spend/total_spend*100:.0f}% of your total supplier spend) is with medium or high risk suppliers. This spend is at risk of disruption.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    [s["name"] for s in scored_sorted],
                    [s["score"] for s in scored_sorted],
                    [s["risk_color"] for s in scored_sorted],
                    "Supplier Performance Scores",
                    ylabel="Score (0-100)",
                    benchmark=80
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_risk"):
                if st.session_state.get("current_company"):
                    try:
                        avg_risk = sum(i["risk_score"] for i in items_sorted) / len(items_sorted) if items_sorted else 5
                        item_data = {i["name"]: {"supply_risk": i["supply_risk"], "impact": i["impact"], "risk_level": i["risk_level"]} for i in items_sorted}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"num_items": num_items, "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk},
                            results={"tool": "Supply Chain Risk Assessment", "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk, "item_risks": item_data},
                            risk_score=int(max(0, 100 - avg_risk * 10)),
                            risk_label="LOW RISK" if avg_risk < 4 else "MEDIUM RISK" if avg_risk < 7 else "HIGH RISK",
                            tool_name="Supply Chain Risk Assessment"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_suppliers"):
                if st.session_state.get("current_company"):
                    try:
                        worst_s = scored_sorted[0] if scored_sorted else {}
                        avg_score = sum(s["score"] for s in scored) / len(scored) if scored else 0
                        supplier_scores = {s["name"]: {"otd": s["otd"], "quality": s["quality"], "score": s["score"]} for s in scored}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"num_suppliers": num_suppliers, "avg_supplier_score": avg_score, "single_source_count": len([s for s in scored if s.get("single_source")]), "high_risk_count": len([s for s in scored if s["risk"] == "High Risk"])},
                            results={"tool": "Supplier Performance Scorecard", "worst_supplier": worst_s.get("name",""), "worst_supplier_score": worst_s.get("score",0), "avg_score": avg_score, "supplier_scores": supplier_scores},
                            risk_score=int(max(0, min(100, avg_score))),
                            risk_label="LOW RISK" if avg_score >= 80 else "MEDIUM RISK" if avg_score >= 60 else "HIGH RISK",
                            tool_name="Supplier Performance Scorecard"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

    # ════════════════════════════════════════
    # TOOL 2: INVENTORY ABC ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Inventory ABC Analysis":
        st.header("Inventory ABC Analysis")
        st.write("ABC Analysis classifies your inventory by value. A items = high value, manage tightly. B items = medium. C items = low value, simplify management.")

        col1, col2 = st.columns(2)
        with col1:
            num_categories = st.number_input("Number of Product Categories", min_value=2, max_value=12, value=5, step=1)
            holding_cost_pct = st.number_input("Annual Holding Cost (% of inventory value)", min_value=1.0, max_value=50.0, value=25.0, step=1.0)
        with col2:
            st.write("")

        categories = []
        cols = st.columns(3)
        for i in range(int(num_categories)):
            col = cols[i % 3]
            with col:
                name = st.text_input(f"Category {i+1}", value=f"Product {chr(65+i)}", key=f"abcname_{i}")
                annual_value = st.number_input(f"Annual Usage Value ({currency_symbol})", min_value=0.0, value=float(500000 - i*80000), step=1000.0, key=f"abcval_{i}")
                stock_value = st.number_input(f"Current Stock Value ({currency_symbol})", min_value=0.0, value=float(annual_value * 0.15), step=1000.0, key=f"abcstock_{i}")
                categories.append({"name": name, "annual_value": annual_value, "stock_value": stock_value})

        if categories:
            st.divider()
            st.header("ABC Analysis Results")

            total_value = sum(c["annual_value"] for c in categories)
            cats_sorted = sorted(categories, key=lambda x: x["annual_value"], reverse=True)

            cumulative = 0
            abc_cats = []
            for c in cats_sorted:
                cumulative += c["annual_value"]
                pct = (c["annual_value"] / total_value * 100) if total_value > 0 else 0
                cum_pct = (cumulative / total_value * 100) if total_value > 0 else 0
                if cum_pct <= 80:
                    abc_class = "A"
                    color = "#CC0000"
                elif cum_pct <= 95:
                    abc_class = "B"
                    color = "#FFD700"
                else:
                    abc_class = "C"
                    color = "#00CC00"
                holding_cost = c["stock_value"] * (holding_cost_pct / 100)
                abc_cats.append({**c, "abc": abc_class, "color": color, "pct": pct, "cum_pct": cum_pct, "holding_cost": holding_cost})

            a_items = [c for c in abc_cats if c["abc"] == "A"]
            b_items = [c for c in abc_cats if c["abc"] == "B"]
            c_items = [c for c in abc_cats if c["abc"] == "C"]
            total_holding = sum(c["holding_cost"] for c in abc_cats)

            col1, col2, col3 = st.columns(3)
            with col1:
                a_val = sum(c["annual_value"] for c in a_items)
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #CC0000;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">A Items (High Value)</p>
                    <p style="color:#CC0000;font-size:1.4rem;font-weight:900;margin:8px 0;">{len(a_items)} categories</p>
                    <p style="color:#888;font-size:0.78rem;margin:0;">{currency_symbol}{a_val:,.0f} annual value</p>
                    <p style="color:#888;font-size:0.75rem;margin:4px 0;">Manage tightly — daily review</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                b_val = sum(c["annual_value"] for c in b_items)
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #FFD700;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">B Items (Medium Value)</p>
                    <p style="color:#FFD700;font-size:1.4rem;font-weight:900;margin:8px 0;">{len(b_items)} categories</p>
                    <p style="color:#888;font-size:0.78rem;margin:0;">{currency_symbol}{b_val:,.0f} annual value</p>
                    <p style="color:#888;font-size:0.75rem;margin:4px 0;">Review weekly</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                c_val = sum(c["annual_value"] for c in c_items)
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #00CC00;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">C Items (Low Value)</p>
                    <p style="color:#00CC00;font-size:1.4rem;font-weight:900;margin:8px 0;">{len(c_items)} categories</p>
                    <p style="color:#888;font-size:0.78rem;margin:0;">{currency_symbol}{c_val:,.0f} annual value</p>
                    <p style="color:#888;font-size:0.75rem;margin:4px 0;">Review monthly — simplify</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            fig = go.Figure(go.Bar(
                x=[c["name"] for c in abc_cats],
                y=[c["annual_value"] for c in abc_cats],
                marker_color=[c["color"] for c in abc_cats],
                text=[f"{c['abc']} — {currency_symbol}{c['annual_value']:,.0f}" for c in abc_cats],
                textposition="outside"
            ))
            fig.update_layout(
                title="Annual Usage Value by Category (Red=A, Yellow=B, Green=C)",
                yaxis_title=f"Annual Usage Value ({currency_symbol})",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Full Classification")
            insights = []
            data_rows = [["Category", "Annual Value", "Stock Value", "Class"]]
            for c in abc_cats:
                data_rows.append([c["name"], f"{currency_symbol}{c['annual_value']:,.0f}", f"{currency_symbol}{c['stock_value']:,.0f}", c["abc"]])
                st.markdown(f"""
                <div style="background:#1a1a1a;border-left:4px solid {c['color']};padding:10px 16px;margin:5px 0;border-radius:0 8px 8px 0;">
                    <span style="color:{c['color']};font-weight:800;">Class {c['abc']}</span>
                    <span style="color:#ffffff;margin-left:10px;font-weight:600;">{c['name']}</span>
                    <span style="color:#888;margin-left:10px;font-size:0.82rem;">Annual Value: {currency_symbol}{c['annual_value']:,.0f} ({c['pct']:.1f}%) | Stock: {currency_symbol}{c['stock_value']:,.0f} | Holding Cost: {currency_symbol}{c['holding_cost']:,.0f}/yr</span>
                </div>
                """, unsafe_allow_html=True)

            insights.append(f"Your A items represent the highest value. These should have daily inventory reviews, tight reorder points and dedicated buyer attention. Never let A items stock out.")
            insights.append(f"Your total annual inventory holding cost is {currency_symbol}{total_holding:,.0f}. Reducing C item safety stock by 30% could save {currency_symbol}{sum(c['holding_cost'] for c in c_items)*0.3:,.0f} per year without meaningful supply risk.")
            if c_items:
                insights.append(f"Consider simplifying ordering for C items by switching to periodic review instead of continuous review. This reduces procurement effort while maintaining adequate stock levels.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.info(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    [c["name"] for c in abc_cats],
                    [c["annual_value"] for c in abc_cats],
                    [c["color"] for c in abc_cats],
                    "Annual Usage Value by Category (Red=A, Yellow=B, Green=C)",
                    ylabel="Annual Value"
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_risk"):
                if st.session_state.get("current_company"):
                    try:
                        avg_risk = sum(i["risk_score"] for i in items_sorted) / len(items_sorted) if items_sorted else 5
                        item_data = {i["name"]: {"supply_risk": i["supply_risk"], "impact": i["impact"], "risk_level": i["risk_level"]} for i in items_sorted}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"num_items": num_items, "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk},
                            results={"tool": "Supply Chain Risk Assessment", "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk, "item_risks": item_data},
                            risk_score=int(max(0, 100 - avg_risk * 10)),
                            risk_label="LOW RISK" if avg_risk < 4 else "MEDIUM RISK" if avg_risk < 7 else "HIGH RISK",
                            tool_name="Supply Chain Risk Assessment"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_abc"):
                if st.session_state.get("current_company"):
                    try:
                        c_in_prime = len([c for c in abc_cats if c["abc"] == "C"])
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"total_categories": len(categories), "total_annual_value": total_value, "holding_cost_pct": holding_cost_pct, "total_holding_cost": total_holding, "a_items": len([c for c in abc_cats if c["abc"]=="A"]), "b_items": len([c for c in abc_cats if c["abc"]=="B"]), "c_items": len([c for c in abc_cats if c["abc"]=="C"])},
                            results={"tool": "Inventory ABC Analysis", "a_items": len([c for c in abc_cats if c["abc"]=="A"]), "b_items": len([c for c in abc_cats if c["abc"]=="B"]), "c_items": len([c for c in abc_cats if c["abc"]=="C"]), "c_items_in_prime": c_in_prime, "total_holding_cost": total_holding},
                            risk_score=int(max(0, 100 - c_in_prime * 5)),
                            risk_label="LOW RISK" if c_in_prime <= 2 else "MEDIUM RISK" if c_in_prime <= 5 else "HIGH RISK",
                            tool_name="Inventory ABC Analysis"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

    # ════════════════════════════════════════
    # TOOL 3: LEAD TIME ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Lead Time Analysis":
        st.header("Lead Time Analysis")
        st.write("Break down your total lead time into its components and find where the delays are happening.")

        col1, col2 = st.columns(2)
        with col1:
            customer_required_lt = st.number_input("Customer Required Lead Time (days)", min_value=1.0, max_value=365.0, value=14.0, step=1.0)
        with col2:
            num_components = st.number_input("Number of Lead Time Components", min_value=2, max_value=10, value=5, step=1)

        st.subheader("Break Down Your Lead Time")
        st.write("Enter each component of your total lead time from order receipt to customer delivery:")

        components = []
        cols = st.columns(2)
        for i in range(int(num_components)):
            col = cols[i % 2]
            with col:
                name = st.text_input(f"Component {i+1}", value=["Order Processing", "Supplier Lead Time", "Inbound Transit", "Internal Processing", "Outbound Delivery"][i] if i < 5 else f"Component {i+1}", key=f"ltname_{i}")
                days = st.number_input(f"Days", min_value=0.0, max_value=90.0, value=float([1, 7, 3, 2, 2][i] if i < 5 else 2), step=0.5, format="%.1f", key=f"ltdays_{i}")
                value_add = st.checkbox("Is this value adding time?", key=f"ltva_{i}", value=(i in [1, 3]))
                components.append({"name": name, "days": days, "value_add": value_add})

        if components:
            st.divider()
            st.header("Lead Time Analysis Results")

            total_lt = sum(c["days"] for c in components)
            value_add_lt = sum(c["days"] for c in components if c["value_add"])
            non_value_add_lt = total_lt - value_add_lt
            lt_efficiency = (value_add_lt / total_lt * 100) if total_lt > 0 else 0
            lt_gap = total_lt - customer_required_lt

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                gap_color = "#CC0000" if lt_gap > 0 else "#00CC00"
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {gap_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Total Lead Time</p>
                    <p style="color:{gap_color};font-size:2rem;font-weight:900;margin:8px 0;">{total_lt:.1f} days</p>
                    <p style="color:#888;font-size:0.75rem;margin:0;">Customer needs: {customer_required_lt:.1f} days</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #00CC00;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Value Adding Time</p>
                    <p style="color:#00CC00;font-size:2rem;font-weight:900;margin:8px 0;">{value_add_lt:.1f} days</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid #CC0000;border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Non-Value Adding Time</p>
                    <p style="color:#CC0000;font-size:2rem;font-weight:900;margin:8px 0;">{non_value_add_lt:.1f} days</p>
                </div>""", unsafe_allow_html=True)
            with col4:
                eff_color = "#00CC00" if lt_efficiency >= 70 else "#FFD700" if lt_efficiency >= 40 else "#CC0000"
                st.markdown(f"""<div style="background:#1a1a1a;border:2px solid {eff_color};border-radius:10px;padding:20px;text-align:center;">
                    <p style="color:#ffffff;margin:0;font-size:0.85rem;">Lead Time Efficiency</p>
                    <p style="color:{eff_color};font-size:2rem;font-weight:900;margin:8px 0;">{lt_efficiency:.0f}%</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            colors_bar = ["#00CC00" if c["value_add"] else "#CC0000" for c in components]
            fig = go.Figure(go.Bar(
                x=[c["name"] for c in components],
                y=[c["days"] for c in components],
                marker_color=colors_bar,
                text=[f"{c['days']:.1f}d {'(VA)' if c['value_add'] else '(NVA)'}" for c in components],
                textposition="outside"
            ))
            fig.add_hline(y=customer_required_lt, line_dash="dash", line_color="#FFD700",
                         annotation_text=f"Customer Requirement: {customer_required_lt:.0f} days",
                         annotation_position="top right")
            fig.update_layout(
                title="Lead Time Components (Green=Value Adding, Red=Non-Value Adding)",
                yaxis_title="Days",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            insights = []
            data_rows = [["Component", "Days", "Type"]]
            for c in components:
                data_rows.append([c["name"], f"{c['days']:.1f}", "Value Adding" if c["value_add"] else "Non-Value Adding"])

            biggest_nva = max([c for c in components if not c["value_add"]], key=lambda x: x["days"], default=None)
            if biggest_nva:
                insights.append(f"Your largest non-value adding component is '{biggest_nva['name']}' at {biggest_nva['days']:.1f} days. This is pure waste — time where nothing useful is happening for the customer. Target this first for reduction.")
            if lt_gap > 0:
                insights.append(f"Your total lead time of {total_lt:.1f} days exceeds customer requirement of {customer_required_lt:.1f} days by {lt_gap:.1f} days. You need to eliminate {lt_gap:.1f} days of lead time to meet customer expectations without holding finished goods buffer stock.")
            insights.append(f"Your lead time is only {lt_efficiency:.0f}% efficient — only {value_add_lt:.1f} of your {total_lt:.1f} days are actually adding value. Lean principle: eliminate or compress every non-value adding step.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    [c["name"] for c in components],
                    [c["days"] for c in components],
                    ["#00CC00" if c["value_add"] else "#CC0000" for c in components],
                    "Lead Time Components (Green=Value Adding, Red=Non-Value Adding)",
                    ylabel="Days",
                    benchmark=customer_required_lt
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_risk"):
                if st.session_state.get("current_company"):
                    try:
                        avg_risk = sum(i["risk_score"] for i in items_sorted) / len(items_sorted) if items_sorted else 5
                        item_data = {i["name"]: {"supply_risk": i["supply_risk"], "impact": i["impact"], "risk_level": i["risk_level"]} for i in items_sorted}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"num_items": num_items, "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk},
                            results={"tool": "Supply Chain Risk Assessment", "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk, "item_risks": item_data},
                            risk_score=int(max(0, 100 - avg_risk * 10)),
                            risk_label="LOW RISK" if avg_risk < 4 else "MEDIUM RISK" if avg_risk < 7 else "HIGH RISK",
                            tool_name="Supply Chain Risk Assessment"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_lt"):
                if st.session_state.get("current_company"):
                    try:
                        component_data = {c["name"]: {"days": c["days"], "value_add": c["value_add"]} for c in components}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"total_lt_days": total_lt, "customer_required_lt": customer_required_lt, "value_add_days": value_add_lt, "non_value_add_days": non_value_add_lt, "lt_efficiency_pct": lt_efficiency, "lt_gap_days": lt_gap},
                            results={"tool": "Lead Time Analysis", "total_lt_days": total_lt, "value_add_days": value_add_lt, "non_value_add_days": non_value_add_lt, "lt_efficiency": lt_efficiency, "lt_gap": lt_gap, "components": component_data},
                            risk_score=int(max(0, min(100, lt_efficiency))),
                            risk_label="LOW RISK" if lt_efficiency >= 70 else "MEDIUM RISK" if lt_efficiency >= 40 else "HIGH RISK",
                            tool_name="Lead Time Analysis"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")

    # ════════════════════════════════════════
    # TOOL 4: SUPPLY CHAIN RISK ASSESSMENT
    # ════════════════════════════════════════
    elif tool == "Supply Chain Risk Assessment":
        st.header("Supply Chain Risk Assessment")
        st.write("Assess the risk level of each critical item in your supply chain based on supply risk and business impact.")

        num_items = st.number_input("Number of Critical Items to Assess", min_value=2, max_value=20, value=6, step=1)

        items = []
        for i in range(int(num_items)):
            with st.expander(f"Item {i+1}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    name = st.text_input("Item Name", value=f"Item {i+1}", key=f"riskname_{i}")
                with col2:
                    supply_risk = st.slider("Supply Risk (1=Easy to source, 10=Very hard)", 1, 10, max(1, 8-i), key=f"risksupply_{i}")
                with col3:
                    impact = st.slider("Business Impact if unavailable (1=Minor, 10=Production stops)", 1, 10, max(1, 9-i), key=f"riskimpact_{i}")
                with col4:
                    annual_spend = st.number_input(f"Annual Spend", min_value=0.0, value=float(200000-i*25000), step=1000.0, key=f"riskspend_{i}")
                num_suppliers = st.number_input("Number of Approved Suppliers", min_value=1, max_value=10, value=max(1, 3-i//2), step=1, key=f"risksups_{i}")
                items.append({"name": name, "supply_risk": supply_risk, "impact": impact, "annual_spend": annual_spend, "num_suppliers": num_suppliers})

        if items:
            st.divider()
            st.header("Risk Assessment Results")

            for item in items:
                risk_score = (item["supply_risk"] * 0.5 + item["impact"] * 0.5)
                if item["num_suppliers"] == 1:
                    risk_score = min(10, risk_score * 1.3)
                if risk_score >= 7:
                    item["risk_level"] = "Critical Risk"
                    item["risk_color"] = "#CC0000"
                elif risk_score >= 4:
                    item["risk_level"] = "Medium Risk"
                    item["risk_color"] = "#FFD700"
                else:
                    item["risk_level"] = "Low Risk"
                    item["risk_color"] = "#00CC00"
                item["risk_score"] = risk_score

            items_sorted = sorted(items, key=lambda x: x["risk_score"], reverse=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[i["supply_risk"] for i in items],
                y=[i["impact"] for i in items],
                mode="markers+text",
                marker=dict(
                    size=[max(15, i["annual_spend"]/10000) for i in items],
                    color=[i["risk_color"] for i in items],
                    opacity=0.8
                ),
                text=[i["name"] for i in items],
                textposition="top center"
            ))
            fig.add_shape(type="rect", x0=6, y0=6, x1=10, y1=10,
                         fillcolor="rgba(204,0,0,0.1)", line=dict(color="#CC0000", dash="dash"))
            fig.update_layout(
                title="Supply Chain Risk Matrix (Bigger bubble = Higher Spend)",
                xaxis_title="Supply Risk (1=Easy, 10=Hard to Source)",
                yaxis_title="Business Impact (1=Minor, 10=Critical)",
                xaxis_range=[0, 11],
                yaxis_range=[0, 11],
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            insights = []
            data_rows = [["Item", "Supply Risk", "Impact", "Suppliers", "Risk Level"]]
            critical_items = []
            single_source_items = []

            for item in items_sorted:
                data_rows.append([item["name"], str(item["supply_risk"]), str(item["impact"]), str(item["num_suppliers"]), item["risk_level"]])
                if item["risk_level"] == "Critical Risk":
                    critical_items.append(item)
                if item["num_suppliers"] == 1:
                    single_source_items.append(item)
                st.markdown(f"""
                <div style="background:#1a1a1a;border-left:4px solid {item['risk_color']};padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                    <span style="color:{item['risk_color']};font-weight:800;">{item['risk_level']}</span>
                    <span style="color:#ffffff;margin-left:10px;font-weight:600;">{item['name']}</span>
                    <span style="color:#888;margin-left:10px;font-size:0.82rem;">Supply Risk: {item['supply_risk']}/10 | Impact: {item['impact']}/10 | Suppliers: {item['num_suppliers']} | Spend: {currency_symbol}{item['annual_spend']:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)

            if critical_items:
                crit_names = ", ".join([i["name"] for i in critical_items])
                insights.append(f"CRITICAL: {crit_names} are in the high risk zone. These items combine difficult sourcing with high business impact. Develop mitigation plans for each — whether dual sourcing, safety stock or alternate specifications.")
            if single_source_items:
                ss_names = ", ".join([i["name"] for i in single_source_items])
                insights.append(f"Single source dependency risk: {ss_names}. You have no backup for these items. Start qualifying at least one alternate supplier for each as a priority.")
            high_impact = [i for i in items if i["impact"] >= 8]
            if high_impact:
                insights.append(f"Items with impact score 8 or above should have documented contingency plans. If these items became unavailable today — do you know exactly what you would do? If not, write that plan this week.")

            st.write("")
            st.subheader("Key Insights")
            for insight in insights:
                st.warning(insight)

            st.divider()
            st.header("Generate Report")
            if st.button("Generate Report", use_container_width=True):
                chart = make_bar_chart(
                    [i["name"] for i in items_sorted],
                    [i["risk_score"] for i in items_sorted],
                    [i["risk_color"] for i in items_sorted],
                    "Supply Chain Risk Scores by Item",
                    ylabel="Risk Score",
                    benchmark=7
                )
                pdf = generate_pdf(company_name or "Unnamed Company", industry, tool, data_rows, insights, currency_symbol, chart_buf=chart)
                st.download_button(label="Download PDF Report", data=pdf,
                    file_name=f"SPO_Deep_{(company_name or 'Report').replace(' ','_')}.pdf",
                    mime="application/pdf", use_container_width=True)

            st.write("")
            if st.button("Save Analysis to Dashboard", use_container_width=True, key="save_risk"):
                if st.session_state.get("current_company"):
                    try:
                        avg_risk = sum(i["risk_score"] for i in items_sorted) / len(items_sorted) if items_sorted else 5
                        item_data = {i["name"]: {"supply_risk": i["supply_risk"], "impact": i["impact"], "risk_level": i["risk_level"]} for i in items_sorted}
                        result = save_analysis(
                            company_id=st.session_state.current_company["id"],
                            analysis_type="Deep",
                            kpi_data={"num_items": num_items, "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk},
                            results={"tool": "Supply Chain Risk Assessment", "critical_count": len(critical_items), "single_source_count": len(single_source_items), "avg_risk_score": avg_risk, "item_risks": item_data},
                            risk_score=int(max(0, 100 - avg_risk * 10)),
                            risk_label="LOW RISK" if avg_risk < 4 else "MEDIUM RISK" if avg_risk < 7 else "HIGH RISK",
                            tool_name="Supply Chain Risk Assessment"
                        )
                        st.success("Saved to dashboard!" if result else "Save failed.")
                    except Exception as e:
                        st.error(f"Save failed: {e}")
                else:
                    st.warning("Login required to save.")