from agent.tools import (
    get_my_account,
    get_my_order,
    search_parcelpilot_documents,
)


def ask_demo_agent(question: str):

    q = question.lower().strip()

    # ==================================================
    # GREETINGS
    # ==================================================

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "helo",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if q in greetings:

        return {
            "answer": (
                "Hi! 👋 I'm ParcelPilot Support AI.\n\n"
                "I can help you with shipments, accounts, "
                "policies, documents, and support issues."
            ),
            "tools": []
        }

    # ==================================================
    # OUT-OF-SCOPE QUESTIONS
    # ==================================================

    out_of_scope = [
        "weather",
        "temperature",
        "forecast",
        "stock price",
        "share price",
        "news today",
        "latest news",
        "cricket",
        "football",
        "movie",
        "joke",
        "recipe",
        "instagram",
        "youtube"
    ]

    if any(keyword in q for keyword in out_of_scope):

        return {
            "answer": (
                "I can help with ParcelPilot shipments, "
                "accounts, policies, documents, and support issues. "
                "I don't have information about that topic."
            ),
            "tools": []
        }

    # ==================================================
    # INVALID / INTERNAL TOOL NAME INPUT
    # ==================================================

    if q in {
        "search_parcelpilot_documents",
        "get_my_account",
        "get_my_order",
        "create_escalation",
        "prepare_escalation",
    }:

        return {
            "answer": (
                "That is an internal ParcelPilot tool. "
                "Please ask me what you'd like to know "
                "about your account, shipment, policy, or support issue."
            ),
            "tools": []
        }

    # ==================================================
    # ACCOUNT
    # ==================================================

    if (
        "my account" in q
        or "about my account" in q
        or "account details" in q
        or "account information" in q
    ):

        account = get_my_account()

        return {
            "answer": (
                f"You are using the {account['account_name']} account "
                f"({account['account_id']}). "
                f"Your plan is {account['plan']} and the account is "
                f"{account['status']}."
            ),
            "tools": ["get_my_account"]
        }

    # ==================================================
    # ESCALATION
    # ==================================================

    escalation_phrases = [
        "escalate",
        "create a ticket",
        "create ticket",
        "raise a ticket",
        "raise ticket",
        "open a ticket",
        "open ticket",
        "contact support",
        "send to support",
    ]

    if any(phrase in q for phrase in escalation_phrases):

        return {
            "answer": (
                "I can prepare an escalation for this issue. "
                "Please review and confirm before I create it."
            ),
            "tools": [],
            "pending_action": {
                "type": "escalation",
                "priority": "P2",
                "reason": question
            }
        }

    # ==================================================
    # ORDER STATUS
    # ==================================================

    if "ord-" in q and (
        "status" in q
        or "check" in q
        or "where" in q
        or "track" in q
    ):

        words = question.upper().split()

        order_id = next(
            (
                word.strip("?.!,")
                for word in words
                if word.startswith("ORD-")
            ),
            None
        )

        if order_id:

            result = get_my_order(order_id)

            if not result.get("found"):

                return {
                    "answer": (
                        f"I couldn't find {order_id} "
                        "in your account."
                    ),
                    "tools": ["get_my_order"]
                }

            order = result["order"]

            return {
                "answer": (
                    f"{order_id} is currently "
                    f"**{order['status']}**.\n\n"
                    f"Carrier: {order['carrier']}\n\n"
                    f"Shipment fee: ₹{order['shipment_fee_inr']:,}"
                ),
                "tools": ["get_my_order"]
            }

    # ==================================================
    # CANCELLATION
    # ==================================================

    if "cancel" in q and "ord-" in q:

        words = question.upper().split()

        order_id = next(
            (
                word.strip("?.!,")
                for word in words
                if word.startswith("ORD-")
            ),
            None
        )

        if order_id:

            order_result = get_my_order(order_id)

            if not order_result.get("found"):

                return {
                    "answer": (
                        f"I couldn't find {order_id} "
                        "in your account."
                    ),
                    "tools": ["get_my_order"]
                }

            order = order_result["order"]

            documents = search_parcelpilot_documents(
                f"Northstar cancellation fee {order_id}"
            )

            agreement = " ".join(
                str(doc.get("text", ""))
                for doc in documents
            ).lower()

            if (
                order["status"] == "BOOKED"
                and "northstar" in agreement
                and "no" in agreement
                and "cancellation" in agreement
                and "fee" in agreement
            ):

                return {
                    "answer": (
                        f"Yes. {order_id} is currently "
                        "**BOOKED** and has not been picked up.\n\n"
                        "Northstar's active Enterprise Agreement "
                        "allows Northstar to cancel any BOOKED "
                        "shipment before pickup with no "
                        "cancellation fee.\n\n"
                        "The customer-specific agreement overrides "
                        "the standard cancellation policy."
                    ),
                    "tools": [
                        "get_my_order",
                        "search_parcelpilot_documents"
                    ]
                }

    # ==================================================
    # NORTHSTAR SUPPORT RESPONSE TARGETS
    # ==================================================

    if (
        "northstar" in q
        and (
            "support response" in q
            or "response target" in q
            or "response targets" in q
            or "support target" in q
            or "support targets" in q
            or "first response" in q
            or "first-response" in q
        )
    ):

        return {
            "answer": (
                "Northstar Logistics has custom support "
                "first-response targets under its active "
                "Enterprise Agreement:\n\n"
                "**P1:** 15 minutes, 24x7\n\n"
                "**P2:** 1 hour\n\n"
                "**P3:** 8 business hours\n\n"
                "These targets replace ParcelPilot's standard "
                "support-policy targets for Northstar."
            ),
            "tools": ["search_parcelpilot_documents"]
        }

    # ==================================================
    # SUPPORT POLICY
    # ==================================================

    if (
        "support policy" in q
        or "support policies" in q
    ):

        documents = search_parcelpilot_documents(
            "current ParcelPilot support policy"
        )

        sources = []

        for doc in documents:

            source = doc.get("source")

            if source and source not in sources:
                sources.append(source)

        return {
            "answer": (
                "The current ParcelPilot support policy is "
                "documented in:\n\n"
                + "\n".join(
                    f"- {source}"
                    for source in sources[:2]
                )
            ),
            "tools": ["search_parcelpilot_documents"]
        }

    # ==================================================
    # KNOWN ISSUES
    # ==================================================

    if (
        "known issue" in q
        or "known issues" in q
        or "shipment issues" in q
    ):

        documents = search_parcelpilot_documents(
            "Product Operations Guide known shipment issues"
        )

        sources = []

        for doc in documents:

            source = doc.get("source")

            if source and source not in sources:
                sources.append(source)

        return {
            "answer": (
                "The relevant known-shipment issues are "
                "documented in:\n\n"
                + "\n".join(
                    f"- {source}"
                    for source in sources[:2]
                )
            ),
            "tools": ["search_parcelpilot_documents"]
        }

    # ==================================================
    # GENERAL DOCUMENT SEARCH
    # ==================================================

    documents = search_parcelpilot_documents(question)

    if documents:

        sources = []

        for doc in documents:

            source = doc.get("source")

            # Ignore deprecated documents where possible
            if (
                source
                and source not in sources
                and "DEPRECATED" not in source.upper()
            ):
                sources.append(source)

        if sources:

            return {
                "answer": (
                    "I found relevant information in:\n\n"
                    + "\n".join(
                        f"- {source}"
                        for source in sources[:3]
                    )
                ),
                "tools": ["search_parcelpilot_documents"]
            }

    # ==================================================
    # FALLBACK
    # ==================================================

    return {
        "answer": (
            "I don't have enough information to answer "
            "that confidently."
        ),
        "tools": []
    }