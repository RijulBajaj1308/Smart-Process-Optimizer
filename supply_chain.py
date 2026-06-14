import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Supply Chain
# Sources:
# Automotive Supply Chain: Tata Motors, Maruti Suzuki, Mahindra supplier standards
# Food and Beverage Supply Chain: HUL, Nestle India, ITC FMCG supply chain standards
# Electronics Supply Chain: Dixon Technologies, Foxconn India, PLI scheme benchmarks
# General Supply Chain: APICS India chapter benchmarks, CII supply chain reports
# Pharmaceutical Supply Chain: FDA Green List initiative, CDSCO GDP guidelines, Dr Reddy's, Sun Pharma supply chain standards

supply_chain_benchmarks = {
    "Automotive Supply Chain": {
        "supplier_otd": 95.000,
        "inventory_turnover": 12.000,
        "order_fulfillment_rate": 97.000,
        "forecast_accuracy": 85.000,
        "supply_chain_cost": 8.000,
        "days_inventory_outstanding": 30.000,
        "supplier_quality_rate": 98.000,
        "lead_time_flexibility": 30.000,
        "sourcing_flexibility": 80.000
    },
    "Food and Beverage Supply Chain": {
        "supplier_otd": 97.000,
        "inventory_turnover": 20.000,
        "order_fulfillment_rate": 98.000,
        "forecast_accuracy": 80.000,
        "supply_chain_cost": 6.000,
        "days_inventory_outstanding": 15.000,
        "supplier_quality_rate": 99.000,
        "lead_time_flexibility": 25.000,
        "sourcing_flexibility": 75.000
    },
    "Electronics Supply Chain": {
        "supplier_otd": 93.000,
        "inventory_turnover": 15.000,
        "order_fulfillment_rate": 96.000,
        "forecast_accuracy": 82.000,
        "supply_chain_cost": 10.000,
        "days_inventory_outstanding": 25.000,
        "supplier_quality_rate": 97.000,
        "lead_time_flexibility": 20.000,
        "sourcing_flexibility": 70.000
    },
    "General Supply Chain": {
        "supplier_otd": 90.000,
        "inventory_turnover": 8.000,
        "order_fulfillment_rate": 93.000,
        "forecast_accuracy": 75.000,
        "supply_chain_cost": 12.000,
        "days_inventory_outstanding": 45.000,
        "supplier_quality_rate": 95.000,
        "lead_time_flexibility": 20.000,
        "sourcing_flexibility": 60.000
    },
    "Pharmaceutical Supply Chain": {
        # Based on FDA Green List initiative, CDSCO GDP guidelines
        # Dr Reddy's, Sun Pharma, Cipla supply chain standards
        # Dual sourcing requirement for critical APIs
        "supplier_otd": 97.000,
        "inventory_turnover": 18.000,
        "order_fulfillment_rate": 99.000,
        "forecast_accuracy": 88.000,
        "supply_chain_cost": 5.000,
        "days_inventory_outstanding": 20.000,
        "supplier_quality_rate": 99.500,
        "lead_time_flexibility": 15.000,
        "sourcing_flexibility": 90.000
    }
}

kpi_labels = {
    "supplier_otd": "Supplier On Time Delivery (%)",
    "inventory_turnover": "Inventory Turnover (times/year)",
    "order_fulfillment_rate": "Order Fulfillment Rate (%)",
    "forecast_accuracy": "Demand Forecast Accuracy (%)",
    "supply_chain_cost": "Supply Chain Cost (% of Revenue)",
    "days_inventory_outstanding": "Days Inventory Outstanding",
    "supplier_quality_rate": "Supplier Quality Rate (%)",
    "lead_time_flexibility": "Lead Time Flexibility (%)",
    "sourcing_flexibility": "Sourcing Flexibility (%)"
}

def analyze_kpis(kpi_data, benchmarks):
    results = {}
    for kpi, value in kpi_data.items():
        benchmark = benchmarks[kpi]
        if kpi in ["supplier_otd", "inventory_turnover", "order_fulfillment_rate",
                   "forecast_accuracy", "supplier_quality_rate",
                   "lead_time_flexibility", "sourcing_flexibility"]:
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

