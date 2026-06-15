import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Distribution
# Sources:
# Warehouse and Distribution: Delhivery, Blue Dart, WERC benchmarking study 2025
# Cold Chain Distribution: Snowman Logistics, Cold Star standards
# E-commerce Fulfillment: Flipkart, Amazon India, Meesho standards
# Pharmaceutical Distribution: GDP compliance standards, CDSCO guidelines
# Automotive Parts Distribution: Tata Motors, Maruti, Mahindra dealer network standards
# Electronics Distribution: Samsung India, LG India, Dixon Technologies standards
# Food and Beverage Distribution: HUL, ITC, Nestle India FMCG distribution standards
# Textile and Apparel Distribution: Raymond, Arvind Mills, Manyavar standards
# Eco Friendly Packaging Distribution: UFlex, ITC Packaging, SR Pulp standards
# Pulp and Paper Distribution: JK Paper, TNPL, Kuantum Papers standards

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

# Custom root causes and recommendations per distribution industry
distribution_insights = {
    "Warehouse and Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in general warehousing is typically caused by stockouts due to inaccurate demand forecasting, poor inventory visibility across multiple storage locations, or delays in order processing due to manual systems",
            "recommendation": "Implement a Warehouse Management System (WMS) with real time inventory visibility and set dynamic reorder points based on historical demand patterns to prevent stockouts"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in warehouse distribution are commonly caused by inefficient route planning, vehicle breakdowns due to poor fleet maintenance, or poor load planning leading to multiple trips",
            "recommendation": "Implement route optimization software to plan efficient delivery routes and establish a preventive maintenance schedule for the delivery fleet to minimize breakdowns"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization is typically caused by poor slotting strategy with fast moving items placed in hard to reach locations, excessive aisle space, or dead stock occupying prime storage areas",
            "recommendation": "Conduct an ABC analysis to slot fast moving items in accessible locations and implement vertical storage solutions to maximize cubic space utilization"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in general warehousing are commonly caused by manual picking without barcode verification, poor product labeling and signage, or inadequate picker training",
            "recommendation": "Implement barcode scanning at point of pick with system verification and improve bin labeling with clear visual indicators to minimize manual picking errors"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover is typically caused by overstocking of slow moving SKUs, poor alignment between purchasing and actual demand, or holding excess safety stock without data justification",
            "recommendation": "Implement demand driven replenishment based on actual consumption data and conduct regular slow moving inventory reviews to prevent capital being tied up in non-moving stock"
        },
        "return_rate": {
            "root_cause": "High returns in general warehousing are commonly caused by incorrect items picked and shipped, damaged goods due to poor packaging, or products shipped past their expiry or shelf life",
            "recommendation": "Implement pre-dispatch quality checks with order verification and improve packaging standards to prevent damage during transit"
        },
        "cost_per_order": {
            "root_cause": "High cost per order is typically caused by inefficient picking routes within the warehouse, excessive overtime due to poor labor planning, or high transportation costs from unoptimized delivery routes",
            "recommendation": "Implement zone or batch picking strategies to reduce picker travel time and optimize staff scheduling based on order volume forecasts to minimize overtime costs"
        }
    },
    "Cold Chain Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in cold chain is typically caused by temperature excursions that render products unsaleable, equipment failures in refrigerated storage, or supplier delays for temperature sensitive products",
            "recommendation": "Install continuous temperature monitoring with automated alerts for excursions and establish backup cold storage arrangements with a third party provider for equipment failure scenarios"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in cold chain are commonly caused by refrigerated vehicle breakdowns, traffic delays extending delivery windows beyond safe temperature limits, or poor route planning for temperature sensitive loads",
            "recommendation": "Implement GPS tracking with temperature monitoring on all refrigerated vehicles and establish contingency delivery protocols for breakdowns including backup vehicle arrangements"
        },
        "warehouse_utilization": {
            "root_cause": "Low cold storage utilization is typically caused by poor product zoning with different temperature requirement products mixed together, inefficient use of vertical space, or excessive space allocated to slow moving products",
            "recommendation": "Segregate products by temperature requirements into dedicated zones and implement vertical racking systems to maximize cubic utilization of expensive cold storage space"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in cold chain are commonly caused by similar looking products stored close together, poor visibility in cold storage environments, or operators rushing to minimize exposure time in freezer areas",
            "recommendation": "Implement voice directed picking systems suitable for cold environments and use color coded product identification to reduce visual confusion between similar products"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in cold chain is typically caused by over-purchasing perishable products relative to actual demand, poor FEFO (First Expired First Out) management, or inaccurate demand forecasting for seasonal products",
            "recommendation": "Implement strict FEFO management with system enforced picking sequences and align purchasing volumes with actual consumption data to minimize waste from expiry"
        },
        "return_rate": {
            "root_cause": "High returns in cold chain are commonly caused by temperature excursions during transit, products delivered past their best before date, or damage to packaging during loading and unloading",
            "recommendation": "Implement end-to-end temperature logging with customer delivery confirmation and strengthen product packaging to withstand cold chain handling conditions"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in cold chain is typically caused by energy intensive refrigeration costs, high maintenance costs for refrigerated vehicles, or small order sizes that make cold chain delivery uneconomical",
            "recommendation": "Consolidate small orders into full vehicle loads by coordinating delivery schedules and invest in energy efficient refrigeration technology to reduce ongoing energy costs"
        }
    },
    "E-commerce Fulfillment": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in e-commerce is typically caused by inventory inaccuracy between the online catalog and physical stock, flash sales creating sudden demand spikes beyond stock levels, or marketplace synchronization errors",
            "recommendation": "Implement real time inventory synchronization across all sales channels and set conservative stock thresholds on marketplaces to avoid overselling beyond available inventory"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in e-commerce are commonly caused by late dispatch from the fulfillment center, last mile delivery failures in remote locations, or courier partner capacity constraints during peak periods",
            "recommendation": "Implement same day dispatch cutoff times with automated order processing and develop relationships with multiple courier partners to ensure capacity during peak demand periods"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in e-commerce fulfillment is typically caused by poor product slotting with high velocity SKUs in inefficient locations, excessive packaging material storage consuming productive space, or poor seasonal inventory planning",
            "recommendation": "Implement velocity based slotting with A-B-C classification and move packaging material storage to a separate area to free up prime picking space for fast moving products"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in e-commerce are commonly caused by similar product variants such as size and color stored in adjacent locations, high picker speed under productivity pressure, or inadequate verification at packing station",
            "recommendation": "Implement scan verify pack systems with mandatory barcode verification at packing stations and use product images on pick lists to help pickers visually confirm correct items"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in e-commerce is typically caused by holding excess safety stock for slow moving SKUs, poor product lifecycle management leading to dead stock, or inaccurate demand forecasting for new product launches",
            "recommendation": "Implement data driven demand forecasting using sales velocity and seasonality data and establish clear dead stock management policies with regular review and clearance cycles"
        },
        "return_rate": {
            "root_cause": "High returns in e-commerce are commonly caused by inaccurate product descriptions and images on the website, sizing issues for apparel and footwear, or damaged products due to inadequate packaging for transit",
            "recommendation": "Enhance product listings with accurate measurements, multiple images, and customer reviews to set correct expectations and strengthen packaging to protect products during courier handling"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in e-commerce is typically caused by high courier charges for low value orders, excessive packaging costs, or high return processing costs eating into margins",
            "recommendation": "Implement minimum order values for free shipping and negotiate volume based courier rates and standardize packaging sizes to reduce material costs and dimensional weight charges"
        }
    },
    "Pharmaceutical Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in pharmaceutical distribution is typically caused by stockouts of critical medicines due to poor demand forecasting, regulatory holds on batches pending quality clearance, or supply disruptions from manufacturers",
            "recommendation": "Maintain strategic safety stock for high demand critical medicines and implement early warning systems for batch quality holds to proactively source alternative stock"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in pharmaceutical distribution are commonly caused by documentation delays for controlled substances, temperature excursions requiring product replacement, or route planning that does not account for hospital and pharmacy opening hours",
            "recommendation": "Streamline documentation processes for controlled substances with pre-cleared paperwork systems and plan delivery routes specifically around customer operating hours and critical delivery windows"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in pharma distribution is typically caused by strict segregation requirements between different product categories consuming excess space, dedicated quarantine areas holding blocked stock, or inefficient use of temperature controlled areas",
            "recommendation": "Optimize warehouse layout to maximize GDP compliant segregation while improving cubic utilization and implement faster batch release processes to reduce time products spend in quarantine"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in pharmaceutical distribution are extremely critical and commonly caused by similar looking drug packaging, multiple strength variants of the same drug stored nearby, or picking under time pressure without adequate verification",
            "recommendation": "Implement mandatory barcode verification for every pick with no override option and use strict segregation of different drug strengths with clear visual differentiation including color coding"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in pharma distribution is typically caused by mandatory minimum stock requirements for essential medicines, long expiry products being overstocked, or slow moving specialty medicines occupying valuable GDP compliant storage space",
            "recommendation": "Implement FEFO picking with automated expiry alerts and work with manufacturers on consignment stock arrangements for slow moving specialty medicines to reduce capital tied up in inventory"
        },
        "return_rate": {
            "root_cause": "High returns in pharmaceutical distribution are commonly caused by products delivered beyond their expiry date, cold chain failures causing product spoilage, or damaged packaging compromising product integrity",
            "recommendation": "Implement strict expiry date management with automated near-expiry alerts and invest in validated cold chain packaging for temperature sensitive products to prevent spoilage during transit"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in pharmaceutical distribution is typically caused by mandatory GDP compliant handling and documentation requirements adding operational overhead, small and frequent orders from pharmacies, or expensive cold chain delivery requirements",
            "recommendation": "Consolidate small pharmacy orders into scheduled delivery routes and invest in GDP compliant automation to reduce manual documentation overhead while maintaining regulatory compliance"
        }
    },
    "Automotive Parts Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in automotive parts distribution is typically caused by the vast SKU range making it difficult to stock all parts, slow moving parts being out of stock when needed, or incorrect part numbers being ordered by dealers",
            "recommendation": "Implement a tiered inventory strategy with fast moving parts stocked locally and slow moving parts available through central warehouse and provide dealers with digital parts catalogs to reduce incorrect ordering"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in automotive parts distribution are commonly caused by service bays waiting for urgent parts, poor route planning for multi-dealer deliveries, or parts arriving damaged requiring replacement shipment",
            "recommendation": "Implement an urgent parts express delivery service for critical repair parts and optimize multi-dealer delivery routes to minimize total delivery time across the dealer network"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in automotive parts distribution is typically caused by bulky parts like bumpers and body panels consuming disproportionate space, slow moving parts occupying prime storage locations, or poor racking design for irregular shaped automotive parts",
            "recommendation": "Implement specialized racking systems for automotive parts including cantilever racks for long parts and bin systems for small parts and relocate slow moving parts to less accessible storage areas"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in automotive parts distribution are critical because wrong parts cause vehicle downtime and are commonly caused by similar looking parts for different vehicle models stored together, or incorrect part number identification by pickers",
            "recommendation": "Implement barcode scanning with VIN cross-reference verification to ensure the correct part for the specific vehicle model is picked and use model year segregation in storage to prevent cross-model picking errors"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in automotive parts is typically caused by stocking excessive quantities of slow moving parts for older vehicle models, poor demand forecasting for seasonal maintenance parts, or overstocking due to minimum order quantities from manufacturers",
            "recommendation": "Implement model year demand analysis to right-size inventory for ageing vehicle models and negotiate lower minimum order quantities with manufacturers for slow moving specialty parts"
        },
        "return_rate": {
            "root_cause": "High returns in automotive parts distribution are commonly caused by incorrect parts ordered due to vehicle model year confusion, parts damaged during transit due to inadequate packaging for heavy metal components, or quality issues with aftermarket parts",
            "recommendation": "Implement a parts compatibility verification system at order entry and use purpose designed packaging for different part categories to prevent damage during transit"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in automotive parts distribution is typically caused by urgent same-day deliveries for breakdown situations, high packaging costs for bulky and heavy parts, or inefficient small order deliveries to individual service bays",
            "recommendation": "Establish scheduled delivery windows for non-urgent parts and implement an express fee for urgent breakdown deliveries to recover the additional cost of priority service"
        }
    },
    "Electronics Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in electronics distribution is typically caused by new product launches creating demand spikes beyond allocated inventory, grey market diversion reducing official channel stock, or long import lead times for components and finished goods",
            "recommendation": "Implement channel inventory allocation systems to protect stock for authorized distributors and develop accurate launch demand forecasts with manufacturer collaboration to secure adequate opening stock"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in electronics distribution are commonly caused by seasonal demand spikes during festive seasons overwhelming logistics capacity, customs clearance delays for imported products, or damage discovered at delivery requiring replacement",
            "recommendation": "Build logistics capacity ahead of seasonal peaks through advance booking with courier partners and streamline customs documentation processes to minimize clearance delays for imported electronics"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in electronics distribution is typically caused by bulky display units and packaging consuming excessive space, dedicated secure storage for high value products reducing overall utilization, or poor seasonal inventory planning leaving excess space during low demand periods",
            "recommendation": "Implement high density storage solutions for boxed electronics and optimize secure storage areas for high value products to balance security with space efficiency"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in electronics distribution are costly due to high product values and are commonly caused by similar model numbers for different product variants stored adjacently, high value products being rushed through without adequate verification, or inadequate lighting in storage areas",
            "recommendation": "Implement mandatory dual verification for high value electronics picks with a checker system and improve warehouse lighting and product identification labeling to minimize confusion between similar models"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in electronics is typically caused by holding obsolete models when new versions are launched, overstocking based on optimistic sales forecasts, or slow clearance of demonstration and display units",
            "recommendation": "Implement structured product lifecycle management with clear end of life policies and establish a demo unit rotation program to prevent display stock from ageing in the warehouse"
        },
        "return_rate": {
            "root_cause": "High returns in electronics distribution are commonly caused by transit damage to fragile products, products with cosmetic defects reaching customers, or technical failures discovered during customer setup",
            "recommendation": "Implement pre-dispatch functional testing for all electronics and use custom foam-fitted packaging for fragile products to prevent transit damage"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in electronics distribution is typically caused by high insurance and security costs for valuable products, specialized handling requirements, or expensive reverse logistics for returned electronics",
            "recommendation": "Optimize insurance costs through better security measures and implement an efficient reverse logistics process for returns with refurbishment capability to recover value from returned products"
        }
    },
    "Food and Beverage Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in FMCG distribution is typically caused by stockouts of high demand SKUs during promotional periods, forecasting failures for new product launches, or supply disruptions from manufacturers during peak seasons",
            "recommendation": "Build collaborative demand planning with key retailers to anticipate promotional spikes and maintain strategic safety stock for top selling SKUs to ensure availability during demand surges"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in food and beverage distribution are commonly caused by traffic congestion in urban delivery areas, retail outlets with strict delivery time windows, or vehicle capacity constraints requiring multiple trips",
            "recommendation": "Schedule deliveries during off-peak traffic hours where possible and optimize vehicle load planning to maximize drop size per trip and minimize the number of vehicles required"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in FMCG distribution is typically caused by excess safety stock held for promotional events, inefficient storage of promotional display materials, or poor slotting of high velocity SKUs requiring frequent replenishment",
            "recommendation": "Implement demand-driven inventory replenishment to reduce excess safety stock and slot high velocity SKUs in ground floor accessible locations to minimize replenishment time and travel"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in FMCG distribution are commonly caused by similar packaging across different product variants, high picking speeds driven by volume targets, or poor visibility of product date codes leading to incorrect FEFO picking",
            "recommendation": "Implement scan based picking with FEFO enforcement at system level and display product images on pick lists to help pickers distinguish between similar looking product variants"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in food distribution is typically caused by overstocking of slow moving SKUs, poor management of near-expiry products, or misalignment between purchasing quantities and actual retail offtake",
            "recommendation": "Implement weekly inventory reviews with near-expiry alerts and align purchasing cycles tightly with actual point-of-sale data from key retail partners to minimize overstocking"
        },
        "return_rate": {
            "root_cause": "High returns in food and beverage distribution are commonly caused by products delivered near expiry that retailers cannot sell in time, damaged products from rough handling during loading and unloading, or temperature abuse causing quality deterioration",
            "recommendation": "Enforce minimum remaining shelf life standards at point of dispatch and train delivery teams on proper handling techniques to minimize product damage during the distribution process"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in FMCG distribution is typically caused by small and fragmented kirana store orders requiring frequent low volume deliveries, high fuel costs from unoptimized routes, or excessive handling costs for loose case picking",
            "recommendation": "Implement minimum order value policies for direct delivery and consolidate small orders through redistribution stockists to improve delivery economics in fragmented retail markets"
        }
    },
    "Textile and Apparel Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in textile distribution is typically caused by size run availability issues where certain sizes stock out faster than others, seasonal collection launches creating temporary supply shortfalls, or poor inventory visibility across multiple warehouse locations",
            "recommendation": "Implement size ratio analysis based on historical sales data to optimize buying ratios across the size curve and maintain centralized inventory visibility across all distribution points"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in textile distribution are commonly caused by seasonal peaks around festivals and fashion seasons overwhelming logistics capacity, complex multi-location deliveries to retail chains, or garment finishing delays at the warehouse level",
            "recommendation": "Build delivery capacity ahead of seasonal peaks through advance logistics booking and complete all garment finishing and tagging at the manufacturing stage to eliminate warehouse finishing delays"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in textile distribution is typically caused by bulky seasonal inventory occupying space between seasons, hanging garment storage being space inefficient compared to folded storage, or end of season unsold stock accumulating in prime storage areas",
            "recommendation": "Implement seasonal inventory rotation with off-site storage for between-season stock and evaluate converting hanging storage to folded storage where garment type permits to improve space efficiency"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in textile distribution are commonly caused by similar styles in different sizes and colors stored together, manual picking of loose garments without barcode verification, or mislabeled products from the supplier",
            "recommendation": "Implement barcode scanning for all garment picks with style-size-color verification and conduct incoming quality checks on supplier labeling to catch mislabeling before products enter the warehouse"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in textile is typically caused by seasonal merchandise that does not sell through, poor trend forecasting leading to over-buying of slow styles, or end of season stock being held at full price beyond optimal clearance timing",
            "recommendation": "Implement open-to-buy planning with regular sell-through analysis and establish clear markdown calendars for end of season clearance to accelerate inventory turnover before the next season"
        },
        "return_rate": {
            "root_cause": "High returns in textile distribution are commonly caused by sizing inconsistency between batches, color variations between online product images and actual products, or fabric quality issues not caught during incoming inspection",
            "recommendation": "Implement standardized size measurements with tolerance controls and conduct incoming quality inspections including color fastness testing before accepting stock into the warehouse"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in textile distribution is typically caused by high reverse logistics costs for returned garments requiring inspection and reprocessing, expensive hanging garment transportation, or complex multi-size order picking with high error rates",
            "recommendation": "Implement efficient returns processing with clear accept-reject criteria and evaluate folded garment transportation instead of hanging where feasible to reduce transportation costs"
        }
    },
    "Eco Friendly Packaging Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in eco packaging distribution is typically caused by production lead time variability for custom molded products, raw material shortages affecting production schedules, or longer order to delivery cycles for made-to-order sustainable packaging",
            "recommendation": "Maintain buffer stock of standard product lines and implement reliable production planning systems to ensure customer orders can be fulfilled within committed lead times"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in eco packaging distribution are commonly caused by production delays affecting dispatch schedules, bulky and fragile nature of molded pulp products requiring special handling, or transport damage requiring replacement shipments",
            "recommendation": "Build production buffer ahead of delivery commitments and use specialized protective packaging and handling procedures to prevent damage to fragile eco packaging products during transit"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in eco packaging distribution is typically caused by bulky and lightweight molded pulp products occupying large volumes relative to their weight, nested stacking limitations for certain product shapes, or moisture sensitivity requiring ventilated storage",
            "recommendation": "Optimize storage layout for efficient nesting and stacking of eco packaging products and ensure adequate ventilation to prevent moisture damage in storage"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in eco packaging distribution are commonly caused by similar looking products for different applications stored together, custom products with subtle specification differences being mixed, or inadequate product identification labeling on similar looking cartons",
            "recommendation": "Implement clear product identification with customer specific labeling and store custom products in dedicated locations with visual identification to prevent mix-ups between similar specifications"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in eco packaging is typically caused by holding excess stock of slow moving custom specifications, seasonal demand variations for agricultural product packaging, or overstocking based on optimistic customer forecast commitments",
            "recommendation": "Implement customer managed inventory programs for large accounts and align stock levels with confirmed customer orders rather than forecast commitments for custom products"
        },
        "return_rate": {
            "root_cause": "High returns in eco packaging distribution are commonly caused by moisture damage during transit or storage causing product distortion, dimensional inconsistencies affecting fit with customer products, or products not meeting sustainability certifications as specified",
            "recommendation": "Implement moisture resistant transit packaging and conduct pre-dispatch dimensional checks to ensure products meet customer specifications before shipment"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in eco packaging distribution is typically caused by high volume to weight ratio making transportation expensive on a per unit basis, custom product handling requirements, or small order sizes for niche eco packaging products",
            "recommendation": "Consolidate orders from multiple customers for similar products onto shared transport loads and establish minimum order quantities to ensure delivery economics are viable for custom eco packaging products"
        }
    },
    "Pulp and Paper Distribution": {
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in pulp and paper distribution is typically caused by production allocation shortfalls during peak demand, specific grade and quality requirements not available in stock, or long lead times for specialty paper grades made to order",
            "recommendation": "Maintain stocking programs for standard grades with committed inventory levels and develop forward order programs with customers for specialty grades to plan production in advance"
        },
        "on_time_delivery": {
            "root_cause": "Late deliveries in pulp and paper distribution are commonly caused by heavy reels and large paper rolls requiring specialized transport, loading and unloading delays at customer sites without adequate handling equipment, or traffic restrictions for heavy vehicles in urban areas",
            "recommendation": "Coordinate delivery scheduling with customers to ensure adequate unloading equipment is available and plan heavy vehicle routes to avoid restricted urban areas and peak traffic periods"
        },
        "warehouse_utilization": {
            "root_cause": "Low warehouse utilization in paper distribution is typically caused by heavy paper reels requiring reinforced flooring limiting storage height, large sheet sizes requiring wide aisle spacing, or moisture sensitive products requiring controlled humidity storage",
            "recommendation": "Invest in specialized paper reel storage systems with adequate floor load capacity and implement humidity and temperature controlled storage to protect paper quality"
        },
        "picking_accuracy": {
            "root_cause": "Picking errors in paper distribution are commonly caused by similar looking products with different GSM weights or surface finishes stored together, grade and quality specification confusion for specialty papers, or incorrect quantity picking for bulk orders",
            "recommendation": "Implement clear grade labeling with GSM and specification details on all storage locations and use weight verification at dispatch to confirm correct quantities for bulk paper orders"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in paper distribution is typically caused by holding large safety stock for commodity grades due to supply variability, slow moving specialty grades tying up capital, or seasonal demand patterns not reflected in purchasing plans",
            "recommendation": "Implement consignment stock arrangements with mills for slow moving specialty grades and align commodity grade purchasing with actual monthly consumption data to reduce excess inventory"
        },
        "return_rate": {
            "root_cause": "High returns in paper distribution are commonly caused by moisture damage during transit causing paper to warp or cockle, physical damage to reels or sheet edges during handling, or quality inconsistencies between production batches",
            "recommendation": "Implement moisture resistant wrapping for all paper products in transit and use specialized reel and sheet handling equipment to prevent physical damage during loading and delivery"
        },
        "cost_per_order": {
            "root_cause": "High cost per order in paper distribution is typically caused by high transportation costs for heavy paper products, specialized handling equipment requirements, or small order quantities that are uneconomical to deliver given the transport weight constraints",
            "recommendation": "Implement minimum order weight thresholds for direct delivery and consolidate small orders onto shared vehicles to improve transportation economics for paper distribution"
        }
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

