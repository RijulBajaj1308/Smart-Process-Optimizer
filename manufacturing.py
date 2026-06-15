import streamlit as st
import plotly.graph_objects as go

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

def generate_dynamic_insights(kpi, value, benchmark, gap, status):
    # Higher is better KPIs
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

    # Lower is better KPIs
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
                kpi,
                result["value"],
                result["benchmark"],
                result["gap"],
                result["status"]
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

    for kpi, score in priority_scores.items():
        if score > 0:
            result = analysis[kpi]
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

    # Before vs After
    st.header("Where You Are vs Where You Could Be")
    st.write("Based on your numbers here is a realistic projection if you act on the recommendations:")

    if improvements:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, (kpi, projected) in enumerate(improvements.items()):
            col = cols[i % 3]
            current = kpi_data[kpi]
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
                        <p style="color: #00CC00; font-size: 1.2rem; margin: 5px 0;">After: {projected:.3f}</p>
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

    # Money Saved Calculator
    st.header("How Much Money Could You Save?")
    st.write(f"Based on your numbers and SPO recommendations in {currency_symbol}")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input(f"Annual Revenue ({currency_symbol})", min_value=0.000, value=1000000.000, step=1000.000, format="%.3f")
        num_workers = st.number_input("Number of Workers", min_value=0, value=50, step=1)
        avg_worker_salary = st.number_input(f"Average Worker Salary ({currency_symbol}/year)", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")

    with col2:
        waste_cost = st.number_input(f"Annual Waste Cost ({currency_symbol})", min_value=0.000, value=50000.000, step=1000.000, format="%.3f")
        downtime_cost = st.number_input(f"Annual Downtime Cost ({currency_symbol})", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")
        rejection_cost = st.number_input(f"Annual Rejection Cost ({currency_symbol})", min_value=0.000, value=20000.000, step=1000.000, format="%.3f")

    efficiency_gain = improvements.get("efficiency_rate", efficiency_rate) - efficiency_rate
    manpower_gain = improvements.get("manpower_utilization", manpower_utilization) - manpower_utilization
    waste_gain = waste_percentage - improvements.get("waste_percentage", waste_percentage)
    rejection_gain = rejection_rate - improvements.get("rejection_rate", rejection_rate)

    efficiency_savings = annual_revenue * (abs(efficiency_gain) / 100)
    manpower_savings = num_workers * avg_worker_salary * (abs(manpower_gain) / 100)
    waste_savings = waste_cost * (abs(waste_gain) / 100)
    rejection_savings = rejection_cost * (abs(rejection_gain) / 100)
    total_savings = efficiency_savings + manpower_savings + waste_savings + rejection_savings

    st.subheader("Projected Annual Savings Based on SPO Recommendations")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Savings", f"{currency_symbol}{efficiency_savings:,.3f}")
        st.metric("Manpower Savings", f"{currency_symbol}{manpower_savings:,.3f}")

    with col2:
        st.metric("Waste Savings", f"{currency_symbol}{waste_savings:,.3f}")
        st.metric("Rejection Savings", f"{currency_symbol}{rejection_savings:,.3f}")

    with col3:
        st.metric("Total Annual Savings", f"{currency_symbol}{total_savings:,.3f}", delta=f"+{currency_symbol}{total_savings:,.3f}")

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
        st.error(f"🚨 HIGH RISK — RPN of {rpn} requires immediate corrective action!")
        st.warning("Stop production at this process step and investigate immediately before resuming.")
    elif rpn >= 100:
        st.warning(f"⚠️ MEDIUM RISK — RPN of {rpn} requires attention and monitoring.")
        st.info("Develop a corrective action plan and implement within 30 days.")
    else:
        st.success(f"✅ LOW RISK — RPN of {rpn} is acceptable.")
        st.info("Maintain current controls and monitor regularly.")