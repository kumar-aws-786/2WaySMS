import boto3
import os

dynamodb_client = boto3.client("dynamodb")


def lambda_handler(event, context):
    print("Event: ", event)
    sessionAttributes = event['sessionState']['sessionAttributes']
    print("Session Attributes:", sessionAttributes)
    if event['invocationSource'] == 'DialogCodeHook':
        currentIntent = event['sessionState']['intent']['name']
        currentSlots = event['sessionState']['intent']['slots']
        if currentIntent == "booking":

            print("Current Slots: ", currentSlots)
            phoneNumber = sessionAttributes['UserPhoneNumber'] if 'UserPhoneNumber' in sessionAttributes else None

            if currentSlots['phone_number'] is None and phoneNumber is not None:
                currentSlots["phone_number"] = {
                    "value": {
                        "resolvedValues": [phoneNumber]
                    }
                }

            if 'phone_number' in currentSlots and currentSlots['phone_number'] is None:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": "phone_number",
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": currentIntent,
                            "slots": currentSlots
                        },
                        "sessionAttributes": event['sessionState']['sessionAttributes']
                    },
                    "messages": [{
                        "content": "Please enter your Phone Number",
                        "contentType": "PlainText"
                    }]
                }

            if 'user_dob' in currentSlots and currentSlots['user_dob'] is None:
                # Perform DynamoDB dip to retrieve customer name
                getUser = dynamodb_client.get_item(
                    TableName=os.environ.get("USER_TABLE"),
                    Key={
                        "PhoneNumber": {"S": currentSlots["phone_number"]["value"]["resolvedValues"][0]}
                    })
                    
                print("Retirved User: ", getUser)
                
                if "Item" in getUser and "Name" in getUser['Item']:
                    resp = f"Hello {getUser["Item"]["Name"]["S"]}! In order to proceed please enter your DOB in YYYY-MM-DD format"
                    respType = "ElicitSlot"
                else:
                    resp = f"Hello Guest! In order to proceed please enter your DOB in YYYY-MM-DD format"
                    respType = "ElicitSlot"
                # else:
                #     resp = f"We are not able to find your account! Please login to our application to continue"
                #     respType = "Close"

                return {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": "user_dob",
                            "type": respType
                        },
                        "intent": {
                            "name": currentIntent,
                            "slots": currentSlots
                        },
                        "sessionAttributes": event['sessionState']['sessionAttributes']
                    },
                    "messages": [
                        {
                            "content": resp,
                            "contentType": "PlainText"
                        }
                    ]
                }
                
                if respType == "Close":
                    resp['sessionState']['intent']['state'] = "Fulfilled"

            if 'booking_choice' in currentSlots and currentSlots['booking_choice'] is None:

                # Validate PhoneNumber and DOB from Dynamo DB

                validateUser = dynamodb_client.query(
                    TableName = os.environ.get("USER_TABLE"),
                    KeyConditions = {
                        "PhoneNumber": {
                            "AttributeValueList": [
                                { "S": currentSlots["phone_number"]["value"]["resolvedValues"][0] }
                            ],
                            "ComparisonOperator": "EQ"
                        }
                    },
                    QueryFilter={
                        "DOB": {
                            "AttributeValueList": [
                                { "S": currentSlots["user_dob"]["value"]["resolvedValues"][0] }
                            ],
                            "ComparisonOperator": "EQ"
                        }
                    }
                    )
                print("Validate User Response: ", validateUser)
                
                if "Items" in validateUser and len(validateUser['Items']) > 0 and validateUser['Items'][0]['PhoneNumber']:
                    return {
                        "sessionState": {
                            "dialogAction": {
                                "slotToElicit": "booking_choice",
                                "type": "ElicitSlot"
                            },
                            "intent": {
                                "name": currentIntent,
                                "slots": currentSlots
                            },
                            "sessionAttributes": event['sessionState']['sessionAttributes']
                        },
                        "messages": [{
                            "content": "We have open slots everyday. Please let me know your expected slot date",
                            "contentType": "PlainText"
                        }]
                    }
                else:
                    return {
                        "sessionState": {
                            "dialogAction": {
                                "slotToElicit": "booking_choice",
                                "type": "ElicitSlot"
                            },
                            "intent": {
                                "name": currentIntent,
                                "slots": currentSlots
                            },
                            "sessionAttributes": event['sessionState']['sessionAttributes']
                        },
                        "messages": [{
                            "content": "When would you like to schedule your booking?",
                            "contentType": "PlainText"
                        }]
                    }

            else:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Close"
                        },
                        "intent": {
                            "name": currentIntent,
                            "slots": currentSlots,
                            "state": "Fulfilled"
                        },
                    },
                    "messages": [{
                        "content": "Your booking has been confirmed",
                        "contentType": "PlainText"
                    }]
                }