def show_distribution(industry, currency_symbol="$"):
    benchmarks = distribution_benchmarks[industry]
    insights = distribution_insights[industry]

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

    # Custom Root Causes and Recommendations
    st.header("What is Wrong and How to Fix It")
    st.caption(f"Customized analysis for {industry}")

    root_causes = []
    recommendations = []
    improvements = {}

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["order_fulfillment_rate"]["root_cause"])
        recommendations.append(insights["order_fulfillment_rate"]["recommendation"])
        improvements["order_fulfillment_rate"] = min(benchmarks["order_fulfillment_rate"], order_fulfillment_rate + 5)

    if analysis["on_time_delivery"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["on_time_delivery"]["root_cause"])
        recommendations.append(insights["on_time_delivery"]["recommendation"])
        improvements["on_time_delivery"] = min(benchmarks["on_time_delivery"], on_time_delivery + 5)

    if analysis["warehouse_utilization"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["warehouse_utilization"]["root_cause"])
        recommendations.append(insights["warehouse_utilization"]["recommendation"])
        improvements["warehouse_utilization"] = min(benchmarks["warehouse_utilization"], warehouse_utilization + 8)

    if analysis["picking_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["picking_accuracy"]["root_cause"])
        recommendations.append(insights["picking_accuracy"]["recommendation"])
        improvements["picking_accuracy"] = min(benchmarks["picking_accuracy"], picking_accuracy + 2)

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["inventory_turnover"]["root_cause"])
        recommendations.append(insights["inventory_turnover"]["recommendation"])
        improvements["inventory_turnover"] = min(benchmarks["inventory_turnover"], inventory_turnover + 3)

    if analysis["return_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["return_rate"]["root_cause"])
        recommendations.append(insights["return_rate"]["recommendation"])
        improvements["return_rate"] = max(benchmarks["return_rate"], return_rate - 2)

    if analysis["cost_per_order"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["cost_per_order"]["root_cause"])
        recommendations.append(insights["cost_per_order"]["recommendation"])
        improvements["cost_per_order"] = max(benchmarks["cost_per_order"], cost_per_order - 10)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Why is this happening?")
        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.success("No critical issues detected!")

    with col2:
        st.subheader("What should you do?")
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("Distribution is performing at benchmark level!")

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
                    <span style="color: #888888; margin-left: 10px;">Current: {result['value']:.3f} | Target: {result['benchmark']:.3f}</span>
                </div>
            """, unsafe_allow_html=True)
            priority_rank += 1

    st.divider()

    # Before vs After
    st.header("Where You Are vs Where You Could Be")
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