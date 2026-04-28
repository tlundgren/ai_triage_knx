# Kinaxis Maestro AI Triage Agent

This project provides the foundation for an AI agent designed to triage Kinaxis Maestro support tickets. Specifically, the agent assesses whether the user who opened the ticket included all the necessary information required for a swift resolution.

## The Problem
In application support, users frequently open tickets without providing the full context a human agent needs to investigate the issue. This creates a bottleneck:
* **Delayed MTTR (Mean Time to Resolution):** Support agents must pause their work to request missing details, creating a frustrating "ping-pong" effect.
* **Analytical Blind Spots:** Missing data makes it difficult to analyze ticket trends and design global solutions for recurring issues.

## The Solution: AI-Driven Triage
AI agents can instantly evaluate the completeness of incoming tickets against a strict rubric. This step can be integrated into your ITSM workflow (e.g., ServiceNow, Jira) in multiple configurations:
* **Pre-Routing Interception:** The AI reviews the ticket before routing. If incomplete, the AI directly asks the user for the missing details.
* **Agent Assist:** The AI routes the ticket but adds an internal note with its analysis, telling the human agent exactly what is missing.
* **Gatekeeper:** The assessment happens at the creation stage—preventing the ticket from being submitted until the user provides sufficient information.

## Project Contents
* **System Prompt:** Contains the core instructions and the evaluation rubric. The rubric includes a section for customization and instructs the AI to output both a human-readable summary and a machine-readable JSON block. The agent categorizes tickets as `COMPLETE`, `PARTIAL`, or `INCOMPLETE`.
* **Python Script:** Processes the machine-readable JSON output to generate a statistical report. This allows you to track metrics over time (e.g., calculating the exact percentage of `PARTIAL` tickets and identifying which specific data points users forget most often).

---
*If you find this project useful, please comply with the license and drop me a message. I would love to hear how your implementation is working for you!*
