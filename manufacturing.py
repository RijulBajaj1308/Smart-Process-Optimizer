import streamlit as st
import plotly.graph_objects as go

manufacturing_benchmarks = {
    "Automotive": {
        "efficiency_rate": 85.000,
        "cycle_time": 25.000,
        "waste_percentage": 4.000,
        "roi": 15.000,
        "manpower_utilization": 85.000,
        "rejection_rate": 2.000,
        "lead_time": 7.000
    },
    "Electronics": {
        "efficiency_rate": 82.000,
        "cycle_time": 20.000,
        "waste_percentage": 3.000,
        "roi": 18.000,
        "manpower_utilization": 82.000,
        "rejection_rate": 2.000,
        "lead_time": 5.000
    },
    "Food and Beverage": {
        "efficiency_rate": 78.000,
        "cycle_time": 20.000,
        "waste_percentage": 2.000,
        "roi": 12.000,
        "manpower_utilization": 78.000,
        "rejection_rate": 1.000,
        "lead_time": 2.000
    },
    "Textile and Apparel": {
        "efficiency_rate": 72.000,
        "cycle_time": 40.000,
        "waste_percentage": 8.000,
        "roi": 8.000,
        "manpower_utilization": 75.000,
        "rejection_rate": 4.000,
        "lead_time": 14.000
    },
    "General Manufacturing": {
        "efficiency_rate": 75.000,
        "cycle_time": 35.000,
        "waste_percentage": 6.000,
        "roi": 10.000,
        "manpower_utilization": 78.000,
        "rejection_rate": 3.000,
        "lead_time": 10.000
    },
    "Eco Friendly Packaging": {
        "efficiency_rate": 80.000,
        "cycle_time": 30.000,
        "waste_percentage": 3.000,
        "roi": 10.000,
        "manpower_utilization": 80.000,
        "rejection_rate": 2.000,
        "lead_time": 8.000
    },
    "Pulp and Paper Manufacturing": {
        "efficiency_rate": 72.000,
        "cycle_time": 45.000,
        "waste_percentage": 8.000,
        "roi": 8.000,
        "manpower_utilization": 75.000,
        "rejection_rate": 4.000,
        "lead_time": 12.000
    },
    "Pharmaceutical Manufacturing": {
        "efficiency_rate": 90.000,
        "cycle_time": 15.000,
        "waste_percentage": 1.000,
        "roi": 20.000,
        "manpower_utilization": 85.000,
        "rejection_rate": 1.000,
        "lead_time": 3.000
    }
}

