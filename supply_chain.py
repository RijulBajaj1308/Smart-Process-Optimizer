import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Supply Chain
# Based on Indian supply chain and logistics industry standards
supply_chain_benchmarks = {
    "Automotive Supply Chain": {
        # Based on Tata Motors, Maruti, Mahindra supply chain standards
        "supplier_otd": 95,
        "inventory_turnover": 12,
        "order_fulfillment_rate": 97,
        "forecast_accuracy": 85,
        "supply_chain_cost": 8,
        "days_inventory_outstanding": 30,
        "supplier_quality_rate": 98
    },
    "Food and Beverage Supply Chain": {
        # Based on Indian FMCG supply chain standards
        "supplier_otd": 97,
        "inventory_turnover": 20,
        "order_fulfillment_rate": 98,
        "forecast_accuracy": 80,
        "supply_chain_cost": 6,
        "days_inventory_outstanding": 15,
        "supplier_quality_rate": 99
    },
    "Electronics Supply Chain": {
        # Based on Indian electronics supply chain standards
        "supplier_otd": 93,
        "inventory_turnover": 15,
        "order_fulfillment_rate": 96,
        "forecast_accuracy": 82,
        "supply_chain_cost": 10,
        "days_inventory_outstanding": 25,
        "supplier_quality_rate": 97
    },
    "General Supply Chain": {
        # Based on average Indian SME supply chain standards
        "supplier_otd": 90,
        "inventory_turnover": 8,
        "order_fulfillment_rate": 93,
        "forecast_accuracy": 75,
        "supply_chain_cost": 12,
        "days_inventory_outstanding": 45,
        "supplier_quality_rate": 95
    }
}

kpi_labels = {
    "supplier_otd": "Supplier On Time Delivery (%)",
    "inventory_turnover": "Inventory Turnover (times/year)",
    "order_fulfillment_rate": "Order Fulfillment Rate (%)",
    "forecast_accuracy": "Demand Forecast Accuracy (%)",
    "supply_chain_cost": "Supply Chain Cost (% of Revenue)",
    "days_inventory_outstanding": "Days Inventory Outstanding",
    "supplier_quality_rate": "Supplier Quality Rate (%)"
}

def analyze_kpis(kpi_data, benchmarks):
    results = {}
    for kpi, value in kpi_data.items():
        benchmark = benchmarks[kpi]
        if kpi in ["supplier_otd", "inventory_turnover",
                   "order_fulfillment_rate", "forecast_accuracy",
                   "supplier_quality_rate"]:
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

