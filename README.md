# Project SAGE
### Senior AI Guidance Engine for Financial Advisors

> *An agentic AI system that thinks like a CFP® professional — analyzing client documents, identifying planning gaps, modeling scenarios, and delivering advisor-ready financial plans.*

---

## What Is SAGE?

Financial advisors spend hours preparing for client meetings: gathering documents, updating net worth statements, modeling scenarios, and synthesizing everything into a coherent plan narrative. SAGE automates that preparation.

Drop in a client's financial documents — tax returns, brokerage statements, balance sheets, insurance policies, equity compensation schedules — and SAGE reasons across all of them like a senior CFP® professional. It surfaces gaps, flags risks, models what-if scenarios with Monte Carlo projections, and hands the advisor a structured, presentation-ready plan — all before they walk into the room.

SAGE is designed for advisors who want to spend their time *advising*, not preparing.

---

## How It Works

SAGE is a true AI agent, not a document parser. It uses a multi-step reasoning loop powered by Claude, with discrete tools it selects and sequences autonomously:

```
Upload Documents
      ↓
Sage Reads & Extracts (PDF tool)
      ↓
Net Worth Analysis → Income Analysis → Expenses & Tax Analysis
      ↓
Balance Sheet + Cash Flow Synthesis
      ↓
Monte Carlo Scenario Modeling
      ↓
Gap Report + Recommendations
      ↓
Advisor Approval Loop (approve, modify, or redirect)
      ↓
Final Plan Output
```

The advisor stays in control at every stage. SAGE presents its findings, explains its reasoning, and asks for confirmation before moving forward — exactly how a brilliant junior partner would operate.

---

## Planning Domains

SAGE reasons across all four core CFP® planning domains:

| Domain | What SAGE Analyzes |
|---|---|
| **Retirement & Investment Planning** | Portfolio allocation, projected shortfalls, equity compensation (RSU/PSU/ISO), vesting schedules, contribution room |
| **Tax Planning** | Effective vs. marginal rates, Roth conversion opportunities, tax-loss harvesting gaps, deferred comp strategy |
| **Estate Planning** | Beneficiary alignment, trust structures, estate tax exposure, transfer strategy gaps |
| **Risk Management & Insurance** | Life, disability, LTC, liability coverage gaps relative to net worth and income |

---

## The Planning Workflow

SAGE mirrors the meeting preparation workflow used at leading RIAs:

1. **Net Worth Review** — Accounts under management, held-away assets, equity compensation, liabilities
2. **Income Analysis** — Salary, distributions, vesting schedules, rental or business income
3. **Expenses & Tax Review** — Cash flow gaps, tax drag, optimization opportunities
4. **Balance Sheet + Cash Flow Report** — How everything connects; new vs. existing client comparison
5. **Scenario Modeling** — Monte Carlo projections showing base case, optimistic, and stress scenarios
6. **Advisor Approval Loop** — SAGE presents, advisor approves or redirects, plan is finalized

---

## Demo

> *The v1 demo uses a hypothetical high-net-worth client with equity compensation, a deferred comp balance, and a retirement planning gap. All data is synthetic.*

**[Live Demo →](https://project-sage.onrender.com)**

**What the demo shows:**
- Drag-and-drop document upload (PDF financial plan + brokerage statement + tax return)
- SAGE's live reasoning loop with tool call transparency
- Net worth → income → expenses → cash flow synthesis
- Monte Carlo projection (10,000 simulations, three scenarios)
- Gap report with prioritized recommendations
- Advisor approval loop: approve, modify, or ask SAGE to remodel

---

## Architecture

```
Frontend (React)
  └── Drag-and-drop upload UI
  └── Live agent reasoning feed
  └── Report viewer + approval interface

Backend (Python / FastAPI)
  └── Anthropic Claude API (claude-sonnet-4-20250514)
  └── Agentic tool loop
       ├── extract_pdf_text()
       ├── parse_financial_statement()
       ├── analyze_equity_compensation()
       ├── run_monte_carlo()
       ├── identify_planning_gaps()
       └── generate_plan_report()
  └── Render deployment
```

---

## Roadmap

**Phase 1 (current) — Demo**
- Hypothetical client data
- Full agentic workflow
- Simplified Monte Carlo engine
- Advisor approval loop

**Phase 2 — Real Document Intelligence**
- Multi-document reconciliation (conflicting data handling)
- Tax return parsing (1040, K-1, W-2)
- Equity compensation schedule parsing (grant agreements, vesting tables)
- Real brokerage statement parsing

**Phase 3 — Platform Integration**
- MCP integration with eMoney and/or RightCapital
- Direct plan value writes with advisor approval gate
- Scenario sync to Decision Center

---

## Why I Built This

I'm a Paraplanner at a wealth management firm. The meeting preparation workflow SAGE automates is work I do manually every week — updating net worth statements, modeling scenarios in planning software, synthesizing client documents into a coherent narrative for the advisor.

I built SAGE because the Paraplanner role is evolving rapidly. The advisors who will win over the next decade are the ones with an AI partner that handles preparation so they can focus entirely on the client relationship. SAGE is that partner.

---

## Tech Stack

- **Backend:** Python 3.11, FastAPI, Anthropic Python SDK
- **Frontend:** React, Tailwind CSS
- **AI:** Claude (claude-sonnet-4-20250514), tool use / agentic loop
- **Deployment:** Render
- **PDF Processing:** PyMuPDF (fitz)
- **Monte Carlo:** NumPy

---

## Related Projects

- **[Receipt Ranger](https://github.com/tristan-mancisidor/receipt-ranger)** — Telegram bot using Claude Vision to parse receipts and log to Google Sheets budgeting system. Deployed on Render.

---

*Built by Tristan Mancisidor*
