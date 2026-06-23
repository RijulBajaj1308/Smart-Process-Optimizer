# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
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
try:
    from auth import save_analysis
except ImportError:
    def save_analysis(*args, **kwargs): return None


def make_flow_map_chart(steps, takt_time=None, map_type="manufacturing"):
    """Draw a horizontal process flow map using matplotlib"""
    n = len(steps)
    fig, (ax_map, ax_bar) = plt.subplots(2, 1, figsize=(max(10, n * 1.8), 7),
                                          gridspec_kw={'height_ratios': [2, 1]})
    fig.patch.set_facecolor('#1A1D27')

    # ── TOP: Flow Map ──
    ax_map.set_facecolor('#1A1D27')
    ax_map.set_xlim(-0.5, n * 2)
    ax_map.set_ylim(-1, 3)
    ax_map.axis('off')

    for i, step in enumerate(steps):
        x = i * 2
        ct = step.get('cycle_time', 0)
        wait = step.get('wait_time', 0)
        workers = step.get('workers', 1)
        va = step.get('value_adding', True)

        # Color based on status
        if takt_time and ct > takt_time:
            box_color = '#CC0000'  # bottleneck
            text_color = 'white'
        elif not va:
            box_color = '#FF6B00'  # non value adding
            text_color = 'white'
        else:
            box_color = '#1a6b3c'  # good
            text_color = 'white'

        # Draw box
        rect = plt.Rectangle((x - 0.7, 0.3), 1.4, 1.4,
                              linewidth=2, edgecolor='#2D3139',
                              facecolor=box_color, zorder=3)
        ax_map.add_patch(rect)

        # Step name
        name = step['name'][:12] + '..' if len(step['name']) > 12 else step['name']
        ax_map.text(x, 1.2, name, ha='center', va='center',
                   fontsize=7.5, color=text_color, fontweight='bold', zorder=4)

        # CT and workers below name
        ax_map.text(x, 0.7, f"CT: {ct:.0f}m | W: {workers}",
                   ha='center', va='center', fontsize=6.5, color='#E8EAF0', zorder=4)

        # Wait time above box
        if wait > 0:
            ax_map.text(x, 2.0, f"Wait: {wait:.0f}m",
                       ha='center', va='center', fontsize=6.5,
                       color='#FF6B00', style='italic')

        # Arrow to next step
        if i < n - 1:
            ax_map.annotate('', xy=(x + 0.7 + 0.2, 1.0),
                           xytext=(x + 0.7, 1.0),
                           arrowprops=dict(arrowstyle='->', color='#E8EAF0', lw=1.5),
                           zorder=5)
            ax_map.plot([x + 0.7, x + 1.3], [1.0, 1.0], color='#2D3139', lw=2, zorder=2)

    # Takt time line
    if takt_time:
        ax_map.text(n * 2 - 0.5, 2.6, f'Takt Time: {takt_time:.0f} mins',
                   ha='right', fontsize=8, color='#FFD700', fontweight='bold')

    # Legend
    legend_items = [
        mpatches.Patch(color='#CC0000', label='Bottleneck'),
        mpatches.Patch(color='#FF6B00', label='Non-Value Adding'),
        mpatches.Patch(color='#1a6b3c', label='Value Adding'),
    ]
    ax_map.legend(handles=legend_items, loc='lower right', fontsize=7,
                 facecolor='#1A1D27', edgecolor='#2D3139', labelcolor='#E8EAF0')
    ax_map.set_title('Process Flow Map', color='#E8EAF0', fontsize=11, fontweight='bold', pad=8)

    # ── BOTTOM: Cycle Time Bar Chart ──
    ax_bar.set_facecolor('#1A1D27')
    names = [s['name'][:10] for s in steps]
    cts = [s.get('cycle_time', 0) for s in steps]
    bar_colors = []
    for s in steps:
        ct = s.get('cycle_time', 0)
        if takt_time and ct > takt_time:
            bar_colors.append('#CC0000')
        elif not s.get('value_adding', True):
            bar_colors.append('#FF6B00')
        else:
            bar_colors.append('#1a6b3c')

    bars = ax_bar.bar(names, cts, color=bar_colors, alpha=0.9, edgecolor='#2D3139')
    for bar, val in zip(bars, cts):
        ax_bar.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                   f'{val:.0f}m', ha='center', va='bottom', fontsize=7, color='#E8EAF0')

    if takt_time:
        ax_bar.axhline(y=takt_time, color='#FFD700', linestyle='--', linewidth=1.5,
                      label=f'Takt: {takt_time:.0f}m')
        ax_bar.legend(fontsize=7, facecolor='#1A1D27', edgecolor='#2D3139', labelcolor='#E8EAF0')

    ax_bar.set_ylabel('Cycle Time (mins)', color='#8B90A0', fontsize=8)
    ax_bar.tick_params(colors='#8B90A0', labelsize=7)
    ax_bar.spines['bottom'].set_color('#2D3139')
    ax_bar.spines['left'].set_color('#2D3139')
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.set_facecolor('#1A1D27')
    plt.setp(ax_bar.xaxis.get_majorticklabels(), rotation=15, ha='right')

    plt.tight_layout(pad=1.5)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#1A1D27')
    buf.seek(0)
    plt.close()
    return buf


