# SENTRA  
### AI Policy Governance & Decision Intelligence Platform

SENTRA is an AI-powered internal decision-support system designed to help organizations  
**evaluate workplace decisions against official policy documents before execution**.

Unlike generic AI chatbots, SENTRA focuses on **policy grounding, explainability, and risk awareness**, ensuring that decisions are compliant, traceable, and defensible.

---

## Problem Statement

Organizational policies (HR, security, conduct, remote work, etc.) are often lengthy  
and complex. Employees and managers frequently misinterpret these policies, leading to:

- Unintentional policy violations  
- Compliance and legal risks  
- Internal disputes and operational inefficiencies  

Existing AI tools typically provide **generic answers** but lack:

- Grounding in official policy documents  
- Clear reasoning and traceability  
- Explicit risk classification  

---

## What SENTRA Does

SENTRA analyzes real-world workplace decision scenarios using official policy documents  
and provides:

- Policy-grounded evaluation  
- Compliance risk classification (Low / Medium / High)  
- Clear reasoning with policy references  
- Safer, policy-compliant alternatives when applicable  

This system is designed as a **decision intelligence platform**, not a generic chatbot.

---

## Project Structure

- `frontend/` — React-based user interface (Vite)
- `backend/` — FastAPI backend (API contracts, schemas, decision engine)
- `app/` — Early exploratory modules (to be consolidated)
- `docs/` — Design notes and architecture (planned)

---

## Project Status

🚧 **Active development (Jan–Feb)**

- Backend API foundation implemented (health check, decision evaluation endpoint)
- Frontend UI skeleton initialized
- Policy ingestion, RAG pipeline, and LLM-based reasoning engine under development

---

## Tech Stack

### Frontend
- React (Vite)

### Backend
- FastAPI  
- Pydantic (data validation)  

### AI / ML (Planned & In Progress)
- Large Language Models (LLMs)  
- Retrieval-Augmented Generation (RAG)  
- Vector Database (Qdrant)

---

