import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Manufacturing
# Sources:
# Automotive: Maruti Suzuki, Tata Motors, Mahindra annual reports
# Electronics: Indian PLI scheme benchmarks
# Food and Beverage: Indian FMCG standards (HUL, Nestle India, ITC)
# Textile: Indian textile industry standards (Raymond, Arvind Mills)
# General Manufacturing: Average Indian SME standards
# Eco Friendly Packaging: UFlex Limited, ITC Packaging, SR Pulp benchmarks
# Pulp and Paper: JK Paper, TNPL, Kuantum Papers benchmarks
# Pharmaceutical: Sun Pharma, Cipla, Dr Reddy's, Aurobindo Pharma — ISPE benchmarking study

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
        # Based on UFlex Limited and ITC Packaging benchmarks
        "efficiency_rate": 80.000,
        "cycle_time": 30.000,
        "waste_percentage": 3.000,
        "roi": 10.000,
        "manpower_utilization": 80.000,
        "rejection_rate": 2.000,
        "lead_time": 8.000
    },
    "Pulp and Paper Manufacturing": {
        # Based on JK Paper, TNPL, Kuantum Papers benchmarks
        "efficiency_rate": 72.000,
        "cycle_time": 45.000,
        "waste_percentage": 8.000,
        "roi": 8.000,
        "manpower_utilization": 75.000,
        "rejection_rate": 4.000,
        "lead_time": 12.000
    },
    "Pharmaceutical Manufacturing": {
        # Based on Sun Pharma, Cipla, Dr Reddy's, Aurobindo Pharma standards
        # ISPE benchmarking: top quartile pharma plants target 90%+ OEE and below 1% batch rejection
        "efficiency_rate": 90.000,
        "cycle_time": 15.000,
        "waste_percentage": 1.000,
        "roi": 20.000,
        "manpower_utilization": 85.000,
        "rejection_rate": 1.000,
        "lead_time": 3.000
    }
}

