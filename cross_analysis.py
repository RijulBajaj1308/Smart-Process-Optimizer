# -*- coding: utf-8 -*-
import streamlit as st
import json
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from datetime import datetime


def generate_cross_analysis(quick_data, deep_data, category):
    """
    Connects Quick Analysis results with Deep Analysis results.
    Returns a list of connected insights.
    """
    insights = []

    if not quick_data or not deep_data:
        return insights

    quick_kpis = quick_data.get("kpi_data", {})
    quick_results = quick_data.get("results", {})
    deep_tool = deep_data.get("tool", "")
    deep_results = deep_data.get("results", {})

    if category == "Manufacturing":

        # Efficiency + Bottleneck
        if "efficiency_rate" in quick_results and quick_results["efficiency_rate"].get("status") in ["Critical", "Needs Improvement"]:
            eff_gap = quick_results["efficiency_rate"].get("gap", 0)
            if "bottleneck_station" in deep_results:
                bn = deep_results["bottleneck_station"]
                bn_ct = deep_results.get("bottleneck_ct", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "Efficiency Gap Linked to Bottleneck",
                    "quick_finding": f"Your efficiency rate is {eff_gap:.1f}% below benchmark",
                    "deep_finding": f"Your bottleneck is {bn} at {bn_ct:.1f} mins cycle time",
                    "connection": f"Your {eff_gap:.1f}% efficiency gap is directly caused by {bn} being your bottleneck. This single station is restricting your entire line output. Fix {bn} first and your efficiency will jump immediately.",
                    "priority": "Critical"
                })

        # Rejection Rate + Pareto
        if "rejection_rate" in quick_results and quick_results["rejection_rate"].get("status") in ["Critical", "Needs Improvement"]:
            rej_gap = quick_results["rejection_rate"].get("gap", 0)
            if "top_defect" in deep_results:
                top_defect = deep_results["top_defect"]
                top_defect_pct = deep_results.get("top_defect_pct", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "Rejection Rate Driven by Specific Defect",
                    "quick_finding": f"Your rejection rate is {rej_gap:.1f}% above benchmark",
                    "deep_finding": f"Your top defect is {top_defect} causing {top_defect_pct:.1f}% of all rejections",
                    "connection": f"Your high rejection rate is not a general quality problem — it is being driven specifically by {top_defect}. Fix this one defect type and you will close most of your rejection rate gap.",
                    "priority": "Critical"
                })

        # Manpower + Efficiency
        if "manpower_utilization" in quick_results and quick_results["manpower_utilization"].get("status") in ["Critical", "Needs Improvement"]:
            mp_gap = quick_results["manpower_utilization"].get("gap", 0)
            if "understaffed_stations" in deep_results:
                understaffed = deep_results["understaffed_stations"]
                overstaffed = deep_results.get("overstaffed_stations", [])
                if understaffed or overstaffed:
                    insights.append({
                        "type": "direct_link",
                        "title": "Manpower Imbalance Confirmed by Deep Analysis",
                        "quick_finding": f"Your manpower utilization is {mp_gap:.1f}% below benchmark",
                        "deep_finding": f"Understaffed: {', '.join(understaffed) if understaffed else 'None'} | Overstaffed: {', '.join(overstaffed) if overstaffed else 'None'}",
                        "connection": f"Your low manpower utilization is confirmed — workers are unevenly distributed. Moving workers from overstaffed to understaffed stations costs nothing and could close your {mp_gap:.1f}% utilization gap.",
                        "priority": "Needs Improvement"
                    })

        # OEE + Efficiency
        if "efficiency_rate" in quick_results and "oee" in deep_results:
            oee = deep_results["oee"]
            availability = deep_results.get("availability", 0)
            if availability < 85:
                insights.append({
                    "type": "supporting",
                    "title": "Machine Downtime Contributing to Low Efficiency",
                    "quick_finding": f"Your efficiency rate is below benchmark",
                    "deep_finding": f"Your OEE is {oee:.1f}% with availability at {availability:.1f}%",
                    "connection": f"Your OEE analysis shows machines are only available {availability:.1f}% of the time. This downtime is a major contributor to your low efficiency. Reducing downtime is your fastest path to efficiency improvement.",
                    "priority": "Needs Improvement"
                })

    elif category == "Distribution":

        # OTD + Route
        if "on_time_delivery" in quick_results and quick_results["on_time_delivery"].get("status") in ["Critical", "Needs Improvement"]:
            otd_gap = quick_results["on_time_delivery"].get("gap", 0)
            if "worst_route" in deep_results:
                worst = deep_results["worst_route"]
                worst_otd = deep_results.get("worst_route_otd", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "OTD Problem Concentrated in Specific Route",
                    "quick_finding": f"Your on time delivery is {otd_gap:.1f}% below benchmark",
                    "deep_finding": f"Your worst performing route is {worst} with {worst_otd:.1f}% OTD",
                    "connection": f"Your overall OTD gap is not evenly spread — it is concentrated in {worst}. Fix this route specifically and your overall OTD will improve significantly.",
                    "priority": "Critical"
                })

        # Return Rate + Returns Analysis
        if "return_rate" in quick_results and quick_results["return_rate"].get("status") in ["Critical", "Needs Improvement"]:
            ret_gap = quick_results["return_rate"].get("gap", 0)
            if "top_return_reason" in deep_results:
                top_reason = deep_results["top_return_reason"]
                top_reason_pct = deep_results.get("top_reason_pct", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "Return Rate Root Cause Identified",
                    "quick_finding": f"Your return rate is {ret_gap:.1f}% above benchmark",
                    "deep_finding": f"The top return reason is {top_reason} at {top_reason_pct:.1f}% of all returns",
                    "connection": f"Your high return rate is primarily caused by {top_reason}. This is your highest priority fix — solving this one issue will dramatically reduce your return costs.",
                    "priority": "Critical"
                })

        # Picking Accuracy + Picking Time
        if "picking_accuracy" in quick_results and quick_results["picking_accuracy"].get("status") in ["Critical", "Needs Improvement"]:
            pick_gap = quick_results["picking_accuracy"].get("gap", 0)
            if "search_time_pct" in deep_results:
                search_pct = deep_results["search_time_pct"]
                insights.append({
                    "type": "supporting",
                    "title": "Picking Accuracy Linked to Search Time",
                    "quick_finding": f"Your picking accuracy is {pick_gap:.3f}% below benchmark",
                    "deep_finding": f"Pickers spend {search_pct:.0f}% of their time searching for items",
                    "connection": f"When pickers spend {search_pct:.0f}% of their time searching, they rush the actual pick to compensate — causing accuracy errors. Fixing your warehouse slotting and labeling will improve both search time and picking accuracy simultaneously.",
                    "priority": "Needs Improvement"
                })

    elif category == "Supply Chain":

        # Supplier OTD + Scorecard
        if "supplier_otd" in quick_results and quick_results["supplier_otd"].get("status") in ["Critical", "Needs Improvement"]:
            otd_gap = quick_results["supplier_otd"].get("gap", 0)
            if "worst_supplier" in deep_results:
                worst = deep_results["worst_supplier"]
                worst_score = deep_results.get("worst_supplier_score", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "Supplier OTD Problem Traced to Specific Vendor",
                    "quick_finding": f"Your supplier on time delivery is {otd_gap:.1f}% below benchmark",
                    "deep_finding": f"Your worst supplier is {worst} with a performance score of {worst_score:.0f}/100",
                    "connection": f"Your overall supplier OTD gap is being dragged down by {worst}. Have an urgent performance review with them and set a 30 day improvement deadline.",
                    "priority": "Critical"
                })

        # Inventory Turnover + ABC
        if "inventory_turnover" in quick_results and quick_results["inventory_turnover"].get("status") in ["Critical", "Needs Improvement"]:
            inv_gap = quick_results["inventory_turnover"].get("gap", 0)
            if "c_items_in_prime" in deep_results:
                c_in_prime = deep_results["c_items_in_prime"]
                insights.append({
                    "type": "supporting",
                    "title": "Low Inventory Turnover Linked to Poor ABC Management",
                    "quick_finding": f"Your inventory turns {inv_gap:.1f} times less than benchmark",
                    "deep_finding": f"{c_in_prime} slow moving C items are taking up prime space and capital",
                    "connection": f"Your low inventory turnover is partly caused by {c_in_prime} slow moving C items sitting in your warehouse. Clearing these items or reducing their reorder quantities will directly improve your inventory turns.",
                    "priority": "Needs Improvement"
                })

        # Lead Time + Lead Time Analysis
        if "lead_time_flexibility" in quick_results and quick_results["lead_time_flexibility"].get("status") in ["Critical", "Needs Improvement"]:
            lt_gap = quick_results["lead_time_flexibility"].get("gap", 0)
            if "non_value_add_days" in deep_results:
                nva_days = deep_results["non_value_add_days"]
                total_days = deep_results.get("total_lt_days", 0)
                insights.append({
                    "type": "direct_link",
                    "title": "Lead Time Flexibility Limited by Non-Value Adding Steps",
                    "quick_finding": f"Your lead time flexibility is {lt_gap:.1f}% below benchmark",
                    "deep_finding": f"{nva_days:.1f} of your {total_days:.1f} total lead time days are non-value adding",
                    "connection": f"Your lead time flexibility is low because {nva_days:.1f} days of your process are pure waiting and delays. Eliminating these non-value adding steps is how you create flexibility without adding resources.",
                    "priority": "Needs Improvement"
                })

    # If no specific connections found, add general insight
    if not insights:
        insights.append({
            "type": "general",
            "title": "Run Both Analyses on Same Metrics for Deeper Connections",
            "quick_finding": "Quick Analysis completed",
            "deep_finding": "Deep Analysis completed",
            "connection": "To get the most from Cross Analysis, make sure your Deep Analysis tool matches your biggest Quick Analysis problem. For example if your Quick Analysis shows low efficiency, run the Bottleneck Identifier in Deep Analysis.",
            "priority": "Info"
        })

    return insights


