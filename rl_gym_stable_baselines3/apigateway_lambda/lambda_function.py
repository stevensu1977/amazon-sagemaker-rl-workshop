import os 
import json
import boto3
import base64

#请添加环境变量SMENDPOINT为你部署的sagemaker_endpoint名字

sagemaker_endpoint = os.environ.get('SM_ENDPOINT','')
 
print(f'sagemaker_endpoint: {sagemaker_endpoint}')
runtime = boto3.Session().client('sagemaker-runtime')


def lambda_handler(event, context):
    # TODO implement
    if "body" not in event:
        print("not found body")
        return {
        'statusCode': 400,
        'body': json.dumps('missing parameter!')
        }
    if sagemaker_endpoint == "" :
         return {
        'statusCode': 502,
        'body': json.dumps('endpoint not found, check environment var : SM_ENDPOINT !')
        }
    data = event["body"]
    if "isBase64Encoded" in event:
        if event["isBase64Encoded"]:
             data = base64.b64decode(event["body"]).decode("utf-8")
    #print({"input":data})
    response = runtime.invoke_endpoint(EndpointName=sagemaker_endpoint, ContentType='application/json', Body=data)
    result = json.loads(response['Body'].read().decode())
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

