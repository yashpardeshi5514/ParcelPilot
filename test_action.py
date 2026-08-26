from tools.actions import create_escalation


result = create_escalation(
    account_id="ACCT-001",
    ticket_id="TKT-501",
    priority="P1",
    reason="Customer reports a critical production issue."
)

print("CREATED:")
print(result)