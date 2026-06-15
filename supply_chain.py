# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go

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
        "supplier_otd": 97.000,
        "inventory_turnover": 18.000,
        "order_fulfillment_rate": 99.000,
        "forecast_accuracy": 88.000,
        "supply_chain_cost": 5.000,
        "days_inventory_outstanding": 20.000,
        "supplier_quality_rate": 99.500,
        "lead_time_flexibility": 15.000,
        "sourcing_flexibility": 90.000
    },
    "Textile and Apparel Supply Chain": {
        "supplier_otd": 88.000,
        "inventory_turnover": 4.000,
        "order_fulfillment_rate": 92.000,
        "forecast_accuracy": 65.000,
        "supply_chain_cost": 14.000,
        "days_inventory_outstanding": 60.000,
        "supplier_quality_rate": 93.000,
        "lead_time_flexibility": 15.000,
        "sourcing_flexibility": 55.000
    },
    "Eco Friendly Packaging Supply Chain": {
        "supplier_otd": 90.000,
        "inventory_turnover": 8.000,
        "order_fulfillment_rate": 93.000,
        "forecast_accuracy": 75.000,
        "supply_chain_cost": 11.000,
        "days_inventory_outstanding": 40.000,
        "supplier_quality_rate": 95.000,
        "lead_time_flexibility": 20.000,
        "sourcing_flexibility": 60.000
    },
    "Pulp and Paper Supply Chain": {
        "supplier_otd": 88.000,
        "inventory_turnover": 6.000,
        "order_fulfillment_rate": 91.000,
        "forecast_accuracy": 72.000,
        "supply_chain_cost": 13.000,
        "days_inventory_outstanding": 50.000,
        "supplier_quality_rate": 94.000,
        "lead_time_flexibility": 18.000,
        "sourcing_flexibility": 55.000
    }
}