def generate_flow_recommendations(steps, takt_time, total_available_mins, map_type):
    """Generate specific recommendations based on the process flow map"""
    recommendations = []
    bottlenecks = []
    non_va_steps = []
    total_ct = sum(s.get('cycle_time', 0) for s in steps)
    total_wait = sum(s.get('wait_time', 0) for s in steps)
    va_time = sum(s.get('cycle_time', 0) for s in steps if s.get('value_adding', True))
    nva_time = total_ct - va_time + total_wait
    process_efficiency = (va_time / (total_ct + total_wait) * 100) if (total_ct + total_wait) > 0 else 0

    for s in steps:
        ct = s.get('cycle_time', 0)
        if takt_time and ct > takt_time:
            bottlenecks.append(s)
        if not s.get('value_adding', True):
            non_va_steps.append(s)

    if bottlenecks:
        for bn in bottlenecks:
            excess = bn['cycle_time'] - takt_time
            workers = bn.get('workers', 1)
            recommendations.append({
                "priority": "Critical",
                "step": bn['name'],
                "issue": f"{bn['name']} has a cycle time of {bn['cycle_time']:.0f} mins — {excess:.0f} mins above your takt time of {takt_time:.0f} mins. This is your bottleneck and it is limiting your entire process.",
                "action": f"Add {max(1, round(bn['cycle_time']/takt_time) - workers)} worker(s) to {bn['name']} or redistribute {excess:.0f} mins of tasks to adjacent stations. Check which tasks at {bn['name']} can be moved upstream or downstream."
            })

    if non_va_steps:
        for nva in non_va_steps:
            recommendations.append({
                "priority": "Needs Improvement",
                "step": nva['name'],
                "issue": f"{nva['name']} is marked as non-value adding with a cycle time of {nva['cycle_time']:.0f} mins. This is pure waste — your customer is not paying for this step.",
                "action": f"Investigate whether {nva['name']} can be eliminated entirely. If it cannot be eliminated, find ways to reduce its time or combine it with an adjacent value-adding step."
            })

    if total_wait > 30:
        worst_wait = max(steps, key=lambda x: x.get('wait_time', 0))
        recommendations.append({
            "priority": "Needs Improvement",
            "step": "Wait Times",
            "issue": f"Total waiting time across your process is {total_wait:.0f} mins. The longest wait is before {worst_wait['name']} at {worst_wait.get('wait_time', 0):.0f} mins. Waiting is pure waste.",
            "action": f"Investigate why {worst_wait['name']} has {worst_wait.get('wait_time', 0):.0f} mins of waiting before it starts. Is it waiting for materials, equipment or a previous step to finish? Eliminate the root cause of this wait."
        })

    if process_efficiency < 60:
        recommendations.append({
            "priority": "Critical",
            "step": "Overall Process",
            "issue": f"Only {process_efficiency:.0f}% of your total process time is value adding. That means {100-process_efficiency:.0f}% is waste. For every hour your process runs, {60*(100-process_efficiency)/100:.0f} mins are not creating value for the customer.",
            "action": "Conduct a full Value Stream Mapping exercise with your team. Walk the process and time every step. Challenge every non-value adding step — can it be eliminated, combined or reduced?"
        })

    if not recommendations:
        recommendations.append({
            "priority": "Good",
            "step": "Overall Process",
            "issue": f"Your process is well balanced with {process_efficiency:.0f}% efficiency and no bottlenecks above takt time.",
            "action": "Focus on incremental improvements. Look for small cycle time reductions at each station and eliminate any remaining wait times."
        })

    return recommendations, process_efficiency, va_time, nva_time, total_wait


