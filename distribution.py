import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Distribution
# Based on Indian distribution and logistics industry standards
distribution_benchmarks = {
    "Warehouse and Distribution": {
        # Based on Indian 3PL and warehouse standards
        "order_fulfillment_rate": 95,
        "on_time_delivery": 92,
        "warehouse_utilization": 85,
        "picking_accuracy": 99,
        "inventory_turnover": 12,
        "return_rate": 2,
        "cost_per_order": 50
    },
    "Cold Chain Distribution": {
        # Based on Indian cold chain standards
        "order_fulfillment_rate": 97,
        "on_time_delivery": 95,
        "warehouse_utilization": 80,
        "picking_accuracy": 99,
        "inventory_turnover": 20,
        "return_rate": 1,
        "cost_per_order": 80
    },
    "E-commerce Fulfillment": {
        # Based on Indian e-commerce standards (Flipkart, Amazon India)
        "order_fulfillment_rate": 98,
        "on_time_delivery": 95,
        "warehouse_utilization": 88,
        "picking_accuracy": 99.5,
        "inventory_turnover": 15,
        "return_rate": 8,
        "cost_per_order": 40
    }
}

kpi_labels = {
    "order_fulfillment_rate": "Order Fulfillment Rate (%)",
    "on_time_delivery": "On Time Delivery (%)",
    "warehouse_utilization": "Warehouse Utilization (%)",
    "picking_accuracy": "Picking Accuracy (%)",
    "inventory_turnover": "Inventory Turnover (times/year)",
    "return_rate": "Return Rate (%)",
    "cost_per_order": "Cost per Order ($)"
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

def show_distribution(industry):
    benchmarks = distribution_benchmarks[industry]

    st.sidebar.title("Enter Your Distribution KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    order_fulfillment_rate = st.sidebar.slider("Order Fulfillment Rate (%)", 0, 100, 88)
    on_time_delivery = st.sidebar.slider("On Time Delivery (%)", 0, 100, 85)
    warehouse_utilization = st.sidebar.slider("Warehouse Utilization (%)", 0, 100, 75)
    picking_accuracy = st.sidebar.slider("Picking Accuracy (%)", 90, 100, 95)
    inventory_turnover = st.sidebar.slider("Inventory Turnover (times/year)", 0, 30, 8)
    return_rate = st.sidebar.slider("Return Rate (%)", 0, 30, 5)
    cost_per_order = st.sidebar.slider("Cost per Order ($)", 0, 200, 70)

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

    # KPI Cards
    st.header("📊 KPI Analysis")
    st.caption(f"Benchmarks based on {industry} standards in India")
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

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low order fulfillment: Possible stockouts, poor inventory management, or picking errors")
        recommendations.append("Implement real time inventory tracking and set reorder points to prevent stockouts")

    if analysis["on_time_delivery"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low on time delivery: Possible routing inefficiencies, traffic delays, or poor scheduling")
        recommendations.append("Optimize delivery routes using route planning software and implement real time tracking")

    if analysis["warehouse_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low warehouse utilization: Possible poor layout, dead stock, or inefficient storage")
        recommendations.append("Conduct a warehouse layout analysis and implement vertical storage solutions")

    if analysis["picking_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low picking accuracy: Possible manual errors, poor labeling, or inadequate training")
        recommendations.append("Implement barcode scanning or RFID systems to reduce picking errors")

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low inventory turnover: Possible overstocking, poor demand forecasting, or slow moving items")
        recommendations.append("Review demand forecasting methods and identify slow moving SKUs for clearance")

    if analysis["return_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High return rate: Possible product quality issues, wrong items shipped, or damaged goods")
        recommendations.append("Implement quality checks before dispatch and improve packaging to reduce damage")

    if analysis["cost_per_order"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High cost per order: Possible inefficient processes, high labor costs, or poor route planning")
        recommendations.append("Identify and eliminate non value adding steps in the order fulfillment process")

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
            st.success("Distribution is performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("🔮 What-If Simulator")
    st.write("Adjust the sliders below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        fulfillment_improvement = st.slider("Improve Order Fulfillment Rate by (%)", 0, 10, 0)
        delivery_improvement = st.slider("Improve On Time Delivery by (%)", 0, 10, 0)
        utilization_improvement = st.slider("Improve Warehouse Utilization by (%)", 0, 20, 0)

    with col2:
        accuracy_improvement = st.slider("Improve Picking Accuracy by (%)", 0, 5, 0)
        return_improvement = st.slider("Reduce Return Rate by (%)", 0, 10, 0)
        cost_improvement = st.slider("Reduce Cost per Order by ($)", 0, 50, 0)

    st.subheader("Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Order Fulfillment Rate", f"{order_fulfillment_rate + fulfillment_improvement}%", f"+{fulfillment_improvement}%")
        st.metric("On Time Delivery", f"{on_time_delivery + delivery_improvement}%", f"+{delivery_improvement}%")

    with col2:
        st.metric("Warehouse Utilization", f"{warehouse_utilization + utilization_improvement}%", f"+{utilization_improvement}%")
        st.metric("Picking Accuracy", f"{picking_accuracy + accuracy_improvement}%", f"+{accuracy_improvement}%")

    with col3:
        st.metric("Return Rate", f"{return_rate - return_improvement}%", f"-{return_improvement}%")
        st.metric("Cost per Order", f"${cost_per_order - cost_improvement}", f"-${cost_improvement}")

    st.divider()

    # ROI Calculator
    st.header("💰 ROI Projection Calculator")
    col1, col2 = st.columns(2)

    with col1:
        monthly_orders = st.number_input("Monthly Orders", min_value=0, value=10000, step=100)
        avg_order_value = st.number_input("Average Order Value ($)", min_value=0, value=100, step=10)

    with col2:
        return_cost = st.number_input("Cost per Return ($)", min_value=0, value=20, step=5)
        labor_cost = st.number_input("Monthly Labor Cost ($)", min_value=0, value=50000, step=1000)

    fulfillment_savings = monthly_orders * avg_order_value * (fulfillment_improvement / 100) * 12
    return_savings = monthly_orders * (return_improvement / 100) * return_cost * 12
    cost_savings = monthly_orders * cost_improvement * 12
    total_savings = fulfillment_savings + return_savings + cost_savings

    st.subheader("Projected Annual Savings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fulfillment Savings", f"${fulfillment_savings:,.0f}")
        st.metric("Return Savings", f"${return_savings:,.0f}")

    with col2:
        st.metric("Cost per Order Savings", f"${cost_savings:,.0f}")

    with col3:
        st.metric("💰 Total Annual Savings", f"${total_savings:,.0f}", delta=f"+${total_savings:,.0f}")