kpi_labels = {
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

def show_manufacturing(industry, currency_symbol="$"):
    benchmarks = manufacturing_benchmarks[industry]

    st.sidebar.title("Enter Your Plant KPIs")
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

    # KPI Cards
    st.header("KPI Analysis")
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
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{status_icons[result['status']]} {kpi_labels[kpi]}</p>
                    <p style="color: {color}; font-size: 2rem; font-weight: 800; margin: 5px 0;">{result['value']:.3f}</p>
                    <p style="color: #888888; font-size: 0.8rem; margin: 0;">Benchmark: {result['benchmark']:.3f}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Risk Assessment Dashboard
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
            <p style="color: #ffffff; margin: 0;">Critical KPIs</p>
            <p style="color: #CC0000; font-size: 3rem; font-weight: 900; margin: 0;">{critical_count}</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Needs Improvement</p>
            <p style="color: #FFD700; font-size: 3rem; font-weight: 900; margin: 0;">{needs_improvement_count}</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div style="background-color: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px; text-align: center;">
            <p style="color: #ffffff; margin: 0;">Good KPIs</p>
            <p style="color: #00CC00; font-size: 3rem; font-weight: 900; margin: 0;">{good_count}</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Root Causes and Recommendations
    st.header("Root Causes and Recommendations")
    root_causes = []
    recommendations = []
    improvements = {}

    if analysis["efficiency_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low efficiency: Possible machine downtime, poor line balancing, or excessive idle time")
        recommendations.append("Conduct a full line balancing study to redistribute workload evenly across all stations")
        improvements["efficiency_rate"] = min(benchmarks["efficiency_rate"], efficiency_rate + 12)

    if analysis["cycle_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High cycle time: Possible bottleneck at a specific station, unskilled labor, or poor workstation layout")
        recommendations.append("Perform time studies at each station to identify the bottleneck and redistribute tasks")
        improvements["cycle_time"] = max(benchmarks["cycle_time"], cycle_time - 10)

    if analysis["waste_percentage"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High waste: Possible overproduction, defective materials, or poor quality control")
        recommendations.append("Implement a waste tracking system and investigate the top 3 sources of waste on the floor")
        improvements["waste_percentage"] = max(benchmarks["waste_percentage"], waste_percentage - 3)

    if analysis["roi"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low ROI: Possible high operational costs, low output, or high rejection rates")
        recommendations.append("Focus on reducing operational costs by eliminating non value adding activities")
        improvements["roi"] = min(benchmarks["roi"], roi + 5)

    if analysis["manpower_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low manpower utilization: Possible poor task distribution, idle workers, or line imbalance")
        recommendations.append("Reassign idle workers as floaters to support overloaded stations")
        improvements["manpower_utilization"] = min(benchmarks["manpower_utilization"], manpower_utilization + 15)

    if analysis["rejection_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High rejection rate: Possible quality control issues, defective raw materials, or operator errors")
        recommendations.append("Conduct root cause analysis on top defect types and implement quality checkpoints")
        improvements["rejection_rate"] = max(benchmarks["rejection_rate"], rejection_rate - 3)

    if analysis["lead_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High lead time: Possible supply chain delays, poor scheduling, or production bottlenecks")
        recommendations.append("Map the entire value stream to identify delays and implement pull based scheduling")
        improvements["lead_time"] = max(benchmarks["lead_time"], lead_time - 3)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Root Causes")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("No critical root causes detected!")

    with col2:
        st.subheader("Recommendations")
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("Plant is performing at benchmark level!")

    st.divider()

    # Action Priority Score
    st.header("Action Priority Score")
    st.write("Focus on these KPIs first for maximum impact:")

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
                    <span style="color: #ffffff; margin-left: 10px;">{kpi_labels[kpi]}</span>
                    <span style="color: #888888; margin-left: 10px;">Current: {result['value']:.3f} | Benchmark: {result['benchmark']:.3f}</span>
                </div>
            """, unsafe_allow_html=True)
            priority_rank += 1

    st.divider()

    # Before vs After Projection
    st.header("Projected Before vs After")
    st.write("If you implement all recommendations here is what your plant could look like:")

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
                        <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{kpi_labels[kpi]}</p>
                        <p style="color: #CC0000; font-size: 1.2rem; margin: 5px 0;">Before: {current:.3f}</p>
                        <p style="color: #00CC00; font-size: 1.2rem; margin: 5px 0;">After: {projected:.3f}</p>
                        <p style="color: #00CC00; font-size: 1rem; font-weight: 800; margin: 0;">{change_str} improvement</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Your plant is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("What-If Simulator")
    st.write("Adjust the values below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        efficiency_improvement = st.number_input("Improve Efficiency Rate by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        manpower_improvement = st.number_input("Improve Manpower Utilization by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        rejection_improvement = st.number_input("Reduce Rejection Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        waste_improvement = st.number_input("Reduce Waste by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")
        cycle_improvement = st.number_input("Reduce Cycle Time by (mins)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        lead_improvement = st.number_input("Reduce Lead Time by (days)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Projected Results")
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
    st.subheader("KPI Gauges")

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

    # ROI Calculator
    st.header("ROI Projection Calculator")
    st.write(f"Enter your plant's financial details in {currency_symbol}")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input(f"Annual Revenue ({currency_symbol})", min_value=0.000, value=1000000.000, step=1000.000, format="%.3f")
        num_workers = st.number_input("Number of Workers", min_value=0, value=50, step=1)
        avg_worker_salary = st.number_input(f"Average Worker Salary ({currency_symbol}/year)", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")

    with col2:
        waste_cost = st.number_input(f"Annual Waste Cost ({currency_symbol})", min_value=0.000, value=50000.000, step=1000.000, format="%.3f")
        downtime_cost = st.number_input(f"Annual Downtime Cost ({currency_symbol})", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")
        rejection_cost = st.number_input(f"Annual Rejection Cost ({currency_symbol})", min_value=0.000, value=20000.000, step=1000.000, format="%.3f")

    efficiency_savings = annual_revenue * (efficiency_improvement / 100)
    manpower_savings = num_workers * avg_worker_salary * (manpower_improvement / 100)
    waste_savings = waste_cost * (waste_improvement / 100)
    rejection_savings = rejection_cost * (rejection_improvement / 100)
    total_savings = efficiency_savings + manpower_savings + waste_savings + rejection_savings

    st.subheader("Projected Annual Savings")
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
    st.write("Process Failure Mode and Effects Analysis — Identify and assess potential failures in your process")
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
        st.warning("Recommended Action: Stop production and investigate immediately.")
    elif rpn >= 100:
        st.warning(f"⚠️ MEDIUM RISK — RPN of {rpn} requires attention and monitoring.")
        st.info("Recommended Action: Develop a corrective action plan within 30 days.")
    else:
        st.success(f"✅ LOW RISK — RPN of {rpn} is acceptable.")
        st.info("Recommended Action: Maintain current controls and monitor regularly.")