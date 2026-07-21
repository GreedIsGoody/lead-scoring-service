# 🚀 Lead Scoring & Churn Prediction Microservice

A production-ready asynchronous Python backend service built with **FastAPI**, **PostgreSQL**, **SQLAlchemy (AsyncIO)**, and **scikit-learn**. The service tracks customer behavior and activity logs in real-time to compute predictive churn risk scores using a Random Forest machine learning model.

---

## 🌟 Key Features

* **Async Architecture:** High-performance asynchronous API powered by FastAPI and `asyncpg`.
* **Database Management:** Object-Relational Mapping (ORM) using SQLAlchemy 2.0 with full timezone awareness (`UTC`).
* **Real-time Event Logging:** Endpoints to record user activity (support tickets, logins, payments).
* **Machine Learning Integration:** Embedded `RandomForestClassifier` for instant churn prediction based on aggregated user behavior metrics.
* **Auto-Initialization & Model Persistence:** Automatic fallback training on synthetic data if pre-trained weights (`.joblib`) are missing.
* **Production Configurations:** Centralized settings management with `pydantic-settings` and `.env` support.
* **Fully Dockerized:** Complete multi-container setup via Docker and Docker Compose with health checks.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Framework:** FastAPI
* **Database:** PostgreSQL 15
* **ORM:** SQLAlchemy 2.0 (AsyncIO) + Asyncpg
* **Machine Learning:** scikit-learn, Pandas, NumPy, Joblib
* **Configuration & Validation:** Pydantic v2, Pydantic Settings
* **Containerization:** Docker, Docker Compose

---

## 🏗️ Project Architecture

```text
lead-scoring-service/
├── src/
│   ├── ml/
│   │   ├── storage/          # Persisted ML model weights (.joblib)
│   │   ├── __init__.py
│   │   └── model.py          # ChurnPredictor class (Random Forest pipeline)
│   ├── config.py             # App settings loaded from environment variables
│   ├── database.py           # Async SQLAlchemy engine & session maker
│   ├── main.py               # FastAPI application & route declarations
│   ├── models.py             # SQLAlchemy DB schemas (Customer, CustomerActivityLog)
│   └── schemas.py            # Pydantic models for request/response validation
├── .env.example              # Environment variables template
├── Dockerfile                # Docker build instructions for FastAPI
├── docker-compose.yml        # Orchestration for FastAPI & PostgreSQL containers
└── requirements.txt          # Python dependencies
