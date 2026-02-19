# GreenOps Carbon Scheduler & Query Estimator

**A reference implementation of the "GreenOps Framework" created by Ramkumar Gudivada, IEEE Senior Member.**

This project provides a practical toolkit for Data Engineers to estimate and reduce the carbon intensity of their cloud data workloads. It translates sustainability theory into executable Python code.

## 🌟 Features

### 1. Carbon-Aware Batch Scheduler (`scheduler.py`)
Automatically defers heavy batch workloads when the local energy grid is "dirty" (high carbon intensity).
- **Core Logic:** Queries real-time grid APIs (e.g., ElectricityMaps, WattTime).
- **SLA Protection:** Ensures jobs execute before critical deadlines, regardless of grid status.
- **Configurable:** Set your own max gCO2/kWh threshold.

### 2. Snowflake Query Carbon Calculator (`estimator.py`)
Estimates the **gCO2 (grams of CO2)** emitted by a single Snowflake query execution.
- **Inputs:** Warehouse Size (XS - 4XL), Duration (Seconds), Cloud Region.
- **Why use it?** Integrate this into your CI/CD pipeline to flag "High Carbon" queries during development.

---

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Usage: Scheduling a Batch Job
```python
from scheduler import CarbonAwareScheduler
from datetime import datetime, timedelta

# Initialize scheduler for US-East (N. Virginia)
# Threshold: 400 gCO2/kWh (Defer if dirtier than this)
scheduler = CarbonAwareScheduler(region='us-east-1', carbon_threshold=400)

def my_heavy_etl():
    print("Running ETL...")

# Deadline: 4 hours from now
deadline = datetime.now() + timedelta(hours=4)

# Attempt to schedule
scheduler.schedule_batch_job("Daily-ETL", deadline, my_heavy_etl)
```

### Usage: Estimating Query Impact
```python
from estimator import estimate_query_carbon

# Calculate impact of a 5-minute query on a Large Warehouse in Virginia
result = estimate_query_carbon(
    warehouse_size='Large', 
    duration_seconds=300, 
    region='us-east-1'
)

print(f"Estimated Emissions: {result['estimated_emissions_gCO2']} gCO2")
```

---

## 📚 Background
"GreenOps" is the practice of optimizing software and infrastructure to minimize carbon emissions. Just as FinOps focuses on cost, GreenOps treats **Carbon Efficiency** as a first-class architectural constraint.

### Key Concepts
1.  **Carbon Constraints:** Treat carbon intensity like latency or throughput.
2.  **Temporal Shifting:** Move workloads to times when the grid is cleaner (e.g., sunny afternoons or windy nights).
3.  **Algorithmic Efficiency:** A faster query is a greener query.

## 👨‍💻 Author
**Ramkumar Gudivada**  
IEEE Senior Member | Principal Data Architect  
*Specializing in Cloud Data Modernization & Sustainable Architecture*

## 📄 License
MIT License - Free to use and modify.
