# 📦 ParcelPilot Support AI

ParcelPilot Support AI is an account-aware customer support assistant built with *Python and Streamlit*.

The system helps customers and support teams handle shipment-related questions, account information, company policies, document-based queries, and support escalations through a single conversational interface.

---

## 🚀 Features

### 👤 Account-Aware Support
The assistant understands the currently selected customer account.

Supported accounts:

- Northstar Logistics — ACCT-001
- LumenWorks — ACCT-002

It can provide:

- Account name
- Account ID
- Subscription plan
- Account status

Example:

> What is my account?

Response:

> You are using the Northstar Logistics account (ACCT-001). Your plan is Enterprise and the account is active.

---

### 📦 Shipment / Order Lookup

The assistant can retrieve shipment information using an order ID.

Example:

> What is the status of ORD-1001?

Response:

> ORD-1001 is currently BOOKED.
>
> Carrier: SwiftShip  
> Shipment fee: ₹4,200

The system also handles unknown orders.

Example:

> What is the status of ORD-9999?

Response:

> I couldn't find ORD-9999 in your account.

---

### 📚 Document Search

ParcelPilot contains a knowledge base of internal support and operational documents.

The assistant can search these documents for relevant information.

Current documents include:

```text
01_Support_Policy_v3_CURRENT.pdf
02_Support_Policy_v2_DEPRECATED.pdf
03_Cancellation_and_Service_Credit_SOP_v4.pdf
04_Product_Operations_Guide_and_Known_Issues.pdf
05_Northstar_Logistics_Enterprise_Agreement.pdf
06_LumenWorks_Service_Agreement.pdf

The document search functionality helps answer questions related to:

Support policies
Shipment operations
Known issues
Cancellation policies
Service credits
Customer-specific agreements
📋 Customer-Specific Policy Handling

ParcelPilot can use customer-specific agreements when answering policy questions.

For example:

Can Northstar cancel ORD-1001 without a cancellation fee?

The system checks:

The current order status.
Whether the shipment has been picked up.
The relevant customer agreement.
The applicable cancellation policy.

For Northstar's Enterprise account, a BOOKED shipment before pickup can be cancelled without a cancellation fee according to the customer-specific agreement.

🎫 Support Escalation

Users can request an escalation when an issue requires support intervention.

Example:

Please escalate this issue to support.

The assistant first prepares the escalation and asks for confirmation.

I can prepare an escalation for this issue.
Please review and confirm before I create it.

After confirmation, the system creates an escalation record.

Example:

Escalation created successfully.

Escalation ID: ESC-0004
Priority: P2
Status: OPEN

Escalations are stored locally in:

data/escalations.json
🔐 Confirmation Before State Changes

State-changing actions are not performed immediately.

The escalation workflow follows:

User Request
     ↓
Prepare Escalation
     ↓
Show Details
     ↓
User Confirmation
     ↓
Create Escalation
     ↓
Store in JSON

This prevents accidental creation of support tickets.

🏗️ System Architecture
                     ┌─────────────────────┐
                     │    Streamlit UI     │
                     │                     │
                     │  Customer Selection │
                     │  Chat Interface     │
                     │  Account Context    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Demo Agent       │
                     │   ask_demo_agent()  │
                     └──────────┬──────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
      ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
      │   Account   │    │    Order    │    │  Document   │
      │    Tool     │    │    Tool     │    │   Search    │
      └─────────────┘    └─────────────┘    └──────┬──────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  ChromaDB /  │
                                            │  Documents   │
                                            └──────────────┘

                                │
                                ▼
                       ┌─────────────────┐
                       │ Escalation Tool │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ escalations.json│
                       └─────────────────┘
📁 Project Structure
ParcelPilot/
│
├── agent/
│   └── tools.py
│
├── chroma_db/
│   └── chroma.sqlite3
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
│   ├── _init_.py
│   ├── ingest.py
│   └── vector_store.py
│
├── tools/
│   ├── _init_.py
│   ├── actions.py
│   ├── data_lookup.py
│   └── document_search.py
│
├── app.py
├── README.md
├── .env
└── .gitignore
🧩 Main Components
app.py

The main Streamlit application.

Responsible for:

Rendering the user interface
Customer/account selection
Maintaining chat history
Receiving user questions
Displaying assistant responses
Displaying tool usage
Handling escalation confirmation

Run the application using:

streamlit run app.py
agent/

Contains the support-agent logic.

The main entry point is:

ask_demo_agent(question)

The agent determines which operation is required based on the user's question.

tools/data_lookup.py

Handles structured data lookup such as:

Customer accounts
Orders
Shipment information
tools/document_search.py

Handles document-based information retrieval.

It searches the ParcelPilot knowledge base and returns relevant documents for support questions.

retrieval/

Contains the document retrieval infrastructure.

The project uses a local vector database for document retrieval.

Main files:

retrieval/
├── ingest.py
└── vector_store.py
tools/actions.py

Contains state-changing support actions.

The escalation workflow includes:

prepare_escalation()
create_escalation()

prepare_escalation() prepares the action without changing system state.

create_escalation() creates and stores the escalation after confirmation.

🗄️ Data Storage
Vector Database

The project contains a local ChromaDB database:

chroma_db/

It stores indexed document information used for document retrieval.

Escalation Storage

Escalations are stored in:

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
1. Clone / open the project

Open the ParcelPilot project directory:

cd ParcelPilot
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install dependencies

Install the required Python packages used by the project.

For example:

pip install streamlit chromadb

If a requirements.txt file is available:

pip install -r requirements.txt
▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

The application will open in the browser at:

http://localhost:8501
🧪 Demo / Test Inputs

The following queries can be used to demonstrate the system.

Account
What is my account?

Expected result:

Northstar Logistics
Account ID: ACCT-001
Plan: Enterprise
Status: Active
Order Status
What is the status of ORD-1001?

Expected result:

ORD-1001 is currently BOOKED.

Carrier: SwiftShip

Shipment fee: ₹4,200
Unknown Order
What is the status of ORD-9999?

Expected result:

I couldn't find ORD-9999 in your account.
Cancellation Policy
Can Northstar cancel ORD-1001 without a cancellation fee?

Expected result:

Yes.

ORD-1001 is currently BOOKED and has not been picked up.

Northstar's active Enterprise Agreement allows Northstar
to cancel any BOOKED shipment before pickup with no
cancellation fee.

The customer-specific agreement overrides the standard
cancellation policy.
Support Policy
What is the support policy?

The system searches the relevant ParcelPilot policy documents.

Known Shipment Issues
What are the known shipment issues?

The system searches the Product Operations and Known Issues documentation.

Shipment Exception
What is the process for raising a shipment exception?

The system searches the relevant operational and SOP documents.

Escalation
Please escalate this issue to support

Expected workflow:

Prepare escalation
        ↓
Ask for confirmation
        ↓
Confirm
        ↓
Create escalation

Example result:

Escalation created successfully.

Escalation ID: ESC-0004
Priority: P2
Status: OPEN
🔄 Example User Flow
User selects:
Northstar Logistics

        ↓

Account Context:
ACCT-001
Enterprise
Active

        ↓

User:
"What is the status of ORD-1001?"

        ↓

Order Tool

        ↓

ORD-1001
BOOKED
SwiftShip
₹4,200

        ↓

Assistant displays response
🧠 Supported Query Categories

ParcelPilot currently handles the following major categories:

Category	Example
Account	What is my account?
Shipment	What is the status of ORD-1001?
Policy	What is the support policy?
Cancellation	Can I cancel ORD-1001?
Operations	What are the known shipment issues?
Documents	Search the ParcelPilot documents
Escalation	Please escalate this issue
🛡️ Safety / State Management

The application separates information retrieval from state-changing actions.

Read-only operations include:

get_my_account
get_my_order
search_parcelpilot_documents

State-changing operation:

create_escalation

An escalation requires explicit user confirmation before creation.

This design reduces the possibility of accidental support-ticket creation.

🎯 Project Objective

The objective of ParcelPilot Support AI is to provide an intelligent internal support interface that can combine:

Customer context
Structured shipment data
Internal documentation
Customer-specific agreements
Support workflows
Controlled state-changing actions

into a single conversational support experience.

🔮 Future Improvements

Potential future enhancements include:

More natural-language intent detection
Better document answer generation
Source citations inside responses
More shipment operations
Ticket tracking
Escalation history
Authentication and role-based access
Database-backed customer and shipment data
Improved error handling
Production deployment
Analytics and support dashboards
Automated test coverage
Better handling of greetings and unrelated questions
📌 Current Limitations

The current demo implementation uses local project data and local storage.

Some conversational questions that are unrelated to ParcelPilot may still trigger document search rather than returning a conversational response.

The system is intended as a support-assistant demonstration/prototype, rather than a production customer-support platform.

👨‍💻 Technology Stack
Technology	Purpose
Python	Application logic
Streamlit	Web interface
ChromaDB	Vector/document retrieval
JSON	Local escalation storage
PDF	Knowledge-base documents
📜 Project Status

Status: Working Prototype

Core functionality implemented:

✅ Streamlit support interface
✅ Customer/account selection
✅ Account lookup
✅ Order lookup
✅ Document search
✅ Customer-specific cancellation handling
✅ Escalation preparation
✅ Confirmation before escalation
✅ Escalation creation
✅ Local escalation storage
✅ Chat history
✅ Custom UI styling
📦 ParcelPilot Support AI

A conversational support assistant for shipment operations, account management, internal policies, and controlled support escalation.