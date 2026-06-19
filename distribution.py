# -*- coding: utf-8 -*-
import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from datetime import datetime
import io

distribution_benchmarks = {
    "Warehouse and Distribution": {
        "order_fulfillment_rate": 95.000,
        "on_time_delivery": 92.000,
        "warehouse_utilization": 85.000,
        "picking_accuracy": 99.900,
        "inventory_turnover": 12.000,
        "return_rate": 2.000,
        "cost_per_order": 50.000
    },
    "Cold Chain Distribution": {
        "order_fulfillment_rate": 97.000,
        "on_time_delivery": 95.000,
        "warehouse_utilization": 80.000,
        "picking_accuracy": 99.900,
        "inventory_turnover": 20.000,
        "return_rate": 1.000,
        "cost_per_order": 80.000
    },
    "E-commerce Fulfillment": {
        "order_fulfillment_rate": 98.500,
        "on_time_delivery": 96.500,
        "warehouse_utilization": 90.000,
        "picking_accuracy": 99.800,
        "inventory_turnover": 15.000,
        "return_rate": 8.000,
        "cost_per_order": 40.000
    },
    "Pharmaceutical Distribution": {
        "order_fulfillment_rate": 99.000,
        "on_time_delivery": 98.000,
        "warehouse_utilization": 75.000,
        "picking_accuracy": 99.990,
        "inventory_turnover": 24.000,
        "return_rate": 0.500,
        "cost_per_order": 120.000
    },
    "Automotive Parts Distribution": {
        "order_fulfillment_rate": 96.000,
        "on_time_delivery": 94.000,
        "warehouse_utilization": 82.000,
        "picking_accuracy": 99.500,
        "inventory_turnover": 8.000,
        "return_rate": 1.500,
        "cost_per_order": 75.000
    },
    "Electronics Distribution": {
        "order_fulfillment_rate": 97.000,
        "on_time_delivery": 95.000,
        "warehouse_utilization": 85.000,
        "picking_accuracy": 99.800,
        "inventory_turnover": 10.000,
        "return_rate": 3.000,
        "cost_per_order": 60.000
    },
    "Food and Beverage Distribution": {
        "order_fulfillment_rate": 97.500,
        "on_time_delivery": 95.500,
        "warehouse_utilization": 88.000,
        "picking_accuracy": 99.700,
        "inventory_turnover": 26.000,
        "return_rate": 2.500,
        "cost_per_order": 35.000
    },
    "Textile and Apparel Distribution": {
        "order_fulfillment_rate": 94.000,
        "on_time_delivery": 91.000,
        "warehouse_utilization": 80.000,
        "picking_accuracy": 99.300,
        "inventory_turnover": 6.000,
        "return_rate": 12.000,
        "cost_per_order": 45.000
    },
    "Eco Friendly Packaging Distribution": {
        "order_fulfillment_rate": 95.000,
        "on_time_delivery": 93.000,
        "warehouse_utilization": 83.000,
        "picking_accuracy": 99.500,
        "inventory_turnover": 10.000,
        "return_rate": 2.000,
        "cost_per_order": 55.000
    },
    "Pulp and Paper Distribution": {
        "order_fulfillment_rate": 94.000,
        "on_time_delivery": 91.000,
        "warehouse_utilization": 80.000,
        "picking_accuracy": 99.200,
        "inventory_turnover": 8.000,
        "return_rate": 1.500,
        "cost_per_order": 65.000
    }
}

performance_labels = {
    "order_fulfillment_rate": "Order Fulfillment Rate (%)",
    "on_time_delivery": "On Time Delivery (%)",
    "warehouse_utilization": "Warehouse Utilization (%)",
    "picking_accuracy": "Picking Accuracy (%)",
    "inventory_turnover": "Inventory Turnover (times/year)",
    "return_rate": "Return Rate (%)",
    "cost_per_order": "Cost per Order"
}

def analyze_kpis(kpi_data, benchmarks):
    results = {}
    for kpi, value in kpi_data.items():
        benchmark = benchmarks[kpi]
        if kpi in ["order_fulfillment_rate", "on_time_delivery",
                   "warehouse_utilization", "picking_accuracy", "inventory_turnover"]:
            gap = value - benchmark
            if gap >= 0:
                status = "Good"
            elif gap >= -5:
                status = "Needs Improvement"
            else:
                status = "Critical"
        else:
            gap = benchmark - value
            if gap >= 0:
                status = "Good"
            elif gap >= -5:
                status = "Needs Improvement"
            else:
                status = "Critical"
        results[kpi] = {
            "value": value,
            "benchmark": benchmark,
            "gap": abs(gap),
            "status": status
        }
    return results

