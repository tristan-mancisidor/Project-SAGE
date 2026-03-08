"""Tool definitions and implementations for the SAGE agentic loop."""

import json
from pathlib import Path

from parsers.pdf_extractor import extract_pdf_text
from parsers.statement_parser import parse_financial_statement
from agent.monte_carlo import run_monte_carlo_simulation


# --- Tool schema definitions (sent to Claude API) ---

TOOL_DEFINITIONS = [
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


def _ensure_dict(value) -> dict:
    """Ensure a value is a dict. Parse JSON strings, wrap other types."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        return {"raw": value}
    if value is None:
        return {}
    return {"raw": str(value)}


# --- Tool execution dispatch ---

def execute_tool(tool_name: str, tool_input: dict, uploaded_files: dict) -> str:
    """Execute a tool by name and return the result as a string."""
    if tool_name == "extract_pdf_text":
        return _handle_extract_pdf(tool_input, uploaded_files)
    elif tool_name == "parse_financial_statement":
        return _handle_parse_statement(tool_input)
    elif tool_name == "analyze_net_worth":
        return _handle_analyze_net_worth(tool_input)
    elif tool_name == "analyze_income_and_expenses":
        return _handle_analyze_income_expenses(tool_input)
    elif tool_name == "run_monte_carlo":
        return _handle_monte_carlo(tool_input)
    elif tool_name == "identify_planning_gaps":
        return _handle_planning_gaps(tool_input)
    elif tool_name == "generate_plan_report":
        return _handle_generate_report(tool_input)
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def _handle_extract_pdf(tool_input: dict, uploaded_files: dict) -> str:
    file_id = tool_input["file_id"]
    if file_id not in uploaded_files:
        return json.dumps({"error": f"File {file_id} not found"})
    file_path = uploaded_files[file_id]["path"]
    text = extract_pdf_text(file_path)
    return json.dumps({"file_id": file_id, "text": text, "char_count": len(text)})


def _handle_parse_statement(tool_input: dict) -> str:
    text = tool_input["text"]
    doc_type = tool_input["document_type"]
    parsed = parse_financial_statement(text, doc_type)
    return json.dumps(parsed)


def _handle_analyze_net_worth(tool_input: dict) -> str:
    client_data = _ensure_dict(tool_input.get("client_data"))
    accounts = client_data.get("accounts", [])
    real_estate = client_data.get("real_estate", [])
    equity_comp = client_data.get("equity_compensation", [])
    liabilities = client_data.get("liabilities", [])

    total_investable = sum(a.get("balance", 0) for a in accounts)
    total_real_estate = sum(r.get("market_value", 0) for r in real_estate)
    total_equity_comp = sum(
        e.get("shares_per_year", 0) * e.get("vesting_years_remaining", 0) * e.get("current_price", 0)
        for e in equity_comp
    )
    total_liabilities = sum(l.get("balance", 0) for l in liabilities)
    mortgage_balances = sum(r.get("mortgage_balance", 0) for r in real_estate)
    total_liabilities += mortgage_balances

    total_assets = total_investable + total_real_estate + total_equity_comp
    net_worth = total_assets - total_liabilities

    result = {
        "total_investable_assets": total_investable,
        "total_real_estate": total_real_estate,
        "total_equity_compensation_value": total_equity_comp,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_worth": net_worth,
        "accounts_summary": [
            {"name": a.get("name"), "type": a.get("account_type"), "balance": a.get("balance", 0), "owner": a.get("owner")}
            for a in accounts
        ]
    }
    return json.dumps(result)


def _handle_analyze_income_expenses(tool_input: dict) -> str:
    client_data = _ensure_dict(tool_input.get("client_data"))
    income_sources = client_data.get("income_sources", [])
    expenses = client_data.get("expenses", [])

    total_income = sum(i.get("annual_amount", 0) for i in income_sources)
    total_expenses = sum(e.get("annual_amount", 0) for e in expenses)
    savings = total_income - total_expenses
    savings_rate = (savings / total_income * 100) if total_income > 0 else 0

    result = {
        "total_annual_income": total_income,
        "total_annual_expenses": total_expenses,
        "annual_savings": savings,
        "savings_rate_pct": round(savings_rate, 1),
        "income_breakdown": [
            {"source": i.get("source"), "amount": i.get("annual_amount", 0), "owner": i.get("owner"), "type": i.get("income_type")}
            for i in income_sources
        ],
        "expense_breakdown": [
            {"category": e.get("category"), "amount": e.get("annual_amount", 0)}
            for e in expenses
        ]
    }
    return json.dumps(result)


def _handle_monte_carlo(tool_input: dict) -> str:
    results = run_monte_carlo_simulation(
        portfolio_value=tool_input["portfolio_value"],
        annual_contribution=tool_input["annual_contribution"],
        annual_withdrawal=tool_input["annual_withdrawal"],
        years_to_retirement=tool_input["years_to_retirement"],
        years_in_retirement=tool_input["years_in_retirement"],
        risk_profile=tool_input["risk_profile"],
    )
    return json.dumps(results)


def _handle_planning_gaps(tool_input: dict) -> str:
    client_data = _ensure_dict(tool_input.get("client_data"))
    monte_carlo = _ensure_dict(tool_input.get("monte_carlo_results"))
    gaps = _identify_gaps(client_data, monte_carlo)
    return json.dumps(gaps)


def _handle_generate_report(tool_input: dict) -> str:
    client_data = _ensure_dict(tool_input.get("client_data"))
    gap_analysis = _ensure_dict(tool_input.get("gap_analysis"))
    monte_carlo = _ensure_dict(tool_input.get("monte_carlo_results"))
    plan_type = tool_input.get("plan_type", "new_client")

    report = {
        "plan_type": plan_type,
        "client_names": client_data.get("client_names", []),
        "sections": {
            "client_snapshot": _build_snapshot(client_data),
            "net_worth": client_data.get("net_worth_analysis", {}),
            "income_cash_flow": client_data.get("income_analysis", {}),
            "monte_carlo": monte_carlo,
            "planning_gaps": gap_analysis,
        },
        "status": "awaiting_approval"
    }
    return json.dumps(report)


# --- Gap analysis engine ---

def _identify_gaps(client_data: dict, monte_carlo: dict) -> dict:
    gaps = []

    # Retirement & Investment gaps
    if monte_carlo:
        success_rate = monte_carlo.get("base_case", {}).get("probability_of_success", 100)
        if success_rate < 80:
            gaps.append({
                "domain": "Retirement & Investment Planning",
                "gap": "Retirement funding shortfall risk",
                "description": f"Monte Carlo base case shows {success_rate}% probability of success, below the 80% threshold.",
                "impact": "High",
                "urgency": "High",
                "recommendation": "Increase annual savings, adjust asset allocation, or consider delaying retirement."
            })

    # Check equity compensation concentration
    equity_comp = client_data.get("equity_compensation", [])
    accounts = client_data.get("accounts", [])
    total_investable = sum(a.get("balance", 0) for a in accounts)
    total_equity = sum(
        e.get("shares_per_year", 0) * e.get("vesting_years_remaining", 0) * e.get("current_price", 0)
        for e in equity_comp
    )
    if total_investable > 0 and total_equity / (total_investable + total_equity) > 0.20:
        pct = round(total_equity / (total_investable + total_equity) * 100, 1)
        gaps.append({
            "domain": "Retirement & Investment Planning",
            "gap": "Equity compensation concentration risk",
            "description": f"Unvested equity compensation represents {pct}% of investable assets. Concentration above 20% introduces significant single-stock risk.",
            "impact": "High",
            "urgency": "Medium",
            "recommendation": "Implement systematic diversification plan: sell 20-25% of vesting shares annually."
        })

    # Tax Planning gaps
    income_sources = client_data.get("income_sources", [])
    total_income = sum(i.get("annual_amount", 0) for i in income_sources)
    if total_income > 200000:
        gaps.append({
            "domain": "Tax Planning",
            "gap": "Roth conversion opportunity window",
            "description": "Current income level suggests potential Roth conversion opportunity before retirement income changes and deferred comp distributions begin.",
            "impact": "High",
            "urgency": "High",
            "recommendation": "Model Roth conversion of amount that fills remaining bracket capacity before deferred comp distributions begin."
        })

    # Deferred comp timing
    deferred_comp = [a for a in accounts if a.get("account_type") == "deferred_comp"]
    if deferred_comp:
        gaps.append({
            "domain": "Tax Planning",
            "gap": "Deferred compensation payout timing risk",
            "description": "Deferred comp distributions may coincide with other retirement income, creating a high-income tax year.",
            "impact": "High",
            "urgency": "Medium",
            "recommendation": "Review deferred comp election schedule. Consider spreading distributions over 5-10 years to avoid bracket spikes."
        })

    # Estate Planning gaps
    estate_docs = client_data.get("estate_documents", {})
    last_updated = estate_docs.get("last_updated", "")
    # Flag if no docs, no date, or docs older than 3 years
    from datetime import datetime
    docs_outdated = False
    if last_updated:
        try:
            updated_date = datetime.strptime(last_updated, "%Y-%m-%d")
            docs_outdated = (datetime.now() - updated_date).days > 3 * 365
        except ValueError:
            docs_outdated = True
    if not estate_docs or not last_updated or docs_outdated:
        desc = "No current estate planning documents on file." if not last_updated else f"Estate documents last updated {last_updated} — over 3 years ago."
        missing = []
        if not estate_docs.get("revocable_trust"):
            missing.append("revocable trust")
        if not estate_docs.get("hipaa_authorization"):
            missing.append("HIPAA authorization")
        if missing:
            desc += f" Missing: {', '.join(missing)}."
        gaps.append({
            "domain": "Estate Planning",
            "gap": "Estate documents outdated" if docs_outdated else "Estate documents missing",
            "description": desc,
            "impact": "High",
            "urgency": "High",
            "recommendation": "Schedule estate attorney review. Establish revocable trust, update all documents, and verify beneficiary designations align with estate intent."
        })

    # Insurance gaps
    insurance = client_data.get("insurance", [])
    life_policies = [p for p in insurance if p.get("policy_type") == "life"]
    total_life_coverage = sum(p.get("coverage_amount", 0) for p in life_policies)
    if total_income > 0 and total_life_coverage < total_income * 10:
        gaps.append({
            "domain": "Risk Management & Insurance",
            "gap": "Life insurance coverage gap",
            "description": f"Total life insurance coverage (${total_life_coverage:,.0f}) is less than 10x annual income (${total_income:,.0f}). Coverage may be insufficient for income replacement and liability payoff.",
            "impact": "High",
            "urgency": "High",
            "recommendation": "Review life insurance needs analysis. Consider term coverage to bridge gap through retirement."
        })

    umbrella = [p for p in insurance if p.get("policy_type") == "umbrella"]
    if not umbrella:
        net_worth = client_data.get("net_worth", 0)
        gaps.append({
            "domain": "Risk Management & Insurance",
            "gap": "No umbrella liability policy",
            "description": "No umbrella liability coverage identified. High-net-worth clients should carry umbrella coverage at least equal to net worth.",
            "impact": "Medium",
            "urgency": "Medium",
            "recommendation": "Add umbrella liability policy with coverage matching net worth."
        })

    return {
        "total_gaps": len(gaps),
        "gaps": gaps,
        "domains_reviewed": [
            "Retirement & Investment Planning",
            "Tax Planning",
            "Estate Planning",
            "Risk Management & Insurance"
        ]
    }


def _build_snapshot(client_data: dict) -> dict:
    return {
        "client_names": client_data.get("client_names", []),
        "ages": client_data.get("ages", []),
        "filing_status": client_data.get("filing_status", ""),
        "retirement_ages": client_data.get("retirement_ages", []),
        "risk_profile": client_data.get("risk_profile", ""),
    }
