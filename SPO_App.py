import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Smart Process Optimizer",
    page_icon="🏭",
    layout="wide"
)

# Title
st.title("🏭 Smart Process Optimizer (SPO)")
st.subheader("A Decision Support Tool for Manufacturing Efficiency")
st.divider()

# Industry Benchmarks
benchmarks = {
    "efficiency_rate": 85,
    "cycle_time": 30,
    "waste_percentage": 5,
    "roi": 15,
    "manpower_utilization": 85,
    "rejection_rate": 3,
    "lead_time": 7
}

# Sidebar - KPI Input
st.sidebar.title("Enter Your Plant KPIs")
st.sidebar.divider()

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

# Analysis Engine
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

# Run analysis every time sliders change
analysis = analyze_kpis(kpi_data, benchmarks)

# KPI Status Section
st.header("📊 KPI Analysis")
col1, col2, col3 = st.columns(3)

status_colors = {
    "Good": "✅",
    "Needs Improvement": "⚠️",
    "Critical": "🚨"
}

kpi_labels = {
    "efficiency_rate": "Efficiency Rate",
    "cycle_time": "Cycle Time",
    "waste_percentage": "Waste Percentage",
    "roi": "ROI",
    "manpower_utilization": "Manpower Utilization",
    "rejection_rate": "Rejection Rate",
    "lead_time": "Lead Time"
}

for i, (kpi, result) in enumerate(analysis.items()):
    col = [col1, col2, col3][i % 3]
    with col:
        st.metric(
            label=f"{status_colors[result['status']]} {kpi_labels[kpi]}",
            value=f"{result['value']}",
            delta=f"Benchmark: {result['benchmark']}"
        )

st.divider()

# Root Cause and Recommendations - Updates with every slider change
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

# Display Root Causes and Recommendations side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Root Causes")
    if root_causes:
        for cause in root_causes:
            st.warning(cause)
    else:
        st.success("No critical root causes detected! Plant is performing well.")

with col2:
    st.subheader("Recommendations")
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("No recommendations needed! Plant is performing at benchmark level.")

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
    st.metric("Efficiency Rate",
              f"{efficiency_rate + efficiency_improvement}%",
              f"+{efficiency_improvement}%")
    st.metric("Manpower Utilization",
              f"{manpower_utilization + manpower_improvement}%",
              f"+{manpower_improvement}%")

with col2:
    st.metric("Rejection Rate",
              f"{rejection_rate - rejection_improvement}%",
              f"-{rejection_improvement}%")
    st.metric("Waste Percentage",
              f"{waste_percentage - waste_improvement}%",
              f"-{waste_improvement}%")

with col3:
    st.metric("Cycle Time",
              f"{cycle_time - cycle_improvement} mins",
              f"-{cycle_improvement} mins")
    st.metric("Lead Time",
              f"{lead_time - lead_improvement} days",
              f"-{lead_improvement} days")