# CLAUDE.md — Project SAGE

## What This Project Is

Project SAGE (Senior AI Guidance Engine) is a CFP-level AI agent for financial advisors. Advisors upload client documents; SAGE reasons across them using an agentic tool loop, produces a structured financial plan gap report, models Monte Carlo scenarios, and presents findings to the advisor for approval before finalizing output.

This is a portfolio project built by Tristan Mancisidor, a Paraplanner at a wealth management firm. The workflow SAGE automates mirrors real RIA meeting preparation.

---

## Current Status

**Phase: Active Development — V1 Demo**

What exists:
- [x] Project scaffolding
- [x] FastAPI backend with tool loop skeleton
- [x] React frontend with upload UI
- [x] PDF extraction tool
- [x] Financial statement parser
- [x] Monte Carlo engine (simplified)
- [x] Gap analysis logic
- [x] Advisor approval loop
- [ ] Render deployment

Update this checklist as features are completed.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| AI | Anthropic Python SDK, claude-sonnet-4-20250514 |
| Frontend | React, Tailwind CSS |
| PDF Processing | PyMuPDF (fitz) |
| Monte Carlo | NumPy |
| Deployment | Render (free tier) |

---

## File Structure

```
project-sage/
├── CLAUDE.md                  ← You are here
├── README.md                  ← Public-facing GitHub portfolio doc
├── SKILL.md                   ← Sage's CFP identity and reasoning framework
├── backend/
│   ├── main.py                ← FastAPI app entry point
│   ├── agent/
│   │   ├── sage.py            ← Core agentic loop
│   │   ├── tools.py           ← Tool definitions and implementations
│   │   ├── prompts.py         ← System prompt and identity (loads from SKILL.md)
│   │   └── monte_carlo.py     ← Monte Carlo projection engine
│   ├── parsers/
│   │   ├── pdf_extractor.py   ← PyMuPDF text extraction
│   │   └── statement_parser.py← Financial statement structure parsing
│   ├── models/
│   │   └── schemas.py         ← Pydantic models for client data
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── UploadZone.jsx      ← Drag-and-drop document upload
│   │   │   ├── AgentFeed.jsx       ← Live reasoning transparency feed
│   │   │   ├── ReportViewer.jsx    ← Structured plan output
│   │   │   └── ApprovalPanel.jsx   ← Advisor approve / modify / redirect
│   │   └── index.css
│   └── package.json
└── .env.example
```

---

## Architecture: The Agentic Loop

SAGE uses Claude's tool use feature. The backend defines discrete tools; Claude decides which to call and in what order to accomplish the advisor's goal.

### Tool Definitions

