from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class OrderAddRequest(BaseModel):
    # Define the structure of the request JSON for order.add intent
    item_name: str
    quantity: int

class OrderTrackRequest(BaseModel):
    # Define the structure of the request JSON for order.track intent
    order_id: str

@app.post("/")
async def dialogflow_webhook(request: Request):
    print('invoked')
    # Parse the incoming JSON request from Dialogflow
    
    dialogflow_request = await request.json()
    print(dialogflow_request.keys())
   

    # Extract the intent name from the Dialogflow request
    intent_name = dialogflow_request["queryResult"]["intent"]["displayName"]
    params = dialogflow_request["queryResult"]["parameters"]
    output_context = dialogflow_request['queryResult']['outputContexts']

    # Handle the "order.add" intent
    if intent_name == "order.add":
        print('Ping Pong')
        print(params)
        resp = {
                "fulfillmentText": f"received {str(params)}"
             }

        return JSONResponse(content=resp)
        
    #     request_data = OrderAddRequest(**dialogflow_request["queryResult"]["parameters"])
    #     # Process the order.add request here
    #     response_text = f"Added {request_data.quantity} {request_data.item_name} to the order."

    # # Handle the "order.track" intent
    # elif intent_name == "order.track":
    #     request_data = OrderTrackRequest(**dialogflow_request["queryResult"]["parameters"])
    #     # Process the order.track request here
    #     response_text = f"Tracking order with ID: {request_data.order_id}"

    # else:
    #     response_text = "Unsupported intent."

    # # Prepare a response to send back to Dialogflow
    # response = {
    #     "fulfillmentText": response_text
    # }

    # return response
