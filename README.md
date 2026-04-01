# SENTRA | AI Policy Decision Intelligence System 🧠📜

![Platform](https://img.shields.io/badge/Platform-Web%20Application-informational)
![API](https://img.shields.io/badge/API-FastAPI-0ba360)
![LLM](https://img.shields.io/badge/LLM-Llama3%20\(Ollama\)-blue)
![Architecture](https://img.shields.io/badge/Architecture-RAG%20Pipeline-purple)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-646cff)
![Status](https://img.shields.io/badge/Status-Production--Oriented-success)

SENTRA is an AI-powered decision intelligence system designed to evaluate workplace decisions against organizational policies **before execution**, enabling structured, explainable, and risk-aware outcomes.

It demonstrates production-focused AI engineering practices such as structured LLM output enforcement, retrieval-augmented reasoning, modular backend design, confidence scoring, and robust API-driven architecture.

---

### ✨ Key Features

* Policy-aware decision evaluation using LLM + RAG pipeline
* Structured JSON output with strict schema enforcement
* Confidence scoring for decision reliability
* Risk classification: LOW / MEDIUM / HIGH
* Explainable reasoning with policy-backed evidence
* Safer alternative recommendation engine
* Fault-tolerant LLM integration (regex parsing + fallback handling)
* Modular architecture (retrieval layer + reasoning layer separation)
* Clean REST API contract for frontend integration

---

### 🧠 Problem Statement

Organizational policies (HR, compliance, security, remote work) are often lengthy and complex. Employees and managers frequently:

* misinterpret policies
* make inconsistent decisions
* introduce compliance risks
* lack structured decision support

Generic AI tools fail because they:

* are not grounded in policy documents
* produce unstructured outputs
* lack explainability
* provide no risk awareness

SENTRA addresses this by combining **policy retrieval + LLM reasoning + structured decision intelligence**.

---

## 🧩 System Design

### 🟢 Stage 1 - Policy Retrieval (RAG Layer)

Retrieves relevant policy context for a given decision:

* semantic retrieval (vector DB ready - Qdrant planned)
* contextual evidence extraction
* confidence-aware retrieval output

Answers:
**"What policies are relevant to this decision?"**

---

### 🟡 Stage 2 - Decision Intelligence (LLM Layer)

Transforms policy context into structured decision output:

* risk classification (LOW / MEDIUM / HIGH)
* confidence scoring
* reasoning generation
* recommendation engine
* safer alternative suggestion

Answers:
**"Is this decision safe, and what should be done?"**

---

## 🏗 System Architecture

React Frontend (Vite)
↓
FastAPI Backend
↓
Decision Engine (Orchestration Layer)
↓
Retriever (RAG Layer)
↓
LLM (Llama3 via Ollama)
↓
Structured JSON Output

Architecture principles:

* clear separation between retrieval and reasoning
* LLM output normalization and validation
* modular and extensible backend design
* API-first communication
* scalable for enterprise policy systems

---

### 📦 Project Structure

```text
SENTRA/
│
├── backend/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   ├── rag/
│   └── main.py
│
├── frontend/
├── data/
├── docs/
├── requirements.txt
└── README.md
```

---


## 📸Screenshots


<img width="3200" height="1728" alt="Screenshot 2026-04-01 095909" src="https://github.com/user-attachments/assets/db683509-1bad-4c99-98f1-2ae789785ce3" />

<img width="3200" height="1734" alt="Screenshot 2026-04-01 095947" src="https://github.com/user-attachments/assets/71e81149-3887-41d0-95f0-9f37689c3921" />

<img width="3200" height="1720" alt="Screenshot 2026-04-01 100035" src="https://github.com/user-attachments/assets/a4d39de9-fed8-499d-b547-e361190c1e35" />



---

### 🛠 Tech Stack

* Backend: Python, FastAPI
* LLM: Llama3 (via Ollama)
* Architecture: RAG (Retrieval-Augmented Generation)
* Vector DB (Planned): Qdrant
* Frontend: React, Vite
* Integration: REST API

---

### ▶ Running Locally

#### Backend

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Runs at:

http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

---

#### Frontend

```bash
cd frontend/sentra-ui
npm install
npm run dev
```

Runs at:

http://localhost:5173

---

### ⚙ Key Engineering Decisions

* enforced structured LLM outputs using schema validation
* regex-based JSON extraction for handling inconsistent LLM responses
* fallback mechanisms to ensure API stability
* modular decision engine separating retrieval and reasoning
* confidence scoring to improve interpretability
* API-first backend for scalable integration

---

### 🚧 Future Improvements

* Full vector database integration (Qdrant)
* Multi-agent LLM architecture
* Policy document ingestion pipeline
* Decision audit logs and tracking
* Dockerization and cloud deployment
* Observability and monitoring

---

### 📄 License

Developed for educational and portfolio demonstration purposes.
