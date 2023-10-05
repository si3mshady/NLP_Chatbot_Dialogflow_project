from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import re

app = FastAPI()

class OrderAddRequest(BaseModel):
    item_name: str
    quantity: int

class OrderTrackRequest(BaseModel):
    order_id: str

# Initialize an empty dictionary to store orders with session IDs as keys
orders = {}

food_items = {
    'Donut': 2.50,
    'Pigs in a Blanket': 4.00,
    'Burrito': 5.50,
    'Shake': 3.00,
    'Sandwich': 4.50,
    'Pancake': 3.25,
}

def json_to_human_readable(json_obj):
    if 'number' in json_obj and 'food-items' in json_obj:
        quantity = int(json_obj['number'][0])
        food_items = ', '.join(json_obj['food-items'])
        return f" {quantity} {food_items}."
    else:
        return "Invalid JSON format."

def parse_session_id(payload: dict):
    # Define a regular expression pattern to match the session ID
    pattern = r"sessions\/([\w-]+)\/contexts"

    # Use re.search to find the match in the payload
    match = re.search(pattern, payload["queryResult"]["outputContexts"][0]['name'])

    if match:
        # Extract the session ID from the match
        session_id = match.group(1)
        return session_id
    else:
        return None

@app.post("/")
async def dialogflow_webhook(request: Request):
    # Parse the incoming JSON request from Dialogflow
    dialogflow_request = await request.json()

    # Extract the intent name from the Dialogflow request
    intent_name = dialogflow_request["queryResult"]["intent"]["displayName"]
    params = dialogflow_request["queryResult"]["parameters"]
    output_context = dialogflow_request['queryResult']['outputContexts']
    session_id = parse_session_id(dialogflow_request)

    # Create a new order dictionary for each session
    if session_id not in orders:
        orders[session_id] = []

    # Handle the "order.add" intent
    if intent_name == "order.add":
        order_items = orders[session_id]

        # Check if both "food-items" and "number" are present
        if "food-items" in params and "number" in params:
            food_items_list = params["food-items"]
            quantities = params["number"]

            # Check if the lengths of the lists match
            if len(food_items_list) == len(quantities):
                for item_name, quantity in zip(food_items_list, quantities):
                    order_items.append({
                        "item_name": item_name,
                        "quantity": quantity
                    })
                response_text = f"Added {format_order(food_items_list, quantities) } to the order......all items in order are as follows {str(orders[session_id])}"
            else:
                response_text = "Invalid input: The number of items and quantities do not match."
        else:
            response_text = "Invalid input: Missing 'food-items' or 'number'."

    # Handle the "order.track" intent
    elif intent_name == "order.track":
        # Implement tracking logic here
        order_items = orders.get(session_id, [])
        response_text = "Order not found."
        if order_items:
            response_text = f"Order details:\n{format_order(order_items)}\nTotal Cost: ${calculate_total_cost(order_items):.2f}"

    else:
        response_text = "Unsupported intent."

    resp = {
        "fulfillmentText": response_text
    }

    return JSONResponse(content=resp)

def calculate_total_cost(order_items):
    total_cost = 0
    for item in order_items:
        item_name = item["item_name"]
        quantity = item["quantity"]
        item_cost = food_items.get(item_name, 0)
        total_cost += item_cost * quantity
    return total_cost

def format_order(food_items_list, quantities):
    formatted_items = []
    for item_name, quantity in zip(food_items_list, quantities):
        formatted_item = f"{quantity} {item_name}"
        formatted_items.append(formatted_item)
    return ', '.join(formatted_items)
