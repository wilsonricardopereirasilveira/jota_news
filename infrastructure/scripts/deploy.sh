#!/bin/bash
set -euo pipefail

# 1. Build Docker images
# 2. Push to ECR
# 3. Deploy Terraform infrastructure
# 4. Update ECS service
# 5. Deploy Lambda functions
# 6. Run database migrations
# 7. Validate deployment

echo "Building API image"
docker build -t jota-news-api -f infrastructure/docker/Dockerfile.api .

echo "Packaging Lambda"
cd lambda_processor && zip -r ../lambda.zip . && cd ..

echo "Deploying Terraform"
cd infrastructure/terraform && terraform init && terraform apply -auto-approve -var-file=environments/${ENV:-dev}.tfvars
