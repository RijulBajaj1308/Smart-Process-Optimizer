import streamlit as st
import plotly.graph_objects as go

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
        "order_fulfillment_rate": 99.000,
        "on_time_delivery": 98.000,
        "warehouse_utilization": 75.000,
        "picking_accuracy": 99.990,
        "inventory_turnover": 24.000,
        "return_rate": 0.500,
        "cost_per_order": 120.000
    },
    "Automotive Parts Distribution": {
        "order_fulfillment_rate": 96.000,
        "on_time_delivery": 94.000,
        "warehouse_utilization": 82.000,
        "picking_accuracy": 99.500,
        "inventory_turnover": 8.000,
        "return_rate": 1.500,
        "cost_per_order": 75.000
    },
    "Electronics Distribution": {
        "order_fulfillment_rate": 97.000,
        "on_time_delivery": 95.000,
        "warehouse_utilization": 85.000,
        "picking_accuracy": 99.800,
        "inventory_turnover": 10.000,
        "return_rate": 3.000,
        "cost_per_order": 60.000
    },
    "Food and Beverage Distribution": {
        "order_fulfillment_rate": 97.500,
        "on_time_delivery": 95.500,
        "warehouse_utilization": 88.000,
        "picking_accuracy": 99.700,
        "inventory_turnover": 26.000,
        "return_rate": 2.500,
        "cost_per_order": 35.000
    },
    "Textile and Apparel Distribution": {
        "order_fulfillment_rate": 94.000,
        "on_time_delivery": 91.000,
        "warehouse_utilization": 80.000,
        "picking_accuracy": 99.300,
        "inventory_turnover": 6.000,
        "return_rate": 12.000,
        "cost_per_order": 45.000
    },
    "Eco Friendly Packaging Distribution": {
        "order_fulfillment_rate": 95.000,
        "on_time_delivery": 93.000,
        "warehouse_utilization": 83.000,
        "picking_accuracy": 99.500,
        "inventory_turnover": 10.000,
        "return_rate": 2.000,
        "cost_per_order": 55.000
    },
    "Pulp and Paper Distribution": {
        "order_fulfillment_rate": 94.000,
        "on_time_delivery": 91.000,
        "warehouse_utilization": 80.000,
        "picking_accuracy": 99.200,
        "inventory_turnover": 8.000,
        "return_rate": 1.500,
        "cost_per_order": 65.000
    }
}

