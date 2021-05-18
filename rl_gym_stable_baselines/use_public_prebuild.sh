%%sh

# The name of our algorithm
algorithm_name=sagemaker-roboschool-stablebaselines-cpu


account=$(aws sts get-caller-identity --query Account --output text)

# Get the region defined in the current configuration (default to us-west-2 if none defined)
region=$(aws configure get region)

echo ${region}

if [[ $region =~ ^cn.* ]]
then
    fullname="${account}.dkr.ecr.${region}.amazonaws.com.cn/${algorithm_name}:latest"
else
    fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"
fi

echo ${fullname}

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --no-include-email)

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws

public_image=public.ecr.aws/o7x6j3x6/sagemaker-roboschool-stablebaselines-cpu

docker pull ${public_image}
docker tag  ${public_image} ${fullname}

docker push ${fullname}
