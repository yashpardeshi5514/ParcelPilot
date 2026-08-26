import pandas as pd
import math
from pathlib import Path


DATA_FILE = Path(
    "data/ParcelPilot_Assessment_Data.xlsx"
)


def clean_value(value):
    """
    Convert Pandas/Excel values into JSON-safe Python values.
    """

    if pd.isna(value):
        return None

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def clean_record(record):
    """
    Convert a Pandas record into a JSON-safe dictionary.
    """

    return {
        key: clean_value(value)
        for key, value in record.items()
    }


class ParcelPilotData:

    def __init__(self):

        self.accounts = pd.read_excel(
            DATA_FILE,
            sheet_name="accounts"
        )

        self.orders = pd.read_excel(
            DATA_FILE,
            sheet_name="orders"
        )

        self.tickets = pd.read_excel(
            DATA_FILE,
            sheet_name="tickets"
        )

        self.snapshot_time = (
            "2026-08-16 11:00 Asia/Kolkata"
        )

    def get_account(self, account_id):

        result = self.accounts[
            self.accounts["account_id"] == account_id
        ]

        if result.empty:
            return None

        return clean_record(
            result.iloc[0].to_dict()
        )

    def get_order(
        self,
        order_id,
        account_id=None
    ):

        result = self.orders[
            self.orders["order_id"] == order_id
        ]

        if account_id:

            result = result[
                result["account_id"] == account_id
            ]

        if result.empty:
            return None

        return clean_record(
            result.iloc[0].to_dict()
        )

    def get_ticket(
        self,
        ticket_id,
        account_id=None
    ):

        result = self.tickets[
            self.tickets["ticket_id"] == ticket_id
        ]

        if account_id:

            result = result[
                result["account_id"] == account_id
            ]

        if result.empty:
            return None

        return clean_record(
            result.iloc[0].to_dict()
        )


parcelpilot_data = ParcelPilotData()