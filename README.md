# ParcelPilot Support AI

An AI-assisted customer support chatbot for ParcelPilot.

The system combines customer account data, shipment data, support policies, customer-specific agreements, and product documentation to answer support questions while enforcing customer-level access control.

## Features

- Natural-language customer support chatbot
- Customer account lookup
- Shipment/order lookup
- PDF document and policy search
- Customer-specific agreement handling
- Current policy vs. deprecated policy handling
- Multi-step support queries
- Customer-level data isolation
- Escalation workflow
- Explicit confirmation before state-changing actions
- Streamlit chat interface
- Tool activity visibility

## Architecture

```text
                    Streamlit UI
                         |
                         v
                  Support Agent
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    Document Search   Data Lookup   Action Tool
          |              |              |
          v              v              v
       PDF/RAG         Excel       Escalations