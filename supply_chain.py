import streamlit as st
import plotly.graph_objects as go

# Industry Specific Benchmarks for Supply Chain
# Sources:
# Automotive: Tata Motors, Maruti Suzuki, Mahindra supplier standards
# Food and Beverage: HUL, Nestle India, ITC FMCG supply chain standards
# Electronics: Dixon Technologies, Foxconn India, PLI scheme benchmarks
# General: APICS India chapter benchmarks, CII supply chain reports
# Pharmaceutical: FDA Green List initiative, CDSCO GDP guidelines
# Textile and Apparel: Raymond, Arvind Mills, Deloitte Apparel Pulse 2025
# Eco Friendly Packaging: UFlex, ITC Packaging, BIS EcoMark standards
# Pulp and Paper: JK Paper, TNPL, ISO 9001 and FSC certification standards

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
        # Based on Raymond, Arvind Mills, Deloitte Apparel and Footwear Pulse 2025
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
        # Based on UFlex, ITC Packaging, BIS EcoMark certification standards
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
        # Based on JK Paper, TNPL, Kuantum Papers — ISO 9001 and FSC standards
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

# Custom root causes and recommendations per supply chain industry
supply_chain_insights = {
    "Automotive Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in automotive is typically caused by tier 2 and tier 3 supplier capacity constraints, semiconductor and electronic component shortages, or just-in-time scheduling failures when any link in the chain is disrupted",
            "recommendation": "Implement supplier tiering visibility beyond tier 1 to identify risk at tier 2 and tier 3 levels and develop dual sourcing strategies for critical electronic and semiconductor components"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in automotive supply chains is typically caused by holding excess safety stock due to supply uncertainty, long production run scheduling creating bulk inventory, or poor demand signal sharing between OEM and suppliers",
            "recommendation": "Implement demand signal sharing through a supplier portal connecting OEM production schedules directly to supplier planning systems to enable synchronized inventory management"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in automotive supply chains is commonly caused by component shortages stopping production, quality holds on incoming supplier batches, or logistics delays disrupting the just-in-time delivery schedule",
            "recommendation": "Develop a real time supply chain visibility platform tracking component availability from supplier through to production line and establish contingency protocols for critical component shortages"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in automotive is typically caused by volatile consumer demand for specific vehicle models, sudden market shifts toward EVs affecting traditional component demand, or dealer ordering patterns not reflecting actual end consumer demand",
            "recommendation": "Implement collaborative forecasting with dealers using point-of-sale data and develop rolling 12 month demand plans with weekly updates to improve accuracy at the supplier scheduling level"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in automotive are commonly caused by premium freight charges for urgent component delivery, high inventory holding costs for safety stock, or inefficient inbound logistics with multiple small shipments",
            "recommendation": "Implement milk run inbound logistics to consolidate supplier deliveries and reduce premium freight by improving supply chain visibility and early warning systems for potential shortages"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in automotive is typically caused by long supplier lead times requiring extended safety stock, production scheduling in large batches, or poor inventory visibility leading to precautionary over-stocking",
            "recommendation": "Work with key suppliers to reduce lead times through capacity reservation agreements and implement kanban based replenishment for high volume standard components to reduce inventory days"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in automotive is commonly caused by inadequate incoming quality inspection, supplier process capability issues not caught during supplier approval, or specification changes not properly communicated to suppliers",
            "recommendation": "Implement supplier quality development programs with regular audits and process capability assessments and establish a formal engineering change management process to ensure specification changes reach all affected suppliers"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in automotive supply chains is typically caused by suppliers operating at full capacity with no buffer, single source dependencies with no alternative supplier, or long tooling changeover times at supplier plants",
            "recommendation": "Negotiate capacity reservation agreements with key suppliers for surge scenarios and develop approved alternate suppliers for critical components to enable flexible sourcing when needed"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in automotive is commonly caused by single source dependencies for proprietary components, geographic concentration of suppliers creating regional disruption risk, or long qualification times for new suppliers",
            "recommendation": "Accelerate supplier diversification by maintaining qualified alternate suppliers for at least 70% of critical components and expand supplier base geographically to reduce regional concentration risk"
        }
    },
    "Food and Beverage Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in food supply chains is typically caused by agricultural raw material availability depending on seasonal harvests, supplier capacity constraints during peak production periods, or transport disruptions for perishable ingredients",
            "recommendation": "Develop long term supply agreements with multiple agricultural suppliers across different growing regions to reduce seasonal supply risk and establish priority logistics arrangements for perishable ingredients"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in food supply chains is typically caused by overstocking of raw materials due to seasonal availability concerns, poor alignment between purchasing and production scheduling, or slow moving finished goods in distribution",
            "recommendation": "Implement demand driven purchasing aligned with production schedules and establish consignment stock arrangements with key ingredient suppliers to reduce owned inventory while maintaining supply security"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in FMCG supply chains is commonly caused by promotional demand spikes not anticipated in supply planning, packaging material shortages delaying finished goods production, or quality holds on incoming raw materials",
            "recommendation": "Implement collaborative planning forecasting and replenishment (CPFR) with key retail customers to better anticipate demand and maintain strategic packaging material buffer stock for top selling SKUs"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in food supply chains is typically caused by unpredictable impact of promotions on demand, seasonal consumption patterns not adequately modeled, or new product launches with no sales history to base forecasts on",
            "recommendation": "Implement statistical forecasting with promotional uplift modeling and develop post-promotion analysis to continuously improve forecast accuracy for future promotional events"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in food and beverage are commonly caused by refrigerated transport for temperature sensitive ingredients, high wastage costs from perishable raw material losses, or inefficient small lot purchasing from multiple suppliers",
            "recommendation": "Consolidate purchasing volumes with fewer strategic suppliers to improve buying power and reduce logistics costs and implement better demand planning to reduce perishable ingredient waste"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in food supply chains is typically caused by bulk purchasing of non-perishable ingredients to take advantage of seasonal pricing, poor FEFO management leading to slow stock rotation, or excess finished goods inventory from inaccurate production planning",
            "recommendation": "Implement FEFO based inventory management with automated alerts for near expiry materials and align finished goods production more closely with confirmed retail orders to reduce inventory days"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in food supply chains is critically important and commonly caused by inadequate food safety controls at supplier level, contamination risks from poor hygiene practices, or raw material adulteration and quality fraud",
            "recommendation": "Implement mandatory FSSC 22000 or equivalent food safety certification for all food ingredient suppliers and conduct regular unannounced audits with microbiological and chemical testing of incoming materials"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in food supply chains is typically caused by agricultural production cycles that cannot be accelerated, long manufacturing lead times for specialty ingredients, or regulatory approval requirements for new ingredient suppliers",
            "recommendation": "Develop a portfolio of pre-approved alternate suppliers for key ingredients and maintain strategic safety stock for ingredients with inherently long or inflexible lead times"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in food supply chains is commonly caused by limited alternate sources for specialty or proprietary ingredients, regional concentration of agricultural raw material production, or regulatory restrictions on ingredient sourcing",
            "recommendation": "Map ingredient sourcing across multiple geographic regions and develop relationships with suppliers in alternative growing regions to reduce single geography dependency for key raw materials"
        }
    },
    "Electronics Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in electronics supply chains is typically caused by semiconductor shortages with long allocation lead times, geopolitical tensions disrupting component imports from Asia, or demand surges outpacing supplier capacity",
            "recommendation": "Implement long term purchase agreements with semiconductor suppliers to secure allocation priority and develop supply chain risk monitoring for geopolitical developments affecting key sourcing regions"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in electronics supply chains is typically caused by holding large safety stock of long lead time components, product obsolescence risk from rapid technology changes, or overstocking based on optimistic demand forecasts",
            "recommendation": "Implement component lifecycle management to proactively identify and reduce end-of-life component inventory and use demand driven replenishment for standard components to minimize excess stock"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in electronics supply chains is commonly caused by single source component dependencies creating vulnerability, quality failures at incoming inspection, or production holds due to component compatibility issues",
            "recommendation": "Accelerate alternate component qualification to reduce single source dependencies for critical components and implement advanced incoming quality inspection with automated testing equipment"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in electronics supply chains is typically caused by short product lifecycle making historical data less relevant, rapid demand shifts driven by technology trends, or channel inventory dynamics hiding true end user demand",
            "recommendation": "Implement sell-through based demand sensing using point-of-sale data from retail partners and develop scenario based planning for technology transition periods to improve forecast accuracy"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in electronics are commonly caused by air freight for urgent component deliveries, high customs and import duties on electronic components, or expensive quality testing requirements for electronic components",
            "recommendation": "Shift from air to sea freight for non-urgent components through better demand planning and explore duty optimization through free trade zone arrangements and import duty drawback schemes"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in electronics supply chains is typically caused by long import lead times requiring extended safety stock, component minimum order quantities exceeding actual consumption, or slow moving components for discontinued product lines",
            "recommendation": "Negotiate smaller minimum order quantities with distributors for slow moving components and implement a proactive excess and obsolete inventory management process to reduce stranded component inventory"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in electronics is commonly caused by counterfeit components entering the supply chain through unauthorized distributors, solder quality issues from PCB suppliers, or specification deviations in electronic components from unqualified sources",
            "recommendation": "Mandate purchasing from authorized distributors only with component traceability requirements and implement incoming testing for critical electronic components to detect counterfeits and specification deviations"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in electronics supply chains is typically caused by semiconductor fabs with 12 to 26 week lead times that cannot be shortened, single source proprietary components with no alternate, or long PCB fabrication lead times",
            "recommendation": "Implement a hub and spoke inventory model with buffer stock of long lead time components and develop close relationships with distributors who maintain their own inventory of critical components"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in electronics is commonly caused by geographic concentration of semiconductor manufacturing in Taiwan and South Korea creating regional risk, few qualified alternates for specialty components, or high qualification costs for new suppliers",
            "recommendation": "Actively pursue qualification of alternate suppliers for critical components especially those geographically concentrated and participate in industry consortiums that facilitate faster alternate supplier qualification"
        }
    },
    "General Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery is typically caused by supplier capacity constraints, poor communication of order requirements, or logistical delays in inbound transportation",
            "recommendation": "Implement supplier scorecards with on time delivery tracking and develop collaborative planning with key suppliers to align their capacity with your demand requirements"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover is typically caused by overstocking due to inaccurate demand forecasting, poor inventory visibility leading to precautionary ordering, or slow moving items accumulating without management review",
            "recommendation": "Implement regular inventory reviews with ABC classification and develop demand driven replenishment to align purchasing with actual consumption rather than fixed reorder cycles"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment is commonly caused by stockouts from inaccurate demand forecasting, supplier delivery failures, or internal process delays in order processing and picking",
            "recommendation": "Implement real time inventory visibility with automated reorder triggers and develop supplier delivery reliability improvement programs with clear performance expectations"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy is typically caused by reliance on gut feel rather than data, poor collaboration with customers on their demand plans, or inadequate statistical forecasting tools",
            "recommendation": "Implement statistical demand forecasting using historical sales data and seasonal patterns and establish regular demand review meetings with key customers to improve forecast inputs"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs are commonly caused by inefficient transportation with low vehicle utilization, high inventory holding costs from excess stock, or expensive emergency procurement to cover shortfalls",
            "recommendation": "Optimize transportation loads to maximize vehicle utilization and reduce excess inventory through better demand planning to lower holding costs and eliminate emergency procurement premium costs"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory outstanding is typically caused by long supplier lead times requiring large safety stock, poor demand visibility causing precautionary overstocking, or slow moving items not being identified and cleared",
            "recommendation": "Work with suppliers to reduce lead times and implement a regular slow moving inventory review process with clear action plans for clearance or return to supplier"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality rate is commonly caused by inadequate supplier qualification processes, lack of incoming quality inspection, or poor specification communication to suppliers",
            "recommendation": "Implement a formal supplier qualification process with quality audits and establish incoming inspection standards for critical materials with clear acceptance criteria"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility is typically caused by suppliers operating at capacity with no surge capability, single source dependencies, or long changeover times at supplier facilities",
            "recommendation": "Develop capacity reservation agreements with key suppliers for surge scenarios and maintain pre-qualified alternate suppliers for critical items to enable flexible sourcing"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility is commonly caused by over-reliance on single suppliers for critical items, lack of alternate supplier qualification, or geographic concentration creating regional disruption risk",
            "recommendation": "Implement a dual sourcing strategy for all critical materials and actively qualify alternate suppliers to ensure at least one backup option is available for every key item"
        }
    },
    "Pharmaceutical Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in pharmaceutical supply chains is typically caused by API manufacturers facing regulatory inspections and facility shutdowns, single source API suppliers from China or specific regions creating concentration risk, or long fermentation and synthesis lead times for biological APIs",
            "recommendation": "Dual source all critical APIs across different geographic regions and engage with API suppliers on capacity reservation agreements to ensure priority supply during industry wide shortages"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in pharma supply chains is typically caused by mandatory safety stock requirements for essential medicines, long API synthesis lead times requiring extended raw material inventory, or stability testing requirements holding finished goods before release",
            "recommendation": "Implement risk-based safety stock optimization that balances regulatory requirements with inventory efficiency and use rolling stability testing programs to reduce finished goods hold times"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in pharmaceutical supply chains is commonly caused by API shortages disrupting production schedules, batch failures requiring replacement production, or regulatory holds on product batches pending quality clearance",
            "recommendation": "Implement a supply risk monitoring system for critical APIs and develop contingency production plans for batch failure scenarios to minimize impact on product availability"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in pharma supply chains is typically caused by tender based demand that is unpredictable in timing and volume, seasonal disease patterns affecting OTC medicine demand, or new product launches with no historical demand data",
            "recommendation": "Implement epidemiological modeling for seasonal disease products and develop close collaboration with government procurement agencies on tender timing to improve demand visibility"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in pharmaceutical supply chains are commonly caused by expensive cold chain logistics for temperature sensitive products, high quality testing costs for incoming materials, or regulatory compliance overhead throughout the supply chain",
            "recommendation": "Optimize cold chain logistics through route consolidation and invest in GDP compliant hub and spoke distribution models to reduce the per unit cost of temperature controlled distribution"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in pharma supply chains is typically caused by long API synthesis lead times requiring extended safety stock, mandatory quarantine periods for incoming materials pending quality release, or regulatory requirements to maintain minimum stock levels for essential medicines",
            "recommendation": "Work with API suppliers to implement real time batch status sharing to reduce quarantine uncertainty and implement risk-based testing to accelerate quality release for materials from trusted suppliers"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality rate in pharmaceutical supply chains is extremely serious and commonly caused by API contamination from inadequate manufacturing controls, data integrity failures in supplier quality documentation, or deviations from registered manufacturing processes",
            "recommendation": "Implement mandatory GMP certification for all API suppliers with regular audits and establish real time quality data sharing with key API suppliers through electronic quality management systems"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in pharma supply chains is typically caused by long API synthesis cycles that cannot be shortened, regulatory approval requirements before changing suppliers or manufacturing sites, or specialized equipment requirements limiting surge capacity",
            "recommendation": "Maintain pre-approved alternate manufacturing sites for critical products and work with regulators on expedited approval pathways for supply emergency scenarios"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in pharmaceutical supply chains is critically important and commonly caused by single source APIs from geographically concentrated regions, lengthy regulatory approval required for new API suppliers, or proprietary synthesis processes limiting the supplier pool",
            "recommendation": "Invest in proactive alternate supplier qualification including regulatory filing for alternate API sources and participate in industry initiatives to reduce regulatory timelines for alternate supplier approval in supply emergency scenarios"
        }
    },
    "Textile and Apparel Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in textile supply chains is typically caused by yarn and fabric suppliers facing power shortages at manufacturing clusters, seasonal labour availability issues at garment supplier factories, or customs delays for imported specialty fabrics and trims",
            "recommendation": "Develop supplier partnerships with on-site capacity monitoring and implement buffer stock programs for imported specialty materials with long and unpredictable lead times"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in textile supply chains is typically caused by seasonal collection buying with long lead times resulting in large upfront inventory commitments, poor sell-through of certain styles leading to end of season markdowns, or excess fabric and trim inventory from over-buying",
            "recommendation": "Implement open-to-buy planning disciplines with regular sell-through reviews and adopt nearshoring strategies for a portion of production to enable faster replenishment of proven sellers"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in textile supply chains is commonly caused by fabric availability constraints delaying garment production, quality rejections of incoming fabric causing production holds, or size ratio imbalances in production output not matching retail demand",
            "recommendation": "Implement fabric inventory management at the supplier level with visibility into fabric availability before committing production orders and strengthen incoming fabric quality inspection to prevent production holds"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in textile supply chains is typically caused by fast changing fashion trends making historical data less relevant, difficulty predicting colour and style preferences by region, or wholesale buyer order patterns not reflecting actual consumer demand",
            "recommendation": "Implement data analytics using social media trend monitoring and early season sell-through data to improve demand forecasting and reduce commitment to styles before reading market signals"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in textile are commonly caused by long sourcing lead times requiring air freight for late orders, high inventory holding costs for seasonal collections, or expensive reverse logistics for high return rate fashion products",
            "recommendation": "Develop a nearshoring strategy for fast fashion replenishment to reduce air freight dependency and implement efficient returns processing with refurbishment and redistribution capability"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in textile supply chains is typically caused by long 3 to 6 month sourcing lead times requiring large advance inventory commitments, end of season unsold inventory requiring clearance, or excess fabric inventory from inaccurate production planning",
            "recommendation": "Reduce sourcing lead times through supplier development programs and implement a fabric platforming strategy where common base fabrics are held at supplier level for rapid commitment on receiving orders"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in textile supply chains is commonly caused by colour fastness failures from inadequate dyeing process controls, dimensional inconsistencies from poor pattern grading, or fabric defects not caught at the mill level reaching garment production",
            "recommendation": "Implement third party quality inspection at fabric mill level before shipment and establish clear quality standards with photographic references and tolerance limits for all critical quality parameters"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in textile supply chains is typically caused by long fabric weaving and dyeing lead times that are difficult to compress, supplier factories running at full capacity with no surge capability, or import lead times for specialty trims and accessories",
            "recommendation": "Develop a fabric platforming program with key suppliers to hold greige fabric ready for rapid dyeing and finishing on demand and identify nearshore suppliers for fast turnaround replenishment orders"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in textile supply chains is commonly caused by geographic concentration of production in specific regions like Bangladesh or Vietnam creating regional disruption risk, long supplier qualification lead times, or proprietary fabric developments limiting alternate sourcing",
            "recommendation": "Diversify production across multiple geographic regions including India, Vietnam and Bangladesh and develop a portfolio of qualified suppliers at each production tier to enable rapid reallocation when needed"
        }
    },
    "Eco Friendly Packaging Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in eco packaging supply chains is typically caused by seasonal availability of agricultural raw materials like bagasse and wheat straw, long certification lead times for new sustainable material suppliers, or small supplier scale limiting production capacity and delivery reliability",
            "recommendation": "Develop long term supply agreements with multiple certified sustainable raw material suppliers across different agricultural regions and build buffer stock for seasonal agricultural materials"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in eco packaging supply chains is typically caused by longer production lead times for custom molded sustainable products, minimum order quantities from sustainable material suppliers exceeding actual consumption, or slow market adoption leading to excess finished product inventory",
            "recommendation": "Implement modular product design to enable standard components across multiple customer applications and negotiate flexible order quantities with sustainable material suppliers to match actual consumption"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in eco packaging supply chains is commonly caused by raw material supply variability from agricultural sources, production yield variability for natural materials compared to synthetic alternatives, or custom product lead times not aligned with customer ordering patterns",
            "recommendation": "Maintain buffer stock of standard eco packaging products and implement rapid response production capability for custom orders with clear lead time commitments to customers"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in eco packaging supply chains is typically caused by rapid and unpredictable growth in demand as companies switch from plastic to sustainable alternatives, new customer onboarding with uncertain initial volumes, or regulatory changes suddenly accelerating or decelerating demand",
            "recommendation": "Develop close relationships with key customers to understand their plastic replacement timelines and implement scalable production capacity that can ramp quickly as sustainable packaging adoption accelerates"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in eco packaging supply chains are commonly caused by higher raw material costs for certified sustainable materials compared to conventional materials, smaller production volumes limiting economies of scale, or premium transportation costs for bulky low density eco packaging products",
            "recommendation": "Drive raw material cost reduction through volume aggregation across customers and invest in process efficiency improvements to reduce the cost premium of sustainable packaging production"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in eco packaging supply chains is typically caused by long agricultural raw material procurement cycles requiring extended safety stock, custom product inventory that cannot be sold to alternate customers, or slow market penetration leaving finished goods inventory unsold",
            "recommendation": "Implement consignment stock arrangements with agricultural material suppliers to reduce owned raw material inventory and focus product standardization to enable inventory to be shared across multiple customers"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in eco packaging supply chains is commonly caused by inconsistent agricultural raw material quality between harvests, lack of standardized quality specifications for sustainable materials, or small suppliers lacking quality management systems",
            "recommendation": "Develop detailed raw material quality specifications with acceptable variation limits and provide quality management system development support to key sustainable material suppliers"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in eco packaging supply chains is typically caused by agricultural raw material availability tied to harvest seasons, custom mold lead times for new product designs, or small supplier scale limiting surge production capability",
            "recommendation": "Invest in standard mold tooling for common product formats to enable rapid production switching and develop contingency raw material sourcing from alternate agricultural regions"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in eco packaging supply chains is commonly caused by limited number of certified sustainable material suppliers in India, geographic concentration of agricultural raw material production, or specific certification requirements limiting the eligible supplier pool",
            "recommendation": "Actively develop and certify alternate sustainable material suppliers and explore multiple agricultural raw material types that can serve as substitutes to increase sourcing flexibility"
        }
    },
    "Pulp and Paper Supply Chain": {
        "supplier_otd": {
            "root_cause": "Low supplier on time delivery in pulp and paper supply chains is typically caused by wood and recycled fiber availability fluctuations, long pulp production cycles at integrated mills, or shipping delays for imported pulp and specialty chemicals",
            "recommendation": "Develop long term wood and recycled fiber supply agreements with multiple suppliers and maintain strategic pulp inventory to buffer against supply disruptions"
        },
        "inventory_turnover": {
            "root_cause": "Low inventory turnover in pulp and paper supply chains is typically caused by long pulp procurement lead times requiring large raw material inventory, bulk chemical purchasing creating excess stock, or finished goods inventory accumulating when market demand slows",
            "recommendation": "Implement demand driven pulp procurement aligned with paper machine production schedules and optimize chemical purchasing cycles to reduce inventory days while maintaining supply security"
        },
        "order_fulfillment_rate": {
            "root_cause": "Low order fulfillment in pulp and paper supply chains is commonly caused by pulp shortages affecting production schedules, paper machine downtime reducing output below committed volumes, or quality failures requiring reprocessing before shipment",
            "recommendation": "Implement pulp supply risk monitoring with contingency sourcing arrangements and improve paper machine reliability through predictive maintenance to consistently achieve production targets"
        },
        "forecast_accuracy": {
            "root_cause": "Low forecast accuracy in pulp and paper supply chains is typically caused by commodity market price volatility driving speculative buying behavior, cyclical demand patterns in the printing and packaging industries, or government policy changes affecting paper import and export volumes",
            "recommendation": "Implement market intelligence monitoring for key demand drivers including e-commerce growth, printing industry trends, and government packaging regulations to improve demand forecasting accuracy"
        },
        "supply_chain_cost": {
            "root_cause": "High supply chain costs in pulp and paper are commonly caused by high energy costs for pulp and paper production, expensive inbound logistics for heavy raw materials, or high outbound transportation costs for heavy paper products",
            "recommendation": "Invest in energy efficiency improvements at the mill level and optimize inbound logistics through strategic location of raw material suppliers relative to the production facility"
        },
        "days_inventory_outstanding": {
            "root_cause": "High days inventory in pulp and paper supply chains is typically caused by long wood procurement and seasoning cycles, bulk chemical purchasing minimums creating excess inventory, or finished paper inventory accumulation during market downturns",
            "recommendation": "Implement just-in-time chemical delivery arrangements with suppliers and develop flexible production planning that can respond to demand signals to avoid finished goods inventory build-up"
        },
        "supplier_quality_rate": {
            "root_cause": "Low supplier quality in pulp and paper supply chains is commonly caused by recycled fiber contamination affecting paper quality, wood species variation impacting pulp properties, or chemical supplier quality inconsistencies affecting bleaching and coating processes",
            "recommendation": "Implement incoming quality testing for all raw materials with clear rejection criteria and work with recycled fiber suppliers to improve sorting and contamination removal to ensure consistent fiber quality"
        },
        "lead_time_flexibility": {
            "root_cause": "Low lead time flexibility in pulp and paper supply chains is typically caused by long wood growth and harvest cycles, pulp mill production campaigns that cannot be easily interrupted, or import lead times for specialty chemicals and coatings",
            "recommendation": "Develop relationships with spot market pulp traders to enable rapid additional procurement when needed and maintain strategic safety stock of specialty chemicals with long import lead times"
        },
        "sourcing_flexibility": {
            "root_cause": "Low sourcing flexibility in pulp and paper supply chains is commonly caused by geographic concentration of wood fiber sources, limited alternate suppliers for specialty pulp grades, or dependency on specific chemical suppliers for proprietary formulations",
            "recommendation": "Develop relationships with pulp suppliers across multiple geographic regions and invest in research to qualify alternate fiber sources and chemical formulations to reduce single source dependencies"
        }
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

def show_supply_chain(industry, currency_symbol="$"):
    benchmarks = supply_chain_benchmarks[industry]
    insights = supply_chain_insights[industry]

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

    # Custom Root Causes and Recommendations
    st.header("What is Wrong and How to Fix It")
    st.caption(f"Customized analysis for {industry}")

    root_causes = []
    recommendations = []
    improvements = {}

    if analysis["supplier_otd"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["supplier_otd"]["root_cause"])
        recommendations.append(insights["supplier_otd"]["recommendation"])
        improvements["supplier_otd"] = min(benchmarks["supplier_otd"], supplier_otd + 5)

    if analysis["inventory_turnover"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["inventory_turnover"]["root_cause"])
        recommendations.append(insights["inventory_turnover"]["recommendation"])
        improvements["inventory_turnover"] = min(benchmarks["inventory_turnover"], inventory_turnover + 3)

    if analysis["order_fulfillment_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["order_fulfillment_rate"]["root_cause"])
        recommendations.append(insights["order_fulfillment_rate"]["recommendation"])
        improvements["order_fulfillment_rate"] = min(benchmarks["order_fulfillment_rate"], order_fulfillment_rate + 5)

    if analysis["forecast_accuracy"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["forecast_accuracy"]["root_cause"])
        recommendations.append(insights["forecast_accuracy"]["recommendation"])
        improvements["forecast_accuracy"] = min(benchmarks["forecast_accuracy"], forecast_accuracy + 8)

    if analysis["supply_chain_cost"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["supply_chain_cost"]["root_cause"])
        recommendations.append(insights["supply_chain_cost"]["recommendation"])
        improvements["supply_chain_cost"] = max(benchmarks["supply_chain_cost"], supply_chain_cost - 3)

    if analysis["days_inventory_outstanding"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["days_inventory_outstanding"]["root_cause"])
        recommendations.append(insights["days_inventory_outstanding"]["recommendation"])
        improvements["days_inventory_outstanding"] = max(benchmarks["days_inventory_outstanding"], days_inventory_outstanding - 10)

    if analysis["supplier_quality_rate"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["supplier_quality_rate"]["root_cause"])
        recommendations.append(insights["supplier_quality_rate"]["recommendation"])
        improvements["supplier_quality_rate"] = min(benchmarks["supplier_quality_rate"], supplier_quality_rate + 3)

    if analysis["lead_time_flexibility"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["lead_time_flexibility"]["root_cause"])
        recommendations.append(insights["lead_time_flexibility"]["recommendation"])
        improvements["lead_time_flexibility"] = min(benchmarks["lead_time_flexibility"], lead_time_flexibility + 8)

    if analysis["sourcing_flexibility"]["status"] in ["Needs Improvement", "Critical"]:
        root_causes.append(insights["sourcing_flexibility"]["root_cause"])
        recommendations.append(insights["sourcing_flexibility"]["recommendation"])
        improvements["sourcing_flexibility"] = min(benchmarks["sourcing_flexibility"], sourcing_flexibility + 10)

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
            st.success("Supply chain is performing at benchmark level!")

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