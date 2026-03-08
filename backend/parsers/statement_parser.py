"""Financial statement parser.

Extracts structured data from raw PDF text based on document type.
V1 uses pattern matching for common financial document formats.
"""

import json
import re


def parse_financial_statement(text: str, document_type: str) -> dict:
    """Parse raw text into structured financial data based on document type."""
    parsers = {
        "brokerage_statement": _parse_brokerage,
        "tax_return": _parse_tax_return,
        "balance_sheet": _parse_balance_sheet,
        "insurance_policy": _parse_insurance,
        "equity_schedule": _parse_equity_schedule,
        "financial_plan": _parse_financial_plan,
    }
    parser = parsers.get(document_type, _parse_generic)
    return parser(text)


def _extract_dollar_amounts(text: str) -> list[float]:
    """Find all dollar amounts in text."""
    pattern = r'\$[\d,]+(?:\.\d{2})?'
    matches = re.findall(pattern, text)
    return [float(m.replace('$', '').replace(',', '')) for m in matches]


def _extract_percentages(text: str) -> list[float]:
    """Find all percentages in text."""
    pattern = r'(\d+(?:\.\d+)?)\s*%'
    matches = re.findall(pattern, text)
    return [float(m) for m in matches]


def _parse_brokerage(text: str) -> dict:
    """Parse brokerage/investment account statement."""
    amounts = _extract_dollar_amounts(text)
    total_value = max(amounts) if amounts else 0

    accounts = []
    account_patterns = [
        (r'(?i)(401\s*\(?k\)?|401k)', "401k"),
        (r'(?i)(roth\s*ira)', "roth_ira"),
        (r'(?i)(traditional\s*ira|ira)', "ira"),
        (r'(?i)(brokerage|taxable|individual)', "brokerage"),
        (r'(?i)(hsa|health\s*savings)', "hsa"),
    ]
    for pattern, account_type in account_patterns:
        if re.search(pattern, text):
            accounts.append({"account_type": account_type, "detected": True})

    return {
        "document_type": "brokerage_statement",
        "total_value": total_value,
        "accounts_detected": accounts,
        "dollar_amounts": amounts[:20],
        "raw_length": len(text),
        "parse_confidence": "medium" if amounts else "low",
    }


def _parse_tax_return(text: str) -> dict:
    """Parse tax return (1040) data."""
    amounts = _extract_dollar_amounts(text)

    agi = 0
    taxable_income = 0
    total_tax = 0

    agi_match = re.search(r'(?i)adjusted\s*gross\s*income.*?\$?([\d,]+)', text)
    if agi_match:
        agi = float(agi_match.group(1).replace(',', ''))

    taxable_match = re.search(r'(?i)taxable\s*income.*?\$?([\d,]+)', text)
    if taxable_match:
        taxable_income = float(taxable_match.group(1).replace(',', ''))

    tax_match = re.search(r'(?i)total\s*tax.*?\$?([\d,]+)', text)
    if tax_match:
        total_tax = float(tax_match.group(1).replace(',', ''))

    effective_rate = (total_tax / agi * 100) if agi > 0 else 0

    return {
        "document_type": "tax_return",
        "adjusted_gross_income": agi,
        "taxable_income": taxable_income,
        "total_tax": total_tax,
        "effective_tax_rate": round(effective_rate, 2),
        "dollar_amounts": amounts[:20],
        "parse_confidence": "medium" if agi > 0 else "low",
    }


def _parse_balance_sheet(text: str) -> dict:
    """Parse personal balance sheet."""
    amounts = _extract_dollar_amounts(text)
    return {
        "document_type": "balance_sheet",
        "dollar_amounts": amounts[:30],
        "total_amounts_found": len(amounts),
        "raw_length": len(text),
        "parse_confidence": "medium" if amounts else "low",
    }


def _parse_insurance(text: str) -> dict:
    """Parse insurance policy document."""
    amounts = _extract_dollar_amounts(text)
    policy_type = "unknown"

    type_patterns = [
        (r'(?i)(life\s*insurance|term\s*life|whole\s*life|universal\s*life)', "life"),
        (r'(?i)(disability|ltd|std)', "disability"),
        (r'(?i)(long[\s-]*term\s*care|ltc)', "ltc"),
        (r'(?i)(umbrella|excess\s*liability)', "umbrella"),
    ]
    for pattern, ptype in type_patterns:
        if re.search(pattern, text):
            policy_type = ptype
            break

    coverage = max(amounts) if amounts else 0
    premium_match = re.search(r'(?i)premium.*?\$?([\d,]+)', text)
    premium = float(premium_match.group(1).replace(',', '')) if premium_match else 0

    return {
        "document_type": "insurance_policy",
        "policy_type": policy_type,
        "coverage_amount": coverage,
        "annual_premium": premium,
        "parse_confidence": "medium" if policy_type != "unknown" else "low",
    }


def _parse_equity_schedule(text: str) -> dict:
    """Parse equity compensation schedule (RSU/ISO/NSO)."""
    amounts = _extract_dollar_amounts(text)

    grant_type = "RSU"
    grant_patterns = [
        (r'(?i)(restricted\s*stock\s*unit|rsu)', "RSU"),
        (r'(?i)(incentive\s*stock\s*option|iso)', "ISO"),
        (r'(?i)(non[\s-]*qualified|nso|nqso)', "NSO"),
        (r'(?i)(performance\s*share|psu)', "PSU"),
    ]
    for pattern, gtype in grant_patterns:
        if re.search(pattern, text):
            grant_type = gtype
            break

    shares_match = re.search(r'(\d[\d,]*)\s*(?:shares|units)', text, re.IGNORECASE)
    shares = int(shares_match.group(1).replace(',', '')) if shares_match else 0

    price_match = re.search(r'(?i)(?:price|value|fmv).*?\$?([\d,.]+)', text)
    price = float(price_match.group(1).replace(',', '')) if price_match else 0

    return {
        "document_type": "equity_schedule",
        "grant_type": grant_type,
        "shares_detected": shares,
        "price_detected": price,
        "total_value": shares * price if shares and price else 0,
        "parse_confidence": "medium" if shares > 0 else "low",
    }


def _parse_financial_plan(text: str) -> dict:
    """Parse existing financial plan document."""
    amounts = _extract_dollar_amounts(text)
    percentages = _extract_percentages(text)

    return {
        "document_type": "financial_plan",
        "dollar_amounts": amounts[:30],
        "percentages": percentages[:20],
        "total_amounts_found": len(amounts),
        "raw_length": len(text),
        "parse_confidence": "medium",
    }


def _parse_generic(text: str) -> dict:
    """Generic fallback parser."""
    amounts = _extract_dollar_amounts(text)
    return {
        "document_type": "unknown",
        "dollar_amounts": amounts[:20],
        "raw_length": len(text),
        "parse_confidence": "low",
    }
