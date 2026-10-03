# InnovatorsUnleashed_mantrayudha
# MantraYudha — 210-Minute MVP Sprint

> **A rapid-build AI customer-support agent developed within a strict 3.5-hour (210-minute) hackathon sprint.**

## 🚀 Overview

**MantraYudha** is an AI-powered customer-support agent designed to handle customer requests using **verification, policy reasoning, controlled tool execution, security, and human escalation**.

The official **MantraYudha – Battle Brief – Official Participant Handbook** is treated as the primary source of project requirements.

The goal is not to build a complete enterprise platform. The goal is to deliver a **working, integrated, demo-ready MVP within 210 minutes**.

---

## ⏱️ 210-Minute Development Plan

| Time            | Phase          | Focus                                                 |
| --------------- | -------------- | ----------------------------------------------------- |
| **0–15 min**    | Setup          | Repository, stack, structure, interfaces              |
| **15–90 min**   | Parallel Build | Frontend, backend, database, AI agent, testing        |
| **90–140 min**  | Integration    | Connect frontend → backend → agent → tools → database |
| **140–175 min** | Testing        | Core scenarios, security, edge cases                  |
| **175–195 min** | Demo Polish    | UI, bugs, demo data, stability                        |
| **195–210 min** | Final Demo     | 3–5 minute demonstration and submission               |

**Absolute limit: 210 minutes.**

---

## 👥 Team Responsibilities

### Member 1 — Frontend

* Chat interface
* User input and responses
* Loading/status states
* Tool/action result display

### Member 2 — Backend + Database

* Customer/order/product data
* APIs
* Agent tools
* Refund/return logic
* Validation and source-of-truth verification

### Member 3 — AI Agent

* System prompt
* Intent detection
* Policy reasoning
* Tool selection
* Multi-intent handling
* Security and prompt-injection protection

### Member 4 — Testing + Integration

* End-to-end integration
* Test cases
* Edge cases
* Security testing
* Bug fixing
* Demo preparation

---

## 🤖 Agent Logic

The agent follows:

**UNDERSTAND → COLLECT → VERIFY → RETRIEVE POLICY → REASON → DECIDE → ACT → VERIFY RESULT**

It supports four terminal decisions:

* **ANSWER** — provide a verified response.
* **ASK** — request missing or unclear information.
* **ACT** — perform an authorized and policy-eligible action.
* **ESCALATE** — send unsafe, suspicious, contradictory, or out-of-scope cases to a human.

---

## 🛠️ Essential Tools

```text
get_customer
get_order
get_product
get_conversations
check_refund_eligibility
calculate_refund
create_return
create_refund
create_support_ticket
escalate_to_human
```

The **database remains the source of truth**. Customer messages cannot override verified information.

---

## 🔐 Security

Customer input is treated as **untrusted**.

The system protects against:

* Prompt injection
* Fake system instructions
* Policy bypass attempts
* Malicious tool arguments
* Unauthorized refunds
* Manipulation of verified data

Authority follows:

**System Rules > Business Policies > Tool Validation > Customer Input**

---

## 🧪 Testing

The MVP tests:

* Normal questions
* Order lookup
* Eligible/ineligible refunds
* Missing or ambiguous information
* Contradictory claims
* Prompt injection
* Suspicious requests
* Multi-intent requests
* Human escalation
* Tool failures

---

## 🚨 Emergency Fallback

If time runs short, remove advanced UI, analytics, complex infrastructure, and non-essential features.

The minimum MVP must retain:

**Chat UI + AI Agent + Database Verification + Policy Reasoning + One Real Tool + ASK + ACT + ESCALATE + Prompt-Injection Defense + End-to-End Demo**

---

## 🎬 Demo

The 3–5 minute demo should showcase:

1. Normal request → **ANSWER**
2. Refund request → **VERIFY + ACT**
3. Missing information → **ASK**
4. Prompt injection → **Reject safely**
5. Suspicious request → **ESCALATE**

> **Build fast. Verify everything. Reason safely. Act only when authorized.**
hi
