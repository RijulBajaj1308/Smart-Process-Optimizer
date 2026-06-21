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

manufacturing_benchmarks = {
    "Automotive": {
        "efficiency_rate": 85.000,
        "cycle_time": 25.000,
        "waste_percentage": 4.000,
        "roi": 15.000,
        "manpower_utilization": 85.000,
        "rejection_rate": 2.000,
        "lead_time": 7.000
    },
    "Electronics": {
        "efficiency_rate": 82.000,
        "cycle_time": 20.000,
        "waste_percentage": 3.000,
        "roi": 18.000,
        "manpower_utilization": 82.000,
        "rejection_rate": 2.000,
        "lead_time": 5.000
    },
    "Food and Beverage": {
        "efficiency_rate": 78.000,
        "cycle_time": 20.000,
        "waste_percentage": 2.000,
        "roi": 12.000,
        "manpower_utilization": 78.000,
        "rejection_rate": 1.000,
        "lead_time": 2.000
    },
    "Textile and Apparel": {
        "efficiency_rate": 72.000,
        "cycle_time": 40.000,
        "waste_percentage": 8.000,
        "roi": 8.000,
        "manpower_utilization": 75.000,
        "rejection_rate": 4.000,
        "lead_time": 14.000
    },
    "General Manufacturing": {
        "efficiency_rate": 75.000,
        "cycle_time": 35.000,
        "waste_percentage": 6.000,
        "roi": 10.000,
        "manpower_utilization": 78.000,
        "rejection_rate": 3.000,
        "lead_time": 10.000
    },
    "Eco Friendly Packaging": {
        "efficiency_rate": 80.000,
        "cycle_time": 30.000,
        "waste_percentage": 3.000,
        "roi": 10.000,
        "manpower_utilization": 80.000,
        "rejection_rate": 2.000,
        "lead_time": 8.000
    },
    "Pulp and Paper Manufacturing": {
        "efficiency_rate": 72.000,
        "cycle_time": 45.000,
        "waste_percentage": 8.000,
        "roi": 8.000,
        "manpower_utilization": 75.000,
        "rejection_rate": 4.000,
        "lead_time": 12.000
    },
    "Pharmaceutical Manufacturing": {
        "efficiency_rate": 90.000,
        "cycle_time": 15.000,
        "waste_percentage": 1.000,
        "roi": 20.000,
        "manpower_utilization": 85.000,
        "rejection_rate": 1.000,
        "lead_time": 3.000
    }
}

performance_labels = {
    "efficiency_rate": "Efficiency Rate (%)",
    "cycle_time": "Cycle Time (mins)",
    "waste_percentage": "Waste Percentage (%)",
    "roi": "ROI (%)",
    "manpower_utilization": "Manpower Utilization (%)",
    "rejection_rate": "Rejection Rate (%)",
    "lead_time": "Lead Time (days)"
}

def analyze_kpis(kpi_data, benchmarks):
    results = {}
    for kpi, value in kpi_data.items():
        benchmark = benchmarks[kpi]
        if kpi in ["efficiency_rate", "roi", "manpower_utilization"]:
            gap = value - benchmark
            if gap >= 0:
                status = "Good"
            elif gap >= -10:
                status = "Needs Improvement"
            else:
                status = "Critical"
        else:
            gap = benchmark - value
            if gap >= 0:
                status = "Good"
            elif gap >= -10:
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
            "metric": performance_labels.get(kpi, kpi),
            "action": f"URGENT — {performance_labels.get(kpi, kpi)} is at {result['value']:.3f} against a benchmark of {result['benchmark']:.3f}. This is your most critical problem and needs immediate attention this week.",
            "priority": "Critical"
        })

    if not critical_kpis and improvement_kpis:
        kpi, result = improvement_kpis[0]
        plan["week1"].append({
            "action": f"Start with {performance_labels.get(kpi, kpi)} — currently {result['value']:.3f} vs benchmark {result['benchmark']:.3f}. This is your biggest gap.",
            "priority": "Needs Improvement"
        })

    plan["week2"].append({"action": "Map your current process from start to finish and identify where time and materials are being lost", "priority": "Standard"})
    for kpi, result in critical_kpis:
        plan["week2"].append({"action": f"Conduct a detailed root cause analysis for {performance_labels.get(kpi, kpi)} — speak to floor workers and supervisors to understand what is actually happening", "priority": "Critical"})
    for kpi, result in improvement_kpis[:2]:
        plan["week2"].append({"action": f"Investigate {performance_labels.get(kpi, kpi)} — identify the top 3 contributing factors and rank them by impact", "priority": "Needs Improvement"})

    for rec in recommendations[:3]:
        plan["week3"].append({"action": rec, "priority": "Implementation"})
    if not recommendations:
        plan["week3"].append({"action": "Implement the process improvements identified during Week 2 investigation", "priority": "Implementation"})

    plan["week4"].append({"action": "Re-enter all your performance numbers in SPO and compare against your Week 1 starting point", "priority": "Review"})
    plan["week4"].append({"action": "Quantify the improvement — calculate how much output, quality or efficiency has improved in numbers", "priority": "Review"})
    plan["week4"].append({"action": "Document what worked and what did not — this becomes your Standard Operating Procedure going forward", "priority": "Review"})
    if good_kpis:
        good_names = ", ".join([performance_labels.get(k, k) for k, r in good_kpis])
        plan["week4"].append({"action": f"Maintain your strong performance in: {good_names} — do not let these slip while fixing other areas", "priority": "Maintain"})

    return plan

