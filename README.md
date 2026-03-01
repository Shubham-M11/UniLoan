# UniLoan - Explainable Smart Loan Evaluation System

UniLoan is a comprehensive web application designed to evaluate loan applications intelligently while providing clear, explainable insights into the decision-making process. The system uses advanced machine learning models (XGBoost) combined with SHAP (SHapley Additive exPlanations) to ensure transparent and fair loan assessments.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)

## Features
- **Smart Loan Prediction**: Utilizes machine learning to assess the risk and probability of loan approval based on user inputs.
- **Explainable AI (XAI)**: Provides clear explanations for the model's predictions using SHAP values, allowing users and administrators to understand the key factors influencing the decision.
- **Modern User Interface**: A responsive and intuitive frontend built with React and Tailwind CSS.
- **Robust API**: A fast and reliable backend powered by FastAPI and SQLAlchemy.

## Tech Stack

### Frontend
- **Framework**: React 18, Vite
- **Styling**: Tailwind CSS, PostCSS
- **Tooling**: ESLint

### Backend
- **Framework**: FastAPI, Uvicorn
- **Database ORM**: SQLAlchemy
- **Machine Learning**: Scikit-Learn, XGBoost
- **Explainability**: SHAP
- **Data Manipulation**: Pandas, NumPy
- **Database Adapter**: psycopg2-binary (PostgreSQL compatible)

## Project Structure
```text
UniLoan/
├── backend/          # FastAPI backend application
│   ├── ml/           # Machine learning models and prediction logic
│   ├── models/       # SQLAlchemy database models
│   ├── routers/      # API endpoints (e.g., /predict)
│   ├── schemas/      # Pydantic schemas for request/response validation
│   ├── services/     # Business logic
│   ├── database.py   # Database connection setup
│   ├── main.py       # FastAPI application entry point
│   └── requirements.txt # Python dependencies
├── frontend/         # React frontend application
│   ├── src/          # Source files (components, styles, etc.)
│   ├── public/       # Static assets
│   ├── package.json  # NPM dependencies and scripts
│   └── vite.config.js# Vite configuration
└── README.md         # Project documentation (this file)
```

## Getting Started

### Prerequisites
- Node.js (v18+ recommended)
- Python (v3.10+ recommended)
- PostgreSQL (if using a local Postgres database)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (if required by `.env`).
5. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The API documentation will be available at `http://localhost:8000/docs`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173/` (or the port specified by Vite).

---
*Built to bring transparency to automated loan evaluations.*
