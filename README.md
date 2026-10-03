# Automated Hostel Utility Optimization & Predictive Resource Management Dashboard for High-Density Institutions

A production-grade, software-only web platform designed for universities, colleges, and high-density residential campuses to monitor, forecast, optimize, and manage utility consumption (**Electricity, Water, LPG Gas**) and student occupancy.

The platform combines real-time resource telemetry, machine learning forecasting (**Random Forest Regressors**), unsupervised anomaly detection (**Isolation Forest**), explainable decision support, and closed-loop maintenance work order dispatching.

---

## 🌐 Live Cloud Deployment (Render.com)

* 🖥️ **Interactive Web Application**: `https://hostel-utility-app.onrender.com`
* ⚙️ **Backend API Server**: `https://hostel-utility-system.onrender.com`
* 📖 **Interactive Swagger API Documentation**: `https://hostel-utility-system.onrender.com/docs`

---

## 🎨 Modern Vibrant Light Theme

The user interface is crafted with an **attractive, high-contrast light theme**:
- **Background**: Soft `bg-slate-50` with subtle ambient radial glow accents.
- **Cards & Containers**: Crisp white cards with smooth hover elevation shadows and clean borders (`border-slate-200/80`).
- **Vibrant Resource Badges**:
  - ⚡ **Electricity**: Warm Amber (`#f59e0b` / `bg-amber-50` / `text-amber-700`)
  - 💧 **Water**: Radiant Sky Blue (`#0284c7` / `bg-sky-50` / `text-sky-700`)
  - 🔥 **Gas & Mess Kitchen**: Coral Rose (`#e11d48` / `bg-rose-50` / `text-rose-700`)
  - 💰 **Tariffs & Costs**: Emerald Green (`#059669` / `bg-emerald-50` / `text-emerald-700`)
  - 🧠 **Machine Learning**: Electric Indigo (`#6366f1` / `bg-indigo-50` / `text-indigo-700`)

---

## 🌟 Key Features & Core Modules

1. **Executive Operations Dashboard**:
   - Live KPI cards: Total Students, Hostel Blocks, Today's Water (L), Today's Electricity (kWh), Today's Gas (kg), Estimated Cost (₹), Active Alerts.
   - **0–100 Multi-Pillar Efficiency Index**: Radial gauge assessing water efficiency, electricity efficiency, gas efficiency, and wastage control penalties.
   - Interactive 7-day multi-resource time-series trend visualizer.
   - Real-time critical anomaly ticker with quick action triggers.

2. **Hostel & Infrastructure Management**:
   - 8 configured residential blocks (*Himalaya Block A, Nilgiri Block B, Aravali Block C, Vindhya Block D, Shivalik Block E, Everest Block F, Sahyadri Block G, Kailash Block H*).
   - Real-time bed capacity and occupancy percentage tracking.
   - Administrative Add/Edit/Delete block modals.

3. **Student Occupancy Tracking**:
   - Daily resident count logging with calendar date picker.
   - Automatic calculation of:
     $$\text{Occupancy \%} = \frac{\text{Current Students}}{\text{Hostel Capacity}} \times 100$$
   - Historical occupancy timeline serving as an autoregressive feature for ML models.

4. **Utility Consumption & Batch Ingestion**:
   - Full sub-metering data grid with searching, date-range filtering, and block isolation.
   - **CSV Batch Uploader**: Drag-and-drop file ingestion with schema validation and automated cost calculation.
   - Single-record manual entry modal and CSV export functionality.

5. **Deep-Dive Resource Analytics**:
   - Dedicated analytical views for **Electricity (kWh)**, **Water (L)**, **Gas (kg)**, and **Per-Student Benchmarking**.
   - Diurnal electricity breakdown (Morning Rush, Class Hours, Evening Study, Night Phantom Load).
   - Cross-hostel per-student comparative table with automated overconsumption alert flags (⚠).

6. **Predictive Machine Learning Engine**:
   - **7-Day Forward Demand Forecast**: Multi-step projection of electricity, water, gas, and utility expenditure.
   - **Academic Model Evaluation Scorecard**: Comparative performance table contrasting **Random Forest Regressors** ($R^2$, MAE, RMSE) against a **Linear Regression** baseline.
   - **Explainability Factors**: Natural language driver breakdown highlighting feature contributions (rolling averages, occupancy pressure, weekend shifts).
   - 1-Click "Retrain ML Models" pipeline.

7. **Isolation Forest Anomaly Detection & Alerts**:
   - Unsupervised outlier detection identifying abnormal consumption spikes (pipe bursts, thermostat failures, gas leaks).
   - Severity categorization: `Critical` ($>70\%$), `High` ($>45\%$), `Medium` ($>25\%$), `Low` ($>15\%$).
   - **1-Click "Dispatch Maintenance Ticket"**: Directly converts an anomaly alert into an assigned work order.

8. **Smart Recommendation Engine**:
   - Explainable action cards categorized by resource (Water, Electricity, Gas, Occupancy).
   - Quantified **Estimated Monthly Cost Savings (₹)** with step-by-step mitigation checklists.

