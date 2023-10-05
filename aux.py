import re

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

# # Example usage:
# payload = "projects/nlpchatbot-utan/agent/sessions/2dd4ba28-bb88-ee42-a23c-13cc189b4b3d/contexts/current-order-context"
# session_id = parse_session_id(payload)
# print(session_id)


p = {
  "responseId": "fd68963a-0fbc-4a4c-a7a9-1e6b687cfc18-afbcf665",
  "queryResult": {
    "queryText": "I want 3 donuts, 3 shakes and 3 sandwiches",
    "parameters": {
      "food-items": [
        "donuts",
        "shakes",
        "sandwiches"
      ],
      "number": [
        3,
        3,
        3
      ]
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Anything else?",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Anything else?"
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/nlpchatbot-utan/agent/sessions/2dd4ba28-bb88-ee42-a23c-13cc189b4b3d/contexts/current-order-context",
        "lifespanCount": 5,
        "parameters": {
          "number": [
            3,
            3,
            3
          ],
          "food-items.original": [
            "donuts",
            "shakes",
            "sandwiches"
          ],
          "number.original": [
            "3",
            "3",
            "3"
          ],
          "food-items": [
            "donuts",
            "shakes",
            "sandwiches"
          ]
        }
      }
    ],
    "intent": {
      "name": "projects/nlpchatbot-utan/agent/intents/03286054-62d3-4acf-b233-0016b2905807",
      "displayName": "order.add"
    },
    "intentDetectionConfidence": 0.8279146,
    "languageCode": "en",
    "sentimentAnalysisResult": {
      "queryTextSentiment": {
        "score": 0.2,
        "magnitude": 0.2
      }
    }
  }
}


print( parse_session_id(p))