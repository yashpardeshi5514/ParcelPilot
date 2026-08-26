📦 ParcelPilot Support AI

ParcelPilot is an intelligent customer support assistant for shipment tracking, account information, document search, policy lookup, and support escalation.

🔗 Repository

GitHub Repository:
https://github.com/yashpardeshi5514/ParcelPilot

Demo Link:
https://parcelpilotsupportai.streamlit.app/

🛠️ Tech Stack

Python

Streamlit

ChromaDB

PDF document retrieval

JSON-based escalation storage

⚙️ Setup Instructions

1. Clone the repository

git clone https://github.com/yashpardeshi5514/ParcelPilot
cd ParcelPilot

2. Create a virtual environment

Windows PowerShell:

python -m venv venv

3. Activate the virtual environment

.\venv\Scripts\Activate.ps1

4. Install dependencies

pip install -r requirements.txt

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open at:

http://localhost:8501

🧪 Example Queries

Try these queries after starting the application:

What is my account?

What is the status of ORD-1001?

What is the status of ORD-9999?

Can Northstar cancel ORD-1001 without a cancellation fee?

What is the cancellation policy for Northstar?

What is the support policy?

What are the known shipment issues?

What is the process for raising a shipment exception?

Please escalate this issue to support

🚨 Escalation Workflow

The application requires confirmation before creating a support escalation.

User requests escalation
        ↓
Prepare escalation
        ↓
Display escalation details
        ↓
User confirmation
        ↓
Create escalation
        ↓
Generate Escalation ID

Example:

Escalation ID: ESC-0004
Priority: P2
Status: OPEN

📚 Knowledge Base

The application uses the following ParcelPilot documents:

Document

Purpose

01_Support_Policy_v3_CURRENT.pdf

Current support policy

02_Support_Policy_v2_DEPRECATED.pdf

Deprecated support policy

03_Cancellation_and_Service_Credit_SOP_v4.pdf

Cancellation and service-credit procedures

04_Product_Operations_Guide_and_Known_Issues.pdf

Product operations and known issues

05_Northstar_Logistics_Enterprise_Agreement.pdf

Northstar-specific agreement

06_LumenWorks_Service_Agreement.pdf

LumenWorks-specific agreement

👥 Supported Accounts

Northstar Logistics

Account ID: ACCT-001
Plan: Enterprise
Status: Active

LumenWorks

Account ID: ACCT-002
Plan: Growth
Status: Active

📦 Example Shipment

Order ID: ORD-1001
Status: BOOKED
Carrier: SwiftShip
Shipment Fee: ₹4,200

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
│   ├── ingest.py
│   └── vector_store.py
│
├── tools/
│   ├── actions.py
│   ├── data_lookup.py
│   └── document_search.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

🔐 Environment Variables

If environment variables are required, create a .env file in the project root.

Example:

OPENAI_API_KEY=your_api_key_here

Do not commit API keys, passwords, or other secrets to GitHub.

Make sure .env is included in .gitignore.

🧪 Testing

Account Test

python -c "from agent.demo_agent import ask_demo_agent; print(ask_demo_agent('What is my account?'))"

Order Test

python -c "from agent.demo_agent import ask_demo_agent; print(ask_demo_agent('What is the status of ORD-1001?'))"

Cancellation Test

python -c "from agent.demo_agent import ask_demo_agent; print(ask_demo_agent('Can Northstar cancel ORD-1001 without a cancellation fee?'))"

Escalation Test

python -c "from agent.demo_agent import ask_demo_agent; print(ask_demo_agent('Please escalate this issue to support'))"

📌 Current Capabilities

Account lookup

Customer account context

Shipment/order lookup

Unknown order handling

Document search

Support policy lookup

Customer-specific agreement handling

Cancellation policy checking

Shipment issue lookup

Support escalation

Confirmation before state-changing actions

Local escalation storage

Streamlit conversational interface

📊 Project Status

Status: Working Prototype

The core ParcelPilot support workflow is implemented and can be run locally using Streamlit.