"""AI-powered document classifier and financial data extractor."""

import anthropic
import json
import os


def classify_and_parse_document(
    text: str,
    file_name: str,
    page_images: list[str] = None
) -> dict:
    """Use Claude to classify a document and extract structured financial data.

    Handles: brokerage statements, 1040s, paystubs, W-2s, insurance policies,
    estate documents, equity schedules, bank statements, mortgage statements.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    content = []

    if page_images:
        for img_b64 in page_images[:5]:
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": img_b64}
            })

    content.append({
        "type": "text",
        "text": f"""You are a senior financial paraplanner extracting structured data from a client document.

Document filename: {file_name}
{"Extracted text (may be incomplete for scanned docs):" if text else "This appears to be a scanned document — use the images above."}

{text[:8000] if text else ""}

Extract ALL financial data into the JSON structure below. Be thorough — extract every account, balance, income item, and liability with actual numbers. Do not summarize.

Return ONLY valid JSON, no markdown fences, no preamble:

{{
  "document_type": "<brokerage_statement | tax_return_1040 | paystub | w2 | estate_document | insurance_policy | balance_sheet | budget | equity_schedule | bank_statement | mortgage_statement | unknown>",
  "institution": "<firm name or null>",
  "document_date": "<YYYY-MM or null>",
  "owner": "<account owner name(s) or null>",
  "accounts": [
    {{
      "name": "<account name>",
      "account_type": "<401k | ira | roth_ira | brokerage | hsa | checking | savings | deferred_comp | pension | 529 | other>",
      "balance": <number or null>,
      "owner": "<name>",
      "institution": "<firm>",
      "allocation_notes": "<equity/bond mix if known>"
    }}
  ],
  "income": [
    {{
      "source": "<description>",
      "annual_amount": <number or null>,
      "period_amount": <number or null>,
      "period": "<annual | monthly | biweekly | per_paycheck>",
      "income_type": "<salary | bonus | rsu_vesting | dividend | rental | other>",
      "owner": "<name>"
    }}
  ],
  "expenses": [
    {{"category": "<description>", "annual_amount": <number or null>, "monthly_amount": <number or null>}}
  ],
  "assets": [
    {{"description": "<description>", "asset_type": "<real_estate | vehicle | business | other>", "market_value": <number or null>, "owner": "<name>"}}
  ],
  "liabilities": [
    {{"description": "<description>", "balance": <number or null>, "interest_rate": <number or null>, "monthly_payment": <number or null>, "lender": "<name or null>"}}
  ],
  "insurance": [
    {{"policy_type": "<life | disability | ltc | umbrella | property | health | other>", "coverage_amount": <number or null>, "annual_premium": <number or null>, "insured": "<name>", "carrier": "<name or null>", "details": "<key policy details>"}}
  ],
  "equity_compensation": [
    {{"grant_type": "<RSU | ISO | NSO | PSU | ESPP | other>", "company": "<name>", "shares_per_year": <number or null>, "vesting_years_remaining": <number or null>, "current_price": <number or null>, "owner": "<name>"}}
  ],
  "tax_info": {{
    "tax_year": <year or null>,
    "filing_status": "<single | mfj | mfs | hoh | null>",
    "adjusted_gross_income": <number or null>,
    "taxable_income": <number or null>,
    "total_tax": <number or null>,
    "effective_rate": <number or null>,
    "state": "<two-letter state or null>"
  }},
  "estate_info": {{
    "document_types_present": ["<will | trust | poa | healthcare_directive | hipaa | other>"],
    "last_updated": "<YYYY or null>",
    "notes": "<relevant details>"
  }},
  "notes": ["<important observations that don't fit elsewhere>"],
  "parse_confidence": "<high | medium | low>",
  "warnings": ["<ambiguities, missing data, or potential issues>"]
}}"""
    })

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": content}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw[raw.find("\n")+1:]
        if "```" in raw:
            raw = raw[:raw.rfind("```")]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "document_type": "unknown",
            "parse_confidence": "low",
            "warnings": ["Failed to parse AI extraction response", raw[:300]],
            "accounts": [], "income": [], "expenses": [], "assets": [],
            "liabilities": [], "insurance": [], "equity_compensation": [],
            "tax_info": {}, "estate_info": {}, "notes": []
        }