9. **Maintenance Management Hub**:
   - Work order lifecycle tracking: `Open` $\rightarrow$ `Assigned` $\rightarrow$ `In Progress` $\rightarrow$ `Resolved` $\rightarrow$ `Closed`.
   - Technician assignment, priority tags, and timestamped activity logs.

10. **Financial Audit & Reporting Center**:
    - Generates **Daily Operational Summaries**, **Weekly Audits**, and **Monthly Institutional Reviews**.
    - **Estimated Possible Savings Calculator** comparing actual operational expenditure against historical baseline.
    - One-click Print / PDF export and CSV reports.

11. **Configurable Tariff Rates & Settings**:
    - Dynamic unit tariff rate configuration for Electricity (₹/kWh), Water (₹/L), and Gas (₹/kg).
    - Demo database reset and re-seeding engine.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | React 18, Vite 5, Tailwind CSS, Recharts, Lucide React, Axios, React Router Dom |
| **Backend API** | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn |
| **Machine Learning** | Scikit-learn (Random Forest Regressor, Isolation Forest, Linear Regression), Pandas, NumPy, Joblib |
| **Database** | SQLite (Zero-config local) / PostgreSQL / MySQL |
| **Security** | JWT (JSON Web Tokens), Bcrypt password hashing, Role-Based Access Control |
| **Testing** | Pytest, FastAPI TestClient, Httpx |
| **Deployment** | Render.com (Web Service + Static Site with SPA Rewrites), Git |

---

## 👥 Demo User Accounts & Roles

The system is pre-populated with demo credentials for instant evaluation:

| Role | Email | Password | Permissions & Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@hostel.edu` | `Admin@123` | Full access across all 8 blocks, utilities, ML retraining, rates, user management, and reporting |
| **Warden (Block A)** | `warden.blocka@hostel.edu` | `Warden@123` | Assigned to Himalaya Block A: view block consumption, occupancy, alerts, recommendations, and maintenance |
| **Warden (Block C)** | `warden.blockc@hostel.edu` | `Warden@123` | Assigned to Aravali Block C: view block consumption, occupancy, alerts, recommendations, and maintenance |
| **Maintenance Staff** | `maintenance@hostel.edu` | `Maint@123` | View assigned work orders, anomaly logs, status transitions, and append repair notes |

*(Note: The login page includes 1-click quick login buttons for instant access).*

---

## 📊 Mathematical Formulations & Business Logic

### 1. Per-Student Resource Consumption
$$\text{Water per Student} = \frac{\text{Water Consumption (Litres)}}{\text{Resident Student Count}}$$
$$\text{Electricity per Student} = \frac{\text{Electricity Consumption (kWh)}}{\text{Resident Student Count}}$$
$$\text{Gas per Student} = \frac{\text{Gas Consumption (kg)}}{\text{Resident Student Count}}$$

### 2. Total Operational Utility Cost
$$\text{Total Cost (₹)} = (\text{Electricity} \times \text{Rate}_E) + (\text{Water} \times \text{Rate}_W) + (\text{Gas} \times \text{Rate}_G)$$

### 3. Multi-Pillar Efficiency Index (0–100)
$$\text{Score} = (0.28 \times \text{WaterEff}) + (0.32 \times \text{ElecEff}) + (0.15 \times \text{GasEff}) + (0.25 \times \text{WastageControl})$$

---

## 🚀 Local Installation & Quick Start

### 1. 1-Click Launch (Windows)
Double click `start_all.bat` in the root folder to start both Backend and Frontend.

### 2. Manual Commands

#### Backend API Setup
```bash
cd backend
python -m venv .venv
# Activate virtualenv:
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
* Access Swagger Docs: `http://127.0.0.1:8000/docs`

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
* Access Dashboard: `http://localhost:5173`

---

## 🧪 Running Automated Tests

```bash
cd backend
pytest -v
```

---

## 📂 Project Architecture

```
hostel-utility-system/
├── backend/
│   ├── app/
│   │   ├── api/             # 13 REST API Routers
│   │   ├── database/        # Connection, Models, and Seed Generator
│   │   ├── ml/              # Feature engineering, RF Regressors, Isolation Forest, Efficiency
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   ├── services/        # JWT Authentication and Password hashing
│   │   └── main.py          # FastAPI application entry point
│   ├── ml_models/           # Saved serialized Scikit-learn models (.joblib)
│   ├── tests/               # Pytest automated test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Recharts visualizers, Sidebar, Header, Modals, Badges
│   │   ├── contexts/        # AuthContext with JWT session management
│   │   ├── pages/           # 12 React views (Dashboard, Analytics, Predictions, etc.)
│   │   ├── services/        # Axios API client
│   │   ├── App.jsx          # Protected route tree
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── sample_consumption.csv # Ready-to-import CSV sample dataset
├── render.yaml              # Render Cloud deployment blueprint
├── start_all.bat            # 1-Click Windows Launcher
└── README.md
```
