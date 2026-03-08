"""Hypothetical client data for James & Sarah Chen.

This data is used in demo mode. All data is synthetic.
Profile defined in CLAUDE.md.
"""

DEMO_CLIENT_DATA = {
    "client_names": ["James Chen", "Sarah Chen"],
    "ages": [52, 49],
    "filing_status": "married_filing_jointly",
    "state": "CA",
    "retirement_ages": [62, 60],
    "risk_profile": "moderate",

    "accounts": [
        {
            "name": "James 401(k) — Fidelity",
            "account_type": "401k",
            "balance": 620000,
            "owner": "James",
            "managed": True,
        },
        {
            "name": "Sarah 401(k) — Vanguard",
            "account_type": "401k",
            "balance": 185000,
            "owner": "Sarah",
            "managed": True,
        },
        {
            "name": "Joint Brokerage — Schwab",
            "account_type": "brokerage",
            "balance": 340000,
            "owner": "Joint",
            "managed": True,
        },
        {
            "name": "James Roth IRA — Schwab",
            "account_type": "roth_ira",
            "balance": 95000,
            "owner": "James",
            "managed": True,
        },
        {
            "name": "Sarah Roth IRA — Schwab",
            "account_type": "roth_ira",
            "balance": 72000,
            "owner": "Sarah",
            "managed": True,
        },
        {
            "name": "James HSA — HealthEquity",
            "account_type": "hsa",
            "balance": 38000,
            "owner": "James",
            "managed": False,
        },
        {
            "name": "Joint Savings — Chase",
            "account_type": "savings",
            "balance": 50000,
            "owner": "Joint",
            "managed": False,
        },
        {
            "name": "James Deferred Comp Plan",
            "account_type": "deferred_comp",
            "balance": 220000,
            "owner": "James",
            "managed": False,
        },
    ],

    "real_estate": [
        {
            "description": "Primary Residence — Walnut Creek, CA",
            "market_value": 950000,
            "mortgage_balance": 280000,
            "owner": "Joint",
        },
    ],

    "equity_compensation": [
        {
            "grant_type": "RSU",
            "shares_per_year": 2000,
            "vesting_years_remaining": 4,
            "current_price": 85.0,
            "owner": "James",
        },
    ],

    "liabilities": [
        {
            "description": "Mortgage — Primary Residence",
            "balance": 280000,
            "rate": 3.25,
            "monthly_payment": 2450,
        },
    ],

    "insurance": [
        {
            "policy_type": "life",
            "coverage_amount": 500000,
            "annual_premium": 1200,
            "owner": "James",
            "details": "20-year term, expires in 8 years",
        },
        {
            "policy_type": "life",
            "coverage_amount": 250000,
            "annual_premium": 680,
            "owner": "Sarah",
            "details": "20-year term, expires in 11 years",
        },
        {
            "policy_type": "disability",
            "coverage_amount": 14000,
            "annual_premium": 2400,
            "owner": "James",
            "details": "Own-occupation, 60% income replacement, 90-day elimination",
        },
        {
            "policy_type": "property",
            "coverage_amount": 950000,
            "annual_premium": 3200,
            "owner": "Joint",
            "details": "Homeowners — HO-3 policy",
        },
    ],

    "income_sources": [
        {
            "source": "James — Base Salary (TechCorp)",
            "annual_amount": 280000,
            "owner": "James",
            "income_type": "salary",
        },
        {
            "source": "James — RSU Vesting (estimated annual)",
            "annual_amount": 170000,
            "owner": "James",
            "income_type": "rsu_vesting",
        },
        {
            "source": "Sarah — Salary (Regional Medical Center)",
            "annual_amount": 100000,
            "owner": "Sarah",
            "income_type": "salary",
        },
    ],

    "expenses": [
        {"category": "Mortgage (P&I + escrow)", "annual_amount": 36000},
        {"category": "Property taxes", "annual_amount": 11400},
        {"category": "Insurance premiums (all)", "annual_amount": 7480},
        {"category": "Healthcare / medical", "annual_amount": 8500},
        {"category": "Groceries & dining", "annual_amount": 18000},
        {"category": "Transportation (2 vehicles)", "annual_amount": 14000},
        {"category": "Utilities & home maintenance", "annual_amount": 9600},
        {"category": "Children (college savings, activities)", "annual_amount": 24000},
        {"category": "Travel & recreation", "annual_amount": 12000},
        {"category": "Charitable giving", "annual_amount": 8000},
        {"category": "Miscellaneous", "annual_amount": 6000},
    ],

    "estate_documents": {
        "will": True,
        "revocable_trust": False,
        "durable_poa": True,
        "healthcare_directive": True,
        "hipaa_authorization": False,
        "last_updated": "2018-03-15",
        "notes": "Documents drafted in 2018 before James's equity compensation began. No trust established. Beneficiary designations may not align with current intent.",
    },

    "notes": [
        "James considering early retirement at 60 if equity comp performs well.",
        "Sarah wants to continue working part-time after 60.",
        "Two children: ages 19 (college sophomore) and 16 (high school junior).",
        "James's deferred comp plan allows lump sum or 5/10/15-year installment elections.",
        "No long-term care insurance in place.",
        "No umbrella liability policy.",
        "Current 60/40 allocation: 60% equities (US large cap tilt), 40% fixed income (intermediate-term).",
    ],
}
