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

2. Shipment / Order Lookup
Users can ask about shipment information using an order ID.

Example

User:
What is the status of ORD-1001?
Assistant:
ORD-1001 is currently BOOKED.

Carrier: SwiftShip

Shipment fee: ₹4,200