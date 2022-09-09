if [ -n "$1" ]; then
  echo "SageMaker endpoint name : $1"
  SM_ENDPOINT=$1 
else
  echo "You need provide Sagemaker endpoint name"
  exit 0
fi


AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
LAMBDA_NAME=stablebaselines3-lambda-func
LAMBDA_EXECUTE_ROLE=Stablebaselines3LambdaExecuteRole

if [ -f "lambda_execute_role.json" ]; then
    rm lambda_execute_role.json
fi

sed -e "s/AWS_REGION/${AWS_REGION}/g;s/AWS_ACCOUNT_ID/${AWS_ACCOUNT_ID}/g" lambda_execute_role.json.template > lambda_execute_role.json


create_iam_requirements() {
    
    echo "start create policy and lambda execute role ......"
    aws iam create-policy \
    --policy-name Stablebaselines3LambdaIAMPolicy \
    --policy-document file://lambda_execute_role.json
    POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`Stablebaselines3LambdaIAMPolicy`].Arn' --output text )

    aws iam create-role --role-name ${LAMBDA_EXECUTE_ROLE} --assume-role-policy-document file://trust_policy.json

    aws iam attach-role-policy --policy-arn ${POLICY_ARN} --role-name ${LAMBDA_EXECUTE_ROLE} 

    ROLE_ARN=$(aws iam get-role --role-name ${LAMBDA_EXECUTE_ROLE} --query 'Role.Arn' --output text)

    echo "create policy ${POLICY_ARN}, role ${LAMBDA_EXECUTE_ROLE} successfully" 
}

create_lambda() {

  echo "start create lambda ......"


  if [ -f "stablebaselines3-lambda-package.zip" ]; then
    rm stablebaselines3-lambda-package.zip
  fi

  zip stablebaselines3-lambda-package.zip lambda_function.py

  aws lambda create-function \
      --function-name ${LAMBDA_NAME} \
      --runtime python3.8 \
      --zip-file fileb://stablebaselines3-lambda-package.zip \
      --handler lambda_function.lambda_handler \
      --environment Variables={SM_ENDPOINT=${SM_ENDPOINT}} \
      --role ${ROLE_ARN} 

  #need add permission for lambda 
  aws lambda add-permission \
      --function-name stablebaselines3-lambda-func \
      --action lambda:InvokeFunction \
      --statement-id apigatewayv2 \
      --principal apigateway.amazonaws.com


  LAMBDA_ARN=$(aws lambda get-function  --function-name ${LAMBDA_NAME} --query 'Configuration.FunctionArn' --output text)

  echo "${LAMBDA_ARN} create successfully"

}

create_apigateway() {

  echo "create APIGateway"

  aws apigatewayv2 create-api \
      --name stablebase3-endpoint-http-api \
      --protocol-type HTTP \
      --route-key "POST /predict" \
      --target ${LAMBDA_ARN}


  #Get API Endpoint
  APGW_ENDPOINT=$(aws apigatewayv2 get-apis --query 'Items[?Name==`stablebase3-endpoint-http-api`].ApiEndpoint' --output text)

  echo "create apigateway ${APGW_ENDPOINT} successfully"
  
  #Test API Gateway + Lambda + SageMaker Inference
  #curl -v -X POST -d @obs.json ${END_POINT}/predict

}

#step1 create iam requirements
create_iam_requirements
sleep 1

#step2 create lambda 
create_lambda
sleep 1

#step3  create apigateway use step2 lambda
create_apigateway

echo "test script : curl -v -X POST -d @obs.json ${APGW_ENDPOINT}/predict"