def make_cross_chart(insights):
    if not insights:
        return None

    titles = [ins["title"][:30] + "..." if len(ins["title"]) > 30 else ins["title"] for ins in insights]
    priority_colors = {
        "Critical": "#CC0000",
        "Needs Improvement": "#FFD700",
        "Info": "#444444",
        "supporting": "#FF6B00"
    }
    bar_colors = [priority_colors.get(ins["priority"], "#888888") for ins in insights]

    fig, ax = plt.subplots(figsize=(8, max(3, len(insights) * 0.8 + 1)))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f9f9f9")

    y_pos = range(len(titles))
    ax.barh(list(y_pos), [1] * len(titles), color=bar_colors, alpha=0.85)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(titles, fontsize=9)
    ax.set_xticks([])
    ax.set_title("Cross Analysis — Connected Findings", fontsize=11, fontweight="bold", pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    red_patch = mpatches.Patch(color="#CC0000", label="Critical Connection")
    yellow_patch = mpatches.Patch(color="#FFD700", label="Needs Attention")
    ax.legend(handles=[red_patch, yellow_patch], fontsize=8, loc="lower right")

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    plt.close()
    return buf


def generate_cross_pdf(company_name, category, industry, insights, quick_summary, deep_summary):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch,
                            leftMargin=0.7*inch, rightMargin=0.7*inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle("T", parent=styles["Title"], textColor=colors.HexColor("#CC0000"), fontSize=20, spaceAfter=2)
    sub_style = ParagraphStyle("S", parent=styles["Normal"], fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=14)
    heading_style = ParagraphStyle("H", parent=styles["Heading2"], textColor=colors.HexColor("#CC0000"), fontSize=13, spaceBefore=16, spaceAfter=8)
    body_style = ParagraphStyle("B", parent=styles["Normal"], fontSize=9.5, leading=14, spaceAfter=8, alignment=TA_LEFT)
    footer_style = ParagraphStyle("F", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#999999"))

    elements.append(Paragraph("Smart Process Optimizer", title_style))
    elements.append(Paragraph("Cross Analysis Report", sub_style))

    meta = [
        ["Company", company_name],
        ["Category", category],
        ["Industry", industry],
        ["Report Date", datetime.now().strftime("%B %d, %Y")],
    ]
    meta_table = Table(meta, colWidths=[1.7*inch, 4.3*inch])
    meta_table.setStyle(TableStyle([
        ("FONTSIZE", (0,0), (-1,-1), 9.5),
        ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#CC0000")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 2),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 4))
    elements.append(Table([[""]], colWidths=[6*inch], style=[("LINEBELOW", (0,0), (-1,0), 1, colors.HexColor("#CC0000"))]))

    # Summary boxes
    elements.append(Paragraph("Analysis Summary", heading_style))
    summary_data = [
        ["Quick Analysis", "Deep Analysis"],
        [quick_summary, deep_summary]
    ]
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a1a1a")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    elements.append(summary_table)

    # Chart
    if insights:
        chart = make_cross_chart(insights)
        if chart:
            elements.append(Spacer(1, 8))
            elements.append(RLImage(chart, width=6.5*inch, height=max(2.5*inch, len(insights) * 0.6*inch + inch)))
            elements.append(Spacer(1, 8))

    # Connected Insights
    elements.append(Paragraph("Connected Findings", heading_style))
    for i, insight in enumerate(insights, 1):
        priority_color = "#CC0000" if insight["priority"] == "Critical" else "#B8860B" if insight["priority"] == "Needs Improvement" else "#444444"

        elements.append(Paragraph(f"<b>{i}. {insight['title']}</b>", ParagraphStyle(
            "IH", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor(priority_color), spaceAfter=4, spaceBefore=12
        )))

        insight_data = [
            ["Quick Analysis Found", insight["quick_finding"]],
            ["Deep Analysis Found", insight["deep_finding"]],
            ["Connection", insight["connection"]],
        ]
        insight_table = Table(insight_data, colWidths=[1.5*inch, 4.5*inch])
        insight_table.setStyle(TableStyle([
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#CC0000")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#eeeeee")),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        elements.append(insight_table)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Generated by Smart Process Optimizer (SPO) - smart-process-optimizer.streamlit.app", footer_style))
    doc.build(elements)
    buffer.seek(0)
    return buffer


def show_cross_analysis(company, analyses):
    """
    Shows the Cross Analysis tab on the dashboard for a company.
    """
    if len(analyses) < 2:
        st.markdown("""
        <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 20px 24px; text-align: center;">
            <p style="color: #E8001D; font-weight: 700; margin: 0 0 8px 0;">Cross Analysis Not Available Yet</p>
            <p style="color: #555555; font-size: 0.85rem; margin: 0;">You need at least one Quick Analysis and one Deep Analysis for this company to run Cross Analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Get latest quick and deep analyses
    quick_analysis = None
    deep_analysis = None

    for a in analyses:
        if a["analysis_type"] == "Quick" and not quick_analysis:
            quick_analysis = a
        elif a["analysis_type"] == "Deep" and not deep_analysis:
            deep_analysis = a
        if quick_analysis and deep_analysis:
            break

    if not quick_analysis or not deep_analysis:
        st.markdown("""
        <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 20px 24px; text-align: center;">
            <p style="color: #E8001D; font-weight: 700; margin: 0 0 8px 0;">Need Both Quick and Deep Analysis</p>
            <p style="color: #555555; font-size: 0.85rem; margin: 0;">Run both a Quick Analysis and a Deep Analysis for this company to unlock Cross Analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Parse saved data
    try:
        quick_kpi = json.loads(quick_analysis.get("kpi_data", "{}"))
        quick_results = json.loads(quick_analysis.get("results", "{}"))
        deep_kpi = json.loads(deep_analysis.get("kpi_data", "{}"))
        deep_results = json.loads(deep_analysis.get("results", "{}"))
    except:
        quick_kpi, quick_results, deep_kpi, deep_results = {}, {}, {}, {}

    quick_data = {"kpi_data": quick_kpi, "results": quick_results}
    deep_data = {"kpi_data": deep_kpi, "results": deep_results, "tool": deep_analysis.get("analysis_type", "")}

    category = company.get("category", "Manufacturing")
    industry = company.get("industry", "")

    # Show header
    st.markdown(f"""
    <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;">
        <p style="color: #E8001D; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 4px 0;">Cross Analysis</p>
        <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Connecting your Quick Analysis findings with your Deep Analysis findings to reveal the real root causes.</p>
    </div>
    """, unsafe_allow_html=True)

    # Show summary boxes
    col1, col2 = st.columns(2)
    with col1:
        quick_risk = quick_analysis.get("risk_score", "N/A")
        quick_label = quick_analysis.get("risk_label", "")
        st.markdown(f"""
        <div style="background: #1a1a1a; border: 2px solid #CC0000; border-radius: 10px; padding: 16px 20px;">
            <p style="color: #CC0000; font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 8px 0;">Quick Analysis</p>
            <p style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin: 0;">Risk Score: {quick_risk}/100</p>
            <p style="color: #888888; font-size: 0.82rem; margin: 4px 0 0 0;">{quick_label}</p>
            <p style="color: #555555; font-size: 0.75rem; margin: 4px 0 0 0;">{quick_analysis.get('created_at', '')[:10]}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        deep_risk = deep_analysis.get("risk_score", "N/A")
        deep_label = deep_analysis.get("risk_label", "")
        st.markdown(f"""
        <div style="background: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; padding: 16px 20px;">
            <p style="color: #FFD700; font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 8px 0;">Deep Analysis</p>
            <p style="color: #ffffff; font-size: 1.1rem; font-weight: 700; margin: 0;">Risk Score: {deep_risk}/100</p>
            <p style="color: #888888; font-size: 0.82rem; margin: 4px 0 0 0;">{deep_label}</p>
            <p style="color: #555555; font-size: 0.75rem; margin: 4px 0 0 0;">{deep_analysis.get('created_at', '')[:10]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Generate cross analysis insights
    insights = generate_cross_analysis(quick_data, deep_data, category)

    if insights:
        st.subheader("Connected Findings")
        st.write("Here is how your Quick Analysis and Deep Analysis results connect:")
        st.write("")

        for i, insight in enumerate(insights, 1):
            if insight["priority"] == "Critical":
                color = "#CC0000"
                icon = "🚨"
            elif insight["priority"] == "Needs Improvement":
                color = "#FFD700"
                icon = "⚠️"
            else:
                color = "#444444"
                icon = "ℹ️"

            st.markdown(f"""
            <div style="background: #1a1a1a; border: 1px solid {color}; border-radius: 10px; padding: 20px; margin-bottom: 12px;">
                <p style="color: {color}; font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 8px 0;">{icon} Connection {i} — {insight['priority']}</p>
                <p style="color: #ffffff; font-size: 1rem; font-weight: 700; margin: 0 0 12px 0;">{insight['title']}</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                    <div style="background: rgba(204,0,0,0.08); border-radius: 6px; padding: 10px 14px;">
                        <p style="color: #CC0000; font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 4px 0;">Quick Analysis Found</p>
                        <p style="color: #cccccc; font-size: 0.85rem; margin: 0;">{insight['quick_finding']}</p>
                    </div>
                    <div style="background: rgba(255,215,0,0.08); border-radius: 6px; padding: 10px 14px;">
                        <p style="color: #FFD700; font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 4px 0;">Deep Analysis Found</p>
                        <p style="color: #cccccc; font-size: 0.85rem; margin: 0;">{insight['deep_finding']}</p>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.04); border-left: 3px solid {color}; border-radius: 0 6px 6px 0; padding: 10px 14px;">
                    <p style="color: #aaaaaa; font-size: 0.88rem; margin: 0; line-height: 1.6;">{insight['connection']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Generate PDF
    st.subheader("Generate Cross Analysis Report")
    st.write("Download a combined PDF report connecting your Quick and Deep Analysis findings")

    if st.button("Generate Cross Analysis Report", use_container_width=True, key=f"cross_pdf_{company['id']}"):
        quick_summary = f"Risk Score: {quick_analysis.get('risk_score', 'N/A')}/100 — {quick_analysis.get('risk_label', '')}"
        deep_summary = f"Risk Score: {deep_analysis.get('risk_score', 'N/A')}/100 — {deep_analysis.get('risk_label', '')}"

        pdf = generate_cross_pdf(
            company.get("name", "Company"),
            category,
            industry,
            insights,
            quick_summary,
            deep_summary
        )

        st.download_button(
            label="Download Cross Analysis PDF",
            data=pdf,
            file_name=f"SPO_Cross_Analysis_{company.get('name', 'Report').replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key=f"cross_dl_{company['id']}"
        )