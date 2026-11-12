# nassau-candy-route-analysis
# 🍬 Factory-to-Customer Shipping Route Efficiency Analysis

An end-to-end data analytics and decision-support pipeline built for **Nassau Candy Distributor** to evaluate factory-to-customer shipping performance, identify transit bottlenecks, and optimize supply chain operations across North America.

---

## 📋 Project Overview
Managing fulfillment across multiple manufacturing plants often introduces hidden transit inefficiencies, carrier delays, and high shipping variance. This project ingests **10,194 historical shipment records**, cleans complex date-offset anomalies, engineers factory-to-state shipping corridors, and delivers an interactive **Streamlit** dashboard for executive decision-making.

---

## 🛠️ Tech Stack & Libraries
* **Python** (Data Cleaning, Feature Engineering)
* **Pandas & NumPy** (Data Manipulation & Statistical Analysis)
* **Streamlit** (Interactive Web Application & Dashboard)
* **Plotly** (Geographic Heatmaps & Interactive Visualizations)

---

## 🚀 Key Features & Analytical Workflow
1. **Data Cleaning & Date Normalization:** Audited schema integrity ($\text{Sales} = \text{Gross Profit} + \text{Cost}$) and resolved synthetic date-offset anomalies in the raw export to restore true operational lead times ($0$ to $11$ days).
2. **Product-to-Factory Mapping:** Linked all **15 product SKUs** to their respective origin manufacturing plants (*Lot's O' Nuts*, *Wicked Choccy's*, *Sugar Shack*, *Secret Factory*, and *The Other Factory*) and geographic coordinates.
3. **Route Benchmarking:** Ranked the **Top 10 most efficient** and **Bottom 10 least efficient** shipping lanes (identifying cross-border and northeast corridor bottlenecks).
4. **Ship Mode Evaluation:** Compared transit time trade-offs across *Same Day*, *First Class*, *Second Class*, and *Standard Class* shipping tiers.
5. **Interactive Dashboard:** Deployed a live Streamlit application featuring KPI cards, route leaderboards, US geographic shipping heatmaps, and state-level drill-downs.

---

## 📂 Repository Structure
```text
nassau-candy-route-analysis/
│
├── app.py                     # Interactive Streamlit dashboard application
├── nassau_candy_cleaned.csv   # Cleaned and feature-engineered dataset
├── Research_Paper.pdf         # Comprehensive research paper & documentation
└── requirements.txt           # Python dependencies for cloud deployment
