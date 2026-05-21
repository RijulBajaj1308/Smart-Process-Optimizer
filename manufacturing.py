import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Manufacturing
# Based on Indian industry standards comparing Maruti Suzuki, Tata Motors, Mahindra and other leading Indian manufacturers
manufacturing_benchmarks = {
    "Automotive": {
        # Based on Maruti Suzuki, Tata Motors, Mahindra standards
        "efficiency_rate": 85,
        "cycle_time": 25,
        "waste_percentage": 4,
        "roi": 15,
        "manpower_utilization": 85,
        "rejection_rate": 2,
        "lead_time": 7
    },
    "Electronics": {
        # Based on Indian electronics PLI scheme benchmarks
        "efficiency_rate": 82,
        "cycle_time": 20,
        "waste_percentage": 3,
        "roi": 18,
        "manpower_utilization": 82,
        "rejection_rate": 2,
        "lead_time": 5
    },
    "Food and Beverage": {
        # Based on Indian FMCG and food processing standards
        "efficiency_rate": 78,
        "cycle_time": 20,
        "waste_percentage": 2,
        "roi": 12,
        "manpower_utilization": 78,
        "rejection_rate": 1,
        "lead_time": 2
    },
    "Textile and Apparel": {
        # Based on Indian textile industry standards
        "efficiency_rate": 72,
        "cycle_time": 40,
        "waste_percentage": 8,
        "roi": 8,
        "manpower_utilization": 75,
        "rejection_rate": 4,
        "lead_time": 14
    },
    "General Manufacturing": {
        # Based on average Indian SME manufacturing standards
        "efficiency_rate": 75,
        "cycle_time": 35,
        "waste_percentage": 6,
        "roi": 10,
        "manpower_utilization": 78,
        "rejection_rate": 3,
        "lead_time": 10
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

def show_manufacturing(industry):
    benchmarks = manufacturing_benchmarks[industry]

    st.sidebar.title("Enter Your Plant KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} Industry (India)")

    efficiency_rate = st.sidebar.slider("Efficiency Rate (%)", 0, 100, 65)
    cycle_time = st.sidebar.slider("Cycle Time (mins)", 0, 120, 45)
    waste_percentage = st.sidebar.slider("Waste Percentage (%)", 0, 50, 12)
    roi = st.sidebar.slider("ROI (%)", 0, 50, 8)
    manpower_utilization = st.sidebar.slider("Manpower Utilization (%)", 0, 100, 70)
    rejection_rate = st.sidebar.slider("Rejection Rate (%)", 0, 50, 8)
    lead_time = st.sidebar.slider("Lead Time (days)", 0, 30, 10)

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
    st.header("📊 KPI Analysis")
    st.caption(f"Benchmarks based on {industry} industry standards in India")
    col1, col2, col3 = st.columns(3)

    status_colors = {
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
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{status_colors[result['status']]} {kpi_labels[kpi]}</p>
                    <p style="color: {color}; font-size: 2rem; font-weight: 800; margin: 5px 0;">{result['value']}</p>
                    <p style="color: #888888; font-size: 0.8rem; margin: 0;">Benchmark: {result['benchmark']}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Root Causes and Recommendations
    st.header("🔍 Root Causes and Recommendations")
    root_causes = []
    recommendations = []

    if analysis["efficiency_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low efficiency: Possible machine downtime, poor line balancing, or excessive idle time")
        recommendations.append("Conduct a full line balancing study to redistribute workload evenly across all stations")

    if analysis["cycle_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High cycle time: Possible bottleneck at a specific station, unskilled labor, or poor workstation layout")
        recommendations.append("Perform time studies at each station to identify the bottleneck and redistribute tasks")

    if analysis["waste_percentage"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High waste: Possible overproduction, defective materials, or poor quality control")
        recommendations.append("Implement a waste tracking system and investigate the top 3 sources of waste on the floor")

    if analysis["roi"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low ROI: Possible high operational costs, low output, or high rejection rates")
        recommendations.append("Focus on reducing operational costs by eliminating non value adding activities")

    if analysis["manpower_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low manpower utilization: Possible poor task distribution, idle workers, or line imbalance")
        recommendations.append("Reassign idle workers as floaters to support overloaded stations")

    if analysis["rejection_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High rejection rate: Possible quality control issues, defective raw materials, or operator errors")
        recommendations.append("Conduct root cause analysis on top defect types and implement quality checkpoints")

    if analysis["lead_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High lead time: Possible supply chain delays, poor scheduling, or production bottlenecks")
        recommendations.append("Map the entire value stream to identify delays and implement pull based scheduling")

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

    # What-If Simulator
    st.header("🔮 What-If Simulator")
    st.write("Adjust the sliders below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        efficiency_improvement = st.slider("Improve Efficiency Rate by (%)", 0, 30, 0)
        manpower_improvement = st.slider("Improve Manpower Utilization by (%)", 0, 30, 0)
        rejection_improvement = st.slider("Reduce Rejection Rate by (%)", 0, 10, 0)

    with col2:
        waste_improvement = st.slider("Reduce Waste by (%)", 0, 20, 0)
        cycle_improvement = st.slider("Reduce Cycle Time by (mins)", 0, 30, 0)
        lead_improvement = st.slider("Reduce Lead Time by (days)", 0, 10, 0)

    st.subheader("Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Rate", f"{efficiency_rate + efficiency_improvement}%", f"+{efficiency_improvement}%")
        st.metric("Manpower Utilization", f"{manpower_utilization + manpower_improvement}%", f"+{manpower_improvement}%")

    with col2:
        st.metric("Rejection Rate", f"{rejection_rate - rejection_improvement}%", f"-{rejection_improvement}%")
        st.metric("Waste Percentage", f"{waste_percentage - waste_improvement}%", f"-{waste_improvement}%")

    with col3:
        st.metric("Cycle Time", f"{cycle_time - cycle_improvement} mins", f"-{cycle_improvement} mins")
        st.metric("Lead Time", f"{lead_time - lead_improvement} days", f"-{lead_improvement} days")

    st.divider()

    # Gauge Charts
    st.header("📈 Performance Charts")
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
    st.header("💰 ROI Projection Calculator")
    st.write("Enter your plant's financial details to see the projected financial impact of improvements")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input("Annual Revenue ($)", min_value=0, value=1000000, step=10000)
        num_workers = st.number_input("Number of Workers", min_value=1, value=50, step=1)
        avg_worker_salary = st.number_input("Average Worker Salary ($/year)", min_value=0, value=30000, step=1000)

    with col2:
        waste_cost = st.number_input("Annual Waste Cost ($)", min_value=0, value=50000, step=1000)
        downtime_cost = st.number_input("Annual Downtime Cost ($)", min_value=0, value=30000, step=1000)
        rejection_cost = st.number_input("Annual Rejection Cost ($)", min_value=0, value=20000, step=1000)

    efficiency_savings = annual_revenue * (efficiency_improvement / 100)
    manpower_savings = num_workers * avg_worker_salary * (manpower_improvement / 100)
    waste_savings = waste_cost * (waste_improvement / 100)
    rejection_savings = rejection_cost * (rejection_improvement / 100)
    total_savings = efficiency_savings + manpower_savings + waste_savings + rejection_savings

    st.subheader("Projected Annual Savings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Savings", f"${efficiency_savings:,.0f}")
        st.metric("Manpower Savings", f"${manpower_savings:,.0f}")

    with col2:
        st.metric("Waste Savings", f"${waste_savings:,.0f}")
        st.metric("Rejection Savings", f"${rejection_savings:,.0f}")

    with col3:
        st.metric("💰 Total Annual Savings", f"${total_savings:,.0f}", delta=f"+${total_savings:,.0f}")

    st.divider()

    # PFMEA Module
    st.header("⚠️ PFMEA Module")
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