performance_labels = {
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

def generate_dynamic_insights(kpi, value, benchmark, gap, status):
    if kpi == "supplier_otd":
        if status == "Critical":
            cause = f"Your suppliers are only delivering on time {value:.3f}% of the time against a benchmark of {benchmark:.3f}%. That means {gap:.1f} out of every 100 deliveries are late. Late supplier deliveries cascade into your own production delays and customer failures."
            rec = f"At {value:.3f}% supplier OTD you need to act now. Start by identifying your worst performing suppliers and have direct conversations with them about their capacity and planning. Develop at least one backup supplier for your top 3 most critical materials."
        else:
            cause = f"Your supplier on time delivery of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. Most suppliers are reliable but a few are causing delays that ripple through your supply chain."
            rec = f"A {gap:.3f}% OTD gap is manageable. Identify which specific suppliers are causing the delays and address them directly. Implement supplier scorecards so performance is tracked and visible."

    elif kpi == "inventory_turnover":
        if status == "Critical":
            cause = f"Your inventory only turns {value:.3f} times per year against a benchmark of {benchmark:.3f}. Your stock is sitting for far too long. Capital is locked up in slow moving inventory that is costing you money every day it sits in your warehouse."
            rec = f"At {value:.3f} turns you have a serious inventory problem. Run a full stock analysis this week — identify which items have not moved in 60 days or more. Those are your problem items. Either stop reordering them or clear the existing stock through promotions or redistribution."
        else:
            cause = f"Your inventory turns {value:.3f} times per year which is {gap:.3f} turns below the {benchmark:.3f} benchmark. Stock is moving slower than it should and capital is being tied up unnecessarily."
            rec = f"Closing a {gap:.3f} turn gap means better alignment between purchasing and actual demand. Review your reorder quantities and frequency for your slowest moving items to free up working capital."

    elif kpi == "order_fulfillment_rate":
        if status == "Critical":
            cause = f"Your order fulfillment rate of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. For every 100 orders your customers place, more than {gap:.1f} are not being fulfilled. That is lost revenue and damaged customer relationships."
            rec = f"At {value:.3f}% fulfillment this is urgent. Are stockouts the main cause or are supplier delays stopping you from fulfilling? Identify the root cause first then fix either your inventory levels or your supplier reliability depending on the answer."
        else:
            cause = f"Your order fulfillment rate is {gap:.3f}% below benchmark. You are almost there but a small number of orders are still falling through."
            rec = f"A {gap:.3f}% fulfillment gap is close to closing. Identify the specific SKUs or suppliers causing the shortfall and address those specifically rather than making broad changes."

    elif kpi == "forecast_accuracy":
        if status == "Critical":
            cause = f"Your demand forecast accuracy of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. You are getting your demand predictions wrong by a significant margin. This leads to either excess inventory when you over-forecast or stockouts when you under-forecast."
            rec = f"At {value:.3f}% forecast accuracy your planning process needs an overhaul. Start using your historical sales data to build statistical forecasts rather than relying on gut feel or simple averages. Even basic trend analysis will significantly improve your accuracy."
        else:
            cause = f"Your forecast accuracy of {value:.3f}% is {gap:.3f}% below benchmark. Your predictions are reasonable but the gap is costing you in excess inventory or missed sales."
            rec = f"Closing a {gap:.3f}% forecast accuracy gap requires reviewing your forecasting methodology. Are you accounting for seasonality and promotions in your forecasts? Those two factors alone can close this gap for most businesses."

    elif kpi == "supply_chain_cost":
        if status == "Critical":
            cause = f"Your supply chain costs are {gap:.3f}% of revenue above the benchmark of {benchmark:.3f}%. You are spending significantly more on your supply chain than industry leaders. This is directly reducing your profitability on every unit you sell."
            rec = f"At {value:.3f}% of revenue in supply chain costs you need to identify your biggest cost drivers immediately. Is it transportation, inventory holding, or supplier pricing? Once you know where the money is going you can target the biggest savings opportunity."
        else:
            cause = f"Your supply chain costs are {gap:.3f}% above benchmark as a percentage of revenue. You are slightly more expensive to operate than industry leaders."
            rec = f"A {gap:.3f}% cost reduction as a percentage of revenue is achievable. Look at transport consolidation, better supplier terms and inventory reduction as your three levers."

    elif kpi == "days_inventory_outstanding":
        if status == "Critical":
            cause = f"You are holding {value:.3f} days of inventory against a benchmark of {benchmark:.3f} days. Your stock is sitting for {gap:.1f} more days than it should be. Every extra day of inventory is cash that could be working elsewhere in your business."
            rec = f"At {value:.3f} days of inventory you have a significant cash flow opportunity. Map which product categories are driving the high DIO and implement tighter reorder discipline for those categories specifically."
        else:
            cause = f"Your days inventory outstanding of {value:.3f} days is {gap:.3f} days above the {benchmark:.3f} day benchmark. You are holding slightly more stock than you need to."
            rec = f"Reducing your DIO by {gap:.3f} days would free up meaningful working capital. Review your safety stock levels — they may be higher than necessary given your actual supply variability."

    elif kpi == "supplier_quality_rate":
        if status == "Critical":
            cause = f"Your supplier quality rate of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. Suppliers are sending you substandard materials at an unacceptable rate. This is causing rework, waste and potentially reaching your end customers."
            rec = f"At {value:.3f}% supplier quality rate you need to implement incoming inspection immediately for your highest risk suppliers. Then have formal quality review meetings with those suppliers to understand why defects are occurring and what they are doing to fix it."
        else:
            cause = f"Your supplier quality rate of {value:.3f}% is {gap:.3f}% below benchmark. Most supplier materials are acceptable but a small percentage of quality failures are creating unnecessary cost."
            rec = f"A {gap:.3f}% supplier quality gap is manageable. Identify which specific suppliers are causing the quality failures and implement corrective action requests with clear timelines for improvement."

    elif kpi == "lead_time_flexibility":
        if status == "Critical":
            cause = f"Your supply chain can only flex its lead time by {value:.3f}% when you need urgent delivery, against a benchmark of {benchmark:.3f}%. When you need materials faster than normal your supply chain cannot respond. This makes you vulnerable to stockouts during demand spikes."
            rec = f"At {value:.3f}% lead time flexibility you are too rigid. Negotiate expedite agreements with your top 5 suppliers now so you have a defined fast track option when you need it. Pay for the capacity reservation — it is worth it."
        else:
            cause = f"Your lead time flexibility of {value:.3f}% is {gap:.3f}% below benchmark. You can flex your supply chain somewhat but not as much as industry leaders."
            rec = f"Improving lead time flexibility by {gap:.3f}% requires developing better relationships with your key suppliers so they prioritize your urgent orders when needed."

    elif kpi == "sourcing_flexibility":
        if status == "Critical":
            cause = f"Only {value:.3f}% of your critical materials have backup suppliers against a benchmark of {benchmark:.3f}%. You have significant single source dependency risk. If any of those single source suppliers fails to deliver you have no alternative and your production stops."
            rec = f"At {value:.3f}% sourcing flexibility you are dangerously exposed to supply disruption. Identify your top 10 single source materials and start qualifying alternate suppliers for them immediately. Even having one approved backup changes your risk profile significantly."
        else:
            cause = f"Your sourcing flexibility of {value:.3f}% is {gap:.3f}% below benchmark. You have backup suppliers for most critical materials but some gaps remain."
            rec = f"Closing a {gap:.3f}% sourcing flexibility gap means qualifying backup suppliers for your remaining single source materials. Prioritize by spend and criticality to production."

    else:
        cause = f"This metric is {gap:.3f} units away from the industry benchmark of {benchmark:.3f}. This gap is affecting your overall supply chain performance."
        rec = f"Focus on understanding why this metric is {gap:.3f} units below benchmark and develop a specific action plan to close the gap within the next 30 days."

    return cause, rec

def show_supply_chain(industry, currency_symbol="$"):
    benchmarks = supply_chain_benchmarks[industry]

    st.sidebar.title("Enter Your Performance Numbers")
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

    # Performance Cards
    st.header("Performance Analysis")
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
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{status_icons[result['status']]} {performance_labels[kpi]}</p>
                    <p style="color: {color}; font-size: 2rem; font-weight: 800; margin: 5px 0;">{result['value']:.3f}</p>
                    <p style="color: #888888; font-size: 0.8rem; margin: 0;">Benchmark: {result['benchmark']:.3f}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Risk Assessment
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
    st.caption(f"Analysis based on your actual numbers compared to {industry} benchmark")

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

            if kpi in ["supplier_otd", "inventory_turnover", "order_fulfillment_rate",
                       "forecast_accuracy", "supplier_quality_rate",
                       "lead_time_flexibility", "sourcing_flexibility"]:
                improvements[kpi] = min(result["benchmark"], result["value"] + result["gap"] * 0.5)
            else:
                improvements[kpi] = max(result["benchmark"], result["value"] - result["gap"] * 0.5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What is happening in your supply chain?")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("Your supply chain is performing at or above benchmark level!")

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
                        <p style="color: #ffffff; font-size: 0.9rem; margin: 0;">{performance_labels[kpi]}</p>
                        <p style="color: #CC0000; font-size: 1.2rem; margin: 5px 0;">Now: {current:.3f}</p>
                        <p style="color: #00CC00; font-size: 1.2rem; margin: 5px 0;">After: {projected:.3f}</p>
                        <p style="color: #00CC00; font-size: 1rem; font-weight: 800; margin: 0;">{change_str} improvement</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Your supply chain is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("Play With the Numbers")
    st.write("Change the values below to see what happens to your results")
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

    st.subheader("Your Projected Results")
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

    # Money Saved Calculator
    st.header("How Much Money Could You Save?")
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