def calculate_priority_score(analysis):
    scores = {}
    for kpi, result in analysis.items():
        if result["status"] == "Critical":
            scores[kpi] = result["gap"] * 3
        elif result["status"] == "Needs Improvement":
            scores[kpi] = result["gap"] * 1.5
        else:
            scores[kpi] = 0
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def generate_action_plan(analysis, performance_labels, recommendations):
    critical_kpis = [(kpi, result) for kpi, result in analysis.items() if result["status"] == "Critical"]
    improvement_kpis = [(kpi, result) for kpi, result in analysis.items() if result["status"] == "Needs Improvement"]
    good_kpis = [(kpi, result) for kpi, result in analysis.items() if result["status"] == "Good"]

    plan = {"week1": [], "week2": [], "week3": [], "week4": []}

    for kpi, result in critical_kpis:
        plan["week1"].append({
            "action": f"URGENT — {performance_labels.get(kpi, kpi)} is at {result['value']:.3f} against a benchmark of {result['benchmark']:.3f}. This is your most critical problem and needs immediate attention this week.",
            "priority": "Critical"
        })

    if not critical_kpis and improvement_kpis:
        kpi, result = improvement_kpis[0]
        plan["week1"].append({
            "action": f"Start with {performance_labels.get(kpi, kpi)} — currently {result['value']:.3f} vs benchmark {result['benchmark']:.3f}. This is your biggest gap.",
            "priority": "Needs Improvement"
        })

    plan["week2"].append({"action": f"Map your current {category_name.lower()} process from start to finish and identify where time and resources are being lost", "priority": "Standard"})
    for kpi, result in critical_kpis:
        plan["week2"].append({"action": f"Conduct a detailed root cause analysis for {performance_labels.get(kpi, kpi)} — speak to your team to understand what is actually happening", "priority": "Critical"})
    for kpi, result in improvement_kpis[:2]:
        plan["week2"].append({"action": f"Investigate {performance_labels.get(kpi, kpi)} — identify the top 3 contributing factors and rank them by impact", "priority": "Needs Improvement"})

    for rec in recommendations[:3]:
        plan["week3"].append({"action": rec, "priority": "Implementation"})
    if not recommendations:
        plan["week3"].append({"action": "Implement the process improvements identified during Week 2 investigation", "priority": "Implementation"})

    plan["week4"].append({"action": "Re-enter all your performance numbers in SPO and compare against your Week 1 starting point", "priority": "Review"})
    plan["week4"].append({"action": "Quantify the improvement — calculate how much has actually changed in numbers", "priority": "Review"})
    plan["week4"].append({"action": "Document what worked and what did not — this becomes your Standard Operating Procedure going forward", "priority": "Review"})
    if good_kpis:
        good_names = ", ".join([performance_labels.get(k, k) for k, r in good_kpis])
        plan["week4"].append({"action": f"Maintain your strong performance in: {good_names}", "priority": "Maintain"})

    return plan

