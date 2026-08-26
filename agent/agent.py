import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.tools import (
    search_parcelpilot_documents,
    get_my_account,
    get_my_order,
    get_my_ticket,
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=api_key
)


MODEL = "gemini-3.6-flash"


SYSTEM_PROMPT = """
You are ParcelPilot Support AI.

You are a customer-facing support assistant.

You help customers with:
- account questions
- shipment questions
- order status
- cancellation questions
- service credit questions
- support tickets
- ParcelPilot product issues

IMPORTANT RULES:

1. Never invent customer, order, ticket, policy,
   agreement, or product information.

2. Use the structured-data tools when the question
   requires account, order, or ticket information.

3. Use document search when the question requires
   policies, SOPs, customer agreements, or product
   documentation.

4. A signed customer agreement overrides the general
   ParcelPilot support policy.

5. Current policy overrides deprecated policy.

6. Current product documentation is preferred over
   historical ticket guidance.

7. Historical tickets may contain incorrect guidance
   and must not be treated as authoritative.

8. If sources conflict, identify the conflict and use
   the higher-authority source.

9. Never expose another customer's information.

10. If you cannot determine an answer confidently,
    explain what information is missing.

11. Do not claim an action was performed unless the
    application actually performed it.

12. Give concise answers, but explain important
    support decisions.

13. When using document search, mention the relevant
    source document in your answer.
"""


# --------------------------------------------------
# Gemini function declarations
# --------------------------------------------------

SEARCH_DOCUMENTS = {
    "name": "search_parcelpilot_documents",
    "description": (
        "Search ParcelPilot policies, SOPs, customer "
        "agreements, and product documentation. "
        "Use this when answering questions about "
        "support rules, cancellation, service credits, "
        "SLAs, plans, or known product issues."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "The information to search for. "
                    "Use a focused natural-language query."
                ),
            }
        },
        "required": ["query"],
    },
}


GET_MY_ACCOUNT = {
    "name": "get_my_account",
    "description": (
        "Get the authenticated customer's ParcelPilot "
        "account information."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


GET_MY_ORDER = {
    "name": "get_my_order",
    "description": (
        "Look up an order belonging to the authenticated "
        "customer. Use this when the customer asks about "
        "a specific order."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "ParcelPilot order ID, for example ORD-1001.",
            }
        },
        "required": ["order_id"],
    },
}


GET_MY_TICKET = {
    "name": "get_my_ticket",
    "description": (
        "Look up a support ticket belonging to the "
        "authenticated customer."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "ticket_id": {
                "type": "string",
                "description": "ParcelPilot ticket ID, for example TKT-501.",
            }
        },
        "required": ["ticket_id"],
    },
}


FUNCTION_DECLARATIONS = [
    SEARCH_DOCUMENTS,
    GET_MY_ACCOUNT,
    GET_MY_ORDER,
    GET_MY_TICKET,
]


TOOLS = types.Tool(
    function_declarations=FUNCTION_DECLARATIONS
)


AVAILABLE_FUNCTIONS = {
    "search_parcelpilot_documents":
        search_parcelpilot_documents,

    "get_my_account":
        get_my_account,

    "get_my_order":
        get_my_order,

    "get_my_ticket":
        get_my_ticket,
}


def execute_function(function_name, arguments):

    function = AVAILABLE_FUNCTIONS.get(function_name)

    if function is None:
        return {
            "error": f"Unknown function: {function_name}"
        }

    try:
        result = function(**arguments)

        return result

    except Exception as e:
        return {
            "error": str(e)
        }


def ask_agent(user_message: str):

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=SYSTEM_PROMPT
                    + "\n\nUser request:\n"
                    + user_message
                )
            ],
        )
    ]

    config = types.GenerateContentConfig(
        tools=[TOOLS]
    )

    # --------------------------------------------
    # Agent loop
    # --------------------------------------------

    for step in range(10):

        print(f"\n[Agent step {step + 1}]")

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        if not response.candidates:
            return "I couldn't generate a response."

        model_content = response.candidates[0].content

        function_calls = []

        for part in model_content.parts:

            if part.function_call:
                function_calls.append(
                    part.function_call
                )

        # ----------------------------------------
        # No tool call → final answer
        # ----------------------------------------

        if not function_calls:

            return response.text

        # ----------------------------------------
        # Add Gemini's tool request to conversation
        # ----------------------------------------

        contents.append(model_content)

        # ----------------------------------------
        # Execute requested functions
        # ----------------------------------------

        for function_call in function_calls:

            function_name = function_call.name
            arguments = dict(function_call.args or {})

            print(
                f"[Tool] {function_name}"
            )

            print(
                f"[Arguments] {arguments}"
            )

            result = execute_function(
                function_name,
                arguments
            )

            print(
                f"[Tool result] {result}"
            )

            function_response = types.Part.from_function_response(
                name=function_name,
                response={
                    "result": result
                },
            )

            contents.append(
                types.Content(
                    role="user",
                    parts=[function_response]
                )
            )

    return (
        "I was unable to complete the request "
        "within the allowed tool steps."
    )


if __name__ == "__main__":

    question = input(
        "Ask ParcelPilot Support AI: "
    )

    answer = ask_agent(question)

    print("\nAssistant:")
    print(answer)