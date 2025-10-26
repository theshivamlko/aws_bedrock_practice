import json
import boto3

def lambda_handler(event, context):
    dbClient = boto3.client('dynamodb')
    print(f"Input Params: {json.dumps(event)}")

    account_id = event['parameters'][0]['value']

    response = dbClient.get_item(
        TableName='customerAccountStatus',
        Key={'AccountID': {'N': str(account_id)}}
    )

    print(f"DynamoDB raw response: {json.dumps(response)}")

    # Handle case: no record found
    if 'Item' not in response:
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event['actionGroup'],
                "apiPath": event['apiPath'],
                "httpMethod": event['httpMethod'],
                "httpStatusCode": 404,
                "body": {
                    "text": f"No account found for ID {account_id}"
                }
            },
            "sessionAttributes": event.get("sessionAttributes", {}),
            "promptSessionAttributes": event.get("promptSessionAttributes", {})
        }

    # Extract clean data
    item = response["Item"]
    account_name = item["AccountName"]["S"]
    account_status = item["AccountStatus"]["S"]

    # ✅ Proper Bedrock Agent-friendly structure
    response_body = {
        "text": f"Account {account_name} (ID {account_id}) is currently {account_status}.",
        "json": {
            "AccountID": account_id,
            "AccountName": account_name,
            "AccountStatus": account_status
        }
    }

    # Return clean structure to Bedrock Agent
    final_response = {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event["actionGroup"],
            "apiPath": event["apiPath"],
            "httpMethod": event["httpMethod"],
            "httpStatusCode": 200,
            "body": response_body
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {})
    }

    print(f"Final response to Bedrock Agent: {json.dumps(final_response)}")
    return final_response