def generate_dynamic_insights(kpi, value, benchmark, gap, status):
    if kpi == "efficiency_rate":
        if status == "Critical":
            cause = f"Your efficiency is {gap:.1f}% below the industry benchmark of {benchmark:.1f}%. You are losing more than 1 in every {round(100/gap):.0f} hours of productive time. This is a serious problem that is directly costing you output and revenue every single day."
            rec = f"This needs urgent attention. Start with a full line balancing study this week — identify which stations are causing the most downtime and fix them first. Every 1% improvement in efficiency at your scale translates to significant output gains."
        else:
            cause = f"Your efficiency is {gap:.1f}% below the industry benchmark of {benchmark:.1f}%. You are close but not there yet. Small inefficiencies are adding up across your production process."
            rec = f"You are {gap:.1f}% away from benchmark. Focus on reducing the top 2 or 3 causes of downtime and review your line balancing to squeeze out the remaining gap."

    elif kpi == "manpower_utilization":
        if status == "Critical":
            cause = f"Your manpower utilization is {gap:.1f}% below benchmark. This means a significant portion of your workforce is not being used productively. You are paying for labor that is sitting idle."
            rec = f"Conduct an immediate manpower efficiency study. Identify which stations have idle workers and redistribute them to where they are needed. The goal is to ensure every worker is contributing value during their shift."
        else:
            cause = f"Your manpower utilization is {gap:.1f}% below the {benchmark:.1f}% benchmark. Some of your workers have idle time that could be put to better use."
            rec = f"Review your task allocation across stations. Small adjustments in how work is distributed could close this {gap:.1f}% gap and improve your overall productivity without adding any cost."

    elif kpi == "roi":
        if status == "Critical":
            cause = f"Your ROI of {value:.1f}% is {gap:.1f}% below the industry benchmark of {benchmark:.1f}%. For every unit of investment you are generating significantly less return than your competitors. This will affect your ability to reinvest and grow."
            rec = f"Focus on the highest cost drivers in your operation first. Reducing waste, rejection and downtime typically delivers the fastest ROI improvement. Start by quantifying your top 3 cost centers."
        else:
            cause = f"Your ROI is {gap:.1f}% below benchmark. You are generating returns but leaving money on the table compared to industry leaders."
            rec = f"Closing this {gap:.1f}% ROI gap requires targeting your biggest cost inefficiencies. Review your waste costs, rejection costs and downtime costs to find where the biggest savings opportunity lies."

    elif kpi == "cycle_time":
        if status == "Critical":
            cause = f"Your cycle time of {value:.1f} mins is {gap:.1f} mins above the benchmark of {benchmark:.1f} mins. Your production is running significantly slower than industry standard. This means fewer units produced per shift and higher cost per unit."
            rec = f"Your cycle time gap of {gap:.1f} mins is too large to ignore. Start with time studies at every station this week to find your bottleneck. The bottleneck station is costing you the most — fix that first and your whole line speeds up."
        else:
            cause = f"Your cycle time is {gap:.1f} mins above benchmark. Your line is slightly slower than it should be. This is manageable but needs attention before it gets worse."
            rec = f"A {gap:.1f} min cycle time gap is within reach to close. Review your slowest stations and look for quick wins — small layout changes or task redistributions that can shave time off the bottleneck."

    elif kpi == "waste_percentage":
        if status == "Critical":
            cause = f"Your waste is {gap:.1f}% above the benchmark of {benchmark:.1f}%. You are throwing away {gap:.1f}% more of your inputs than industry leaders. This is a direct hit on your margins and your sustainability credentials."
            rec = f"At {value:.1f}% waste you have a serious problem. Implement an immediate waste tracking system to categorize where the waste is coming from. Once you know the top 3 waste sources you can target them specifically."
        else:
            cause = f"Your waste is {gap:.1f}% above benchmark. You are generating more waste than you should be. At your scale this adds up to a significant cost."
            rec = f"A {gap:.1f}% waste reduction is achievable with focused effort. Map your production process and identify the top 2 points where waste is generated and attack those first."

    elif kpi == "rejection_rate":
        if status == "Critical":
            cause = f"Your rejection rate of {value:.1f}% is {gap:.1f}% above the benchmark of {benchmark:.1f}%. You are rejecting {gap:.1f}% more product than industry leaders. This means wasted materials, wasted labor and potentially unhappy customers."
            rec = f"A rejection rate of {value:.1f}% is a quality emergency. Start by categorizing your rejections — what are the top 3 defect types? Once you know that you can trace them to their root cause and eliminate them systematically."
        else:
            cause = f"Your rejection rate is {gap:.1f}% above benchmark. You are rejecting more product than you should be. Each rejection is wasted material, wasted labor and wasted time."
            rec = f"Closing this {gap:.1f}% rejection gap requires understanding where defects originate. Implement quality checkpoints at the 2 or 3 most critical stages of your process to catch defects early before they become rejections."

    elif kpi == "lead_time":
        if status == "Critical":
            cause = f"Your lead time of {value:.1f} days is {gap:.1f} days above the benchmark of {benchmark:.1f} days. Your customers are waiting significantly longer than they should be. This puts you at a competitive disadvantage and risks losing orders."
            rec = f"A lead time of {value:.1f} days when the benchmark is {benchmark:.1f} days is a serious competitive risk. Map your entire process from order receipt to delivery and identify where the longest delays occur. Those are your priority targets."
        else:
            cause = f"Your lead time is {gap:.1f} days above benchmark. You are slower than your competitors in getting products to customers. In a competitive market this gap matters."
            rec = f"Closing a {gap:.1f} day lead time gap is achievable. Look at your scheduling and order processing first — often lead time improvements come from better planning rather than faster production."

    else:
        cause = f"This metric is {gap:.1f} units away from the industry benchmark of {benchmark:.1f}. This gap is affecting your overall operational performance."
        rec = f"Focus on understanding why this metric is {gap:.1f} units below benchmark and develop a specific action plan to close the gap within the next 30 days."

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
    labels = [performance_labels.get(k, k).replace(' (%)', '').replace(' (mins)', '').replace(' (days)', '') for k in kpis]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f9f9f9')
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], your_vals, width=0.35, color=bar_colors, alpha=0.9)
    ax.bar([i + 0.2 for i in x], bench_vals, width=0.35, color='#444444', alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=7.5, rotation=15, ha='right')
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
    labels = [performance_labels.get(k, k).replace(' (%)', '').replace(' (mins)', '').replace(' (days)', '') for k in kpis]
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
                          root_causes, recommendations, priority_list, projections, pfmea_data=None, action_plan_data=None, include_charts=True):
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
        ["Company / Plant", company_name],
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

    if pfmea_data:
        elements.append(Paragraph("Process Failure Mode and Effects Analysis (PFMEA)", heading_style))
        pfmea_rows = [
            ["Process Step", pfmea_data.get('process_step') or "Not specified"],
            ["Failure Mode", pfmea_data.get('failure_mode') or "Not specified"],
            ["Effect of Failure", pfmea_data.get('failure_effect') or "Not specified"],
            ["Severity", str(pfmea_data.get('severity', 'N/A'))],
            ["Occurrence", str(pfmea_data.get('occurrence', 'N/A'))],
            ["Detection", str(pfmea_data.get('detection', 'N/A'))],
            ["RPN Score", str(pfmea_data.get('rpn', 'N/A'))],
            ["Risk Level", pfmea_data.get('risk_level', 'N/A')],
        ]
        pfmea_table = Table(pfmea_rows, colWidths=[1.7*inch, 4.3*inch])
        pfmea_table.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 9.5),
            ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#CC0000')),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(pfmea_table)


    if action_plan_data:
        elements.append(Paragraph("30 Day Action Plan", heading_style))
        week_names = {
            "week1": "Week 1 — Immediate Action",
            "week2": "Week 2 — Investigate",
            "week3": "Week 3 — Implement",
            "week4": "Week 4 — Measure and Review"
        }
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


