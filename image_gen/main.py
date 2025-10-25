import json
import boto3
import base64
import datetime


def lambda_handler(event, context):
    client_bedrock = boto3.client('bedrock-runtime')
    client_s3 = boto3.client('s3')
    input_prompt = event['prompt']

    response = client_bedrock.invoke_model(
        modelId='amazon.titan-image-generator-v1',
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": input_prompt
            },
            "imageGenerationConfig": {
                "quality": "standard",
                "numberOfImages": 1,
                "cfgScale": 10.0,
                "seed": 1
            }
        })
    )

    response_body = response['body'].read()
    print("response_body=====")
    print(response_body)

    base64_bytes = response_body.decode('utf-8')
    data = json.loads(base64_bytes)
    base64_str = data["images"][0]

    image_bytes = base64.b64decode(base64_str)
    file_name = f"image_name_{datetime.datetime.today().strftime('%Y-%M-%D-%M-%S')}"

    client_s3.put_object(
        Body=image_bytes,
        Key=file_name,
        Bucket='navoki-movieposterdesign1'
    )

    generate_presigned_url = client_s3.generate_presigned_url('get_object', Params={
        "Bucket": 'navoki-movieposterdesign1', 'Key': file_name
    }, HttpMethod=None, ExpiresIn=1000)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(response, default=str)
    }