def generate_flow_pdf(company_name, industry, map_type, steps, takt_time,
                      recommendations, process_efficiency, va_time, nva_time, total_wait, chart_buf):
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
    elements.append(Paragraph(f"Process Flow Map Analysis — {map_type}", sub_style))

    meta = [
        ["Company", company_name],
        ["Industry", industry],
        ["Map Type", map_type],
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

    # Summary metrics
    elements.append(Paragraph("Process Summary", heading_style))
    summary_data = [
        ["Metric", "Value"],
        ["Total Steps", str(len(steps))],
        ["Process Efficiency", f"{process_efficiency:.1f}%"],
        ["Value Adding Time", f"{va_time:.0f} mins"],
        ["Non-Value Adding Time", f"{nva_time:.0f} mins"],
        ["Total Wait Time", f"{total_wait:.0f} mins"],
        ["Takt Time", f"{takt_time:.0f} mins" if takt_time else "Not set"],
    ]
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(summary_table)

    # Flow map chart
    if chart_buf:
        elements.append(Paragraph("Process Flow Map", heading_style))
        elements.append(RLImage(chart_buf, width=6.5*inch, height=3.5*inch))
        elements.append(Spacer(1, 8))

    # Step details
    elements.append(Paragraph("Process Step Details", heading_style))
    step_data = [["Step", "Cycle Time", "Wait Time", "Workers", "Type"]]
    for s in steps:
        step_data.append([
            s['name'],
            f"{s.get('cycle_time', 0):.0f} mins",
            f"{s.get('wait_time', 0):.0f} mins",
            str(s.get('workers', 1)),
            "Value Adding" if s.get('value_adding', True) else "Non-Value Adding"
        ])
    step_table = Table(step_data, colWidths=[1.5*inch, 1.1*inch, 1.1*inch, 0.8*inch, 1.5*inch])
    step_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(step_table)

    # Recommendations
    elements.append(Paragraph("Specific Recommendations", heading_style))
    for i, rec in enumerate(recommendations, 1):
        priority_color = '#CC0000' if rec['priority'] == 'Critical' else '#B8860B' if rec['priority'] == 'Needs Improvement' else '#008000'
        elements.append(Paragraph(f"<b>{i}. {rec['step']} — {rec['priority']}</b>",
            ParagraphStyle('RH', parent=styles['Normal'], fontSize=10,
                          textColor=colors.HexColor(priority_color), spaceAfter=4, spaceBefore=10)))
        elements.append(Paragraph(f"<b>What is happening:</b> {rec['issue']}", body_style))
        elements.append(Paragraph(f"<b>What to do:</b> {rec['action']}", body_style))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Generated by Smart Process Optimizer (SPO) - smart-process-optimizer.streamlit.app", footer_style))
    doc.build(elements)
    buffer.seek(0)
    return buffer


def show_manufacturing_flow_map(industry, currency_symbol="$"):
    st.markdown("""
    <div style="background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.15);border-radius:10px;padding:16px 20px;margin-bottom:24px;">
        <p style="color:#E8001D;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin:0 0 4px 0;">Process Flow Map</p>
        <p style="color:#cccccc;font-size:0.9rem;margin:0;">Map your production process step by step. SPO will identify bottlenecks, waste and give you specific recommendations for each station.</p>
    </div>
    """, unsafe_allow_html=True)

    company_name = st.text_input("Company / Plant Name", placeholder="e.g. Ahuja Radios", key="flow_company")

    col1, col2 = st.columns(2)
    with col1:
        takt_time = st.number_input("Takt Time (mins) — How often does customer need one unit?",
                                     min_value=0.0, max_value=480.0, value=30.0, step=0.5, format="%.1f")
        shifts_per_day = st.number_input("Shifts per Day", min_value=1, max_value=3, value=2, step=1)
    with col2:
        hours_per_shift = st.number_input("Hours per Shift", min_value=1.0, max_value=12.0, value=8.0, step=0.5)
        num_steps = st.number_input("Number of Process Steps", min_value=2, max_value=15, value=5, step=1)

    total_available_mins = shifts_per_day * hours_per_shift * 60

    st.divider()
    st.subheader("Enter Your Process Steps")
    st.caption("Enter each step from start to finish — left to right as they happen on your floor")

    steps = []
    for i in range(int(num_steps)):
        with st.expander(f"Step {i+1}", expanded=(i < 3)):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                name = st.text_input("Step Name", value=f"Step {i+1}",
                                    key=f"mfg_fname_{i}",
                                    placeholder="e.g. Welding")
            with col2:
                ct = st.number_input("Cycle Time (mins)", min_value=0.0,
                                    max_value=480.0, value=float(20 + i*5),
                                    step=0.5, format="%.1f", key=f"mfg_fct_{i}")
            with col3:
                wait = st.number_input("Wait Before (mins)", min_value=0.0,
                                      max_value=480.0, value=0.0,
                                      step=0.5, format="%.1f", key=f"mfg_fwait_{i}")
            with col4:
                workers = st.number_input("Workers", min_value=1, max_value=20,
                                         value=1, step=1, key=f"mfg_fworkers_{i}")
            with col5:
                va = st.checkbox("Value Adding?", value=True, key=f"mfg_fva_{i}")

            defect_rate = st.number_input("Defect Rate at this step (%)",
                                         min_value=0.0, max_value=100.0,
                                         value=0.0, step=0.1, format="%.1f",
                                         key=f"mfg_fdefect_{i}")
            steps.append({
                "name": name,
                "cycle_time": ct,
                "wait_time": wait,
                "workers": workers,
                "value_adding": va,
                "defect_rate": defect_rate
            })

    if steps:
        st.divider()
        st.header("Process Flow Map Results")

        # Generate chart
        chart_buf = make_flow_map_chart(steps, takt_time, "manufacturing")
        st.image(chart_buf, use_column_width=True)

        st.write("")

        # Summary metrics
        total_ct = sum(s['cycle_time'] for s in steps)
        total_wait = sum(s['wait_time'] for s in steps)
        va_time = sum(s['cycle_time'] for s in steps if s['value_adding'])
        nva_time = total_ct - va_time
        process_efficiency = (va_time / (total_ct + total_wait) * 100) if (total_ct + total_wait) > 0 else 0
        bottleneck = max(steps, key=lambda x: x['cycle_time'])
        daily_output = total_available_mins / bottleneck['cycle_time'] if bottleneck['cycle_time'] > 0 else 0
        target_output = total_available_mins / takt_time if takt_time > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            eff_color = "#00CC00" if process_efficiency >= 80 else "#FFD700" if process_efficiency >= 60 else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {eff_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Process Efficiency</p>
                <p style="color:{eff_color};font-size:2rem;font-weight:900;margin:8px 0;">{process_efficiency:.1f}%</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid #CC0000;border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Bottleneck</p>
                <p style="color:#CC0000;font-size:1.1rem;font-weight:900;margin:8px 0;">{bottleneck['name']}</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">{bottleneck['cycle_time']:.0f} mins</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid #FFD700;border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Daily Output</p>
                <p style="color:#FFD700;font-size:2rem;font-weight:900;margin:8px 0;">{daily_output:.0f}</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">Target: {target_output:.0f} units</p>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid #E8EAF0;border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Total Waste Time</p>
                <p style="color:#E8EAF0;font-size:2rem;font-weight:900;margin:8px 0;">{nva_time + total_wait:.0f}m</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">NVA + Wait</p>
            </div>""", unsafe_allow_html=True)

        st.divider()

        # Recommendations
        recommendations, _, _, _, _ = generate_flow_recommendations(
            steps, takt_time, total_available_mins, "manufacturing"
        )

        st.header("What SPO Found in Your Process")
        for i, rec in enumerate(recommendations, 1):
            if rec['priority'] == 'Critical':
                color = "#CC0000"
                icon = "🚨"
            elif rec['priority'] == 'Needs Improvement':
                color = "#FFD700"
                icon = "⚠️"
            else:
                color = "#00CC00"
                icon = "✅"

            st.markdown(f"""
            <div style="background:#1A1D27;border:1px solid {color};border-radius:10px;padding:20px;margin-bottom:12px;">
                <p style="color:{color};font-size:0.7rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px 0;">{icon} {rec['priority']} — {rec['step']}</p>
                <p style="color:#E8EAF0;font-size:0.9rem;font-weight:600;margin:0 0 8px 0;">What is happening</p>
                <p style="color:#8B90A0;font-size:0.85rem;margin:0 0 12px 0;">{rec['issue']}</p>
                <p style="color:#E8EAF0;font-size:0.9rem;font-weight:600;margin:0 0 8px 0;">What to do</p>
                <p style="color:#8B90A0;font-size:0.85rem;margin:0;">{rec['action']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Step detail table
        st.divider()
        st.header("Step by Step Breakdown")
        for step in steps:
            ct = step['cycle_time']
            is_bn = ct == bottleneck['cycle_time']
            color = "#CC0000" if is_bn else "#FFD700" if not step['value_adding'] else "#00CC00"
            label = "BOTTLENECK" if is_bn else "NON-VALUE ADDING" if not step['value_adding'] else "OK"
            st.markdown(f"""
            <div style="background:#1A1D27;border-left:4px solid {color};padding:10px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                <span style="color:{color};font-weight:800;font-size:0.8rem;">{label}</span>
                <span style="color:#E8EAF0;margin-left:10px;font-weight:600;">{step['name']}</span>
                <span style="color:#8B90A0;margin-left:10px;font-size:0.82rem;">CT: {ct:.0f}m | Wait: {step['wait_time']:.0f}m | Workers: {step['workers']} | Defect: {step['defect_rate']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Generate Report
        st.header("Generate Report")
        if st.button("Generate Process Flow Map Report", use_container_width=True, key="flow_report_mfg"):
            report_company = company_name or "Unnamed Company"
            recommendations, process_efficiency, va_time, nva_time, total_wait = generate_flow_recommendations(
                steps, takt_time, total_available_mins, "manufacturing"
            )
            chart_buf2 = make_flow_map_chart(steps, takt_time, "manufacturing")
            pdf = generate_flow_pdf(
                report_company, industry, "Manufacturing Process Flow",
                steps, takt_time, recommendations, process_efficiency,
                va_time, nva_time, total_wait, chart_buf2
            )
            st.download_button("Download PDF Report", pdf,
                file_name=f"SPO_FlowMap_{report_company.replace(' ','_')}.pdf",
                mime="application/pdf", use_container_width=True)

        st.write("")
        if st.button("Save Flow Map to Dashboard", use_container_width=True, key="flow_save_mfg"):
            if st.session_state.get("current_company"):
                try:
                    recommendations, process_efficiency, va_time, nva_time, total_wait = generate_flow_recommendations(
                        steps, takt_time, total_available_mins, "manufacturing"
                    )
                    result = save_analysis(
                        company_id=st.session_state.current_company["id"],
                        analysis_type="Deep",
                        kpi_data={"takt_time": takt_time, "num_steps": len(steps), "total_ct": total_ct, "total_wait": total_wait, "process_efficiency": process_efficiency},
                        results={"tool": "Process Flow Map", "bottleneck": bottleneck['name'], "bottleneck_ct": bottleneck['cycle_time'], "daily_output": daily_output, "target_output": target_output, "process_efficiency": process_efficiency},
                        risk_score=int(max(0, min(100, process_efficiency))),
                        risk_label="LOW RISK" if process_efficiency >= 80 else "MEDIUM RISK" if process_efficiency >= 60 else "HIGH RISK",
                        tool_name="Process Flow Map"
                    )
                    st.success("Saved to dashboard!" if result else "Save failed.")
                except Exception as e:
                    st.error(f"Save failed: {e}")
            else:
                st.warning("Login required to save.")


def show_distribution_flow_map(industry, currency_symbol="$"):
    st.markdown("""
    <div style="background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.15);border-radius:10px;padding:16px 20px;margin-bottom:24px;">
        <p style="color:#E8001D;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin:0 0 4px 0;">Order Flow Map</p>
        <p style="color:#cccccc;font-size:0.9rem;margin:0;">Map your order fulfillment process from receipt to delivery. SPO identifies where orders are getting delayed and what to fix.</p>
    </div>
    """, unsafe_allow_html=True)

    company_name = st.text_input("Company / Facility Name", placeholder="e.g. Delhivery Hub", key="dist_flow_company")

    col1, col2 = st.columns(2)
    with col1:
        target_fulfillment_time = st.number_input("Target Order Fulfillment Time (mins)",
                                                   min_value=1.0, max_value=1440.0, value=120.0, step=5.0)
        daily_orders = st.number_input("Daily Order Volume", min_value=1, max_value=100000, value=500, step=10)
    with col2:
        shift_hours = st.number_input("Operating Hours per Day", min_value=1.0, max_value=24.0, value=10.0, step=0.5)
        num_steps = st.number_input("Number of Process Steps", min_value=2, max_value=12, value=6, step=1)

    default_steps = ["Order Receipt", "Pick", "Pack", "QC Check", "Label & Sort", "Dispatch"]
    st.divider()
    st.subheader("Enter Your Order Flow Steps")

    steps = []
    for i in range(int(num_steps)):
        with st.expander(f"Step {i+1}", expanded=(i < 3)):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                default_name = default_steps[i] if i < len(default_steps) else f"Step {i+1}"
                name = st.text_input("Step Name", value=default_name, key=f"dist_fname_{i}")
            with col2:
                ct = st.number_input("Time per Order (mins)", min_value=0.0, max_value=120.0,
                                    value=float(5 + i*3), step=0.5, format="%.1f", key=f"dist_fct_{i}")
            with col3:
                wait = st.number_input("Wait Time (mins)", min_value=0.0, max_value=120.0,
                                      value=0.0, step=0.5, format="%.1f", key=f"dist_fwait_{i}")
            with col4:
                workers = st.number_input("Staff at this Step", min_value=1, max_value=50,
                                         value=max(1, i+1), step=1, key=f"dist_fworkers_{i}")
            va = st.checkbox("Value Adding?", value=(i != 3), key=f"dist_fva_{i}")
            error_rate = st.number_input("Error Rate (%)", min_value=0.0, max_value=100.0,
                                        value=0.0, step=0.1, format="%.1f", key=f"dist_ferror_{i}")
            steps.append({
                "name": name,
                "cycle_time": ct,
                "wait_time": wait,
                "workers": workers,
                "value_adding": va,
                "defect_rate": error_rate
            })

    if steps:
        st.divider()
        st.header("Order Flow Map Results")

        chart_buf = make_flow_map_chart(steps, target_fulfillment_time / len(steps), "distribution")
        st.image(chart_buf, use_column_width=True)

        total_order_time = sum(s['cycle_time'] for s in steps) + sum(s['wait_time'] for s in steps)
        va_time = sum(s['cycle_time'] for s in steps if s['value_adding'])
        nva_time = sum(s['cycle_time'] for s in steps if not s['value_adding'])
        total_wait = sum(s['wait_time'] for s in steps)
        process_efficiency = (va_time / total_order_time * 100) if total_order_time > 0 else 0
        on_time = total_order_time <= target_fulfillment_time
        bottleneck = max(steps, key=lambda x: x['cycle_time'])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            time_color = "#00CC00" if on_time else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {time_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Total Order Time</p>
                <p style="color:{time_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{total_order_time:.0f}m</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">Target: {target_fulfillment_time:.0f}m</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            eff_color = "#00CC00" if process_efficiency >= 80 else "#FFD700" if process_efficiency >= 60 else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {eff_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Process Efficiency</p>
                <p style="color:{eff_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{process_efficiency:.1f}%</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid #CC0000;border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Slowest Step</p>
                <p style="color:#CC0000;font-size:1rem;font-weight:900;margin:8px 0;">{bottleneck['name']}</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">{bottleneck['cycle_time']:.0f} mins/order</p>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid #FFD700;border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Total Waste</p>
                <p style="color:#FFD700;font-size:1.8rem;font-weight:900;margin:8px 0;">{nva_time + total_wait:.0f}m</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">per order</p>
            </div>""", unsafe_allow_html=True)

        st.divider()
        recommendations, _, _, _, _ = generate_flow_recommendations(
            steps, target_fulfillment_time / len(steps), shift_hours * 60, "distribution"
        )

        st.header("What SPO Found in Your Order Flow")
        for rec in recommendations:
            color = "#CC0000" if rec['priority'] == 'Critical' else "#FFD700" if rec['priority'] == 'Needs Improvement' else "#00CC00"
            icon = "🚨" if rec['priority'] == 'Critical' else "⚠️" if rec['priority'] == 'Needs Improvement' else "✅"
            st.markdown(f"""
            <div style="background:#1A1D27;border:1px solid {color};border-radius:10px;padding:20px;margin-bottom:12px;">
                <p style="color:{color};font-size:0.7rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px 0;">{icon} {rec['priority']} — {rec['step']}</p>
                <p style="color:#8B90A0;font-size:0.85rem;margin:0 0 8px 0;">{rec['issue']}</p>
                <p style="color:#E8EAF0;font-size:0.85rem;margin:0;"><b>Action:</b> {rec['action']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.header("Generate Report")
        if st.button("Generate Order Flow Map Report", use_container_width=True, key="flow_report_dist"):
            report_company = company_name or "Unnamed Company"
            recs, pe, va, nva, tw = generate_flow_recommendations(
                steps, target_fulfillment_time / len(steps), shift_hours * 60, "distribution"
            )
            chart_buf2 = make_flow_map_chart(steps, target_fulfillment_time / len(steps), "distribution")
            pdf = generate_flow_pdf(report_company, industry, "Distribution Order Flow", steps,
                                    target_fulfillment_time / len(steps), recs, pe, va, nva, tw, chart_buf2)
            st.download_button("Download PDF Report", pdf,
                file_name=f"SPO_OrderFlow_{report_company.replace(' ','_')}.pdf",
                mime="application/pdf", use_container_width=True)

        st.write("")
        if st.button("Save Flow Map to Dashboard", use_container_width=True, key="flow_save_dist"):
            if st.session_state.get("current_company"):
                try:
                    result = save_analysis(
                        company_id=st.session_state.current_company["id"],
                        analysis_type="Deep",
                        kpi_data={"target_time": target_fulfillment_time, "actual_time": total_order_time, "process_efficiency": process_efficiency, "daily_orders": daily_orders},
                        results={"tool": "Order Flow Map", "total_order_time": total_order_time, "process_efficiency": process_efficiency, "slowest_step": bottleneck['name']},
                        risk_score=int(max(0, min(100, process_efficiency))),
                        risk_label="LOW RISK" if process_efficiency >= 80 else "MEDIUM RISK" if process_efficiency >= 60 else "HIGH RISK",
                        tool_name="Order Flow Map"
                    )
                    st.success("Saved to dashboard!" if result else "Save failed.")
                except Exception as e:
                    st.error(f"Save failed: {e}")
            else:
                st.warning("Login required to save.")


def show_supply_chain_flow_map(industry, currency_symbol="$"):
    st.markdown("""
    <div style="background:rgba(232,0,29,0.04);border:1px solid rgba(232,0,29,0.15);border-radius:10px;padding:16px 20px;margin-bottom:24px;">
        <p style="color:#E8001D;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin:0 0 4px 0;">Supply Chain Flow Map</p>
        <p style="color:#cccccc;font-size:0.9rem;margin:0;">Map your supply chain from suppliers to customer. Add as many suppliers as you have. SPO identifies risks, delays and single points of failure.</p>
    </div>
    """, unsafe_allow_html=True)

    company_name = st.text_input("Company Name", placeholder="e.g. Tata Motors", key="sc_flow_company")

    col1, col2 = st.columns(2)
    with col1:
        customer_required_lt = st.number_input("Customer Required Lead Time (days)",
                                               min_value=1.0, max_value=365.0, value=14.0, step=1.0)
        num_suppliers = st.number_input("Number of Suppliers", min_value=1, max_value=20, value=3, step=1)
    with col2:
        num_internal_steps = st.number_input("Number of Internal Steps", min_value=1, max_value=10, value=4, step=1)

    st.divider()

    # Suppliers
    st.subheader("Your Suppliers")
    suppliers = []
    for i in range(int(num_suppliers)):
        with st.expander(f"Supplier {i+1}", expanded=(i < 2)):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                name = st.text_input("Supplier Name", value=f"Supplier {i+1}", key=f"sc_sname_{i}")
            with col2:
                lead_time = st.number_input("Lead Time (days)", min_value=0.0, max_value=90.0,
                                           value=float(3 + i*2), step=0.5, format="%.1f", key=f"sc_slt_{i}")
            with col3:
                reliability = st.number_input("On Time Delivery (%)", min_value=0.0, max_value=100.0,
                                             value=float(95 - i*5), step=1.0, format="%.1f", key=f"sc_srel_{i}")
            with col4:
                backup = st.checkbox("Has Backup Supplier?", value=(i == 0), key=f"sc_sbackup_{i}")
            material = st.text_input("Material / Component Supplied", value=f"Material {i+1}", key=f"sc_smat_{i}")
            suppliers.append({
                "name": name,
                "lead_time": lead_time,
                "reliability": reliability,
                "has_backup": backup,
                "material": material
            })

    st.divider()

    # Internal Steps
    st.subheader("Your Internal Process Steps")
    default_internal = ["Inbound QC", "Warehouse Storage", "Production", "Outbound QC", "Dispatch", "Last Mile Delivery"]
    internal_steps = []
    for i in range(int(num_internal_steps)):
        with st.expander(f"Internal Step {i+1}", expanded=(i < 2)):
            col1, col2, col3 = st.columns(3)
            with col1:
                default_name = default_internal[i] if i < len(default_internal) else f"Step {i+1}"
                name = st.text_input("Step Name", value=default_name, key=f"sc_iname_{i}")
            with col2:
                days = st.number_input("Time (days)", min_value=0.0, max_value=30.0,
                                      value=float(1 + i*0.5), step=0.5, format="%.1f", key=f"sc_idays_{i}")
            with col3:
                va = st.checkbox("Value Adding?", value=True, key=f"sc_iva_{i}")
            wait_days = st.number_input("Wait/Queue Time (days)", min_value=0.0, max_value=10.0,
                                       value=0.0, step=0.1, format="%.1f", key=f"sc_iwait_{i}")
            internal_steps.append({
                "name": name,
                "cycle_time": days * 24 * 60,  # convert to mins for compatibility
                "days": days,
                "wait_time": wait_days * 24 * 60,
                "wait_days": wait_days,
                "value_adding": va
            })

    if suppliers and internal_steps:
        st.divider()
        st.header("Supply Chain Flow Map Results")

        # Build combined steps for chart (suppliers + internal)
        all_steps_for_chart = []
        for s in suppliers:
            all_steps_for_chart.append({
                "name": s['name'][:10],
                "cycle_time": s['lead_time'] * 60,
                "wait_time": 0,
                "workers": 1,
                "value_adding": True,
                "defect_rate": 100 - s['reliability']
            })
        for s in internal_steps:
            all_steps_for_chart.append({
                "name": s['name'][:10],
                "cycle_time": s['days'] * 60,
                "wait_time": s['wait_days'] * 60,
                "workers": 1,
                "value_adding": s['value_adding'],
                "defect_rate": 0
            })

        chart_buf = make_flow_map_chart(all_steps_for_chart, customer_required_lt * 60 / len(all_steps_for_chart), "supply_chain")
        st.image(chart_buf, use_column_width=True)

        # Calculations
        max_supplier_lt = max(s['lead_time'] for s in suppliers)
        total_internal_days = sum(s['days'] + s['wait_days'] for s in internal_steps)
        total_lt = max_supplier_lt + total_internal_days
        lt_gap = total_lt - customer_required_lt
        single_source_count = sum(1 for s in suppliers if not s['has_backup'])
        worst_supplier = min(suppliers, key=lambda x: x['reliability'])
        va_days = sum(s['days'] for s in internal_steps if s['value_adding'])
        nva_days = sum(s['days'] for s in internal_steps if not s['value_adding'])
        wait_days_total = sum(s['wait_days'] for s in internal_steps)
        lt_efficiency = (va_days / total_lt * 100) if total_lt > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            lt_color = "#00CC00" if total_lt <= customer_required_lt else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {lt_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Total Lead Time</p>
                <p style="color:{lt_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{total_lt:.1f}d</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">Customer needs: {customer_required_lt:.0f}d</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            risk_color = "#CC0000" if single_source_count > 0 else "#00CC00"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {risk_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Single Source Risk</p>
                <p style="color:{risk_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{single_source_count}</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">suppliers with no backup</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            rel_color = "#00CC00" if worst_supplier['reliability'] >= 95 else "#FFD700" if worst_supplier['reliability'] >= 85 else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {rel_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Weakest Supplier OTD</p>
                <p style="color:{rel_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{worst_supplier['reliability']:.0f}%</p>
                <p style="color:#8B90A0;font-size:0.78rem;margin:0;">{worst_supplier['name']}</p>
            </div>""", unsafe_allow_html=True)
        with col4:
            eff_color = "#00CC00" if lt_efficiency >= 70 else "#FFD700" if lt_efficiency >= 40 else "#CC0000"
            st.markdown(f"""<div style="background:#1A1D27;border:2px solid {eff_color};border-radius:10px;padding:16px;text-align:center;">
                <p style="color:#E8EAF0;margin:0;font-size:0.82rem;">Supply Chain Efficiency</p>
                <p style="color:{eff_color};font-size:1.8rem;font-weight:900;margin:8px 0;">{lt_efficiency:.1f}%</p>
            </div>""", unsafe_allow_html=True)

        st.divider()

        # Recommendations
        st.header("What SPO Found in Your Supply Chain")
        sc_recommendations = []

        if lt_gap > 0:
            sc_recommendations.append({
                "priority": "Critical",
                "step": "Total Lead Time",
                "issue": f"Your total lead time of {total_lt:.1f} days exceeds your customer requirement of {customer_required_lt:.0f} days by {lt_gap:.1f} days. You cannot meet your customer's delivery expectations with the current supply chain.",
                "action": f"You need to eliminate {lt_gap:.1f} days from your supply chain. Start with your internal wait times ({wait_days_total:.1f} days) — these are pure waste. Then negotiate shorter lead times with your fastest supplier."
            })

        if single_source_count > 0:
            ss_names = [s['name'] for s in suppliers if not s['has_backup']]
            sc_recommendations.append({
                "priority": "Critical",
                "step": "Single Source Risk",
                "issue": f"You have {single_source_count} supplier(s) with no backup: {', '.join(ss_names)}. If any of these suppliers fails, your production stops immediately with no alternative.",
                "action": f"Qualify at least one backup supplier for {', '.join(ss_names)} within 60 days. Even a partially qualified backup changes your risk profile significantly."
            })

        if worst_supplier['reliability'] < 90:
            sc_recommendations.append({
                "priority": "Critical",
                "step": worst_supplier['name'],
                "issue": f"{worst_supplier['name']} delivers on time only {worst_supplier['reliability']:.0f}% of the time. That means {100-worst_supplier['reliability']:.0f} out of every 100 deliveries from them are late — causing downstream delays in your production.",
                "action": f"Hold an urgent performance review with {worst_supplier['name']}. Set a 30 day improvement target of minimum 95% OTD. If they cannot meet this, accelerate finding a backup supplier."
            })

        if nva_days > 0:
            nva_steps = [s['name'] for s in internal_steps if not s['value_adding']]
            sc_recommendations.append({
                "priority": "Needs Improvement",
                "step": "Non-Value Adding Steps",
                "issue": f"Your internal process has {nva_days:.1f} days of non-value adding time at: {', '.join(nva_steps)}. Your customer is not paying for these steps.",
                "action": f"Investigate whether {', '.join(nva_steps)} can be eliminated or combined with adjacent steps. Even reducing these by 50% would save {nva_days/2:.1f} days from your lead time."
            })

        if wait_days_total > 0.5:
            sc_recommendations.append({
                "priority": "Needs Improvement",
                "step": "Internal Wait Times",
                "issue": f"Your internal steps have {wait_days_total:.1f} days of waiting and queue time. This is time where your materials are sitting idle and not moving toward the customer.",
                "action": "Map where materials are physically sitting and waiting. Install visual management (kanban or min-max signals) to eliminate queue buildup between your internal steps."
            })

        if not sc_recommendations:
            sc_recommendations.append({
                "priority": "Good",
                "step": "Overall Supply Chain",
                "issue": f"Your supply chain is performing well with a total lead time of {total_lt:.1f} days within your customer requirement.",
                "action": "Focus on maintaining supplier relationships and continuously monitoring OTD performance."
            })

        for rec in sc_recommendations:
            color = "#CC0000" if rec['priority'] == 'Critical' else "#FFD700" if rec['priority'] == 'Needs Improvement' else "#00CC00"
            icon = "🚨" if rec['priority'] == 'Critical' else "⚠️" if rec['priority'] == 'Needs Improvement' else "✅"
            st.markdown(f"""
            <div style="background:#1A1D27;border:1px solid {color};border-radius:10px;padding:20px;margin-bottom:12px;">
                <p style="color:{color};font-size:0.7rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px 0;">{icon} {rec['priority']} — {rec['step']}</p>
                <p style="color:#8B90A0;font-size:0.85rem;margin:0 0 8px 0;">{rec['issue']}</p>
                <p style="color:#E8EAF0;font-size:0.85rem;margin:0;"><b>Action:</b> {rec['action']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Supplier breakdown
        st.divider()
        st.header("Supplier Breakdown")
        for s in suppliers:
            rel_color = "#00CC00" if s['reliability'] >= 95 else "#FFD700" if s['reliability'] >= 85 else "#CC0000"
            backup_text = "✅ Has backup" if s['has_backup'] else "🚨 No backup"
            st.markdown(f"""
            <div style="background:#1A1D27;border-left:4px solid {rel_color};padding:12px 16px;margin:6px 0;border-radius:0 8px 8px 0;">
                <span style="color:#E8EAF0;font-weight:700;">{s['name']}</span>
                <span style="color:#8B90A0;margin-left:10px;font-size:0.82rem;">
                    {s['material']} | LT: {s['lead_time']:.0f}d | OTD: 
                    <span style="color:{rel_color}">{s['reliability']:.0f}%</span> | {backup_text}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.header("Generate Report")
        if st.button("Generate Supply Chain Flow Map Report", use_container_width=True, key="flow_report_sc"):
            report_company = company_name or "Unnamed Company"
            chart_buf2 = make_flow_map_chart(all_steps_for_chart, customer_required_lt * 60 / len(all_steps_for_chart), "supply_chain")
            sc_steps_for_pdf = [{"name": s['name'], "cycle_time": s['lead_time']*60, "wait_time": 0,
                                  "workers": 1, "value_adding": True, "defect_rate": 100-s['reliability']} for s in suppliers] + \
                               [{"name": s['name'], "cycle_time": s['days']*60, "wait_time": s['wait_days']*60,
                                 "workers": 1, "value_adding": s['value_adding'], "defect_rate": 0} for s in internal_steps]
            pdf = generate_flow_pdf(
                report_company, industry, "Supply Chain Flow Map",
                sc_steps_for_pdf, customer_required_lt * 60 / len(all_steps_for_chart),
                sc_recommendations, lt_efficiency, va_days, nva_days, wait_days_total, chart_buf2
            )
            st.download_button("Download PDF Report", pdf,
                file_name=f"SPO_SCFlowMap_{report_company.replace(' ','_')}.pdf",
                mime="application/pdf", use_container_width=True)

        st.write("")
        if st.button("Save Flow Map to Dashboard", use_container_width=True, key="flow_save_sc"):
            if st.session_state.get("current_company"):
                try:
                    result = save_analysis(
                        company_id=st.session_state.current_company["id"],
                        analysis_type="Deep",
                        kpi_data={"total_lt": total_lt, "customer_required_lt": customer_required_lt, "num_suppliers": num_suppliers, "single_source_count": single_source_count, "lt_efficiency": lt_efficiency},
                        results={"tool": "Supply Chain Flow Map", "total_lt_days": total_lt, "lt_gap": lt_gap, "worst_supplier": worst_supplier['name'], "single_source_count": single_source_count},
                        risk_score=int(max(0, min(100, lt_efficiency))),
                        risk_label="LOW RISK" if lt_efficiency >= 70 else "MEDIUM RISK" if lt_efficiency >= 40 else "HIGH RISK",
                        tool_name="Supply Chain Flow Map"
                    )
                    st.success("Saved to dashboard!" if result else "Save failed.")
                except Exception as e:
                    st.error(f"Save failed: {e}")
            else:
                st.warning("Login required to save.")