def generate_dynamic_insights(kpi, value, benchmark, gap, status):
    if kpi == "order_fulfillment_rate":
        if status == "Critical":
            cause = f"Your order fulfillment rate is {gap:.3f}% below the benchmark of {benchmark:.3f}%. This means for every 100 orders your customers place, more than {gap:.1f} of them are not being fulfilled. That is lost revenue and disappointed customers."
            rec = f"At {value:.3f}% fulfillment you are losing a significant number of orders. Check your stock availability first — are you running out of your top selling items? Fix your reorder triggers and get real time inventory visibility in place this week."
        else:
            cause = f"Your order fulfillment rate of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. You are almost there but a small number of orders are still not being fulfilled."
            rec = f"You are {gap:.3f}% away from benchmark. Identify which specific products are causing the unfulfilled orders and fix their reorder points. This is a small fix that could close the gap quickly."

    elif kpi == "on_time_delivery":
        if status == "Critical":
            cause = f"Your on time delivery rate of {value:.3f}% is {gap:.3f}% below the benchmark of {benchmark:.3f}%. More than {gap:.1f} in every 100 deliveries are arriving late. Late deliveries damage customer trust and can cost you repeat business."
            rec = f"At {value:.3f}% on time delivery you need to urgently review your delivery routes and schedules. Are your vehicles being loaded optimally? Are routes planned or ad hoc? Start with route optimization and you should see immediate improvement."
        else:
            cause = f"Your on time delivery rate is {gap:.3f}% below benchmark. Most deliveries are on time but a small percentage are consistently late."
            rec = f"A {gap:.3f}% gap in on time delivery is fixable. Look at which routes or customers are causing the late deliveries — often the problem is concentrated in specific areas or time slots."

    elif kpi == "warehouse_utilization":
        if status == "Critical":
            cause = f"Your warehouse is only {value:.3f}% utilized against a benchmark of {benchmark:.3f}%. You are paying for {gap:.1f}% more space than you are using. That is dead cost sitting in your P&L every month."
            rec = f"At {value:.3f}% utilization your warehouse layout needs a serious review. Start by identifying dead stock occupying space and relocate or clear it. Then look at whether you can use vertical space more effectively with additional racking."
        else:
            cause = f"Your warehouse utilization of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. You have unused capacity that is costing you money."
            rec = f"Closing a {gap:.3f}% utilization gap is achievable with better slotting. Move your fast moving items to easily accessible locations and use the freed up space more efficiently."

    elif kpi == "picking_accuracy":
        if status == "Critical":
            cause = f"Your picking accuracy of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. For every 1000 orders picked, approximately {gap*10:.0f} contain errors. Wrong items shipped means returns, customer complaints and rework costs."
            rec = f"At {value:.3f}% picking accuracy you need to implement scan and verify immediately. Manual picking without verification is the most common cause of this problem. Even basic barcode scanning at the pick point will dramatically improve your accuracy."
        else:
            cause = f"Your picking accuracy of {value:.3f}% is {gap:.3f}% below benchmark. You are very close but small picking errors are still slipping through."
            rec = f"A {gap:.3f}% accuracy gap at this level means your process is mostly working but needs tightening. Check if errors are concentrated in specific product areas or with specific pickers and address those specifically."

    elif kpi == "inventory_turnover":
        if status == "Critical":
            cause = f"Your inventory turns only {value:.3f} times per year against a benchmark of {benchmark:.3f}. Your stock is sitting for too long. Capital is tied up in slow moving inventory that is not generating returns."
            rec = f"At {value:.3f} turns you have a slow moving inventory problem. Run an ABC analysis this week to identify your slowest moving SKUs. Then either reduce their reorder quantities or run promotions to clear the excess stock."
        else:
            cause = f"Your inventory turns {value:.3f} times per year which is {gap:.3f} turns below the {benchmark:.3f} benchmark. Your stock is moving slower than it should be."
            rec = f"Closing a {gap:.3f} turn gap means better demand forecasting and tighter purchasing discipline. Align your purchasing more closely with actual sales velocity to stop over-ordering slow moving items."

    elif kpi == "return_rate":
        if status == "Critical":
            cause = f"Your return rate of {value:.3f}% is {gap:.3f}% above the {benchmark:.3f}% benchmark. You are processing significantly more returns than you should be. Every return costs you twice — once for the outbound delivery and once for the return handling."
            rec = f"At {value:.3f}% returns you need to understand why customers are sending things back. Are items damaged in transit? Are wrong items being sent? Are products not meeting expectations? The answer determines the fix."
        else:
            cause = f"Your return rate of {value:.3f}% is {gap:.3f}% above benchmark. Returns are slightly higher than they should be and each one is an unnecessary cost."
            rec = f"A {gap:.3f}% excess return rate is manageable. Check if returns are concentrated in specific product categories or customers. Often a small fix in packaging or product descriptions can make a meaningful difference."

    elif kpi == "cost_per_order":
        if status == "Critical":
            cause = f"Your cost per order is {gap:.3f} units above the benchmark. You are spending significantly more per order than industry leaders. This is eating into your margins on every single transaction."
            rec = f"At this cost per order level you need to look at your biggest cost drivers immediately. Is it labor, transport, packaging or returns processing? Identify the top two costs and target them specifically for reduction."
        else:
            cause = f"Your cost per order is {gap:.3f} units above the {benchmark:.3f} benchmark. You are slightly more expensive per order than you should be."
            rec = f"Closing a {gap:.3f} unit cost per order gap requires looking at where you can consolidate or streamline. Batching orders, optimizing routes or renegotiating courier rates are typically the fastest wins."

    else:
        cause = f"This metric is {gap:.3f} units away from the industry benchmark of {benchmark:.3f}. This gap is affecting your overall distribution performance."
        rec = f"Focus on understanding why this metric is {gap:.3f} units below benchmark and develop a specific action plan to close the gap within the next 30 days."

    return cause, rec