def show_manufacturing(industry, currency_symbol="$"):
    benchmarks = manufacturing_benchmarks[industry]

    st.sidebar.title("Enter Your Performance Numbers")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} Industry (India)")

    efficiency_rate = st.sidebar.number_input("Efficiency Rate (%)", min_value=0.000, max_value=100.000, value=65.000, step=0.001, format="%.3f")
    cycle_time = st.sidebar.number_input("Cycle Time (mins)", min_value=0.000, max_value=120.000, value=45.000, step=0.001, format="%.3f")
    waste_percentage = st.sidebar.number_input("Waste Percentage (%)", min_value=0.000, max_value=50.000, value=12.000, step=0.001, format="%.3f")
    roi = st.sidebar.number_input("ROI (%)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
    manpower_utilization = st.sidebar.number_input("Manpower Utilization (%)", min_value=0.000, max_value=100.000, value=70.000, step=0.001, format="%.3f")
    rejection_rate = st.sidebar.number_input("Rejection Rate (%)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
    lead_time = st.sidebar.number_input("Lead Time (days)", min_value=0.000, max_value=30.000, value=10.000, step=0.001, format="%.3f")

    kpi_data = {
        "efficiency_rate": efficiency_rate,
        "cycle_time": cycle_time,
        "waste_percentage": waste_percentage,
        "roi": roi,
        "manpower_utilization": manpower_utilization,
        "rejection_rate": rejection_rate,
        "lead_time": lead_time
    }

    analysis = analyze_kpis(kpi_data, benchmarks)

    # Company name field
    company_name = st.text_input("Company / Plant Name", placeholder="e.g. Ahuja Radios")
    st.divider()

    # Performance Cards
    st.header("Performance Analysis")
    st.caption(f"Benchmarks based on {industry} industry standards in India")
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

    # Risk Assessment
    st.header("Overall Plant Risk Assessment")

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

    # Dynamic Root Causes and Recommendations
    st.header("What is Wrong and How to Fix It")
    st.caption(f"Analysis based on your actual numbers compared to {industry} industry benchmark")

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

            if kpi in ["efficiency_rate", "roi", "manpower_utilization"]:
                improvements[kpi] = min(result["benchmark"], result["value"] + result["gap"] * 0.5)
            else:
                improvements[kpi] = max(result["benchmark"], result["value"] - result["gap"] * 0.5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What is happening in your plant?")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("Your plant is performing at or above benchmark level. Keep it up!")

    with col2:
        st.subheader("What should you do about it?")
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("No action required. Focus on maintaining your current performance.")

    st.divider()

    # Action Priority Score
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

    week_colors = {
        "week1": "#CC0000",
        "week2": "#FF6B00",
        "week3": "#FFD700",
        "week4": "#00CC00"
    }
    week_labels = {
        "week1": "Week 1 — Immediate Action",
        "week2": "Week 2 — Investigate",
        "week3": "Week 3 — Implement",
        "week4": "Week 4 — Measure and Review"
    }
    week_desc = {
        "week1": "Fix these now — they are costing you the most",
        "week2": "Dig deeper to understand the real causes",
        "week3": "Put the solutions in place",
        "week4": "Check what improved and plan your next cycle"
    }

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
                action_text = item["action"]
                st.markdown(f"""
                    <p style="color: #cccccc; font-size: 0.88rem; margin: 6px 0; padding-left: 8px;">
                        {icon} &nbsp;{action_text}
                    </p>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Projected Outcome
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
                if kpi in ["efficiency_rate", "roi", "manpower_utilization"]:
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
        st.success("Your plant is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("Play With the Numbers")
    st.write("Change the values below to see what happens to your results")
    col1, col2 = st.columns(2)

    with col1:
        efficiency_improvement = st.number_input("Improve Efficiency Rate by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        manpower_improvement = st.number_input("Improve Manpower Utilization by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        rejection_improvement = st.number_input("Reduce Rejection Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        waste_improvement = st.number_input("Reduce Waste by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")
        cycle_improvement = st.number_input("Reduce Cycle Time by (mins)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        lead_improvement = st.number_input("Reduce Lead Time by (days)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Your Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Rate", f"{efficiency_rate + efficiency_improvement:.3f}%", f"+{efficiency_improvement:.3f}%")
        st.metric("Manpower Utilization", f"{manpower_utilization + manpower_improvement:.3f}%", f"+{manpower_improvement:.3f}%")

    with col2:
        st.metric("Rejection Rate", f"{rejection_rate - rejection_improvement:.3f}%", f"-{rejection_improvement:.3f}%")
        st.metric("Waste Percentage", f"{waste_percentage - waste_improvement:.3f}%", f"-{waste_improvement:.3f}%")

    with col3:
        st.metric("Cycle Time", f"{cycle_time - cycle_improvement:.3f} mins", f"-{cycle_improvement:.3f} mins")
        st.metric("Lead Time", f"{lead_time - lead_improvement:.3f} days", f"-{lead_improvement:.3f} days")

    st.divider()

    # Gauge Charts
    st.header("Performance Charts")
    st.subheader("Performance Gauges")

    def create_gauge(title, value, benchmark, max_val):
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            delta={"reference": benchmark},
            title={"text": title},
            gauge={
                "axis": {"range": [0, max_val]},
                "bar": {"color": "darkred"},
                "steps": [
                    {"range": [0, benchmark * 0.7], "color": "red"},
                    {"range": [benchmark * 0.7, benchmark], "color": "orange"},
                    {"range": [benchmark, max_val], "color": "green"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": benchmark
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(t=50, b=0, l=0, r=0))
        return fig

    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(create_gauge("Efficiency Rate", efficiency_rate, benchmarks["efficiency_rate"], 100), use_container_width=True)
        st.plotly_chart(create_gauge("ROI", roi, benchmarks["roi"], 50), use_container_width=True)

    with col2:
        st.plotly_chart(create_gauge("Manpower Utilization", manpower_utilization, benchmarks["manpower_utilization"], 100), use_container_width=True)
        st.plotly_chart(create_gauge("Waste %", waste_percentage, benchmarks["waste_percentage"], 50), use_container_width=True)

    with col3:
        st.plotly_chart(create_gauge("Rejection Rate", rejection_rate, benchmarks["rejection_rate"], 50), use_container_width=True)
        st.plotly_chart(create_gauge("Lead Time", lead_time, benchmarks["lead_time"], 30), use_container_width=True)

    st.divider()

    # PFMEA Module
    st.header("PFMEA Module")
    st.write("Identify and assess potential failure risks in your production process")
    col1, col2 = st.columns(2)

    with col1:
        process_step = st.text_input("Process Step", placeholder="e.g. Assembly, Welding, Painting")
        failure_mode = st.text_input("Potential Failure Mode", placeholder="e.g. Incorrect assembly, Weld crack")
        failure_effect = st.text_input("Effect of Failure", placeholder="e.g. Product defect, Safety hazard")

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
        st.warning("Stop production at this process step and investigate immediately before resuming.")
    elif rpn >= 100:
        risk_level_text = "MEDIUM RISK"
        st.warning(f"⚠️ MEDIUM RISK — RPN of {rpn} requires attention and monitoring.")
        st.info("Develop a corrective action plan and implement within 30 days.")
    else:
        risk_level_text = "LOW RISK"
        st.success(f"✅ LOW RISK — RPN of {rpn} is acceptable.")
        st.info("Maintain current controls and monitor regularly.")

    st.divider()

    # Generate Report
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
            category="Manufacturing",
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
            pfmea_data=pfmea_data,
            action_plan_data=action_plan,
            include_charts=True
        )

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"SPO_Report_{report_company.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )