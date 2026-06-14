import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Distribution
# Sources:
# Warehouse and Distribution: Delhivery, Blue Dart, WERC benchmarking study 2025
# Cold Chain Distribution: Snowman Logistics, Cold Star standards
# E-commerce Fulfillment: Flipkart, Amazon India, Meesho standards
# Pharmaceutical Distribution: GDP compliance standards, CDSCO guidelines, Medplus, Apollo Pharmacy standards

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
        # Based on GDP compliance standards, CDSCO guidelines
        # Medplus, Apollo Pharmacy, Mahindra Logistics Pharma standards
        "order_fulfillment_rate": 99.000,
        "on_time_delivery": 98.000,
        "warehouse_utilization": 75.000,
        "picking_accuracy": 99.990,
        "inventory_turnover": 24.000,
        "return_rate": 0.500,
        "cost_per_order": 120.000
    }
}

kpi_labels = {
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

def show_distribution(industry, currency_symbol="$"):
    benchmarks = distribution_benchmarks[industry]

    st.sidebar.title("Enter Your Distribution KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    order_fulfillment_rate = st.sidebar.number_input("Order Fulfillment Rate (%)", min_value=0.000, max_value=100.000, value=88.000, step=0.001, format="%.3f")
    on_time_delivery = st.sidebar.number_input("On Time Delivery (%)", min_value=0.000, max_value=100.000, value=85.000, step=0.001, format="%.3f")
    warehouse_utilization = st.sidebar.number_input("Warehouse Utilization (%)", min_value=0.000, max_value=100.000, value=75.000, step=0.001, format="%.3f")
    picking_accuracy = st.sidebar.number_input("Picking Accuracy (%)", min_value=90.000, max_value=100.000, value=95.000, step=0.001, format="%.3f")
    inventory_turnover = st.sidebar.number_input("Inventory Turnover (times/year)", min_value=0.000, max_value=30.000, value=8.000, step=0.001, format="%.3f")
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

    # KPI Cards
    st.header("KPI Analysis")
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
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{status_icons[result['status']]} {kpi_labels[kpi]}</p>
                    <p style="color: {color}; font-size: 2rem; font-weight: 800; margin: 5px 0;">{result['value']:.3f}</p>
                    <p style="color: #888888; font-size: 0.8rem; margin: 0;">Benchmark: {result['benchmark']:.3f}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Risk Assessment Dashboard
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

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low order fulfillment: Possible stockouts, poor inventory management, or picking errors")
        recommendations.append("Implement real time inventory tracking and set reorder points to prevent stockouts")
        improvements["order_fulfillment_rate"] = min(benchmarks["order_fulfillment_rate"], order_fulfillment_rate + 5)

    if analysis["on_time_delivery"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low on time delivery: Possible routing inefficiencies, traffic delays, or poor scheduling")
        recommendations.append("Optimize delivery routes using route planning software and implement real time tracking")
        improvements["on_time_delivery"] = min(benchmarks["on_time_delivery"], on_time_delivery + 5)

    if analysis["warehouse_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low warehouse utilization: Possible poor layout, dead stock, or inefficient storage")
        recommendations.append("Conduct a warehouse layout analysis and implement vertical storage solutions")
        improvements["warehouse_utilization"] = min(benchmarks["warehouse_utilization"], warehouse_utilization + 8)

    if analysis["picking_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low picking accuracy: Possible manual errors, poor labeling, or inadequate training")
        recommendations.append("Implement barcode scanning or RFID systems to reduce picking errors")
        improvements["picking_accuracy"] = min(benchmarks["picking_accuracy"], picking_accuracy + 2)

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low inventory turnover: Possible overstocking, poor demand forecasting, or slow moving items")
        recommendations.append("Review demand forecasting methods and identify slow moving SKUs for clearance")
        improvements["inventory_turnover"] = min(benchmarks["inventory_turnover"], inventory_turnover + 3)

    if analysis["return_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High return rate: Possible product quality issues, wrong items shipped, or damaged goods")
        recommendations.append("Implement quality checks before dispatch and improve packaging to reduce damage")
        improvements["return_rate"] = max(benchmarks["return_rate"], return_rate - 2)

    if analysis["cost_per_order"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High cost per order: Possible inefficient processes, high labor costs, or poor route planning")
        recommendations.append("Identify and eliminate non value adding steps in the order fulfillment process")
        improvements["cost_per_order"] = max(benchmarks["cost_per_order"], cost_per_order - 10)

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
    st.write("If you implement all recommendations here is what your distribution could look like:")

    if improvements:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, (kpi, projected) in enumerate(improvements.items()):
            col = cols[i % 3]
            current = kpi_data[kpi]
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
                        <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{kpi_labels[kpi]}</p>
                        <p style="color: #CC0000; font-size: 1.2rem; margin: 5px 0;">Before: {current:.3f}</p>
                        <p style="color: #00CC00; font-size: 1.2rem; margin: 5px 0;">After: {projected:.3f}</p>
                        <p style="color: #00CC00; font-size: 1rem; font-weight: 800; margin: 0;">{change_str} improvement</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Your distribution is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("What-If Simulator")
    st.write("Adjust the values below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        fulfillment_improvement = st.number_input("Improve Order Fulfillment Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        delivery_improvement = st.number_input("Improve On Time Delivery by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        utilization_improvement = st.number_input("Improve Warehouse Utilization by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        accuracy_improvement = st.number_input("Improve Picking Accuracy by (%)", min_value=0.000, max_value=5.000, value=0.000, step=0.001, format="%.3f")
        return_improvement = st.number_input("Reduce Return Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        cost_improvement = st.number_input(f"Reduce Cost per Order by ({currency_symbol})", min_value=0.000, max_value=50.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Projected Results")
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

    # ROI Calculator
    st.header("ROI Projection Calculator")
    col1, col2 = st.columns(2)

    with col1:
        monthly_orders = st.number_input("Monthly Orders", min_value=0, value=10000, step=1)
        avg_order_value = st.number_input(f"Average Order Value ({currency_symbol})", min_value=0.000, value=100.000, step=0.001, format="%.3f")

    with col2:
        return_cost = st.number_input(f"Cost per Return ({currency_symbol})", min_value=0.000, value=20.000, step=0.001, format="%.3f")
        labor_cost = st.number_input(f"Monthly Labor Cost ({currency_symbol})", min_value=0.000, value=50000.000, step=0.001, format="%.3f")

    fulfillment_savings = monthly_orders * avg_order_value * (fulfillment_improvement / 100) * 12
    return_savings = monthly_orders * (return_improvement / 100) * return_cost * 12
    cost_savings = monthly_orders * cost_improvement * 12
    total_savings = fulfillment_savings + return_savings + cost_savings

    st.subheader("Projected Annual Savings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fulfillment Savings", f"{currency_symbol}{fulfillment_savings:,.3f}")
        st.metric("Return Savings", f"{currency_symbol}{return_savings:,.3f}")

    with col2:
        st.metric("Cost per Order Savings", f"{currency_symbol}{cost_savings:,.3f}")

    with col3:
        st.metric("Total Annual Savings", f"{currency_symbol}{total_savings:,.3f}", delta=f"+{currency_symbol}{total_savings:,.3f}")