def make_performance_chart(analysis, performance_labels):
    kpis = list(analysis.keys())
    your_vals = [analysis[k]['value'] for k in kpis]
    bench_vals = [analysis[k]['benchmark'] for k in kpis]
    bar_colors = []
    for k in kpis:
        if analysis[k]['status'] == 'Critical':
            bar_colors.append('#CC0000')
        elif analysis[k]['status'] == 'Needs Improvement':
            bar_colors.append('#FFD700')
        else:
            bar_colors.append('#00CC00')
    labels = [performance_labels.get(k, k).replace(' (%)', '').replace(' (mins)', '').replace(' (days)', '').replace(' (times/year)', '').replace(' (% of Revenue)', '') for k in kpis]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f9f9f9')
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], your_vals, width=0.35, color=bar_colors, alpha=0.9)
    ax.bar([i + 0.2 for i in x], bench_vals, width=0.35, color='#444444', alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=7, rotation=20, ha='right')
    ax.set_title('Your Performance vs Industry Benchmark', fontsize=11, fontweight='bold', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    red_patch = mpatches.Patch(color='#CC0000', label='Critical')
    yellow_patch = mpatches.Patch(color='#FFD700', label='Needs Improvement')
    green_patch = mpatches.Patch(color='#00CC00', label='Good')
    bench_patch = mpatches.Patch(color='#444444', label='Benchmark')
    ax.legend(handles=[red_patch, yellow_patch, green_patch, bench_patch], fontsize=7, loc='upper right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    return buf

def make_risk_pie(critical, needs_improvement, good):
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor('#ffffff')
    labels = ['Critical', 'Needs Improvement', 'Good']
    sizes = [critical, needs_improvement, good]
    clrs = ['#CC0000', '#FFD700', '#00CC00']
    non_zero = [(l, s, c) for l, s, c in zip(labels, sizes, clrs) if s > 0]
    if non_zero:
        lbls, szs, cs = zip(*non_zero)
        ax.pie(szs, labels=lbls, colors=cs, autopct='%1.0f%%', startangle=90, textprops={'fontsize': 9})
        ax.set_title('Risk Distribution', fontsize=10, fontweight='bold')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    return buf

def make_projected_outcome_chart(projections, performance_labels):
    if not projections:
        return None
    kpis = list(projections.keys())
    current_vals = [projections[k][0] for k in kpis]
    projected_vals = [projections[k][1] for k in kpis]
    labels = [performance_labels.get(k, k).replace(' (%)', '').replace(' (mins)', '').replace(' (days)', '').replace(' (times/year)', '').replace(' (% of Revenue)', '') for k in kpis]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f9f9f9')
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], current_vals, width=0.35, color='#CC0000', alpha=0.9, label='Now')
    ax.bar([i + 0.2 for i in x], projected_vals, width=0.35, color='#00CC00', alpha=0.9, label='Projected')
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8, rotation=15, ha='right')
    ax.set_title('Projected Outcome After Implementing Recommendations', fontsize=10, fontweight='bold', pad=8)
    ax.legend(fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    plt.close()
    return buf


def generate_pdf_report(company_name, category, industry, business_model, currency_symbol,
                          analysis, performance_labels, risk_score, risk_label,
                          root_causes, recommendations, priority_list, projections, pfmea_data=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6*inch, bottomMargin=0.6*inch,
                             leftMargin=0.7*inch, rightMargin=0.7*inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], textColor=colors.HexColor('#CC0000'), fontSize=20, spaceAfter=2)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#555555'), spaceAfter=14)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], textColor=colors.HexColor('#CC0000'), fontSize=13, spaceBefore=16, spaceAfter=8)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9.5, leading=14, spaceAfter=8, alignment=TA_LEFT)
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#999999'))

    elements.append(Paragraph("Smart Process Optimizer", title_style))
    elements.append(Paragraph("Performance Analysis Report", subtitle_style))

    meta_data = [
        ["Company / Facility", company_name],
        ["Category", category],
        ["Industry", industry],
        ["Business Model", business_model],
        ["Report Date", datetime.now().strftime("%B %d, %Y")],
    ]
    meta_table = Table(meta_data, colWidths=[1.7*inch, 4.3*inch])
    meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#CC0000')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 4))
    elements.append(Table([['']], colWidths=[6*inch], style=[('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#CC0000'))]))

    elements.append(Paragraph("Performance Analysis", heading_style))
    perf_rows = [["Metric", "Your Number", "Benchmark", "Status"]]
    for kpi, result in analysis.items():
        perf_rows.append([
            performance_labels.get(kpi, kpi),
            f"{result['value']:.3f}",
            f"{result['benchmark']:.3f}",
            result['status']
        ])
    perf_table = Table(perf_rows, colWidths=[2.3*inch, 1.3*inch, 1.3*inch, 1.1*inch])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]
    for i, (kpi, result) in enumerate(analysis.items()):
        row_idx = i + 1
        if result['status'] == 'Critical':
            style_cmds.append(('TEXTCOLOR', (3, row_idx), (3, row_idx), colors.HexColor('#CC0000')))
        elif result['status'] == 'Needs Improvement':
            style_cmds.append(('TEXTCOLOR', (3, row_idx), (3, row_idx), colors.HexColor('#B8860B')))
        else:
            style_cmds.append(('TEXTCOLOR', (3, row_idx), (3, row_idx), colors.HexColor('#008000')))
    perf_table.setStyle(TableStyle(style_cmds))
    elements.append(perf_table)

    if include_charts:
        try:
            from reportlab.platypus import Image as RLImage
            perf_chart = make_performance_chart(analysis, performance_labels)
            elements.append(Spacer(1, 8))
            elements.append(RLImage(perf_chart, width=6.5*inch, height=2.6*inch))
            elements.append(Spacer(1, 8))
        except Exception:
            pass

    elements.append(Paragraph("Overall Risk Assessment", heading_style))
    elements.append(Paragraph(f"<b>Risk Score:</b> {risk_score} / 100 &nbsp;&nbsp; <b>Status:</b> {risk_label}", body_style))

    if include_charts:
        try:
            from reportlab.platypus import Image as RLImage
            critical_count = sum(1 for r in analysis.values() if r['status'] == 'Critical')
            needs_count = sum(1 for r in analysis.values() if r['status'] == 'Needs Improvement')
            good_count = sum(1 for r in analysis.values() if r['status'] == 'Good')
            risk_chart = make_risk_pie(critical_count, needs_count, good_count)
            elements.append(RLImage(risk_chart, width=3*inch, height=2.3*inch))
        except Exception:
            pass

    if root_causes:
        elements.append(Paragraph("What is Happening", heading_style))
        for cause in root_causes:
            elements.append(Paragraph(f"&bull; {cause}", body_style))

    if recommendations:
        elements.append(Paragraph("What You Should Do", heading_style))
        for rec in recommendations:
            elements.append(Paragraph(f"&bull; {rec}", body_style))

    if priority_list:
        elements.append(Paragraph("Priority Order to Fix", heading_style))
        for i, item in enumerate(priority_list, 1):
            elements.append(Paragraph(f"{i}. {item}", body_style))

    if projections:
        elements.append(Paragraph("Projected Outcome", heading_style))
        proj_rows = [["Metric", "Now", "Projected"]]
        for kpi, (current, projected) in projections.items():
            proj_rows.append([performance_labels.get(kpi, kpi), f"{current:.3f}", f"{projected:.3f}"])
        proj_table = Table(proj_rows, colWidths=[2.5*inch, 1.75*inch, 1.75*inch])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(proj_table)


    if action_plan_data:
        elements.append(Paragraph("30 Day Action Plan", heading_style))
        week_names = {"week1": "Week 1 — Immediate Action", "week2": "Week 2 — Investigate", "week3": "Week 3 — Implement", "week4": "Week 4 — Measure and Review"}
        for week_key, week_name in week_names.items():
            items = action_plan_data.get(week_key, [])
            if items:
                elements.append(Paragraph(f"<b>{week_name}</b>", body_style))
                for item in items:
                    elements.append(Paragraph(f"&bull; {item['action']}", body_style))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Generated by Smart Process Optimizer (SPO) - smart-process-optimizer.streamlit.app", footer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def show_distribution(industry, currency_symbol="$"):
    benchmarks = distribution_benchmarks[industry]

    st.sidebar.title("Enter Your Performance Numbers")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    order_fulfillment_rate = st.sidebar.number_input("Order Fulfillment Rate (%)", min_value=0.000, max_value=100.000, value=88.000, step=0.001, format="%.3f")
    on_time_delivery = st.sidebar.number_input("On Time Delivery (%)", min_value=0.000, max_value=100.000, value=85.000, step=0.001, format="%.3f")
    warehouse_utilization = st.sidebar.number_input("Warehouse Utilization (%)", min_value=0.000, max_value=100.000, value=75.000, step=0.001, format="%.3f")
    picking_accuracy = st.sidebar.number_input("Picking Accuracy (%)", min_value=90.000, max_value=100.000, value=95.000, step=0.001, format="%.3f")
    inventory_turnover = st.sidebar.number_input("Inventory Turnover (times/year)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
    return_rate = st.sidebar.number_input("Return Rate (%)", min_value=0.000, max_value=30.000, value=5.000, step=0.001, format="%.3f")
    cost_per_order = st.sidebar.number_input(f"Cost per Order ({currency_symbol})", min_value=0.000, max_value=500.000, value=70.000, step=0.001, format="%.3f")

    kpi_data = {
        "order_fulfillment_rate": order_fulfillment_rate,
        "on_time_delivery": on_time_delivery,
        "warehouse_utilization": warehouse_utilization,
        "picking_accuracy": picking_accuracy,
        "inventory_turnover": inventory_turnover,
        "return_rate": return_rate,
        "cost_per_order": cost_per_order
    }

    analysis = analyze_kpis(kpi_data, benchmarks)

    company_name = st.text_input("Company / Facility Name", placeholder="e.g. Ahuja Radios")
    st.divider()

    st.header("Performance Analysis")
    st.caption(f"Benchmarks based on {industry} standards in India")
    col1, col2, col3 = st.columns(3)

    status_icons = {
        "Good": "✅",
        "Needs Improvement": "⚠️",
        "Critical": "🚨"
    }

    for i, (kpi, result) in enumerate(analysis.items()):
        col = [col1, col2, col3][i % 3]
        with col:
            if result['status'] == "Good":
                color = "#00CC00"
            elif result['status'] == "Needs Improvement":
                color = "#FFD700"
            else:
                color = "#CC0000"

            st.markdown(f"""
                <div style="
                    background-color: #1a1a1a;
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px 0;
                    text-align: center;">
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{status_icons[result['status']]} {performance_labels[kpi]}</p>
                    <p style="color: {color}; font-size: 2rem; font-weight: 800; margin: 5px 0;">{result['value']:.3f}</p>
                    <p style="color: #888888; font-size: 0.8rem; margin: 0;">Benchmark: {result['benchmark']:.3f}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.header("Overall Distribution Risk Assessment")

    critical_count = sum(1 for r in analysis.values() if r['status'] == "Critical")
    needs_improvement_count = sum(1 for r in analysis.values() if r['status'] == "Needs Improvement")
    good_count = sum(1 for r in analysis.values() if r['status'] == "Good")
    risk_score = 100 - ((critical_count * 20) + (needs_improvement_count * 10))
    risk_score = max(0, min(100, risk_score))

    if risk_score >= 80:
        risk_color = "#00CC00"
        risk_label = "LOW RISK"
        risk_icon = "✅"
    elif risk_score >= 50:
        risk_color = "#FFD700"
        risk_label = "MEDIUM RISK"
        risk_icon = "⚠️"
    else:
        risk_color = "#CC0000"
        risk_label = "HIGH RISK"
        risk_icon = "🚨"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid {risk_color}; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Overall Risk Score</p>
            <p style="color: {risk_color}; font-size: 3rem; font-weight: 900; margin: 0;">{risk_score}</p>
            <p style="color: {risk_color}; font-size: 1rem; margin: 0;">{risk_icon} {risk_label}</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #CC0000; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Critical Areas</p>
            <p style="color: #CC0000; font-size: 3rem; font-weight: 900; margin: 0;">{critical_count}</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Needs Improvement</p>
            <p style="color: #FFD700; font-size: 3rem; font-weight: 900; margin: 0;">{needs_improvement_count}</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Performing Well</p>
            <p style="color: #00CC00; font-size: 3rem; font-weight: 900; margin: 0;">{good_count}</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    st.header("What is Wrong and How to Fix It")
    st.caption(f"Analysis based on your actual numbers compared to {industry} benchmark")

    root_causes = []
    recommendations = []
    improvements = {}

    for kpi, result in analysis.items():
        if result["status"] in ["Needs Improvement", "Critical"]:
            cause, rec = generate_dynamic_insights(
                kpi, result["value"], result["benchmark"], result["gap"], result["status"]
            )
            root_causes.append(cause)
            recommendations.append(rec)

            if kpi in ["order_fulfillment_rate", "on_time_delivery",
                       "warehouse_utilization", "picking_accuracy", "inventory_turnover"]:
                improvements[kpi] = min(result["benchmark"], result["value"] + result["gap"] * 0.5)
            else:
                improvements[kpi] = max(result["benchmark"], result["value"] - result["gap"] * 0.5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What is happening in your distribution?")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("Your distribution is performing at or above benchmark level!")

    with col2:
        st.subheader("What should you do about it?")
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("No action required. Focus on maintaining your current performance.")

    st.divider()

    st.header("What to Fix First")
    st.write("Focus on these areas first for maximum impact:")

    priority_scores = calculate_priority_score(analysis)
    priority_rank = 1
    priority_list_names = []

    for kpi, score in priority_scores.items():
        if score > 0:
            result = analysis[kpi]
            priority_list_names.append(performance_labels[kpi])
            if result['status'] == "Critical":
                color = "#CC0000"
                icon = "🚨"
            else:
                color = "#FFD700"
                icon = "⚠️"

            st.markdown(f"""
                <div style="background-color: #1a1a1a; border-left: 4px solid {color}; padding: 10px 15px; margin: 5px 0; border-radius: 5px;">
                    <span style="color: {color}; font-weight: 800;">{icon} #{priority_rank}</span>
                    <span style="color: #ffffff; margin-left: 10px;">{performance_labels[kpi]}</span>
                    <span style="color: #888888; margin-left: 10px;">Your number: {result['value']:.3f} | Target: {result['benchmark']:.3f} | Gap: {result['gap']:.3f}</span>
                </div>
            """, unsafe_allow_html=True)
            priority_rank += 1


    st.divider()

    # 30 Day Action Plan
    st.header("Your 30 Day Action Plan")
    st.write("Based on your analysis here is a structured plan to improve your performance over the next 30 days:")

    action_plan = generate_action_plan(analysis, performance_labels, recommendations)

    week_colors = {"week1": "#CC0000", "week2": "#FF6B00", "week3": "#FFD700", "week4": "#00CC00"}
    week_labels = {"week1": "Week 1 — Immediate Action", "week2": "Week 2 — Investigate", "week3": "Week 3 — Implement", "week4": "Week 4 — Measure and Review"}
    week_desc = {"week1": "Fix these now — they are costing you the most", "week2": "Dig deeper to understand the real causes", "week3": "Put the solutions in place", "week4": "Check what improved and plan your next cycle"}

    for week_key, week_name in week_labels.items():
        items = action_plan[week_key]
        if items:
            color = week_colors[week_key]
            st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 12px 16px; margin: 12px 0; background: rgba(255,255,255,0.02); border-radius: 0 8px 8px 0;">
                    <p style="color: {color}; font-weight: 800; font-size: 1rem; margin: 0 0 2px 0;">{week_name}</p>
                    <p style="color: #555555; font-size: 0.8rem; margin: 0 0 10px 0;">{week_desc[week_key]}</p>
            """, unsafe_allow_html=True)
            for item in items:
                priority = item.get("priority", "Standard")
                if priority == "Critical":
                    icon = "🚨"
                elif priority == "Needs Improvement":
                    icon = "⚠️"
                elif priority == "Maintain":
                    icon = "✅"
                else:
                    icon = "→"
                st.markdown(f"""
                    <p style="color: #cccccc; font-size: 0.88rem; margin: 6px 0; padding-left: 8px;">
                        {icon} &nbsp;{item["action"]}
                    </p>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.header("Projected Outcome")
    st.write("Based on your numbers here is a realistic projection if you act on the recommendations:")

    projections_data = {}
    if improvements:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, (kpi, projected) in enumerate(improvements.items()):
            col = cols[i % 3]
            current = kpi_data[kpi]
            projections_data[kpi] = (current, projected)
            with col:
                if kpi in ["order_fulfillment_rate", "on_time_delivery",
                           "warehouse_utilization", "picking_accuracy", "inventory_turnover"]:
                    change = projected - current
                    change_str = f"+{change:.3f}"
                else:
                    change = current - projected
                    change_str = f"-{change:.3f}"

                st.markdown(f"""
                    <div style="background-color: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 15px; margin: 5px 0; text-align: center;">
                        <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{performance_labels[kpi]}</p>
                        <p style="color: #CC0000; font-size: 1.2rem; margin: 5px 0;">Now: {current:.3f}</p>
                        <p style="color: #00CC00; font-size: 1.2rem; margin: 5px 0;">Projected: {projected:.3f}</p>
                        <p style="color: #00CC00; font-size: 1rem; font-weight: 800; margin: 0;">{change_str} improvement</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Your distribution is already performing at benchmark level!")

    st.divider()

    st.header("Play With the Numbers")
    st.write("Change the values below to see what happens to your results")
    col1, col2 = st.columns(2)

    with col1:
        fulfillment_improvement = st.number_input("Improve Order Fulfillment Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        delivery_improvement = st.number_input("Improve On Time Delivery by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        utilization_improvement = st.number_input("Improve Warehouse Utilization by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        accuracy_improvement = st.number_input("Improve Picking Accuracy by (%)", min_value=0.000, max_value=5.000, value=0.000, step=0.001, format="%.3f")
        return_improvement = st.number_input("Reduce Return Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        cost_improvement = st.number_input(f"Reduce Cost per Order by ({currency_symbol})", min_value=0.000, max_value=50.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Your Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Order Fulfillment Rate", f"{order_fulfillment_rate + fulfillment_improvement:.3f}%", f"+{fulfillment_improvement:.3f}%")
        st.metric("On Time Delivery", f"{on_time_delivery + delivery_improvement:.3f}%", f"+{delivery_improvement:.3f}%")

    with col2:
        st.metric("Warehouse Utilization", f"{warehouse_utilization + utilization_improvement:.3f}%", f"+{utilization_improvement:.3f}%")
        st.metric("Picking Accuracy", f"{picking_accuracy + accuracy_improvement:.3f}%", f"+{accuracy_improvement:.3f}%")

    with col3:
        st.metric("Return Rate", f"{return_rate - return_improvement:.3f}%", f"-{return_improvement:.3f}%")
        st.metric("Cost per Order", f"{currency_symbol}{cost_per_order - cost_improvement:.3f}", f"-{currency_symbol}{cost_improvement:.3f}")

    st.divider()

    st.header("PFMEA Module")
    st.write("Identify and assess potential failure risks in your distribution process")
    col1, col2 = st.columns(2)

    with col1:
        process_step = st.text_input("Process Step", placeholder="e.g. Picking, Packing, Loading")
        failure_mode = st.text_input("Potential Failure Mode", placeholder="e.g. Wrong item picked, Damaged packaging")
        failure_effect = st.text_input("Effect of Failure", placeholder="e.g. Customer return, Delivery delay")

    with col2:
        severity = st.slider("Severity (1-10)", 1, 10, 5)
        occurrence = st.slider("Occurrence (1-10)", 1, 10, 5)
        detection = st.slider("Detection (1-10)", 1, 10, 5)

    rpn = severity * occurrence * detection

    st.subheader("Risk Assessment")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Severity", severity)
    with col2:
        st.metric("Occurrence", occurrence)
    with col3:
        st.metric("Detection", detection)
    with col4:
        if rpn >= 200:
            st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #CC0000; border-radius: 10px; padding: 15px; text-align: center;">
                <p style="color: #ffffff; margin: 0;">RPN Score</p>
                <p style="color: #CC0000; font-size: 2rem; font-weight: 800; margin: 0;">{rpn}</p></div>""", unsafe_allow_html=True)
        elif rpn >= 100:
            st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; padding: 15px; text-align: center;">
                <p style="color: #ffffff; margin: 0;">RPN Score</p>
                <p style="color: #FFD700; font-size: 2rem; font-weight: 800; margin: 0;">{rpn}</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 15px; text-align: center;">
                <p style="color: #ffffff; margin: 0;">RPN Score</p>
                <p style="color: #00CC00; font-size: 2rem; font-weight: 800; margin: 0;">{rpn}</p></div>""", unsafe_allow_html=True)

    if rpn >= 200:
        risk_level_text = "HIGH RISK"
        st.error(f"🚨 HIGH RISK — RPN of {rpn} requires immediate corrective action!")
        st.warning("Stop the affected process step and investigate immediately before resuming.")
    elif rpn >= 100:
        risk_level_text = "MEDIUM RISK"
        st.warning(f"⚠️ MEDIUM RISK — RPN of {rpn} requires attention and monitoring.")
        st.info("Develop a corrective action plan and implement within 30 days.")
    else:
        risk_level_text = "LOW RISK"
        st.success(f"✅ LOW RISK — RPN of {rpn} is acceptable.")
        st.info("Maintain current controls and monitor regularly.")

    st.divider()

    st.header("Generate Report")
    st.write("Download a complete PDF report of this analysis to share or keep for your records")

    if st.button("Generate Report", use_container_width=True):
        report_company = company_name if company_name else "Unnamed Company"

        pfmea_data = {
            "process_step": process_step,
            "failure_mode": failure_mode,
            "failure_effect": failure_effect,
            "severity": severity,
            "occurrence": occurrence,
            "detection": detection,
            "rpn": rpn,
            "risk_level": risk_level_text
        }

        pdf_buffer = generate_pdf_report(
            company_name=report_company,
            category="Distribution",
            industry=industry,
            business_model=st.session_state.get("business_model", "N/A"),
            currency_symbol=currency_symbol,
            analysis=analysis,
            performance_labels=performance_labels,
            risk_score=risk_score,
            risk_label=risk_label,
            root_causes=root_causes,
            recommendations=recommendations,
            priority_list=priority_list_names,
            projections=projections_data,
            pfmea_data=pfmea_data
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"SPO_Report_{report_company.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )