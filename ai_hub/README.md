# 🤖 AI Hub — RAG + Agents (Hospital Management System)

## 📌 Table of Contents
1. [📌 Project Overview](#-project-overview)
2. [👤 User Stories](#-user-stories)
3. [🎨 UX / UI Design](#-ux--ui-design)
4. [🛠 Technologies Used](#-technologies-used)
5. [📂 System Architecture](#-system-architecture)
6. [🗄 Data Models](#-data-models)
7. [🔐 Authentication & Authorization](#-authentication--authorization)
8. [📅 App Features](#-app-features)


---

## 📌 Project Overview

The AI Hub is a production-style AI module for the Hospital Management System. It provides retrieval-augmented generation (RAG), compliance checks, and applied ML workflows to support clinical operations.

**Who it is for**
- Admins: manage policy docs, run compliance checks, monitor results.
- Doctors: generate discharge drafts and review for completeness.

**Safety principles**
- Assistive drafts only; clinician review required.
- No hallucinations: answers must be grounded in retrieved policy context.
- Citations required for every RAG response.
- Optional PII redaction for prompts and outputs using placeholders such as `[PATIENT_NAME]` and `[PATIENT_ID]`.

---

## 👤 User Stories

| Role  | User story | Acceptance criteria |
| ----- | ---------- | ------------------- |
| Admin | Uploads policy docs and rebuilds index | Docs appear in knowledge base and index builds successfully |
| User  | Asks a policy question and gets answer + citations + request ID | Response includes citations list and a request ID |
| User  | Enables PII redaction | Output replaces identifiers with placeholders |
| Admin | Runs compliance agent on a discharge draft | Checklist and issues are shown |
| Doctor | Generates discharge draft and reviews before finalizing | Draft marked not final; review required |
| Admin | Runs no-show predictor | Returns risk score and factors |
| Admin | Classifies complaint | Returns department label and suggested response |

---

## 🎨 UX / UI Design

**Key pages**
- `/ai/` — AI Hub home dashboard
- `/ai/rag/` — Policy / SOP Q&A
- `/ai/rag/upload/` — Knowledge document upload

**UI table**
| Page | Purpose | Inputs | Outputs |
| ---- | ------- | ------ | ------- |
| `/ai/` | Navigate AI Hub features | None | Feature cards |
| `/ai/rag/` | Policy Q&A | Question, redact toggle | Answer, citations, request ID |
| `/ai/rag/upload/` | Add documents | .txt / .pdf file | Upload confirmation |
| `/ai/agent/compliance/` | Compliance review | Draft text, redact toggle | Checklist, issues |
| `/ai/draft/` | Draft assistant | Notes, redact toggle | Draft + patient instructions |
| `/ai/ml/no-show/` | No-show risk | Days until, hour | Risk score |
| `/ai/nlp/triage/` | Complaint classifier | Complaint text | Label + confidence |

---
## 🧭 How to Use (AI Hub)

The AI Hub provides assistive, non-clinical, policy-aware AI tools for demonstration and educational purposes only. Outputs are drafts and decision-support artifacts and must be reviewed by a qualified clinician before any clinical use.

### Routes Overview

| Route | Purpose | Access Control | Example Usage |
| ----- | ------- | -------------- | ------------- |
| `/ai/` | AI Hub landing page | Authenticated users (Admin/Doctor) | Navigate to AI features |
| `/ai/rag/` | Policy / SOP Q&A | Authenticated users (Admin/Doctor) | Ask policy questions with citations |
| `/ai/rag/compliance/` | Compliance RAG entry point | Authenticated users (Admin/Doctor) | Review compliance guidance via RAG |
| `/ai/agent/compliance/` | Compliance agent | Authenticated users (Admin/Doctor) | Assess draft completeness and issues |
| `/ai/rag/upload/` | Knowledge document upload | Admin only (recommended) | Upload .txt/.pdf and rebuild index |

### `/ai/` ? AI Hub Home

- **What it does:** Provides a dashboard for navigating AI features.
- **How to use:** Select a feature card.
- **Input:** None.
- **Output:** Links to AI tools.
- **Safeguards:** Access requires login; routes should be limited to Admin/Doctor roles.

### `/ai/rag/` ? Policy / SOP Q&A

- **What it does:** Answers questions using retrieved policy context with citations.
- **How to use:** Enter a question and optionally enable PII Redaction.
- **Input:** Policy question text; optional redact toggle.
- **Output:** Answer with citations and a Request ID for traceability.
- **Safeguards:** PII Redaction replaces identifiers with placeholders; responses are drafts.

### `/ai/rag/compliance/` ? Compliance RAG

- **What it does:** Provides policy-aware compliance guidance using retrieved sources.
- **How to use:** Open the page and submit compliance-related questions.
- **Input:** Compliance question or scenario.
- **Output:** Guidance with citations and a Request ID.
- **Safeguards:** Grounded answers; clinician review required for any applied decisions.

### `/ai/agent/compliance/` ? Compliance Agent

- **What it does:** Reviews discharge drafts for required sections and policy alignment.
- **How to use:** Paste a draft and submit.
- **Input:** Discharge draft text; optional redact toggle.
- **Output:** Checklist of missing sections, issues, and recommendations.
- **Safeguards:** Outputs are non-final; intended for clinician review only.

### `/ai/rag/upload/` ? Knowledge Document Upload

- **What it does:** Allows administrators to add policy documents to the knowledge base.
- **How to use:** Upload a `.txt` or `.pdf` file, then run `python manage.py build_rag_index`.
- **Input:** Document file.
- **Output:** Upload confirmation and updated index after build.
- **Safeguards:** Restrict to Admin role; documents should contain no sensitive patient data.

### Safeguards and Traceability

- **Role-based access:** AI Hub is intended for Admin and Doctor roles only.
- **PII Redaction:** Optional redaction replaces identifiers with placeholders.
- **Request IDs:** Each AI request is logged with a Request ID for auditing.
- **Clinical review:** All AI outputs are drafts and must be reviewed before use.

---

## 🛠 Technologies Used

- Django 4.2
- Python 3.11
- FAISS for vector retrieval (if enabled)
- TF-IDF retrieval fallback
- OpenAI API (`LLM_PROVIDER=openai`)
- JSONL tracing + request IDs

**Technology table**
| Component | Purpose |
| --------- | ------- |
| Django | Web framework |
| FAISS / TF-IDF | Retrieval layer |
| OpenAI | LLM responses |
| JSONL traces | Observability |
| Heroku config vars | Production configuration |

---

## 📂 System Architecture

```
User
  -> Django Views
    -> Retrieve (FAISS / TF-IDF)
      -> Prompt Builder
        -> LLM Provider
          -> Answer + Citations + Request ID
```

**Document flow**
- Knowledge docs live in `ai_hub/knowledge_base/`
- Index artifacts live in `ai_hub/artifacts/`
- Index is built via `python manage.py build_rag_index`

---

## 🗄 Data Models

| Model | Purpose | Key fields |
| ----- | ------- | ---------- |
| AgentQueryLog | RAG Q&A tracing | user, query, response, latency_ms, metadata, created_at |
| AiDraft | Draft storage | user, notes, draft_text, reviewed |
| AiPredictionLog | ML predictions | input_text, predicted_label, confidence, metadata |
| AgentRun | Agent runs | run_type, status, total_latency_ms |
| AgentStepTrace | Agent steps | step_name, output_text |
| AiRequestTrace | Observability | request_id, operation_type, latency_ms, metadata |

---

## 🔐 Authentication & Authorization

- AI Hub routes should be protected by login and role checks.
- Admin and Doctor roles access AI Hub features.
- Patient access should be restricted for safety.

---

## 📅 App Features

### ✅ RAG Policy / SOP Q&A
**How it works**
- Retrieves top-k policy snippets.
- Builds a grounded prompt and returns answer + citations + request ID.

**Example questions**
- What are the required sections of a discharge summary?
- What is the appointment policy for no-shows?
- What fields are required on an invoice?

**Output**
- Answer text
- Citation list
- Request ID

### ✅ Knowledge Document Upload + Index Build
**Supported files**
- `.txt`, `.pdf`

**Flow**
1. Upload doc at `/ai/rag/upload/`
2. Run `python manage.py build_rag_index`
3. Query via `/ai/rag/`

**Common issues**
- No docs uploaded → empty index
- Missing artifacts → run index build

### ✅ PII Redaction Mode
**What gets redacted**
- Names, phone numbers, emails, IDs

**Example**
Before:
```
Patient John Smith (ID 12345) has chest pain.
```
After:
```
Patient [PATIENT_NAME] (ID [PATIENT_ID]) has chest pain.
```

### ✅ Compliance Agent
**Checks**
- Completeness (diagnosis, treatment, meds, follow-up, red flags, sign-off)
- Policy alignment with citations
- Safe tone and no hallucinations

**Example input**
```
Diagnosis: pneumonia. Treatment: IV antibiotics. Discharged home.
```

**Example output**
```
Missing: Medication list, Follow-up plan, Red flags.
Severity: High. Add required sections and patient instructions.
```

### ✅ Discharge Draft Assistant
- Generates discharge draft + patient instructions
- Required sections A–H
- Drafts are assistive only; clinician review required

### ✅ No-Show Risk Predictor
**Features used**
- Days until appointment
- Appointment hour

**Output**
- Risk score from 0.0 to 1.0

### ✅ Complaint Classifier
**Categories**
- General medicine, cardiology, respiratory, GI, etc.
- Severity levels L1/L2/L3

**Example**
Input: "Shortness of breath and chest tightness"
Output: "Cardiology, L2, advise urgent clinical review"

---

## 🧪 Example Prompts

**RAG Q&A (10)**
1. What sections must a discharge summary include?
2. What red flags should be listed for discharge?
3. What is the no-show policy?
4. How soon should reminders be sent?
5. What fields are required on an invoice?
6. What is the dispute window for billing?
7. What is the privacy rule for AI drafts?
8. Who must review AI outputs?
9. What follow-up information is required?
10. How should medication changes be documented?

**Discharge drafts (3)**
1. Diagnosis: asthma; treatment: nebulizers; discharge today.
2. Diagnosis: UTI; meds listed; missing follow-up.
3. Diagnosis: pneumonia; missing medication list and red flags.

**Compliance checks (5)**
1. Missing medications
2. Missing follow-up plan
3. Missing red flags
4. Missing sign-off
5. Missing diagnosis

**Complaint classifier inputs (5)**
1. "Chest pain with sweating"
2. "Persistent cough and fever"
3. "Severe abdominal pain"
4. "Dizziness after medication"
5. "Post-op wound redness"

---

## 💳 Stripe Payment Integration (AI Hub Notes)



Stripe is used elsewhere in the system for billing and appointment-related payment workflows. The AI Hub is fully independent of payment processing and does not initiate, handle, or store any payment transactions.

Key boundaries and controls:

- Separation of concerns is maintained by keeping Stripe logic in the billing/payments modules, while AI Hub functionality remains isolated to AI-assisted workflows.
- AI Hub uses the same Django authentication and session management as the core application, ensuring consistent access control.
- Role-based permissions apply to AI Hub routes, aligning security posture with the rest of the system.
- AI features are provided for decision-support and educational purposes only and are not presented as a commercial service.


---

## 🧪 Validation, Testing & Lighthouse

**Testing checklist**
| Test | Steps | Expected result |
| ---- | ----- | --------------- |
| RAG returns citations | Ask Q in `/ai/rag/` | Answer + citations appear |
| Request ID displayed | Submit query | Request ID visible |
| PII redaction | Check redact toggle | Placeholders used |
| Missing API key | Unset key | User-friendly error, 400 |
| Rate limit | Rapid POSTs | Rate limit message |
| Upload success | Upload doc | Success message |

---

## 🚀 Deployment Guide (Heroku)

**Config vars**
- `AI_FEATURES_ENABLED`
- `AGENTS_ENABLED`
- `AI_MOCK_MODE`
- `LLM_PROVIDER`
- `LLM_MODEL`
- `OPENAI_API_KEY`
- `RAG_PROVIDER`

**Commands**
```
heroku config:set AI_FEATURES_ENABLED=true
heroku config:set AGENTS_ENABLED=true
heroku config:set AI_MOCK_MODE=false
heroku config:set LLM_PROVIDER=openai
heroku config:set LLM_MODEL=gpt-4o-mini
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set RAG_PROVIDER=faiss
heroku restart
```


---

## 📁 File Structure

```
ai_hub/
  templates/ai_hub/
  services/
  views.py
docs/
  ai_hub/
    knowledge/
```

Recommended location for docs: `docs/ai_hub/knowledge/` (then sync to `ai_hub/knowledge_base/`).

---

## 🙏 Credits & Attribution
Mentors:

* **Rachel Furlong**
* **Spencer Barriball**
- OpenAI API
- FAISS
- Django

---

## 📜 License

This project is licensed under the **MIT License**.
