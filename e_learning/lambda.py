import boto3
import json

client_knowledge = boto3.client('bedrock-agent-runtime')


def lambda_handler(event, context):
    user_prompt = event['prompt']
    print(user_prompt)

    request_body = {
        'input': {
            'text': user_prompt
        },
        'retrieveAndGenerateConfiguration': {
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'ON35CYA45B',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-micro-v1:0',
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': 5
                    }
                }
            }
        }
    }
    response = client_knowledge.retrieve_and_generate(**request_body)

    return {
        'statusCode': 200,
        'body': json.dumps(response['output']['text'])
    }
