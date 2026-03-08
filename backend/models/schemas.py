"""Pydantic models for Project SAGE client data and API payloads."""

from __future__ import annotations

from pydantic import BaseModel
from typing import Dict, List, Optional


class Account(BaseModel):
    name: str
    account_type: str  # "brokerage", "401k", "ira", "roth_ira", "hsa", "deferred_comp", "checking", "savings"
    balance: float
    owner: str  # "James", "Sarah", "Joint"
    managed: bool = True  # under advisory management


class RealEstate(BaseModel):
    description: str
    market_value: float
    mortgage_balance: float = 0.0
    owner: str = "Joint"


class EquityCompensation(BaseModel):
    grant_type: str  # "RSU", "PSU", "ISO", "NSO"
    shares_per_year: int
    vesting_years_remaining: int
    current_price: float
    owner: str


class Liability(BaseModel):
    description: str
    balance: float
    rate: float = 0.0
    monthly_payment: float = 0.0


class InsurancePolicy(BaseModel):
    policy_type: str  # "life", "disability", "ltc", "umbrella", "property"
    coverage_amount: float
    annual_premium: float = 0.0
    owner: str
    details: str = ""


class IncomeSource(BaseModel):
    source: str
    annual_amount: float
    owner: str
    income_type: str = "salary"  # "salary", "bonus", "rsu_vesting", "rental", "business", "social_security"


class Expense(BaseModel):
    category: str
    annual_amount: float


class ClientProfile(BaseModel):
    client_names: list[str]
    ages: list[int]
    filing_status: str = "married_filing_jointly"
    state: str = "CA"
    accounts: list[Account] = []
    real_estate: list[RealEstate] = []
    equity_compensation: list[EquityCompensation] = []
    liabilities: list[Liability] = []
    insurance: list[InsurancePolicy] = []
    income_sources: list[IncomeSource] = []
    expenses: list[Expense] = []
    retirement_ages: list[int] = []
    risk_profile: str = "moderate"
    estate_documents: dict = {}
    notes: list[str] = []


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    status: str = "uploaded"


class AnalyzeRequest(BaseModel):
    file_ids: list[str] = []
    demo_mode: bool = True
    message: Optional[str] = None
    conversation_history: list[dict] = []


class AnalyzeResponse(BaseModel):
    response: str
    tool_calls: list[dict] = []
    conversation_history: list[dict] = []
    status: str = "in_progress"  # "in_progress", "awaiting_approval", "complete"


class ApprovalAction(BaseModel):
    action: str  # "approve", "modify", "redirect"
    section: Optional[str] = None
    feedback: Optional[str] = None
    conversation_history: list[dict] = []
