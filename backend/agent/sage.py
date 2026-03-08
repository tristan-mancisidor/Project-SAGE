"""Core agentic loop for Project SAGE.

Sage uses Claude's tool use to autonomously reason through client financial data.
The loop continues until Claude produces a final text response without tool calls.
"""

from __future__ import annotations

import json
import os

import anthropic

from agent.prompts import load_system_prompt
from agent.tools import TOOL_DEFINITIONS, execute_tool
from agent.demo_data import DEMO_CLIENT_DATA
from models.schemas import AnalyzeResponse


MODEL = "claude-sonnet-4-20250514"
MAX_TOOL_ROUNDS = 20


async def run_sage_loop(
    file_ids: list[str],
    uploaded_files: dict,
    demo_mode: bool = True,
    message: str | None = None,
    conversation_history: list[dict] | None = None,
) -> AnalyzeResponse:
    """Run the Sage agentic loop. Returns when Claude produces a final text response."""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    system_prompt = load_system_prompt()

    # Build or continue conversation
    messages = list(conversation_history) if conversation_history else []
    tool_calls_log = []

    if not messages:
        # First turn — build initial user message
        user_content = _build_initial_message(file_ids, demo_mode, message)
        if demo_mode:
            user_content += f"\n\nHere is the complete client data for James & Sarah Chen:\n{json.dumps(DEMO_CLIENT_DATA, indent=2)}"
        messages.append({"role": "user", "content": user_content})
    elif message:
        # Continuation — advisor follow-up
        messages.append({"role": "user", "content": message})

    # Agentic loop: call Claude, execute tools, feed results back
    for _ in range(MAX_TOOL_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # Collect assistant response
        assistant_content = response.content
        messages.append({"role": "assistant", "content": _serialize_content(assistant_content)})

        # Check if Claude wants to use tools
        tool_use_blocks = [b for b in assistant_content if b.type == "tool_use"]

        if not tool_use_blocks:
            # No tool calls — Claude is done reasoning, extract text
            text_blocks = [b.text for b in assistant_content if b.type == "text"]
            final_text = "\n".join(text_blocks)

            # Determine status based on content
            status = "awaiting_approval" if "approve" in final_text.lower() or "approval" in final_text.lower() else "complete"

            return AnalyzeResponse(
                response=final_text,
                tool_calls=tool_calls_log,
                conversation_history=messages,
                status=status,
            )

        # Execute each tool call and collect results
        tool_results = []
        for tool_block in tool_use_blocks:
            tool_name = tool_block.name
            tool_input = tool_block.input
            tool_id = tool_block.id

            tool_calls_log.append({
                "tool": tool_name,
                "input_summary": _summarize_input(tool_name, tool_input),
            })

            result = execute_tool(tool_name, tool_input, uploaded_files)

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})

    # Exceeded max rounds
    return AnalyzeResponse(
        response="Analysis reached maximum reasoning depth. Please review partial results and provide direction.",
        tool_calls=tool_calls_log,
        conversation_history=messages,
        status="in_progress",
    )


def _build_initial_message(file_ids: list[str], demo_mode: bool, message: str | None) -> str:
    """Build the initial user message for the first turn."""
    if demo_mode:
        return (
            "I'm running in demo mode with the hypothetical client profile for James & Sarah Chen. "
            "Please begin your full analysis. Start by reviewing the client data, then work through "
            "net worth analysis, income and cash flow, Monte Carlo projections, and gap identification. "
            "Present your findings section by section and ask for my approval before finalizing.\n\n"
            f"Additional context: {message}" if message else
            "I'm running in demo mode with the hypothetical client profile for James & Sarah Chen. "
            "Please begin your full analysis. Start by reviewing the client data, then work through "
            "net worth analysis, income and cash flow, Monte Carlo projections, and gap identification. "
            "Present your findings section by section and ask for my approval before finalizing."
        )

    if file_ids:
        file_list = ", ".join(file_ids)
        base = f"I've uploaded the following documents for analysis: {file_list}. "
        base += "Please extract and parse each document, then perform a comprehensive financial plan analysis."
        if message:
            base += f"\n\nAdditional context: {message}"
        return base

    return message or "Please begin the financial planning analysis."


def _serialize_content(content_blocks) -> list[dict]:
    """Serialize Claude API content blocks to dicts for conversation history."""
    serialized = []
    for block in content_blocks:
        if block.type == "text":
            serialized.append({"type": "text", "text": block.text})
        elif block.type == "tool_use":
            serialized.append({
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": block.input,
            })
    return serialized


def _summarize_input(tool_name: str, tool_input: dict) -> str:
    """Create a short summary of tool input for the reasoning feed."""
    if tool_name == "extract_pdf_text":
        return f"Extracting text from file {tool_input.get('file_id', 'unknown')}"
    elif tool_name == "parse_financial_statement":
        return f"Parsing {tool_input.get('document_type', 'document')}"
    elif tool_name == "analyze_net_worth":
        return "Analyzing net worth"
    elif tool_name == "analyze_income_and_expenses":
        return "Analyzing income and expenses"
    elif tool_name == "run_monte_carlo":
        return f"Running Monte Carlo ({tool_input.get('risk_profile', 'moderate')} profile)"
    elif tool_name == "identify_planning_gaps":
        return "Identifying planning gaps"
    elif tool_name == "generate_plan_report":
        return f"Generating {tool_input.get('plan_type', 'plan')} report"
    return f"Executing {tool_name}"
