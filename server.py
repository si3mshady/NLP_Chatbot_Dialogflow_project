from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
# from insert_order import insert_order
from insert_order_test import insert_order, get_next_order_id, delete_items_from_order, print_all_items_in_orders
import re


app = FastAPI()

orders = {}

class OrderAddRequest(BaseModel):
    item_name: str
    quantity: int

class OrderTrackRequest(BaseModel):
    order_id: str

# Initialize an empty dictionary to store orders with session IDs as keys

global current_order_number
current_order_number = None

food_items = {
    1: ('Donut', 2.50),
    2: ('Pigs in a Blanket', 4.00),
    3: ('Burrito', 5.50),
    4: ('Shake', 3.00),
    5: ('Sandwich', 4.50),
    6: ('Pancake', 3.25),
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
    global current_order_number
    global orders
    print(f'all orders temp, {orders}')
   
    # Parse the incoming JSON request from Dialogflow
    dialogflow_request = await request.json()

    # Extract the intent name from the Dialogflow request
    intent_name = dialogflow_request["queryResult"]["intent"]["displayName"]
    params = dialogflow_request["queryResult"]["parameters"]
    output_context = dialogflow_request['queryResult']['outputContexts']
    session_id = parse_session_id(dialogflow_request)
    # print(f'session id {session_id}')

    # print(f'This is the orders dictionary {orders}')

    # Create a new order dictionary for each session

    # if session_id not in orders:
    #     orders[session_id] = []

    # if intent_name == "get.current.order":
    #     resp = {
    #     "fulfillmentText": f"Here is what you have currenly ordered {str(orders[session_id])} ---- total bill ${calculate_total_bill(orders[session_id])}"
    #     }
    #     return JSONResponse(content=resp)

    # Handle the "order.add" intent
    if intent_name == "order.add":
        if session_id not in orders:
            orders[session_id] = []

        order_items = orders[session_id]
        if not current_order_number: #if this value is None resolves 
            current_order_number = get_next_order_id()
            # print("Here is line 82")
            print(f'Here is current order number {current_order_number}'  )


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
                
                #testing to see each item be inserted into db under same order
                current_orders = orders[session_id]
                insert_order(current_orders, session_id,current_order_number)

                response_text = f"Added {format_order(food_items_list, quantities) } to order number {current_order_number}......all items in order are as follows {str(orders[session_id])}"
            else:
                response_text = "Invalid input: The number of items and quantities do not match."
        else:
            response_text = "Invalid input: Missing 'food-items' or 'number'."

    # Handle the "order.track" intent
    # elif intent_name == "order.track":
    #     # Implement tracking logic here
    #     order_items = orders.get(session_id, [])
    #     response_text = "Order not found."
    #     if order_items:
    #         response_text = f"Order details:\n{format_order(order_items)}\nTotal Cost: ${calculate_total_cost(order_items):.2f}"


    elif intent_name == "complete.order":
        current_orders = orders[session_id]
        orders[session_id] = []
        response_text = insert_order(current_orders, session_id,current_order_number)
        current_order_number = None
        # print("This is the response after I complete order", response_text)x

        resp = {
        "fulfillmentText": str(response_text)
        }

        return JSONResponse(content=resp)

    elif intent_name == "delete.menu.item":

        print(params)
        food_item = params.get('food-items')
        order_number = params.get('number')
        response_text = delete_items_from_order(order_number,food_item)
        message =  print_all_items_in_orders()
        resp = {
        "fulfillmentText": response_text
        }
        return JSONResponse(content=resp)
    


    # elif intent_name == "list.all.orders.for.elliott.linkedinpost":
    #     orders = print_all_items_in_orders()

    #     resp = {
    #     "fulfillmentText": f"Here is a listing of all orders from database + {str(orders) }"
    #     }
    #     return JSONResponse(content=resp)


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

def calculate_total_bill(order_items):
    total_bill = 0
    for item in order_items:
        item_name = item['item_name'].lower()  # Convert item name to lowercase for case insensitivity
        quantity = item['quantity']
        # Look up the item ID from the food_items dictionary
        item_id = None
        for key, (name, price) in food_items.items():
            if item_name == name.lower():
                item_id = key
                break
        if item_id is not None:
            item_price = food_items[item_id][1]
            total_bill += item_price * quantity
    return total_bill



def format_order(food_items_list, quantities):
    formatted_items = []
    for item_name, quantity in zip(food_items_list, quantities):
        formatted_item = f"{quantity} {item_name}"
        formatted_items.append(formatted_item)
    return ', '.join(formatted_items)



#wip update bill calculations 
#add delete order 
#add update order
#add order status 


# docker-compose up
#python3 database.py
# uvicorn server:app --reload
# ngrok http 8000
# uvicorn server:app --reload


# Food Items legend
# (1, 'donuts', Decimal('2.50'))
# (2, 'pig in blanket', Decimal('4.00'))
# (3, 'burrito', Decimal('5.50'))
# (4, 'shake', Decimal('3.00'))
# (5, 'sandwich', Decimal('4.50'))
# (6, 'pancake', Decimal('3.25'));")




