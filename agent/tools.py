from tools.document_search import search_documents
from tools.data_lookup import parcelpilot_data
from tools.actions import (
    prepare_escalation,
    create_escalation
)


# Temporary mocked logged-in customer.
# We will replace this with the Streamlit session later.
def get_current_account_id():
    """
    Return the authenticated customer account.

    The account context will be supplied by the application.
    """
    from streamlit import session_state

    return session_state.get(
        "account_id",
        "ACCT-001"
    )


def search_parcelpilot_documents(query: str):
    """
    Search ParcelPilot policies, SOPs, customer agreements,
    and product documentation.
    """

    return search_documents(
        query=query,
        n_results=5
    )


def get_my_account():
    """
    Get the currently authenticated customer's account.
    """

    account = parcelpilot_data.get_account(
        get_current_account_id()
    )

    return account


def get_my_order(order_id: str):
    """
    Get an order belonging to the currently authenticated customer.

    Access is enforced using the authenticated account ID.
    """

    order = parcelpilot_data.get_order(
        order_id=order_id,
        account_id=get_current_account_id()
    )

    if order is None:
        return {
            "found": False,
            "message": "Order not found or access denied."
        }

    return {
        "found": True,
        "order": order
    }


def get_my_ticket(ticket_id: str):
    """
    Get a support ticket belonging to the currently
    authenticated customer.
    """

    ticket = parcelpilot_data.get_ticket(
        ticket_id=ticket_id,
        account_id=get_current_account_id()
    )

    if ticket is None:
        return {
            "found": False,
            "message": "Ticket not found or access denied."
        }

    return {
        "found": True,
        "ticket": ticket
    }

def prepare_ticket_escalation(
    ticket_id: str,
    priority: str,
    reason: str
):
    """
    Prepare an escalation for the authenticated customer.

    This does not create the escalation.
    User confirmation is required.
    """

    return prepare_escalation(
        account_id=get_current_account_id(),
        ticket_id=ticket_id,
        priority=priority,
        reason=reason
    )