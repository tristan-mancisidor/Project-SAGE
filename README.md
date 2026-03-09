# Project SAGE
### Senior AI Guidance Engine

An agentic AI system that thinks like a CFP professional — upload a client's financial documents and SAGE reasons across all of them, surfaces planning gaps, models Monte Carlo scenarios, and delivers an advisor-ready financial plan. Built to automate the meeting preparation workflow that paraplanners do manually every week.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI |
| AI | Anthropic Claude API (claude-sonnet-4-20250514), agentic tool loop |
| Frontend | React, Tailwind CSS |
| PDF Processing | PyMuPDF (fitz) |
| Monte Carlo Engine | NumPy |
| Deployment | Render (backend + static frontend) |

## Key Features

- **Agentic reasoning loop** — SAGE autonomously selects and sequences tools (PDF extraction, financial parsing, net worth analysis, income/expense analysis, Monte Carlo projection, gap identification, report generation) rather than following a fixed pipeline
- **Multi-document financial parsing** — Handles brokerage statements, tax returns, balance sheets, insurance policies, equity compensation schedules, and financial plans
- **CFP-level gap analysis** — Identifies gaps across all four core planning domains: retirement/investment, tax, estate, and risk management/insurance
- **Monte Carlo scenario modeling** — 10,000-simulation projections across base, optimistic, and stress scenarios with configurable risk profiles
- **Advisor approval loop** — SAGE presents findings section by section; the advisor can approve, modify, or redirect before the plan is finalized
- **Live reasoning transparency** — The frontend streams SAGE's tool calls and reasoning in real time so advisors can see the agent thinking, not just the result
- **Equity compensation analysis** — RSU/PSU/ISO vesting schedules, deferred comp payout timing, and Roth conversion opportunity detection

## Architecture Overview

The system is split into a FastAPI backend and a React frontend. On the backend, SAGE operates as a true AI agent using Claude's tool use feature — the backend defines discrete tools (PDF extraction, financial statement parsing, net worth analysis, income/expense analysis, Monte Carlo projection, gap identification, report generation) and Claude decides which to call and in what order. A typical run flows from document upload through PDF extraction, structured parsing, net worth synthesis, income and expense analysis, cash flow modeling, Monte Carlo projections, and finally a gap report with prioritized recommendations. The frontend provides a drag-and-drop upload interface, a live agent reasoning feed that streams tool calls as they happen, a structured report viewer, and an approval panel where the advisor controls the final output. Both services are deployed on Render.

## Demo

- **Backend:** [project-sage.onrender.com](https://project-sage.onrender.com)
- **Frontend:** [project-sage-frontend.onrender.com](https://project-sage-frontend.onrender.com)

The demo uses a synthetic high-net-worth client profile (equity compensation, deferred comp, retirement planning gap) to showcase the full workflow.

## Status

**Live / In Development** (Phase 1 complete)

V1 demo is deployed and functional. Roadmap includes real multi-document reconciliation, tax return parsing (1040, K-1, W-2), and MCP integration with planning platforms like eMoney or RightCapital.

## Background

I'm a Paraplanner at a wealth management firm. The meeting preparation workflow SAGE automates — updating net worth statements, modeling scenarios, synthesizing documents into a coherent plan narrative — is work I do manually every week. I built SAGE because the advisors who will win over the next decade are the ones with an AI partner that handles preparation so they can focus entirely on the client relationship.
