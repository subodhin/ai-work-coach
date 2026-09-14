
# AI Work Coach

> A working prototype for AI-powered workforce upskilling through realistic workplace challenges and adaptive coaching.

**Status:** Early-stage prototype

## Technology & Deployment

| Layer | Technology |
|---|---|
| Frontend | Next.js / React / TypeScript |
| Backend | FastAPI / Python / Pydantic |
| AI | Google Gemini |
| Database | PostgreSQL / Neon |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

The prototype uses **free-tier infrastructure with zero additional infrastructure cost**.

> **Deployment note:** The Render free-tier backend may take approximately one minute to wake after inactivity.

## What It Does

AI Work Coach evaluates how employees use AI on realistic work tasks, identifies skill gaps, and adapts the next challenge accordingly.

```text
Challenge
    ↓
Use AI
    ↓
LLM Evaluation
    ↓
Skill Profile
    ↓
Identify Gap
    ↓
Adaptive Challenge
    ↓
Improve
````

## Architecture

```text
┌──────────────┐
│   Next.js    │
│ React / TS   │
└──────┬───────┘
       │ REST
       ↓
┌──────────────┐
│   FastAPI    │
│   Backend    │
└────┬─────┬───┘
     │     │
     ↓     ↓
┌────────┐ ┌─────────────┐
│Coaching│ │ Gemini LLM  │
│ Logic  │ │ Evaluator   │
└───┬────┘ └──────┬──────┘
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │ PostgreSQL  │
    │    Neon     │
    └─────────────┘
```

## Skill Framework

The evaluator scores six practical AI capabilities:

* Problem Framing
* Context
* Prompting
* Reasoning
* Verification
* Final Output

## Adaptive Coaching

The system uses evaluation history to identify the employee's weakest skill and select the next relevant challenge from a curated challenge library.

Example:

```text
Context: 70
    ↓
Development Focus: Context
    ↓
Next Challenge: Investigate a Slow API
```

## Key Design Decision

The MVP uses **curated challenges + deterministic skill matching** instead of RAG, embeddings, or autonomous agents.

This keeps the prototype explainable, predictable, testable, and cost-conscious.

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set the required environment variables for the backend and frontend before starting the services.

## User Isolation

Each browser receives a generated UUID, allowing independent user journeys and evaluation histories without account creation.

**Start New User** creates a fresh learning journey without deleting existing data.

## Project Status

This is an **early-stage working prototype** focused on validating the core adaptive coaching workflow before expanding into broader enterprise capabilities.
