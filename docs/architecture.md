# Architecture

O sistema utiliza Django com PostgreSQL para armazenamento e SQS para fila de processamento.
A Lambda em `lambda_processor/` realiza classificação de notícias e grava em banco.