```python
tools = [
    {
        "name": "extract_pdf_text",
        "description": "Extract raw text from an uploaded PDF document",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_id": {"type": "string", "description": "ID of the uploaded file"}
            },
            "required": ["file_id"]
        }
    },
    {
        "name": "parse_financial_statement",
        "description": "Parse extracted text into structured financial data (accounts, balances, income, expenses)",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "document_type": {
                    "type": "string",
                    "enum": ["brokerage_statement", "tax_return", "balance_sheet", "insurance_policy", "equity_schedule", "financial_plan"]
                }
            },
            "required": ["text", "document_type"]
        }
    },
    {
        "name": "analyze_net_worth",
        "description": "Synthesize all accounts, assets, and liabilities into a net worth statement",
        "input_schema": {
            "type": "object",
            "properties": {
                "client_data": {"type": "object"}
            },
            "required": ["client_data"]
        }
    },
    {
        "name": "analyze_income_and_expenses",
        "description": "Analyze income sources, expense categories, cash flow, and tax efficiency",
        "input_schema": {
            "type": "object",
            "properties": {
                "client_data": {"type": "object"}
            },
            "required": ["client_data"]
        }
    },
    {
        "name": "run_monte_carlo",
        "description": "Run Monte Carlo simulation projecting portfolio value to end of plan under base, optimistic, and stress scenarios",
        "input_schema": {
            "type": "object",
            "properties": {
                "portfolio_value": {"type": "number"},
                "annual_contribution": {"type": "number"},
                "annual_withdrawal": {"type": "number"},
                "years_to_retirement": {"type": "integer"},
                "years_in_retirement": {"type": "integer"},
                "risk_profile": {"type": "string", "enum": ["conservative", "moderate", "aggressive"]}
            },
            "required": ["portfolio_value", "annual_contribution", "annual_withdrawal", "years_to_retirement", "years_in_retirement", "risk_profile"]
        }
    },
    {
        "name": "identify_planning_gaps",
        "description": "Identify gaps across all four CFP planning domains based on synthesized client data",
        "input_schema": {
            "type": "object",
            "properties": {
                "client_data": {"type": "object"},
                "monte_carlo_results": {"type": "object"}
            },
            "required": ["client_data"]
        }
    },
    {
        "name": "generate_plan_report",
        "description": "Generate final structured advisor-ready plan report with recommendations and approval request",
        "input_schema": {
            "type": "object",
            "properties": {
                "client_data": {"type": "object"},
                "gap_analysis": {"type": "object"},
                "monte_carlo_results": {"type": "object"},
                "plan_type": {"type": "string", "enum": ["new_client", "existing_client_update"]}
            },
            "required": ["client_data", "gap_analysis", "plan_type"]
        }
    }
]
```

---

## The Advisor Approval Loop

After SAGE generates its report, it enters an approval loop — it does not finalize anything without advisor confirmation. The loop works as follows:

1. SAGE presents findings section by section
2. Advisor can: **Approve** (move to next section), **Modify** (provide correction, SAGE updates), or **Redirect** (give SAGE new instructions)
3. After all sections approved, SAGE generates the final output
4. Final output is printable / exportable

This is implemented as a continued conversation with full message history passed on each turn.

---

## Demo Client: The Hypothetical

V1 uses a pre-built hypothetical client profile. Do not use real client data.

**Client Profile: "James & Sarah Chen"**
- Ages: 52 and 49
- Combined income: $380,000 (James: $280K base + RSU grants; Sarah: $100K)
- RSU vesting: 2,000 shares/year over 4 years, current stock price $85
- Investable assets: $1.4M (60/40 allocation)
- Deferred comp balance: $220,000
- Home equity: $650,000
- Liabilities: $280,000 mortgage
- Retirement target: James at 62, Sarah at 60
- Key gaps to surface: Roth conversion opportunity, insurance coverage gap, estate docs outdated, deferred comp payout timing risk

---

## Key Engineering Principles (Carry Forward from Receipt Ranger)

- **Runtime over startup-time**: Derive dynamic values at moment of use, never cache at startup
- **Sanitize AI output before parsing**: Strip ```json fences before JSON.parse()
- **Always stream agent reasoning to frontend**: Advisors need to see SAGE thinking, not just the result
- **CLAUDE.md is the control plane**: Update this file at every meaningful milestone
- **Ship the demo first**: Full fidelity is Phase 2. Working demo is the goal.

---

## Environment Variables

```
ANTHROPIC_API_KEY=
PORT=8000
DEMO_MODE=true
```

---

## Deployment

Render free tier. Same pattern as Receipt Ranger.

- Backend: Python web service
- Frontend: Static site
- Both auto-deploy from GitHub main branch

---

## What To Build Next (Priority Order)

1. Project scaffolding (folder structure, requirements.txt, package.json)
2. FastAPI app with `/upload` and `/analyze` endpoints
3. PDF extraction tool
4. Agentic loop in `sage.py`
5. React upload UI with drag-and-drop
6. Monte Carlo engine
7. Gap analysis logic
8. Agent feed (live reasoning transparency)
9. Approval loop
10. Report viewer
11. Hypothetical client data seeding
12. Render deployment
