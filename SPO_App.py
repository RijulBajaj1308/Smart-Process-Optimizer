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
st.divider()

# Plotly Charts Section
st.header("📈 Performance Charts")

import plotly.graph_objects as go

# KPI Gauge Charts
st.subheader("KPI Gauges")
col1, col2, col3 = st.columns(3)

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

with col1:
    st.plotly_chart(create_gauge("Efficiency Rate", efficiency_rate, 85, 100), use_container_width=True)
    st.plotly_chart(create_gauge("ROI", roi, 15, 50), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge("Manpower Utilization", manpower_utilization, 85, 100), use_container_width=True)
    st.plotly_chart(create_gauge("Waste %", waste_percentage, 5, 50), use_container_width=True)

with col3:
    st.plotly_chart(create_gauge("Rejection Rate", rejection_rate, 3, 50), use_container_width=True)
    st.plotly_chart(create_gauge("Lead Time", lead_time, 7, 30), use_container_width=True)    
st.divider()

# ROI Projection Calculator
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

# Calculate projected savings
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
    st.metric("💰 Total Annual Savings", f"${total_savings:,.0f}", 
              delta=f"+${total_savings:,.0f}")    
st.divider()

# PFMEA Module
st.header("⚠️ PFMEA Module")
st.write("Process Failure Mode and Effects Analysis — Identify and assess potential failures in your process")

st.subheader("Add a Process Step")

col1, col2 = st.columns(2)

with col1:
    process_step = st.text_input("Process Step", placeholder="e.g. Assembly, Welding, Painting")
    failure_mode = st.text_input("Potential Failure Mode", placeholder="e.g. Incorrect assembly, Weld crack")
    failure_effect = st.text_input("Effect of Failure", placeholder="e.g. Product defect, Safety hazard")

with col2:
    severity = st.slider("Severity (1-10)", 1, 10, 5)
    occurrence = st.slider("Occurrence (1-10)", 1, 10, 5)
    detection = st.slider("Detection (1-10)", 1, 10, 5)

# Calculate RPN
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
    st.metric("RPN Score", rpn)

# RPN Risk Level
if rpn >= 200:
    st.error(f"🚨 HIGH RISK — RPN of {rpn} requires immediate corrective action!")
    st.warning("Recommended Action: Stop production and investigate immediately. Implement corrective measures before resuming.")
elif rpn >= 100:
    st.warning(f"⚠️ MEDIUM RISK — RPN of {rpn} requires attention and monitoring.")
    st.info("Recommended Action: Develop a corrective action plan and implement within 30 days.")
else:
    st.success(f"✅ LOW RISK — RPN of {rpn} is acceptable. Continue monitoring.")
    st.info("Recommended Action: Maintain current controls and monitor regularly.")    