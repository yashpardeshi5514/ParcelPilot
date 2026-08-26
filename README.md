# 📦 ParcelPilot Support AI

> An intelligent, account-aware customer support assistant for shipment operations, policy lookup, document search, and controlled support escalation.

---

## 📌 Overview

**ParcelPilot Support AI** is a customer support assistant designed to help users quickly resolve shipment and account-related queries through a conversational interface.

The application combines:

- Customer account context
- Shipment and order lookup
- Internal ParcelPilot document search
- Customer-specific policy handling
- Support escalation workflows
- Confirmation before state-changing actions
- A modern Streamlit-based user interface

The project is designed as a practical support-assistant prototype where structured data, internal documentation, and controlled actions work together in a single application.

---

# ✨ Features

## 👤 1. Account-Aware Support

The system maintains the currently selected customer account and uses that context when answering support questions.

### Supported Accounts

| Account | Account ID | Plan | Status |
|---|---|---|---|
| Northstar Logistics | `ACCT-001` | Enterprise | Active |
| LumenWorks | `ACCT-002` | Growth | Active |

### Example

**User:**

```text
What is my account?

Assistant:

You are using the Northstar Logistics account (ACCT-001).
Your plan is Enterprise and the account is active.

Absolutely. Here is the proper final README.md in one single canvas/code block, ready to copy into your project.

# 📦 ParcelPilot Support AI

> An intelligent, account-aware customer support assistant for shipment operations, policy lookup, document search, and controlled support escalation.

---

## 📌 Overview

**ParcelPilot Support AI** is a customer support assistant designed to help users quickly resolve shipment and account-related queries through a conversational interface.

The application combines:

- Customer account context
- Shipment and order lookup
- Internal ParcelPilot document search
- Customer-specific policy handling
- Support escalation workflows
- Confirmation before state-changing actions
- A modern Streamlit-based user interface

The project is designed as a practical support-assistant prototype where structured data, internal documentation, and controlled actions work together in a single application.

---

# ✨ Features

## 👤 1. Account-Aware Support

The system maintains the currently selected customer account and uses that context when answering support questions.

### Supported Accounts

| Account | Account ID | Plan | Status |
|---|---|---|---|
| Northstar Logistics | `ACCT-001` | Enterprise | Active |
| LumenWorks | `ACCT-002` | Growth | Active |

### Example

**User:**

```text
What is my account?

Assistant:

You are using the Northstar Logistics account (ACCT-001).
Your plan is Enterprise and the account is active.
📦 2. Shipment / Order Lookup

Users can ask about shipment information using an order ID.

Example

User:

What is the status of ORD-1001?

Assistant:

ORD-1001 is currently BOOKED.

Carrier: SwiftShip

Shipment fee: ₹4,200

The system also handles orders that cannot be found.

Example
What is the status of ORD-9999?

Response:

I couldn't find ORD-9999 in your account.
📚 3. ParcelPilot Document Search

The application contains a knowledge base of ParcelPilot support and operational documents.

The document search functionality can be used for questions related to:

Support policies
Cancellation policies
Service credits
Shipment operations
Known shipment issues
Customer-specific agreements
Support procedures
Knowledge Base
01_Support_Policy_v3_CURRENT.pdf
02_Support_Policy_v2_DEPRECATED.pdf
03_Cancellation_and_Service_Credit_SOP_v4.pdf
04_Product_Operations_Guide_and_Known_Issues.pdf
05_Northstar_Logistics_Enterprise_Agreement.pdf
06_LumenWorks_Service_Agreement.pdf
📋 4. Customer-Specific Policy Handling

ParcelPilot can consider customer-specific agreements when answering policy questions.

For example:

Can Northstar cancel ORD-1001 without a cancellation fee?

The system checks:

The customer account.
The order.
The shipment status.
Whether the shipment has been picked up.
Relevant ParcelPilot policies.
Customer-specific agreements.

For the Northstar account, the active Enterprise Agreement allows a BOOKED shipment to be cancelled before pickup without a cancellation fee.

Example Response
Yes. ORD-1001 is currently BOOKED and has not been picked up.

Northstar's active Enterprise Agreement allows Northstar
to cancel any BOOKED shipment before pickup with no
cancellation fee.

The customer-specific agreement overrides the standard
cancellation policy.
🎫 5. Support Escalation

Users can request an escalation when an issue requires support intervention.

Example
Please escalate this issue to support

The system does not immediately create the escalation.

Instead, it prepares a pending action:

I can prepare an escalation for this issue.
Please review and confirm before I create it.

The user can then confirm or cancel the action.