industry_insights = {
    "Automotive": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in automotive manufacturing is typically caused by unplanned machine downtime, frequent model changeovers, or bottlenecks in stamping, welding or assembly lines",
            "recommendation": "Implement Total Productive Maintenance (TPM) to reduce unplanned downtime and conduct SMED analysis to reduce changeover times between vehicle models"
        },
        "cycle_time": {
            "root_cause": "High cycle time in automotive is often caused by excessive material handling between stations, manual operations that could be automated, or unbalanced workloads across the assembly line",
            "recommendation": "Conduct a detailed time and motion study across all assembly stations and implement line rebalancing to eliminate bottlenecks and reduce inter-station waiting time"
        },
        "waste_percentage": {
            "root_cause": "Waste in automotive manufacturing is typically from overproduction due to push based scheduling, scrap from stamping and cutting operations, or rework from welding defects",
            "recommendation": "Implement pull based production scheduling aligned with customer demand and introduce in-process quality checks at stamping and welding stations to catch defects early"
        },
        "roi": {
            "root_cause": "Low ROI in automotive is often driven by high tooling and die maintenance costs, excess inventory of raw materials and WIP, or low throughput due to frequent line stoppages",
            "recommendation": "Optimize tooling maintenance schedules using predictive maintenance data and implement just-in-time inventory management to reduce holding costs and improve cash flow"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in automotive lines is usually caused by poor line balancing where some operators are overloaded while others are idle, or excessive waiting time due to material shortages",
            "recommendation": "Conduct a manpower efficiency study and rebalance operator tasks across stations using takt time analysis to ensure uniform workload distribution"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in automotive is typically caused by dimensional tolerance issues in stamping or casting, welding defects from incorrect parameters, or paint quality failures",
            "recommendation": "Implement Statistical Process Control (SPC) at critical stamping and welding stations, establish proper welding parameter standards, and conduct regular gauge calibration"
        },
        "lead_time": {
            "root_cause": "High lead time in automotive is commonly caused by supplier delays for critical components, long queue times between production stages, or inefficient scheduling of production runs",
            "recommendation": "Develop strategic supplier partnerships with buffer stock agreements for critical components and implement advanced production scheduling software to minimize inter-stage queuing"
        }
    },
    "Electronics": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in electronics manufacturing is often caused by frequent component shortages on the SMT line, high rates of rework at PCB assembly, or equipment downtime on pick and place machines",
            "recommendation": "Implement real time component inventory monitoring on the SMT line and establish preventive maintenance schedules for pick and place machines to minimize unplanned stoppages"
        },
        "cycle_time": {
            "root_cause": "High cycle time in electronics is typically caused by lengthy inspection and testing procedures, manual soldering operations that could be automated, or poor sequencing of PCB assembly steps",
            "recommendation": "Invest in automated optical inspection (AOI) systems to speed up quality checks and review the PCB assembly sequence to minimize component handling and travel time"
        },
        "waste_percentage": {
            "root_cause": "Waste in electronics manufacturing is commonly from solder paste that expires before use, components damaged during handling, or PCBs scrapped due to soldering defects",
            "recommendation": "Implement first in first out (FIFO) material management for solder paste and sensitive components, and install ESD protection measures throughout the assembly area"
        },
        "roi": {
            "root_cause": "Low ROI in electronics is often caused by high component costs due to poor procurement planning, excessive scrap from PCB failures, or low yield rates at final testing",
            "recommendation": "Negotiate volume-based contracts with component suppliers and implement Design for Testability (DFT) principles to improve first pass yield rates at testing"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in electronics is typically caused by operators waiting for component replenishment, excessive time spent on manual inspection, or poor allocation of skilled technicians",
            "recommendation": "Automate routine inspection tasks using AOI and assign skilled technicians specifically to complex rework and troubleshooting tasks rather than routine assembly"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in electronics is commonly caused by solder bridging or insufficient solder at reflow, ESD damage to sensitive components, or incorrect component placement by pick and place machines",
            "recommendation": "Optimize solder paste printing parameters and reflow oven profiles, enforce strict ESD protocols throughout the facility, and calibrate pick and place machines regularly"
        },
        "lead_time": {
            "root_cause": "High lead time in electronics is often caused by long procurement lead times for imported components, extended testing and burn-in periods, or delays in regulatory certification for new products",
            "recommendation": "Maintain strategic safety stock for long lead time components and streamline the testing process by implementing parallel testing protocols rather than sequential testing"
        }
    },
    "Food and Beverage": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in food and beverage manufacturing is typically caused by frequent CIP cycles, lengthy sanitation procedures between product changeovers, or equipment downtime due to food buildup",
            "recommendation": "Optimize CIP cycle parameters to reduce cleaning time without compromising hygiene standards and implement quick changeover procedures for product line switches"
        },
        "cycle_time": {
            "root_cause": "High cycle time in food and beverage is often caused by slow filling and packaging equipment, manual weighing and measuring operations, or bottlenecks at labeling and sealing stations",
            "recommendation": "Audit filling and packaging line speeds against equipment rated capacity and implement automated weighing and dosing systems to replace manual operations"
        },
        "waste_percentage": {
            "root_cause": "Waste in food manufacturing is commonly from overproduction beyond shelf life, product spillage during filling, ingredient losses during mixing, or products rejected due to weight or fill level variations",
            "recommendation": "Implement demand-driven production scheduling to minimize overproduction and install precision filling equipment with automated weight checking to reduce giveaway and spillage"
        },
        "roi": {
            "root_cause": "Low ROI in food and beverage is often driven by high raw material costs from poor yield management, energy intensive processing operations, or high disposal costs for food waste",
            "recommendation": "Conduct a detailed ingredient yield analysis to identify loss points in the process and implement energy management systems to optimize heating, cooling and processing energy consumption"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in food manufacturing is typically caused by manual sorting and inspection operations, excessive sanitation time taking workers away from production, or poor scheduling of cleaning and production shifts",
            "recommendation": "Implement automated sorting and vision inspection systems and schedule sanitation activities during planned downtime periods to maximize productive operator time"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in food and beverage is commonly caused by microbial contamination from inadequate sanitation, incorrect ingredient ratios due to manual dosing errors, or improper temperature control during processing",
            "recommendation": "Strengthen HACCP controls at critical control points, implement automated ingredient dosing systems with load cell verification, and install continuous temperature monitoring throughout the process"
        },
        "lead_time": {
            "root_cause": "High lead time in food manufacturing is often caused by long raw material procurement cycles for seasonal ingredients, extended quality hold periods for microbiological testing, or poor production scheduling",
            "recommendation": "Develop relationships with multiple suppliers for key seasonal ingredients and implement rapid microbiological testing methods to reduce quality hold times"
        }
    },
    "Textile and Apparel": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in textile manufacturing is commonly caused by frequent yarn breakages on looms, high loom downtime due to poor maintenance, or excessive time lost to style changeovers on sewing lines",
            "recommendation": "Implement a preventive maintenance program for looms and weaving machines and conduct SMED analysis on sewing line changeovers to reduce style change downtime"
        },
        "cycle_time": {
            "root_cause": "High cycle time in textile is often caused by manual bundle handling between sewing operations, long queues at bottleneck sewing stations, or slow ironing and finishing operations",
            "recommendation": "Implement unit production system (UPS) to replace bundle system and eliminate inter-operation queuing, and invest in automated pressing and finishing equipment"
        },
        "waste_percentage": {
            "root_cause": "Waste in textile manufacturing is typically from fabric cutting losses, yarn waste from loom stoppages, dye liquor disposal, and defective garments that cannot be reworked",
            "recommendation": "Implement computer aided cutting (CAC) systems to optimize fabric marker efficiency and reduce cutting waste, and invest in dye liquor recycling systems"
        },
        "roi": {
            "root_cause": "Low ROI in textile is often caused by high cost of yarn and fabric due to poor inventory management, energy intensive dyeing and finishing processes, or high rework costs from quality issues",
            "recommendation": "Implement lean inventory management for raw materials and invest in energy efficient dyeing machines with liquor ratio optimization to reduce water and chemical consumption"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in textile is typically caused by poor line balancing on sewing lines, excessive non-productive time spent on material handling, or absenteeism causing line imbalance",
            "recommendation": "Conduct time and motion studies on all sewing operations and rebalance the line based on operation standard minutes and ensure cross training of operators for flexibility"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in textile is commonly caused by weaving defects such as broken picks or float yarns, color variation between dye batches, or sewing defects such as skipped stitches and broken seams",
            "recommendation": "Install online fabric inspection systems on looms to detect weaving defects in real time and implement strict dye recipe management with spectrophotometer verification for color consistency"
        },
        "lead_time": {
            "root_cause": "High lead time in textile is often caused by long yarn procurement lead times, extended dyeing and finishing processes, or poor production planning leading to rush orders disrupting schedules",
            "recommendation": "Maintain strategic yarn inventory for key running styles and implement master production scheduling to sequence orders efficiently and minimize rush order disruptions"
        }
    },
    "General Manufacturing": {
        "efficiency_rate": {
            "root_cause": "Low efficiency is typically caused by unplanned equipment downtime, poor line balancing, excessive changeover times, or material shortages causing production stoppages",
            "recommendation": "Implement a preventive maintenance program and conduct line balancing analysis to distribute workload evenly across all production stations"
        },
        "cycle_time": {
            "root_cause": "High cycle time is commonly caused by bottleneck stations with excessive workload, manual operations that slow the process, or poor workstation layout causing unnecessary movement",
            "recommendation": "Conduct time and motion studies to identify bottlenecks and rebalance workloads, and review workstation layouts using 5S principles to minimize operator movement"
        },
        "waste_percentage": {
            "root_cause": "High waste is often from overproduction, defective materials, unnecessary processing steps, or poor inventory management leading to material expiry or damage",
            "recommendation": "Implement value stream mapping to identify and eliminate non-value-adding activities and establish a robust first-in-first-out material management system"
        },
        "roi": {
            "root_cause": "Low ROI is commonly caused by high operational costs, excess inventory tying up capital, high rejection and rework costs, or underutilized production capacity",
            "recommendation": "Focus on reducing the top 3 cost drivers through process optimization and implement capacity utilization tracking to identify and fill underutilized production time"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization is typically caused by poor task allocation, excessive idle time at certain stations, or workers performing non-productive activities such as searching for tools or materials",
            "recommendation": "Conduct a manpower efficiency study and redistribute tasks based on operator capacity and implement 5S in the workplace to eliminate time wasted searching for tools and materials"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate is commonly caused by inadequate process controls, poor incoming material quality, operator errors due to insufficient training, or equipment that is out of calibration",
            "recommendation": "Implement in-process quality checkpoints at critical stages, establish incoming quality inspection for raw materials, and ensure all measurement equipment is regularly calibrated"
        },
        "lead_time": {
            "root_cause": "High lead time is often caused by poor production scheduling, long supplier lead times for critical materials, or excessive work-in-process inventory causing congestion on the production floor",
            "recommendation": "Implement production scheduling software to optimize job sequencing and develop supplier partnerships with agreed delivery windows to reduce material waiting time"
        }
    },
    "Eco Friendly Packaging": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in eco-friendly packaging is typically caused by inconsistent raw material quality such as bagasse or recycled pulp, frequent mold cleaning required due to material buildup, or equipment not optimized for sustainable materials",
            "recommendation": "Establish strict incoming material quality standards for sustainable raw materials and implement regular mold cleaning schedules to prevent buildup that causes downtime"
        },
        "cycle_time": {
            "root_cause": "High cycle time in eco packaging is often caused by longer drying and curing times required for natural materials, slower forming speeds due to material viscosity, or manual trimming and finishing operations",
            "recommendation": "Optimize drying parameters for natural materials through systematic experimentation and invest in automated trimming equipment to replace manual finishing operations"
        },
        "waste_percentage": {
            "root_cause": "Waste in eco-friendly packaging is commonly from material losses during pulp preparation, off-specification products due to inconsistent material properties, or trimming waste from forming operations",
            "recommendation": "Implement closed-loop pulp recycling to recover and reuse pulp waste from trimming operations and establish tighter incoming material specifications to reduce variability"
        },
        "roi": {
            "root_cause": "Low ROI in eco packaging is often caused by higher raw material costs compared to conventional plastics, lower production speeds due to natural material properties, or high product rejection rates",
            "recommendation": "Explore alternative sustainable raw material suppliers to optimize material costs and focus on improving first-pass yield to reduce the per-unit cost of production"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in eco packaging is typically caused by manual quality inspection of formed products, workers waiting during extended drying cycles, or poor scheduling of forming and drying operations",
            "recommendation": "Implement automated vision systems for product quality inspection and schedule forming and drying operations to ensure continuous operator engagement throughout the shift"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in eco packaging is commonly caused by inconsistent wall thickness due to uneven pulp distribution in molds, surface defects from mold wear, or dimensional variations due to natural material shrinkage",
            "recommendation": "Implement regular mold inspection and refurbishment programs and establish process controls for pulp consistency including concentration and temperature to minimize dimensional variation"
        },
        "lead_time": {
            "root_cause": "High lead time in eco packaging is often caused by long procurement lead times for certified sustainable raw materials, extended product testing requirements for new eco certifications, or seasonal availability of agricultural raw materials",
            "recommendation": "Develop relationships with multiple certified sustainable material suppliers and maintain strategic safety stock for seasonal materials to ensure uninterrupted production"
        }
    },
    "Pulp and Paper Manufacturing": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in pulp and paper is typically caused by paper machine breaks requiring rethreading, poor stock preparation consistency, or unplanned downtime of the recovery boiler or steam systems",
            "recommendation": "Implement online monitoring of paper machine parameters to detect early signs of impending breaks and establish rigorous stock preparation quality controls to ensure consistent furnish"
        },
        "cycle_time": {
            "root_cause": "High cycle time in pulp and paper is commonly caused by slow paper machine speeds due to formation quality issues, extended drying section residence time, or slow winding and reel changeover operations",
            "recommendation": "Optimize paper machine forming section parameters to improve formation quality at higher speeds and implement automatic reel change systems to minimize changeover time"
        },
        "waste_percentage": {
            "root_cause": "Waste in pulp and paper is typically from paper broke during machine breaks, edge trim waste from slitting operations, reject rolls that do not meet specification, or chemical losses in the pulping process",
            "recommendation": "Implement a broke pulper and repulping system to recover and reuse paper broke and establish closed-loop chemical recovery systems to minimize chemical losses"
        },
        "roi": {
            "root_cause": "Low ROI in pulp and paper is often driven by high energy costs for steam and electricity, high chemical costs for pulping and bleaching, or low selling prices due to commodity market pressures",
            "recommendation": "Conduct an energy audit to identify heat recovery opportunities and optimize chemical dosing using online analyzers to reduce chemical consumption while maintaining quality"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in pulp and paper is typically caused by operators spending excessive time managing machine breaks, poor coordination between pulping and papermaking shifts, or manual sampling and testing taking operators away from the machine",
            "recommendation": "Install online quality sensors to reduce manual sampling frequency and improve shift coordination through structured handover protocols and shared real-time production dashboards"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in pulp and paper is commonly caused by basis weight variation from inconsistent headbox jet-to-wire ratio, moisture content variation in the drying section, or caliper variation from press section issues",
            "recommendation": "Implement automatic basis weight and moisture control systems on the paper machine and establish regular press felt and wire conditioning schedules to maintain consistent sheet properties"
        },
        "lead_time": {
            "root_cause": "High lead time in pulp and paper is often caused by long wood or recycled fiber procurement cycles, extended quality testing requirements for specialty grades, or slow order-to-production scheduling",
            "recommendation": "Develop long-term fiber supply agreements with multiple suppliers and implement grade change optimization to minimize machine downtime between different paper grades"
        }
    },
    "Pharmaceutical Manufacturing": {
        "efficiency_rate": {
            "root_cause": "Low efficiency in pharmaceutical manufacturing is typically caused by lengthy batch record review and release processes, frequent equipment cleaning and validation between products, or unplanned equipment downtime requiring extensive requalification",
            "recommendation": "Implement electronic batch records (EBR) to accelerate review and release processes and develop risk-based cleaning validation approaches to reduce cleaning time between products"
        },
        "cycle_time": {
            "root_cause": "High cycle time in pharma manufacturing is commonly caused by lengthy in-process testing and quality holds, slow granulation or blending operations, or extended coating and drying times for solid dosage forms",
            "recommendation": "Implement Process Analytical Technology (PAT) tools for real-time in-process quality monitoring to reduce testing hold times and optimize granulation and coating process parameters"
        },
        "waste_percentage": {
            "root_cause": "Waste in pharmaceutical manufacturing is typically from batch failures due to out-of-specification results, API losses during granulation and blending, or expired materials due to poor inventory management",
            "recommendation": "Implement real-time process monitoring using PAT to detect process deviations early and prevent batch failures, and strengthen material management systems to minimize expiry waste"
        },
        "roi": {
            "root_cause": "Low ROI in pharma is often caused by high API costs due to poor yield management, extensive quality testing costs, high regulatory compliance overhead, or low capacity utilization due to frequent product changeovers",
            "recommendation": "Focus on improving API yield through process optimization and implement a campaign manufacturing approach to group similar products and minimize changeover frequency"
        },
        "manpower_utilization": {
            "root_cause": "Low manpower utilization in pharma is typically caused by operators spending excessive time on manual documentation, waiting for QC results before proceeding, or performing redundant checks required by outdated SOPs",
            "recommendation": "Implement electronic batch records and laboratory information management systems (LIMS) to reduce documentation time and enable real-time data sharing between production and QC"
        },
        "rejection_rate": {
            "root_cause": "High rejection rate in pharmaceutical manufacturing is commonly caused by GMP deviations during manufacturing, contamination from inadequate cleanroom controls, incorrect API potency from blending issues, or packaging defects affecting product integrity",
            "recommendation": "Strengthen GMP training and compliance monitoring, enhance environmental monitoring in cleanrooms, implement in-line blend uniformity testing, and install automated packaging inspection systems"
        },
        "lead_time": {
            "root_cause": "High lead time in pharma is often caused by long API procurement lead times from single-source suppliers, extended stability testing requirements for new batches, or slow regulatory approval processes for product releases",
            "recommendation": "Dual-source critical APIs to reduce supply risk and lead time dependency and implement a rolling stability testing program to avoid batch release delays"
        }
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

def show_manufacturing(industry, currency_symbol="$"):
    benchmarks = manufacturing_benchmarks[industry]
    insights = industry_insights[industry]

    st.sidebar.title("Enter Your Plant KPIs")
    st.sidebar.divider()
    st.sidebar.caption(f"Benchmarks: {industry} Industry (India)")

    efficiency_rate = st.sidebar.number_input("Efficiency Rate (%)", min_value=0.000, max_value=100.000, value=65.000, step=0.001, format="%.3f")
    cycle_time = st.sidebar.number_input("Cycle Time (mins)", min_value=0.000, max_value=120.000, value=45.000, step=0.001, format="%.3f")
    waste_percentage = st.sidebar.number_input("Waste Percentage (%)", min_value=0.000, max_value=50.000, value=12.000, step=0.001, format="%.3f")
    roi = st.sidebar.number_input("ROI (%)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
    manpower_utilization = st.sidebar.number_input("Manpower Utilization (%)", min_value=0.000, max_value=100.000, value=70.000, step=0.001, format="%.3f")
    rejection_rate = st.sidebar.number_input("Rejection Rate (%)", min_value=0.000, max_value=50.000, value=8.000, step=0.001, format="%.3f")
    lead_time = st.sidebar.number_input("Lead Time (days)", min_value=0.000, max_value=30.000, value=10.000, step=0.001, format="%.3f")

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
    st.header("KPI Analysis")
    st.caption(f"Benchmarks based on {industry} industry standards in India")
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
    st.header("Overall Plant Risk Assessment")

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

    # Custom Root Causes and Recommendations
    st.header("Root Causes and Recommendations")
    st.caption(f"Customized analysis for {industry} industry")

    root_causes = []
    recommendations = []
    improvements = {}

    if analysis["efficiency_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["efficiency_rate"]["root_cause"])
        recommendations.append(insights["efficiency_rate"]["recommendation"])
        improvements["efficiency_rate"] = min(benchmarks["efficiency_rate"], efficiency_rate + 12)

    if analysis["cycle_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["cycle_time"]["root_cause"])
        recommendations.append(insights["cycle_time"]["recommendation"])
        improvements["cycle_time"] = max(benchmarks["cycle_time"], cycle_time - 10)

    if analysis["waste_percentage"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["waste_percentage"]["root_cause"])
        recommendations.append(insights["waste_percentage"]["recommendation"])
        improvements["waste_percentage"] = max(benchmarks["waste_percentage"], waste_percentage - 3)

    if analysis["roi"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["roi"]["root_cause"])
        recommendations.append(insights["roi"]["recommendation"])
        improvements["roi"] = min(benchmarks["roi"], roi + 5)

    if analysis["manpower_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["manpower_utilization"]["root_cause"])
        recommendations.append(insights["manpower_utilization"]["recommendation"])
        improvements["manpower_utilization"] = min(benchmarks["manpower_utilization"], manpower_utilization + 15)

    if analysis["rejection_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["rejection_rate"]["root_cause"])
        recommendations.append(insights["rejection_rate"]["recommendation"])
        improvements["rejection_rate"] = max(benchmarks["rejection_rate"], rejection_rate - 3)

    if analysis["lead_time"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["lead_time"]["root_cause"])
        recommendations.append(insights["lead_time"]["recommendation"])
        improvements["lead_time"] = max(benchmarks["lead_time"], lead_time - 3)

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
    st.write("If you implement all recommendations here is what your plant could look like:")

    if improvements:
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, (kpi, projected) in enumerate(improvements.items()):
            col = cols[i % 3]
            current = kpi_data[kpi]
            with col:
                if kpi in ["efficiency_rate", "roi", "manpower_utilization"]:
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
        st.success("Your plant is already performing at benchmark level!")

    st.divider()

    # What-If Simulator
    st.header("What-If Simulator")
    st.write("Adjust the values below to simulate improvements and see projected results")
    col1, col2 = st.columns(2)

    with col1:
        efficiency_improvement = st.number_input("Improve Efficiency Rate by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        manpower_improvement = st.number_input("Improve Manpower Utilization by (%)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        rejection_improvement = st.number_input("Reduce Rejection Rate by (%)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    with col2:
        waste_improvement = st.number_input("Reduce Waste by (%)", min_value=0.000, max_value=20.000, value=0.000, step=0.001, format="%.3f")
        cycle_improvement = st.number_input("Reduce Cycle Time by (mins)", min_value=0.000, max_value=30.000, value=0.000, step=0.001, format="%.3f")
        lead_improvement = st.number_input("Reduce Lead Time by (days)", min_value=0.000, max_value=10.000, value=0.000, step=0.001, format="%.3f")

    st.subheader("Projected Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Rate", f"{efficiency_rate + efficiency_improvement:.3f}%", f"+{efficiency_improvement:.3f}%")
        st.metric("Manpower Utilization", f"{manpower_utilization + manpower_improvement:.3f}%", f"+{manpower_improvement:.3f}%")

    with col2:
        st.metric("Rejection Rate", f"{rejection_rate - rejection_improvement:.3f}%", f"-{rejection_improvement:.3f}%")
        st.metric("Waste Percentage", f"{waste_percentage - waste_improvement:.3f}%", f"-{waste_improvement:.3f}%")

    with col3:
        st.metric("Cycle Time", f"{cycle_time - cycle_improvement:.3f} mins", f"-{cycle_improvement:.3f} mins")
        st.metric("Lead Time", f"{lead_time - lead_improvement:.3f} days", f"-{lead_improvement:.3f} days")

    st.divider()

    # Gauge Charts
    st.header("Performance Charts")
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
    st.header("ROI Projection Calculator")
    st.write(f"Savings are automatically calculated based on SPO recommendations for {industry}")
    col1, col2 = st.columns(2)

    with col1:
        annual_revenue = st.number_input(f"Annual Revenue ({currency_symbol})", min_value=0.000, value=1000000.000, step=1000.000, format="%.3f")
        num_workers = st.number_input("Number of Workers", min_value=0, value=50, step=1)
        avg_worker_salary = st.number_input(f"Average Worker Salary ({currency_symbol}/year)", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")

    with col2:
        waste_cost = st.number_input(f"Annual Waste Cost ({currency_symbol})", min_value=0.000, value=50000.000, step=1000.000, format="%.3f")
        downtime_cost = st.number_input(f"Annual Downtime Cost ({currency_symbol})", min_value=0.000, value=30000.000, step=1000.000, format="%.3f")
        rejection_cost = st.number_input(f"Annual Rejection Cost ({currency_symbol})", min_value=0.000, value=20000.000, step=1000.000, format="%.3f")

    # ROI uses projected improvements from Before vs After section
    efficiency_gain = improvements.get("efficiency_rate", efficiency_rate) - efficiency_rate
    manpower_gain = improvements.get("manpower_utilization", manpower_utilization) - manpower_utilization
    waste_gain = waste_percentage - improvements.get("waste_percentage", waste_percentage)
    rejection_gain = rejection_rate - improvements.get("rejection_rate", rejection_rate)

    efficiency_savings = annual_revenue * (abs(efficiency_gain) / 100)
    manpower_savings = num_workers * avg_worker_salary * (abs(manpower_gain) / 100)
    waste_savings = waste_cost * (abs(waste_gain) / 100)
    rejection_savings = rejection_cost * (abs(rejection_gain) / 100)
    total_savings = efficiency_savings + manpower_savings + waste_savings + rejection_savings

    st.subheader("Projected Annual Savings Based on SPO Recommendations")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Efficiency Savings", f"{currency_symbol}{efficiency_savings:,.3f}")
        st.metric("Manpower Savings", f"{currency_symbol}{manpower_savings:,.3f}")

    with col2:
        st.metric("Waste Savings", f"{currency_symbol}{waste_savings:,.3f}")
        st.metric("Rejection Savings", f"{currency_symbol}{rejection_savings:,.3f}")

    with col3:
        st.metric("Total Annual Savings", f"{currency_symbol}{total_savings:,.3f}", delta=f"+{currency_symbol}{total_savings:,.3f}")

    st.divider()

    # PFMEA Module
    st.header("PFMEA Module")
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