def show_supply_chain(industry):
    benchmarks = supply_chain_benchmarks[industry]

    st.sidebar.title("Enter Your Supply Chain KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    supplier_otd = st.sidebar.slider("Supplier On Time Delivery (%)", 0, 100, 82)
    inventory_turnover = st.sidebar.slider("Inventory Turnover (times/year)", 0, 30, 6)
    order_fulfillment_rate = st.sidebar.slider("Order Fulfillment Rate (%)", 0, 100, 88)
    forecast_accuracy = st.sidebar.slider("Demand Forecast Accuracy (%)", 0, 100, 70)
    supply_chain_cost = st.sidebar.slider("Supply Chain Cost (% of Revenue)", 0, 30, 15)
    days_inventory_outstanding = st.sidebar.slider("Days Inventory Outstanding", 0, 120, 55)
    supplier_quality_rate = st.sidebar.slider("Supplier Quality Rate (%)", 0, 100, 90)

    kpi_data = {
        "supplier_otd": supplier_otd,
        "inventory_turnover": inventory_turnover,
        "order_fulfillment_rate": order_fulfillment_rate,
        "forecast_accuracy": forecast_accuracy,
        "supply_chain_cost": supply_chain_cost,
        "days_inventory_outstanding": days_inventory_outstanding,
        "supplier_quality_rate": supplier_quality_rate
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

    if analysis["supplier_otd"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low supplier on time delivery: Possible supplier capacity issues, poor communication, or logistics delays")
        recommendations.append("Implement supplier scorecards and develop backup suppliers for critical components")

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low inventory turnover: Possible overstocking, poor demand forecasting, or slow moving items")
        recommendations.append("Review reorder points and implement demand driven replenishment strategies")

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low order fulfillment: Possible stockouts, supplier delays, or poor inventory visibility")
        recommendations.append("Implement real time inventory visibility across the supply chain")

    if analysis["forecast_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low forecast accuracy: Possible poor data quality, market volatility, or inadequate forecasting tools")
        recommendations.append("Adopt statistical forecasting methods and collaborate with customers on demand planning")

    if analysis["supply_chain_cost"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High supply chain cost: Possible inefficient transportation, high inventory holding costs, or poor supplier pricing")
        recommendations.append("Conduct total cost analysis and negotiate better terms with key suppliers")

    if analysis["days_inventory_outstanding"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High days inventory outstanding: Possible overstocking, slow moving items, or poor inventory management")
        recommendations.append("Implement ABC analysis to prioritize inventory management and reduce excess stock")

    if analysis["supplier_quality_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low supplier quality rate: Possible inadequate supplier quality controls or lack of audits")
        recommendations.append("Conduct regular supplier quality audits and implement incoming quality inspection")

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
            st.success("Supply chain is performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("🔮 What-If Simulator")
    st.write("Adjust the sliders below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        otd_improvement = st.slider("Improve Supplier OTD by (%)", 0, 10, 0)
        turnover_improvement = st.slider("Improve Inventory Turnover by (times)", 0, 10, 0)
        fulfillment_improvement = st.slider("Improve Order Fulfillment by (%)", 0, 10, 0)

    with col2:
        forecast_improvement = st.slider("Improve Forecast Accuracy by (%)", 0, 20, 0)
        cost_improvement = st.slider("Reduce Supply Chain Cost by (%)", 0, 10, 0)
        dio_improvement = st.slider("Reduce Days Inventory by (days)", 0, 30, 0)

    st.subheader("Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Supplier OTD", f"{supplier_otd + otd_improvement}%", f"+{otd_improvement}%")
        st.metric("Inventory Turnover", f"{inventory_turnover + turnover_improvement} times", f"+{turnover_improvement}")

    with col2:
        st.metric("Order Fulfillment", f"{order_fulfillment_rate + fulfillment_improvement}%", f"+{fulfillment_improvement}%")
        st.metric("Forecast Accuracy", f"{forecast_accuracy + forecast_improvement}%", f"+{forecast_improvement}%")

    with col3:
        st.metric("Supply Chain Cost", f"{supply_chain_cost - cost_improvement}%", f"-{cost_improvement}%")
        st.metric("Days Inventory", f"{days_inventory_outstanding - dio_improvement} days", f"-{dio_improvement}")

    st.divider()

    # ROI Calculator
    st.header("💰 ROI Projection Calculator")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input("Annual Revenue ($)", min_value=0, value=5000000, step=100000)
        inventory_holding_cost = st.number_input("Annual Inventory Holding Cost ($)", min_value=0, value=200000, step=10000)

    with col2:
        supplier_defect_cost = st.number_input("Annual Supplier Defect Cost ($)", min_value=0, value=100000, step=10000)
        logistics_cost = st.number_input("Annual Logistics Cost ($)", min_value=0, value=300000, step=10000)

    cost_reduction_savings = annual_revenue * (cost_improvement / 100)
    inventory_savings = inventory_holding_cost * (dio_improvement / days_inventory_outstanding) if days_inventory_outstanding > 0 else 0
    quality_savings = supplier_defect_cost * (forecast_improvement / 100)
    total_savings = cost_reduction_savings + inventory_savings + quality_savings

    st.subheader("Projected Annual Savings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Supply Chain Cost Savings", f"${cost_reduction_savings:,.0f}")
        st.metric("Inventory Savings", f"${inventory_savings:,.0f}")

    with col2:
        st.metric("Quality Savings", f"${quality_savings:,.0f}")

    with col3:
        st.metric("💰 Total Annual Savings", f"${total_savings:,.0f}", delta=f"+${total_savings:,.0f}")