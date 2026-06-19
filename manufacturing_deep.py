# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def show_manufacturing_deep(industry, currency_symbol="$"):

    st.markdown("""
    <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.15); border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;">
        <p style="color: #E8001D; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 4px 0;">Deep Analysis Mode</p>
        <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">Enter detailed process data to pinpoint exactly where your problems are and by how much they are costing you.</p>
    </div>
    """, unsafe_allow_html=True)

    tool = st.selectbox(
        "Select a Deep Analysis Tool",
        [
            "Bottleneck Identifier",
            "OEE Calculator (Overall Equipment Effectiveness)",
            "Defect Pareto Analysis",
            "Manpower Planning Tool"
        ]
    )

    st.divider()

    # ════════════════════════════════════════
    # TOOL 1: BOTTLENECK IDENTIFIER
    # ════════════════════════════════════════
    if tool == "Bottleneck Identifier":
        st.header("Bottleneck Identifier")
        st.write("Enter your production stations and their cycle times. SPO will identify your bottleneck and tell you exactly how much it is costing you.")

        col1, col2 = st.columns(2)
        with col1:
            takt_time = st.number_input(
                "Takt Time (mins) — How often does a customer need one unit?",
                min_value=0.1, max_value=480.0, value=30.0, step=0.1, format="%.1f"
            )
            num_stations = st.number_input("Number of Stations", min_value=2, max_value=20, value=5, step=1)
            shifts_per_day = st.number_input("Shifts per Day", min_value=1, max_value=3, value=2, step=1)
            hours_per_shift = st.number_input("Hours per Shift", min_value=1.0, max_value=12.0, value=8.0, step=0.5)

        st.write("")
        st.subheader("Enter Station Data")

        stations = []
        cols = st.columns(3)
        for i in range(int(num_stations)):
            col = cols[i % 3]
            with col:
                name = st.text_input(f"Station {i+1} Name", value=f"Station {i+1}", key=f"sname_{i}")
                ct = st.number_input(f"Cycle Time (mins)", min_value=0.1, max_value=480.0, value=float(20 + i*5), step=0.1, format="%.1f", key=f"sct_{i}")
                stations.append({"name": name, "cycle_time": ct})

        if stations:
            st.divider()
            st.header("Bottleneck Analysis Results")

            bottleneck = max(stations, key=lambda x: x["cycle_time"])
            bottleneck_idx = stations.index(bottleneck)
            avg_ct = sum(s["cycle_time"] for s in stations) / len(stations)
            available_mins = shifts_per_day * hours_per_shift * 60
            current_output = available_mins / bottleneck["cycle_time"]
            ideal_output = available_mins / takt_time
            efficiency = (current_output / ideal_output) * 100 if ideal_output > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid #CC0000; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Bottleneck Station</p>
                    <p style="color: #CC0000; font-size: 1.4rem; font-weight: 900; margin: 8px 0;">{bottleneck['name']}</p>
                    <p style="color: #888; font-size: 0.8rem; margin: 0;">{bottleneck['cycle_time']:.1f} mins</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Current Output</p>
                    <p style="color: #FFD700; font-size: 1.4rem; font-weight: 900; margin: 8px 0;">{current_output:.0f}</p>
                    <p style="color: #888; font-size: 0.8rem; margin: 0;">units per day</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Target Output</p>
                    <p style="color: #00CC00; font-size: 1.4rem; font-weight: 900; margin: 8px 0;">{ideal_output:.0f}</p>
                    <p style="color: #888; font-size: 0.8rem; margin: 0;">units per day</p>
                </div>""", unsafe_allow_html=True)
            with col4:
                color = "#00CC00" if efficiency >= 85 else "#FFD700" if efficiency >= 70 else "#CC0000"
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {color}; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Line Efficiency</p>
                    <p style="color: {color}; font-size: 1.4rem; font-weight: 900; margin: 8px 0;">{efficiency:.1f}%</p>
                    <p style="color: #888; font-size: 0.8rem; margin: 0;">vs 85% benchmark</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            # Station chart
            station_names = [s["name"] for s in stations]
            cycle_times = [s["cycle_time"] for s in stations]
            colors_bar = ["#CC0000" if s["name"] == bottleneck["name"] else "#1a6b3c" for s in stations]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=station_names,
                y=cycle_times,
                marker_color=colors_bar,
                text=[f"{ct:.1f} mins" for ct in cycle_times],
                textposition="outside"
            ))
            fig.add_hline(y=takt_time, line_dash="dash", line_color="#FFD700",
                         annotation_text=f"Takt Time: {takt_time:.1f} mins",
                         annotation_position="top right")
            fig.update_layout(
                title="Cycle Time by Station (Red = Bottleneck)",
                xaxis_title="Station",
                yaxis_title="Cycle Time (mins)",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            # What if analysis
            st.subheader("What If You Fix the Bottleneck?")
            second_highest = sorted(stations, key=lambda x: x["cycle_time"], reverse=True)[1] if len(stations) > 1 else bottleneck
            new_bottleneck_ct = second_highest["cycle_time"]
            new_output = available_mins / new_bottleneck_ct
            output_gain = new_output - current_output
            new_efficiency = (new_output / ideal_output) * 100 if ideal_output > 0 else 0

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px;">
                    <p style="color: #00CC00; font-weight: 800; font-size: 1rem; margin: 0 0 12px 0;">If you fix {bottleneck['name']}:</p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">New bottleneck becomes: <b style="color:#FFD700">{second_highest['name']} ({new_bottleneck_ct:.1f} mins)</b></p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">Daily output increases from <b style="color:#CC0000">{current_output:.0f}</b> to <b style="color:#00CC00">{new_output:.0f}</b> units</p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">That is <b style="color:#00CC00">+{output_gain:.0f} extra units per day</b></p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">Line efficiency improves from <b style="color:#CC0000">{efficiency:.1f}%</b> to <b style="color:#00CC00">{new_efficiency:.1f}%</b></p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                units_per_year = output_gain * 250
                revenue_per_unit = st.number_input(f"Revenue per Unit ({currency_symbol})", min_value=0.0, value=100.0, step=1.0)
                annual_gain = units_per_year * revenue_per_unit
                st.markdown(f"""
                <div style="background: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px;">
                    <p style="color: #00CC00; font-weight: 800; font-size: 1rem; margin: 0 0 12px 0;">Financial Impact:</p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">Extra units per year: <b style="color:#00CC00">{units_per_year:,.0f}</b></p>
                    <p style="color: #cccccc; font-size: 0.9rem; margin: 4px 0;">Additional annual revenue: <b style="color:#00CC00">{currency_symbol}{annual_gain:,.0f}</b></p>
                    <p style="color: #888888; font-size: 0.78rem; margin-top: 8px;">Based on 250 working days per year</p>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.subheader("Recommendation")
            idle_time = sum(bottleneck["cycle_time"] - s["cycle_time"] for s in stations if s["cycle_time"] < bottleneck["cycle_time"])
            st.info(f"Your bottleneck is {bottleneck['name']} at {bottleneck['cycle_time']:.1f} mins. This single station is limiting your entire line to {current_output:.0f} units per day. There are {idle_time:.1f} mins of combined idle time across your other stations that could be redistributed to {bottleneck['name']} to reduce its cycle time. Conduct a time study at {bottleneck['name']} to identify which tasks can be moved to adjacent stations.")

    # ════════════════════════════════════════
    # TOOL 2: OEE CALCULATOR
    # ════════════════════════════════════════
    elif tool == "OEE Calculator (Overall Equipment Effectiveness)":
        st.header("OEE Calculator")
        st.write("OEE measures how effectively your equipment is being used. World class OEE is 85%. Enter your data below.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Availability")
            planned_time = st.number_input("Planned Production Time (mins/day)", min_value=1.0, max_value=1440.0, value=480.0, step=1.0)
            downtime = st.number_input("Unplanned Downtime (mins/day)", min_value=0.0, max_value=480.0, value=60.0, step=1.0)
            availability = ((planned_time - downtime) / planned_time) * 100 if planned_time > 0 else 0

            st.subheader("Performance")
            ideal_cycle_time = st.number_input("Ideal Cycle Time (mins per unit)", min_value=0.01, max_value=120.0, value=2.0, step=0.1, format="%.2f")
            total_units = st.number_input("Total Units Produced", min_value=1, max_value=10000, value=180, step=1)
            run_time = planned_time - downtime
            performance = ((ideal_cycle_time * total_units) / run_time) * 100 if run_time > 0 else 0
            performance = min(performance, 100)

        with col2:
            st.subheader("Quality")
            good_units = st.number_input("Good Units Produced (no defects)", min_value=0, max_value=10000, value=170, step=1)
            quality = (good_units / total_units) * 100 if total_units > 0 else 0

            st.subheader("Losses Breakdown")
            st.write("What is causing your downtime?")
            loss1 = st.number_input("Machine Breakdown (mins)", min_value=0.0, value=30.0, step=1.0)
            loss2 = st.number_input("Changeover/Setup (mins)", min_value=0.0, value=20.0, step=1.0)
            loss3 = st.number_input("Minor Stoppages (mins)", min_value=0.0, value=10.0, step=1.0)

        oee = (availability / 100) * (performance / 100) * (quality / 100) * 100

        st.divider()
        st.header("OEE Results")

        oee_color = "#00CC00" if oee >= 85 else "#FFD700" if oee >= 60 else "#CC0000"
        avail_color = "#00CC00" if availability >= 90 else "#FFD700" if availability >= 75 else "#CC0000"
        perf_color = "#00CC00" if performance >= 95 else "#FFD700" if performance >= 80 else "#CC0000"
        qual_color = "#00CC00" if quality >= 99 else "#FFD700" if quality >= 95 else "#CC0000"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {oee_color}; border-radius: 10px; padding: 20px; text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Overall OEE</p>
                <p style="color: {oee_color}; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{oee:.1f}%</p>
                <p style="color: #888; font-size: 0.78rem; margin: 0;">Benchmark: 85%</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {avail_color}; border-radius: 10px; padding: 20px; text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Availability</p>
                <p style="color: {avail_color}; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{availability:.1f}%</p>
                <p style="color: #888; font-size: 0.78rem; margin: 0;">Benchmark: 90%</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {perf_color}; border-radius: 10px; padding: 20px; text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Performance</p>
                <p style="color: {perf_color}; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{performance:.1f}%</p>
                <p style="color: #888; font-size: 0.78rem; margin: 0;">Benchmark: 95%</p>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {qual_color}; border-radius: 10px; padding: 20px; text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Quality</p>
                <p style="color: {qual_color}; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{quality:.1f}%</p>
                <p style="color: #888; font-size: 0.78rem; margin: 0;">Benchmark: 99%</p>
            </div>""", unsafe_allow_html=True)

        st.write("")

        # OEE Waterfall chart
        world_class_oee = 85.0
        oee_gap = world_class_oee - oee if oee < world_class_oee else 0

        fig = go.Figure()
        components = ["Availability", "Performance", "Quality", "OEE"]
        values = [availability, performance, quality, oee]
        bar_colors = [
            "#00CC00" if v >= 90 else "#FFD700" if v >= 75 else "#CC0000"
            for v in values
        ]
        fig.add_trace(go.Bar(
            x=components,
            y=values,
            marker_color=bar_colors,
            text=[f"{v:.1f}%" for v in values],
            textposition="outside"
        ))
        fig.add_hline(y=85, line_dash="dash", line_color="#ffffff",
                     annotation_text="World Class OEE: 85%",
                     annotation_position="top right")
        fig.update_layout(
            title="OEE Components vs World Class Benchmark",
            yaxis_title="Percentage (%)",
            yaxis_range=[0, 110],
            plot_bgcolor="#0a0a0a",
            paper_bgcolor="#0a0a0a",
            font_color="#ffffff",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        # Losses breakdown
        st.subheader("Losses Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            total_loss = loss1 + loss2 + loss3
            if total_loss > 0:
                loss_fig = go.Figure(go.Pie(
                    labels=["Machine Breakdown", "Changeover/Setup", "Minor Stoppages"],
                    values=[loss1, loss2, loss3],
                    marker_colors=["#CC0000", "#FFD700", "#FF6B00"],
                    hole=0.4
                ))
                loss_fig.update_layout(
                    title="Downtime Sources",
                    plot_bgcolor="#0a0a0a",
                    paper_bgcolor="#0a0a0a",
                    font_color="#ffffff",
                    height=300
                )
                st.plotly_chart(loss_fig, use_container_width=True)

        with col2:
            biggest_loss = max(
                [("Machine Breakdown", loss1), ("Changeover/Setup", loss2), ("Minor Stoppages", loss3)],
                key=lambda x: x[1]
            )
            if oee >= 85:
                st.success(f"World class OEE achieved at {oee:.1f}%! Focus on maintaining current performance.")
            else:
                st.warning(f"Your OEE of {oee:.1f}% is {world_class_oee - oee:.1f}% below world class standard of 85%.")
                st.info(f"Your biggest loss is {biggest_loss[0]} at {biggest_loss[1]:.0f} mins per day. This should be your first target for improvement.")
                lost_units = (downtime / ideal_cycle_time) if ideal_cycle_time > 0 else 0
                st.info(f"Your {downtime:.0f} mins of daily downtime is costing you approximately {lost_units:.0f} units per day in lost production.")

    # ════════════════════════════════════════
    # TOOL 3: DEFECT PARETO ANALYSIS
    # ════════════════════════════════════════
    elif tool == "Defect Pareto Analysis":
        st.header("Defect Pareto Analysis")
        st.write("Enter your defect types and quantities. SPO will identify which defects are causing 80% of your quality problems.")

        st.subheader("Enter Your Defect Data")
        num_defects = st.number_input("Number of Defect Types", min_value=2, max_value=10, value=5, step=1)

        defects = []
        cols = st.columns(2)
        for i in range(int(num_defects)):
            col = cols[i % 2]
            with col:
                name = st.text_input(f"Defect Type {i+1}", value=f"Defect {i+1}", key=f"dname_{i}")
                qty = st.number_input(f"Quantity", min_value=0, max_value=10000, value=max(1, 50 - i*8), step=1, key=f"dqty_{i}")
                if qty > 0:
                    defects.append({"name": name, "qty": qty})

        if defects:
            st.divider()
            st.header("Pareto Analysis Results")

            defects_sorted = sorted(defects, key=lambda x: x["qty"], reverse=True)
            total = sum(d["qty"] for d in defects_sorted)
            cumulative = 0
            cumulative_pcts = []
            individual_pcts = []

            for d in defects_sorted:
                cumulative += d["qty"]
                cumulative_pcts.append((cumulative / total) * 100)
                individual_pcts.append((d["qty"] / total) * 100)

            names = [d["name"] for d in defects_sorted]
            qtys = [d["qty"] for d in defects_sorted]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=names,
                y=qtys,
                name="Defect Count",
                marker_color="#CC0000",
                text=[f"{q}" for q in qtys],
                textposition="outside",
                yaxis="y"
            ))
            fig.add_trace(go.Scatter(
                x=names,
                y=cumulative_pcts,
                name="Cumulative %",
                mode="lines+markers",
                line=dict(color="#FFD700", width=2),
                marker=dict(size=8),
                yaxis="y2"
            ))
            fig.add_hline(y=80, line_dash="dash", line_color="#00CC00",
                         annotation_text="80% Line",
                         annotation_position="top right",
                         yref="y2")
            fig.update_layout(
                title="Defect Pareto Chart — Focus on the bars left of the 80% line",
                xaxis_title="Defect Type",
                yaxis=dict(title="Defect Count", side="left"),
                yaxis2=dict(title="Cumulative %", side="right", overlaying="y", range=[0, 110]),
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=400,
                legend=dict(x=0.7, y=0.1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Find vital few
            vital_few = []
            cumulative_check = 0
            for i, d in enumerate(defects_sorted):
                cumulative_check += (d["qty"] / total) * 100
                vital_few.append(d)
                if cumulative_check >= 80:
                    break

            st.subheader("The Vital Few — Fix These First")
            vital_pct = sum(d["qty"] for d in vital_few) / total * 100
            st.markdown(f"""
            <div style="background: rgba(232,0,29,0.04); border: 1px solid rgba(232,0,29,0.2); border-radius: 10px; padding: 16px 20px; margin-bottom: 16px;">
                <p style="color: #cccccc; font-size: 0.9rem; margin: 0;">
                    <b style="color: #CC0000;">{len(vital_few)} out of {len(defects_sorted)} defect types</b> are causing
                    <b style="color: #CC0000;">{vital_pct:.1f}%</b> of your total quality problems.
                    Fix these first and you will solve most of your quality issues.
                </p>
            </div>
            """, unsafe_allow_html=True)

            for i, d in enumerate(vital_few):
                pct = (d["qty"] / total) * 100
                st.markdown(f"""
                <div style="background: #1a1a1a; border-left: 4px solid #CC0000; padding: 10px 16px; margin: 6px 0; border-radius: 0 8px 8px 0;">
                    <span style="color: #CC0000; font-weight: 800;">#{i+1} Priority</span>
                    <span style="color: #ffffff; margin-left: 10px; font-weight: 600;">{d['name']}</span>
                    <span style="color: #888888; margin-left: 10px;">{d['qty']} units ({pct:.1f}% of all defects)</span>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.subheader("Total Defect Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Defects", f"{total:,}")
            with col2:
                st.metric("Defect Types Analyzed", f"{len(defects_sorted)}")
            with col3:
                st.metric("Vital Few Defects", f"{len(vital_few)} types = {vital_pct:.0f}% of problem")

    # ════════════════════════════════════════
    # TOOL 4: MANPOWER PLANNING
    # ════════════════════════════════════════
    elif tool == "Manpower Planning Tool":
        st.header("Manpower Planning Tool")
        st.write("Enter your takt time and station cycle times. SPO will calculate the ideal number of workers per station and identify where you are over or understaffed.")

        col1, col2 = st.columns(2)
        with col1:
            takt_time = st.number_input(
                "Takt Time (mins) — How often does a customer need one unit?",
                min_value=0.1, max_value=480.0, value=15.0, step=0.1, format="%.1f"
            )
            efficiency_factor = st.number_input(
                "Worker Efficiency Factor (%)",
                min_value=50.0, max_value=100.0, value=85.0, step=1.0,
                help="Typical worker efficiency is 80-90%. This accounts for fatigue, breaks and minor delays."
            )
        with col2:
            num_stations = st.number_input("Number of Stations", min_value=2, max_value=20, value=5, step=1)
            daily_demand = st.number_input("Daily Production Target (units)", min_value=1, max_value=10000, value=200, step=1)

        st.write("")
        st.subheader("Enter Station Data")

        stations = []
        cols = st.columns(3)
        for i in range(int(num_stations)):
            col = cols[i % 3]
            with col:
                name = st.text_input(f"Station {i+1} Name", value=f"Station {i+1}", key=f"mpname_{i}")
                ct = st.number_input(f"Cycle Time (mins)", min_value=0.1, max_value=480.0, value=float(10 + i*3), step=0.1, format="%.1f", key=f"mpct_{i}")
                current_workers = st.number_input(f"Current Workers", min_value=1, max_value=20, value=1, step=1, key=f"mpw_{i}")
                stations.append({"name": name, "cycle_time": ct, "current_workers": current_workers})

        if stations:
            st.divider()
            st.header("Manpower Planning Results")

            adjusted_takt = takt_time * (efficiency_factor / 100)

            results = []
            for s in stations:
                ideal_workers = s["cycle_time"] / adjusted_takt
                ideal_workers_rounded = max(1, round(ideal_workers))
                diff = ideal_workers_rounded - s["current_workers"]
                if diff > 0:
                    status = "Understaffed"
                    color = "#CC0000"
                elif diff < 0:
                    status = "Overstaffed"
                    color = "#FFD700"
                else:
                    status = "Optimal"
                    color = "#00CC00"
                results.append({
                    "name": s["name"],
                    "cycle_time": s["cycle_time"],
                    "current_workers": s["current_workers"],
                    "ideal_workers": ideal_workers,
                    "ideal_workers_rounded": ideal_workers_rounded,
                    "diff": diff,
                    "status": status,
                    "color": color
                })

            total_current = sum(r["current_workers"] for r in results)
            total_ideal = sum(r["ideal_workers_rounded"] for r in results)
            total_diff = total_ideal - total_current

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid #ffffff; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Current Workers</p>
                    <p style="color: #ffffff; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{total_current}</p>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid #00CC00; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Ideal Workers</p>
                    <p style="color: #00CC00; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{total_ideal}</p>
                </div>""", unsafe_allow_html=True)
            with col3:
                diff_color = "#CC0000" if total_diff > 0 else "#FFD700" if total_diff < 0 else "#00CC00"
                diff_text = f"+{total_diff}" if total_diff > 0 else str(total_diff)
                diff_label = "Need to Add" if total_diff > 0 else "Can Reduce" if total_diff < 0 else "Perfectly Balanced"
                st.markdown(f"""<div style="background: #1a1a1a; border: 2px solid {diff_color}; border-radius: 10px; padding: 20px; text-align: center;">
                    <p style="color: #ffffff; margin: 0; font-size: 0.85rem;">Difference</p>
                    <p style="color: {diff_color}; font-size: 2.5rem; font-weight: 900; margin: 8px 0;">{diff_text}</p>
                    <p style="color: {diff_color}; font-size: 0.78rem; margin: 0;">{diff_label}</p>
                </div>""", unsafe_allow_html=True)

            st.write("")

            # Station by station breakdown
            st.subheader("Station by Station Breakdown")
            for r in results:
                diff_str = f"+{r['diff']}" if r['diff'] > 0 else str(r['diff'])
                st.markdown(f"""
                <div style="background: #1a1a1a; border-left: 4px solid {r['color']}; padding: 12px 16px; margin: 6px 0; border-radius: 0 8px 8px 0; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: {r['color']}; font-weight: 800; font-size: 0.9rem;">{r['status']}</span>
                        <span style="color: #ffffff; margin-left: 10px; font-weight: 600;">{r['name']}</span>
                        <span style="color: #888888; margin-left: 10px; font-size: 0.82rem;">Cycle Time: {r['cycle_time']:.1f} mins</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #888888; font-size: 0.82rem;">Current: {r['current_workers']} | Ideal: {r['ideal_workers_rounded']} | </span>
                        <span style="color: {r['color']}; font-weight: 700;">{diff_str} workers</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Current Workers",
                x=[r["name"] for r in results],
                y=[r["current_workers"] for r in results],
                marker_color="#444444",
                text=[str(r["current_workers"]) for r in results],
                textposition="outside"
            ))
            fig.add_trace(go.Bar(
                name="Ideal Workers",
                x=[r["name"] for r in results],
                y=[r["ideal_workers_rounded"] for r in results],
                marker_color="#CC0000",
                text=[str(r["ideal_workers_rounded"]) for r in results],
                textposition="outside"
            ))
            fig.update_layout(
                title="Current vs Ideal Workers per Station",
                xaxis_title="Station",
                yaxis_title="Number of Workers",
                barmode="group",
                plot_bgcolor="#0a0a0a",
                paper_bgcolor="#0a0a0a",
                font_color="#ffffff",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            st.write("")
            understaffed = [r for r in results if r["status"] == "Understaffed"]
            overstaffed = [r for r in results if r["status"] == "Overstaffed"]

            if understaffed:
                stations_str = ", ".join([r["name"] for r in understaffed])
                st.warning(f"These stations are understaffed and creating bottlenecks: {stations_str}. Add workers here first.")
            if overstaffed:
                stations_str = ", ".join([r["name"] for r in overstaffed])
                st.info(f"These stations are overstaffed: {stations_str}. Consider moving surplus workers to understaffed stations before hiring new ones.")
            if not understaffed and not overstaffed:
                st.success("Your manpower allocation is perfectly balanced for your current takt time!")