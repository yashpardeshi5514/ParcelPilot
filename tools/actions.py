import json
from pathlib import Path
from datetime import datetime


ACTIONS_FILE = Path("data/escalations.json")

def prepare_escalation(
    account_id: str,
    ticket_id: str,
    priority: str,
    reason: str
):
    """
    Prepare an escalation for user confirmation.

    This function does NOT change state.
    """

    return {
        "requires_confirmation": True,
        "account_id": account_id,
        "ticket_id": ticket_id,
        "priority": priority,
        "reason": reason
    }


def create_escalation(
    account_id: str,
    ticket_id: str,
    priority: str,
    reason: str
):
    """
    Create a support escalation.

    This is a state-changing operation and should only
    be called after explicit user confirmation.
    """

    ACTIONS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if ACTIONS_FILE.exists():

        with open(
            ACTIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            escalations = json.load(file)

    else:

        escalations = []

    escalation = {
        "escalation_id": f"ESC-{len(escalations) + 1:04d}",
        "account_id": account_id,
        "ticket_id": ticket_id,
        "priority": priority,
        "reason": reason,
        "status": "OPEN",
        "created_at": datetime.now().isoformat()
    }

    escalations.append(escalation)

    with open(
        ACTIONS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            escalations,
            file,
            indent=2
        )

    return escalation