Confirmation Flow
User Request
     │
     ▼
Prepare Escalation
     │
     ▼
Display Priority + Reason
     │
     ▼
User Confirmation
     │
     ├──────────────► Cancel
     │
     ▼
Create Escalation
     │
     ▼
Store Escalation

Example:

Escalation created successfully.

Escalation ID: ESC-0004
Priority: P2
Status: OPEN
🔐 6. Confirmation Before State Changes

The project separates read-only operations from state-changing operations.

Read-only operations
get_my_account()
get_my_order()
search_parcelpilot_documents()
State-changing operation
create_escalation()

State-changing actions require explicit user confirmation before execution.

This helps prevent accidental creation of support escalations.

🏗️ System Architecture
                    ┌─────────────────────────┐
                    │      Streamlit UI       │
                    │                         │
                    │ Customer Selection      │
                    │ Chat Interface          │
                    │ Account Context         │
                    │ Escalation Confirmation │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Demo Agent         │
                    │                         │
                    │   ask_demo_agent()      │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
       │   Account    │   │    Order     │   │  Document    │
       │    Lookup    │   │    Lookup    │   │    Search    │
       └──────────────┘   └──────────────┘   └───────┬──────┘
                                                     │
                                                     ▼
                                             ┌──────────────┐
                                             │ ParcelPilot  │
                                             │ Knowledge    │
                                             │ Base         │
                                             └──────────────┘

                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Escalation Tool  │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ escalations.json │
                        └──────────────────┘
🔄 Application Workflow
Step 1 — Customer Selection

The user selects an account from the Streamlit sidebar.

Example:

Northstar Logistics
ACCT-001
Enterprise
Active

The selected account is stored in Streamlit session state.

Step 2 — User Query

The user enters a question through the chat interface.

Example:

What is the status of ORD-1001?
Step 3 — Agent Processing

The question is passed to:

ask_demo_agent(user_message)

The agent determines which operation is required.

Step 4 — Tool Execution

Depending on the question, the system can call:

get_my_account()
get_my_order()
search_parcelpilot_documents()
Step 5 — Response Generation

The tool result is converted into a user-friendly response and displayed in the Streamlit chat interface.

🧩 Main Components
app.py

The main Streamlit application.

Responsibilities include:

Rendering the user interface
Customer/account selection
Maintaining chat history
Receiving user queries
Displaying assistant responses
Showing tool usage
Handling escalation confirmation
Displaying account context

Run the application with:

streamlit run app.py
agent/

Contains the agent logic.

Main function:

ask_demo_agent(question)

The agent determines which ParcelPilot operation should be performed based on the user's question.

tools/data_lookup.py

Handles structured data lookup.

Responsibilities include:

Account lookup
Order lookup
Shipment information
tools/document_search.py

Handles searches across the ParcelPilot document knowledge base.

It is used for questions involving policies, operational information, agreements, and support procedures.

tools/actions.py

Contains state-changing support actions.

Main functions:

prepare_escalation()
create_escalation()
prepare_escalation()

Creates a pending escalation request without changing application state.

create_escalation()

Creates the escalation after the user has explicitly confirmed the action.

retrieval/

Contains the document retrieval components.

retrieval/
├── ingest.py
└── vector_store.py

These components support indexing and retrieving information from the ParcelPilot document knowledge base.

📁 Project Structure
ParcelPilot/
│
├── agent/
│   ├── agent.py
│   ├── demo_agent.py
│   └── tools.py
│
├── data/
│   ├── 01_Support_Policy_v3_CURRENT.pdf
│   ├── 02_Support_Policy_v2_DEPRECATED.pdf
│   ├── 03_Cancellation_and_Service_Credit_SOP_v4.pdf
│   ├── 04_Product_Operations_Guide_and_Known_Issues.pdf
│   ├── 05_Northstar_Logistics_Enterprise_Agreement.pdf
│   ├── 06_LumenWorks_Service_Agreement.pdf
│   └── escalations.json
│
├── retrieval/
│   ├── __init__.py
│   ├── ingest.py
│   └── vector_store.py
│
├── tools/
│   ├── __init__.py
│   ├── actions.py
│   ├── data_lookup.py
│   └── document_search.py
│
├── chroma_db/
│
├── app.py
├── README.md
├── requirements.txt
├── .env
└── .gitignore

The exact contents of folders may vary depending on the final project version.

🗄️ Data Storage
Vector Database

The project uses a local vector database for document retrieval.

chroma_db/

The database contains indexed information from the ParcelPilot document collection.

Escalation Storage

Escalations are stored locally in:

data/escalations.json

Example:

{
  "escalation_id": "ESC-0004",
  "account_id": "ACCT-001",
  "ticket_id": "TKT-PENDING",
  "priority": "P2",
  "reason": "Please escalate this issue to support",
  "status": "OPEN"
}
⚙️ Installation
1. Open the Project
cd ParcelPilot
2. Create a Virtual Environment

Windows:

python -m venv venv
3. Activate the Virtual Environment

PowerShell:

.\venv\Scripts\Activate.ps1
4. Install Dependencies

If requirements.txt is available:

pip install -r requirements.txt

Otherwise, install the required packages used by the project, for example:

pip install streamlit chromadb
▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

The application will normally be available at:

http://localhost:8501
🧪 Demo Test Cases

The following queries can be used to demonstrate the project.

Test 1 — Account
Input
What is my account?
Expected Output
You are using the Northstar Logistics account (ACCT-001).
Your plan is Enterprise and the account is active.
Tool
get_my_account
Test 2 — Order Status
Input
What is the status of ORD-1001?
Expected Output
ORD-1001 is currently BOOKED.

Carrier: SwiftShip

Shipment fee: ₹4,200
Tool
get_my_order
Test 3 — Unknown Order
Input
What is the status of ORD-9999?
Expected Output
I couldn't find ORD-9999 in your account.
Tool
get_my_order
Test 4 — Cancellation Policy
Input
Can Northstar cancel ORD-1001 without a cancellation fee?
Expected Output
Yes. ORD-1001 is currently BOOKED and has not been picked up.

Northstar's active Enterprise Agreement allows Northstar
to cancel any BOOKED shipment before pickup with no
cancellation fee.

The customer-specific agreement overrides the standard
cancellation policy.
Tools
get_my_order
search_parcelpilot_documents
Test 5 — Support Policy
Input
What is the support policy?
Expected Behavior

The system searches the ParcelPilot support-policy documents and returns the relevant documents.

Test 6 — Known Shipment Issues
Input
What are the known shipment issues?
Expected Behavior

The system searches the Product Operations and Known Issues documentation.

Test 7 — Shipment Exception
Input
What is the process for raising a shipment exception?
Expected Behavior

The system searches the relevant ParcelPilot operational documentation and SOP.

Test 8 — Escalation
Input
Please escalate this issue to support
Expected Behavior

The system prepares an escalation and requests confirmation.

I can prepare an escalation for this issue.
Please review and confirm before I create it.

After confirmation:

Escalation created successfully.

Escalation ID: ESC-XXXX
Priority: P2
Status: OPEN
🔄 Escalation State Flow
                    User
                     │
                     ▼
          "Please escalate this"
                     │
                     ▼
          Prepare Escalation
                     │
                     ▼
        Pending Action Created
                     │
                     ▼
          Confirmation Required
                 /       \
                /         \
               ▼           ▼
            Cancel       Confirm
               │           │
               ▼           ▼
              End    create_escalation()
                           │
                           ▼
                  escalations.json
                           │
                           ▼
                     ESC-XXXX
                     Status: OPEN
🛡️ Error Handling

The application handles errors during agent execution so that a failure does not completely break the user interface.

If an unexpected error occurs, the application displays:

Sorry, I encountered an error while processing your request.

The application also handles missing orders by returning a clear message instead of exposing internal errors.

🎯 Design Goals

ParcelPilot Support AI was designed around the following principles:

1. Account Awareness

Responses should use the currently selected customer account.

2. Tool-Based Operations

Different support operations are separated into dedicated tools.

3. Document-Based Knowledge

Policy and operational questions can be answered using the ParcelPilot document knowledge base.

4. Customer-Specific Rules

Customer agreements can take precedence over standard policies where applicable.

5. Safe State Changes

Actions that modify stored data require explicit confirmation.

6. Modular Architecture

The application separates:

UI
Agent
Tools
Retrieval
Data
Actions

This makes the project easier to maintain and extend.

📊 Technology Stack
Technology	Purpose
Python	Core application logic
Streamlit	Web UI and conversational interface
ChromaDB	Vector/document retrieval
JSON	Local escalation persistence
PDF	ParcelPilot knowledge-base documents
Python Virtual Environment	Dependency isolation
🚧 Current Limitations

The current project is a prototype/demo implementation.

Known limitations include:

Local data storage is used.
Escalations are stored in a JSON file.
The application does not use a production database.
Authentication is not implemented.
Role-based access control is not implemented.
Some unrelated natural-language questions may be routed to document search.
The current agent logic uses deterministic intent handling rather than a fully autonomous production agent.
The project is intended for demonstration and development purposes.