def show_supply_chain(industry, currency_symbol="$"):
    benchmarks = supply_chain_benchmarks[industry]

    st.sidebar.title("Enter Your Supply Chain KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    supplier_otd = st.sidebar.number_input("Supplier On Time Delivery (%)", min_value=0.000, max_value=100.000, value=82.000, step=0.001, format="%.3f")
    inventory_turnover = st.sidebar.number_input("Inventory Turnover (times/year)", min_value=0.000, max_value=30.000, value=6.000, step=0.001, format="%.3f")
    order_fulfillment_rate = st.sidebar.number_input("Order Fulfillment Rate (%)", min_value=0.000, max_value=100.000, value=88.000, step=0.001, format="%.3f")
    forecast_accuracy = st.sidebar.number_input("Demand Forecast Accuracy (%)", min_value=0.000, max_value=100.000, value=70.000, step=0.001, format="%.3f")
    supply_chain_cost = st.sidebar.number_input("Supply Chain Cost (% of Revenue)", min_value=0.000, max_value=30.000, value=15.000, step=0.001, format="%.3f")
    days_inventory_outstanding = st.sidebar.number_input("Days Inventory Outstanding", min_value=0.000, max_value=120.000, value=55.000, step=0.001, format="%.3f")
    supplier_quality_rate = st.sidebar.number_input("Supplier Quality Rate (%)", min_value=0.000, max_value=100.000, value=90.000, step=0.001, format="%.3f")
    lead_time_flexibility = st.sidebar.number_input("Lead Time Flexibility (%)", min_value=0.000, max_value=100.000, value=15.000, step=0.001, format="%.3f")
    sourcing_flexibility = st.sidebar.number_input("Sourcing Flexibility (%)", min_value=0.000, max_value=100.000, value=50.000, step=0.001, format="%.3f")

    kpi_data = {
        "supplier_otd": supplier_otd,
        "inventory_turnover": inventory_turnover,
        "order_fulfillment_rate": order_fulfillment_rate,
        "forecast_accuracy": forecast_accuracy,
        "supply_chain_cost": supply_chain_cost,
        "days_inventory_outstanding": days_inventory_outstanding,
        "supplier_quality_rate": supplier_quality_rate,
        "lead_time_flexibility": lead_time_flexibility,
        "sourcing_flexibility": sourcing_flexibility
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
    st.header("Overall Supply Chain Risk Assessment")

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

    if analysis["supplier_otd"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low supplier on time delivery: Possible supplier capacity issues, poor communication, or logistics delays")
        recommendations.append("Implement supplier scorecards and develop backup suppliers for critical components")
        improvements["supplier_otd"] = min(benchmarks["supplier_otd"], supplier_otd + 5)

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low inventory turnover: Possible overstocking, poor demand forecasting, or slow moving items")
        recommendations.append("Review reorder points and implement demand driven replenishment strategies")
        improvements["inventory_turnover"] = min(benchmarks["inventory_turnover"], inventory_turnover + 3)

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low order fulfillment: Possible stockouts, supplier delays, or poor inventory visibility")
        recommendations.append("Implement real time inventory visibility across the supply chain")
        improvements["order_fulfillment_rate"] = min(benchmarks["order_fulfillment_rate"], order_fulfillment_rate + 5)

    if analysis["forecast_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low forecast accuracy: Possible poor data quality, market volatility, or inadequate forecasting tools")
        recommendations.append("Adopt statistical forecasting methods and collaborate with customers on demand planning")
        improvements["forecast_accuracy"] = min(benchmarks["forecast_accuracy"], forecast_accuracy + 8)

    if analysis["supply_chain_cost"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High supply chain cost: Possible inefficient transportation, high inventory holding costs, or poor supplier pricing")
        recommendations.append("Conduct total cost analysis and negotiate better terms with key suppliers")
        improvements["supply_chain_cost"] = max(benchmarks["supply_chain_cost"], supply_chain_cost - 3)

    if analysis["days_inventory_outstanding"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("High days inventory outstanding: Possible overstocking, slow moving items, or poor inventory management")
        recommendations.append("Implement ABC analysis to prioritize inventory management and reduce excess stock")
        improvements["days_inventory_outstanding"] = max(benchmarks["days_inventory_outstanding"], days_inventory_outstanding - 10)

    if analysis["supplier_quality_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low supplier quality rate: Possible inadequate supplier quality controls or lack of audits")
        recommendations.append("Conduct regular supplier quality audits and implement incoming quality inspection")
        improvements["supplier_quality_rate"] = min(benchmarks["supplier_quality_rate"], supplier_quality_rate + 3)

    if analysis["lead_time_flexibility"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low lead time flexibility: Heavy reliance on single transportation mode or single supplier with no expedite options")
        recommendations.append("Develop expedite agreements with key suppliers and diversify transportation modes")
        improvements["lead_time_flexibility"] = min(benchmarks["lead_time_flexibility"], lead_time_flexibility + 8)

    if analysis["sourcing_flexibility"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append("Low sourcing flexibility: High single source dependency creating supply disruption risk")
        recommendations.append("Identify critical single source components and qualify at least one backup supplier for each")
        improvements["sourcing_flexibility"] = min(benchmarks["sourcing_flexibility"], sourcing_flexibility + 10)

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
    st.write("If you implement all recommendations here is what your supply chain could look like:")

    if improvements:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, (kpi, projected) in enumerate(improvements.items()):
            col = cols[i % 3]
            current = kpi_data[kpi]
            with col:
                if kpi in ["supplier_otd", "inventory_turnover", "order_fulfillment_rate",
                           "forecast_accuracy", "supplier_quality_rate",
                           "lead_time_flexibility", "sourcing_flexibility"]:
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
        st.success("Your supply chain is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("What-If Simulator")
    st.write("Adjust the values below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        otd_improvement = st.number_input("Improve Supplier OTD by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        turnover_improvement = st.number_input("Improve Inventory Turnover by (times)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        fulfillment_improvement = st.number_input("Improve Order Fulfillment by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        flexibility_improvement = st.number_input("Improve Lead Time Flexibility by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        forecast_improvement = st.number_input("Improve Forecast Accuracy by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")
        cost_improvement = st.number_input("Reduce Supply Chain Cost by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        dio_improvement = st.number_input("Reduce Days Inventory by (days)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        sourcing_improvement = st.number_input("Improve Sourcing Flexibility by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Supplier OTD", f"{supplier_otd + otd_improvement:.3f}%", f"+{otd_improvement:.3f}%")
        st.metric("Inventory Turnover", f"{inventory_turnover + turnover_improvement:.3f} times", f"+{turnover_improvement:.3f}")
        st.metric("Lead Time Flexibility", f"{lead_time_flexibility + flexibility_improvement:.3f}%", f"+{flexibility_improvement:.3f}%")

    with col2:
        st.metric("Order Fulfillment", f"{order_fulfillment_rate + fulfillment_improvement:.3f}%", f"+{fulfillment_improvement:.3f}%")
        st.metric("Forecast Accuracy", f"{forecast_accuracy + forecast_improvement:.3f}%", f"+{forecast_improvement:.3f}%")
        st.metric("Sourcing Flexibility", f"{sourcing_flexibility + sourcing_improvement:.3f}%", f"+{sourcing_improvement:.3f}%")

    with col3:
        st.metric("Supply Chain Cost", f"{supply_chain_cost - cost_improvement:.3f}%", f"-{cost_improvement:.3f}%")
        st.metric("Days Inventory", f"{days_inventory_outstanding - dio_improvement:.3f} days", f"-{dio_improvement:.3f}")

    st.divider()

    # ROI Calculator
    st.header("ROI Projection Calculator")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input(f"Annual Revenue ({currency_symbol})", min_value=0.000, value=5000000.000, step=1000.000, format="%.3f")
        inventory_holding_cost = st.number_input(f"Annual Inventory Holding Cost ({currency_symbol})", min_value=0.000, value=200000.000, step=1000.000, format="%.3f")

    with col2:
        supplier_defect_cost = st.number_input(f"Annual Supplier Defect Cost ({currency_symbol})", min_value=0.000, value=100000.000, step=1000.000, format="%.3f")
        logistics_cost = st.number_input(f"Annual Logistics Cost ({currency_symbol})", min_value=0.000, value=300000.000, step=1000.000, format="%.3f")

    cost_reduction_savings = annual_revenue * (cost_improvement / 100)
    inventory_savings = inventory_holding_cost * (dio_improvement / days_inventory_outstanding) if days_inventory_outstanding > 0 else 0
    quality_savings = supplier_defect_cost * (forecast_improvement / 100)
    total_savings = cost_reduction_savings + inventory_savings + quality_savings

    st.subheader("Projected Annual Savings")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Supply Chain Cost Savings", f"{currency_symbol}{cost_reduction_savings:,.3f}")
        st.metric("Inventory Savings", f"{currency_symbol}{inventory_savings:,.3f}")

    with col2:
        st.metric("Quality Savings", f"{currency_symbol}{quality_savings:,.3f}")

    with col3:
        st.metric("Total Annual Savings", f"{currency_symbol}{total_savings:,.3f}", delta=f"+{currency_symbol}{total_savings:,.0f}")