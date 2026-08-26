# ParcelPilot Support AI — Architecture Note

## 1. Overview

ParcelPilot is an AI-powered customer support assistant built to answer shipment, account, policy, operational, and support questions.

The application combines an AI agent with specialized tools for document retrieval, structured-data lookup, and support escalation.

## 2. Agent Design

The agent acts as the reasoning layer between the user and the available ParcelPilot tools.

The agent determines which capability is required for a user request and uses the appropriate tool.

The main capabilities include:

- Document search
- Account lookup
- Shipment lookup
- Support information retrieval
- Escalation preparation and creation

The agent returns a natural-language response based on the information returned by the tools.

## 3. Tool Design

Tools are separated by responsibility.

### Document Search

Used for questions involving:

- Support policies
- Product operations
- Known issues
- Cancellation procedures
- Customer agreements

### Structured Data Lookup

Used for questions involving:

- Account information
- Account status
- Customer plan
- Shipment/order information

### Escalation Tool

Used when the user wants to escalate an issue.

The system prepares the escalation first and requires confirmation before performing the state-changing action.

This reduces accidental escalation creation.

## 4. Document and Structured Data Handling

PDF documents are stored in the data directory and used as the knowledge base for policy and operational questions.

Structured customer and shipment information is handled separately from document retrieval.

This separation allows factual account and shipment lookups to use structured data while policy and operational questions use document retrieval.

## 5. Source Reliability and Conflict Handling

Customer-specific agreements are treated as higher-priority sources when they contain customer-specific rules.

For example, a customer agreement can override a standard cancellation policy for that customer.

Current policy documents are preferred over deprecated policy versions.

This helps prevent outdated policy information from being treated as the current rule.

## 6. Major Technical Trade-offs

### Streamlit

Streamlit was selected because it allows rapid development of an interactive AI support interface using Python.

### Retrieval-Based Knowledge

Document retrieval allows the assistant to answer questions using the provided ParcelPilot knowledge base instead of relying only on model knowledge.

### Separate Tools

Separating document search, structured lookup, and actions makes the system easier to maintain and extend.

### Confirmation Before Actions

Escalation creation requires confirmation because it changes application state.

### Prototype Architecture

The current implementation uses local storage and local retrieval components rather than production infrastructure.

This keeps the prototype simple while demonstrating the core workflow.