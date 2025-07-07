region = "us-east-1"
environment = "prod"
vpc_id = "vpc-xxxxxxxx"
public_subnet_ids = ["subnet-yyyyy1", "subnet-yyyyy2"]
private_subnet_ids = ["subnet-yyyyy3", "subnet-yyyyy4"]

# Production DB credentials
# Use secure values via environment variables/CI secrets in real usage
db_name = "news_prod"
db_username = "news"
db_password = "change_me_prod"
