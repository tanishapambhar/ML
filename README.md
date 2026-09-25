# FraudShield AI - Vehicle Insurance Fraud Detection System

FraudShield AI is an end-to-end full-stack machine learning application designed to assess, evaluate, and detect potential insurance fraud in vehicle claim filings. 

The application pairs a modern, responsive **React (Vite)** single-page application with a high-performance **FastAPI (Python)** inference engine backed by a pre-trained **Scikit-Learn Machine Learning Pipeline**.

---

## 🚀 Features

- **Real-Time Fraud Prediction**: Evaluates 24 claim indicators including driver demographics, accident site specifics, filing channel, vehicle specifications, and claim amounts.
- **Dynamic Probability Scoring**: Provides an estimated risk percentage and adjuster recommendation for each claim.
- **Modern Responsive UI**: Built with React, Vite, and Lucide Icons, featuring light/dark mode support, dynamic form validations, and interactive metric dashboards.
- **RESTful API**: FastAPI backend providing automated OpenAPI documentation, CORS support, and health telemetry.

---

## 📁 Repository Structure

```
Vehical/
├── BACKEND/
│   ├── ml/
│   │   ├── api/
│   │   │   └── main.py                 # FastAPI application & /predict endpoint
│   │   └── model/
│   │       └── vehicle_fraud_pipeline.pkl  # Trained ML pipeline (scikit-learn 1.6.1)
│   ├── insurance_fraud_data.csv        # Dataset used for training & analysis
│   ├── requirements.txt                # Python backend dependencies
│   └── vehical.ipynb                   # Jupyter notebook with EDA & model training
├── FRONTEND/
│   └── my-react-app/
│       ├── public/                     # Static assets & icons
│       ├── src/
│       │   ├── pages/
│       │   │   ├── Home.jsx            # Landing page & live telemetry dashboard
│       │   │   ├── About.jsx           # Model specifications & training metrics
│       │   │   ├── Prediction.jsx      # Claim intake form & live prediction display
│       │   │   └── Contact.jsx         # Support & contact form
│       │   ├── App.jsx                 # Routing configuration
│       │   ├── Layout.jsx              # Navbar, footer, and theme controller
│       │   └── main.jsx                # Application root
│       ├── .env.example                # Environment variables template
│       ├── package.json                # Frontend dependencies & scripts
│       └── vite.config.js              # Vite server & proxy configuration
├── .gitignore                          # Git ignore rules for node_modules, venv, etc.
└── README.md                           # Documentation & quickstart guide
```

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:
- **Node.js** (v18.0.0 or higher) & **npm**
- **Python** (v3.10 to v3.14) & **pip**
- **Git**

---

## ⚡ Quickstart Guide

### 1. Setup & Start the Backend

1. Navigate to the `BACKEND` directory:
   ```bash
   cd BACKEND
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn ml.api.main:app --host 127.0.0.1 --port 8000 --reload
   ```

   The API will be available at:
   - **API Base URL**: `http://127.0.0.1:8000`
   - **Interactive API Docs (Swagger)**: `http://127.0.0.1:8000/docs`
   - **Health Check**: `http://127.0.0.1:8000/health`

---

### 2. Setup & Start the Frontend

Open a **new terminal window**:

1. Navigate to the frontend directory:
   ```bash
   cd FRONTEND/my-react-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables (optional for default localhost):
   ```bash
   cp .env.example .env
   ```
   *(Default: `VITE_API_URL=http://127.0.0.1:8000`)*

4. Start the Vite development server:
   ```bash
   npm run dev
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

---

## 📡 API Endpoints

### 1. `GET /health`
Returns the status of the API and verifies that the ML model pipeline is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes": [0, 1]
}
```

### 2. `POST /predict`
Evaluates claim data and returns a fraud prediction.

**Request Sample:**
```json
{
  "age_of_driver": 35,
  "safety_rating": 73,
  "annual_income": 65000,
  "high_education": 1,
  "address_change": 0,
  "property_status": "Own",
  "claim_date": "5/12/2020",
  "claim_day_of_week": "Tuesday",
  "accident_site": "Urban",
  "past_num_of_claims": 1,
  "witness_present": 0,
  "liab_prct": 70,
  "channel": "Online",
  "police_report": 1,
  "age_of_vehicle": 5,
  "vehicle_category": "Medium",
  "vehicle_price": 28000,
  "total_claim": 12500,
  "injury_claim": 3500,
  "policy_deductible": 500,
  "annual_premium": 1450,
  "days_open": 18,
  "form_defects": 1
}
```

**Response Sample:**
```json
{
  "prediction": 0,
  "result": "Not Fraud",
  "probability": 0.0
}
```

---

## 🚢 Pushing to GitHub

Follow these steps to initialize git and push this project to your GitHub repository:

1. **Initialize Git** (from the project root directory `Vehical/`):
   ```bash
   git init
   ```

2. **Stage all files**:
   ```bash
   git add .
   ```

3. **Check status** (ensure `node_modules/`, `venv/`, and `.DS_Store` are excluded by `.gitignore`):
   ```bash
   git status
   ```

4. **Commit the changes**:
   ```bash
   git commit -m "Initial commit: full-stack vehicle insurance fraud detection system"
   ```

5. **Create a new repository on GitHub** (e.g. `vehicle-insurance-fraud-detection`).

6. **Link your local repository to GitHub and push**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git
   git push -u origin main
   ```

---

## 📄 License
This project is licensed under the MIT License.
