resource "aws_db_subnet_group" "this" {
  name       = "rds-${var.environment}-subnets"
  subnet_ids = var.subnet_ids
}

resource "aws_security_group" "rds" {
  name        = "rds-${var.environment}-sg"
  description = "RDS access"
  vpc_id      = var.vpc_id
}

resource "aws_db_instance" "this" {
  identifier         = "news-${var.environment}"
  engine             = "postgres"
  engine_version     = "14.7"
  instance_class     = var.instance_class
  allocated_storage  = 20
  username           = var.db_username
  password           = var.db_password
  db_subnet_group_name = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  multi_az           = var.multi_az
  storage_encrypted  = true
  backup_retention_period = 7
  skip_final_snapshot = true
  apply_immediately  = true
}

resource "aws_secretsmanager_secret" "db" {
  name = "news-${var.environment}-db"
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = aws_db_instance.this.address
    port     = 5432
    dbname   = var.db_name
  })
}

output "endpoint" {
  value = aws_db_instance.this.address
}

output "db_secret_arn" {
  value = aws_secretsmanager_secret.db.arn
}

output "security_group_id" {
  value = aws_security_group.rds.id
}