performance_labels = {
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

def generate_dynamic_insights(kpi, value, benchmark, gap, status):
    if kpi == "order_fulfillment_rate":
        if status == "Critical":
            cause = f"Your order fulfillment rate is {gap:.3f}% below the benchmark of {benchmark:.3f}%. This means for every 100 orders your customers place, more than {gap:.1f} of them are not being fulfilled. That is lost revenue and disappointed customers."
            rec = f"At {value:.3f}% fulfillment you are losing a significant number of orders. Check your stock availability first — are you running out of your top selling items? Fix your reorder triggers and get real time inventory visibility in place this week."
        else:
            cause = f"Your order fulfillment rate of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. You are almost there but a small number of orders are still not being fulfilled."
            rec = f"You are {gap:.3f}% away from benchmark. Identify which specific products are causing the unfulfilled orders and fix their reorder points. This is a small fix that could close the gap quickly."

    elif kpi == "on_time_delivery":
        if status == "Critical":
            cause = f"Your on time delivery rate of {value:.3f}% is {gap:.3f}% below the benchmark of {benchmark:.3f}%. More than {gap:.1f} in every 100 deliveries are arriving late. Late deliveries damage customer trust and can cost you repeat business."
            rec = f"At {value:.3f}% on time delivery you need to urgently review your delivery routes and schedules. Are your vehicles being loaded optimally? Are routes planned or ad hoc? Start with route optimization and you should see immediate improvement."
        else:
            cause = f"Your on time delivery rate is {gap:.3f}% below benchmark. Most deliveries are on time but a small percentage are consistently late."
            rec = f"A {gap:.3f}% gap in on time delivery is fixable. Look at which routes or customers are causing the late deliveries — often the problem is concentrated in specific areas or time slots."

    elif kpi == "warehouse_utilization":
        if status == "Critical":
            cause = f"Your warehouse is only {value:.3f}% utilized against a benchmark of {benchmark:.3f}%. You are paying for {gap:.1f}% more space than you are using. That is dead cost sitting in your P&L every month."
            rec = f"At {value:.3f}% utilization your warehouse layout needs a serious review. Start by identifying dead stock occupying space and relocate or clear it. Then look at whether you can use vertical space more effectively with additional racking."
        else:
            cause = f"Your warehouse utilization of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. You have unused capacity that is costing you money."
            rec = f"Closing a {gap:.3f}% utilization gap is achievable with better slotting. Move your fast moving items to easily accessible locations and use the freed up space more efficiently."

    elif kpi == "picking_accuracy":
        if status == "Critical":
            cause = f"Your picking accuracy of {value:.3f}% is {gap:.3f}% below the {benchmark:.3f}% benchmark. For every 1000 orders picked, approximately {gap*10:.0f} contain errors. Wrong items shipped means returns, customer complaints and rework costs."
            rec = f"At {value:.3f}% picking accuracy you need to implement scan and verify immediately. Manual picking without verification is the most common cause of this problem. Even basic barcode scanning at the pick point will dramatically improve your accuracy."
        else:
            cause = f"Your picking accuracy of {value:.3f}% is {gap:.3f}% below benchmark. You are very close but small picking errors are still slipping through."
            rec = f"A {gap:.3f}% accuracy gap at this level means your process is mostly working but needs tightening. Check if errors are concentrated in specific product areas or with specific pickers and address those specifically."

    elif kpi == "inventory_turnover":
        if status == "Critical":
            cause = f"Your inventory turns only {value:.3f} times per year against a benchmark of {benchmark:.3f}. Your stock is sitting for too long. Capital is tied up in slow moving inventory that is not generating returns."
            rec = f"At {value:.3f} turns you have a slow moving inventory problem. Run an ABC analysis this week to identify your slowest moving SKUs. Then either reduce their reorder quantities or run promotions to clear the excess stock."
        else:
            cause = f"Your inventory turns {value:.3f} times per year which is {gap:.3f} turns below the {benchmark:.3f} benchmark. Your stock is moving slower than it should be."
            rec = f"Closing a {gap:.3f} turn gap means better demand forecasting and tighter purchasing discipline. Align your purchasing more closely with actual sales velocity to stop over-ordering slow moving items."

    elif kpi == "return_rate":
        if status == "Critical":
            cause = f"Your return rate of {value:.3f}% is {gap:.3f}% above the {benchmark:.3f}% benchmark. You are processing significantly more returns than you should be. Every return costs you twice — once for the outbound delivery and once for the return handling."
            rec = f"At {value:.3f}% returns you need to understand why customers are sending things back. Are items damaged in transit? Are wrong items being sent? Are products not meeting expectations? The answer determines the fix."
        else:
            cause = f"Your return rate of {value:.3f}% is {gap:.3f}% above benchmark. Returns are slightly higher than they should be and each one is an unnecessary cost."
            rec = f"A {gap:.3f}% excess return rate is manageable. Check if returns are concentrated in specific product categories or customers. Often a small fix in packaging or product descriptions can make a meaningful difference."

    elif kpi == "cost_per_order":
        if status == "Critical":
            cause = f"Your cost per order is {gap:.3f} units above the benchmark. You are spending significantly more per order than industry leaders. This is eating into your margins on every single transaction."
            rec = f"At this cost per order level you need to look at your biggest cost drivers immediately. Is it labor, transport, packaging or returns processing? Identify the top two costs and target them specifically for reduction."
        else:
            cause = f"Your cost per order is {gap:.3f} units above the {benchmark:.3f} benchmark. You are slightly more expensive per order than you should be."
            rec = f"Closing a {gap:.3f} unit cost per order gap requires looking at where you can consolidate or streamline. Batching orders, optimizing routes or renegotiating courier rates are typically the fastest wins."

    else:
        cause = f"This metric is {gap:.3f} units away from the industry benchmark of {benchmark:.3f}. This gap is affecting your overall distribution performance."
        rec = f"Focus on understanding why this metric is {gap:.3f} units below benchmark and develop a specific action plan to close the gap within the next 30 days."

    return cause, rec

def show_distribution(industry, currency_symbol="$"):
    benchmarks = distribution_benchmarks[industry]

    st.sidebar.title("Enter Your Performance Numbers")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} (India)")

    order_fulfillment_rate = st.sidebar.number_input("Order Fulfillment Rate (%)", min_value=0.000, max_value=100.000, value=88.000, step=0.001, format="%.3f")
    on_time_delivery = st.sidebar.number_input("On Time Delivery (%)", min_value=0.000, max_value=100.000, value=85.000, step=0.001, format="%.3f")
    warehouse_utilization = st.sidebar.number_input("Warehouse Utilization (%)", min_value=0.000, max_value=100.000, value=75.000, step=0.001, format="%.3f")
    picking_accuracy = st.sidebar.number_input("Picking Accuracy (%)", min_value=90.000, max_value=100.000, value=95.000, step=0.001, format="%.3f")
    inventory_turnover = st.sidebar.number_input("Inventory Turnover (times/year)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
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

            if kpi in ["order_fulfillment_rate", "on_time_delivery",
                       "warehouse_utilization", "picking_accuracy", "inventory_turnover"]:
                improvements[kpi] = min(result["benchmark"], result["value"] + result["gap"] * 0.5)
            else:
                improvements[kpi] = max(result["benchmark"], result["value"] - result["gap"] * 0.5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What is happening in your distribution?")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("Your distribution is performing at or above benchmark level!")

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
                if kpi in ["order_fulfillment_rate", "on_time_delivery",
                           "warehouse_utilization", "picking_accuracy", "inventory_turnover"]:
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
        st.success("Your distribution is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("Play With the Numbers")
    st.write("Change the values below to see what happens to your results")
    col1, col2 = st.columns(2)

    with col1:
        fulfillment_improvement = st.number_input("Improve Order Fulfillment Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        delivery_improvement = st.number_input("Improve On Time Delivery by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        utilization_improvement = st.number_input("Improve Warehouse Utilization by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        accuracy_improvement = st.number_input("Improve Picking Accuracy by (%)", min_value=0.000, max_value=5.000, value=0.000, step=0.001, format="%.3f")
        return_improvement = st.number_input("Reduce Return Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")
        cost_improvement = st.number_input(f"Reduce Cost per Order by ({currency_symbol})", min_value=0.000, max_value=50.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Your Projected Results")
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

    # Money Saved Calculator
    st.header("How Much Money Could You Save?")
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