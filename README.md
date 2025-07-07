# Jota News

A comprehensive news classification and distribution system built with Django, designed to handle high-volume news processing with automatic categorization, tagging, and urgency scoring.

## Overview

Jota News automatically processes news articles through a complete pipeline:
**Webhook Reception** → **SQS Queue** → **Lambda Processing** → **Classification** → **Database** → **REST API**

### Key Features

- ✅ **Automatic News Classification** - Categorizes news into Poder, Tributos, Saúde, Trabalhista
- ✅ **Smart Tag Extraction** - Automatically extracts relevant tags from content
- ✅ **Urgency Scoring** - Calculates urgency based on keywords and timing
- ✅ **REST API** - Complete API with filtering, pagination, and authentication
- ✅ **Scalable Architecture** - Ready for AWS deployment with ECS, RDS, Lambda, SQS
- ✅ **Performance Optimized** - Processes 200+ articles/second
- ✅ **Security Focused** - JWT authentication, rate limiting, input validation

## Quick Start

### Docker (Recommended)

```bash
# Clone and start
git clone https://github.com/wilsonricardopereirasilveira/jota_news.git
cd jota_news
docker-compose up --build -d
```

### Local Development

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install and run
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial_categories.json
python manage.py createsuperuser
python manage.py runserver
```

## Installation

### Prerequisites

- Docker & Docker Compose (for containerized deployment)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for production)
- Redis 7+ (for caching)

### Environment Configuration

Create `.env` file in project root:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
POSTGRES_DB=jota_news
POSTGRES_USER=jota
POSTGRES_PASSWORD=jota
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Cache & Queue
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Webhook Authentication
WEBHOOK_API_KEY=your-webhook-api-key

# AWS (Production)
AWS_REGION=us-east-1
SQS_NEWS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/account/news-queue
```

## Docker Deployment

### Commands

```bash
# Build and start all services
docker-compose build
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web

# Execute commands
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

### Services

- **web**: Django application server
- **db**: PostgreSQL 15 database
- **redis**: Redis cache and message broker
- **celery**: Background task processor

## Local Development

### Database Setup

**PostgreSQL (Recommended):**

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE jota_news;
CREATE USER jota WITH ENCRYPTED PASSWORD 'jota';
GRANT ALL PRIVILEGES ON DATABASE jota_news TO jota;
\q
```

**SQLite (Development):**

Edit `jota_news/settings/development.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Application Setup

```bash
# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/initial_categories.json

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Additional Services (Optional)

```bash
# Start Redis
redis-server

# Start Celery worker
celery -A jota_news worker -l info
```

## API Documentation

### Authentication

**JWT Token:**
```bash
# Get token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your-username", "password": "your-password"}'

# Use token
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/news/
```

### Webhook Endpoint

**Receive News Article:**
```bash
curl -X POST http://localhost:8000/api/webhook/news/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-webhook-api-key" \
  -d '{
    "title": "STF maintains ceiling for Income Tax education deduction",
    "content": "The Supreme Federal Court decided to maintain the limit...",
    "source": "Jota Info",
    "published_at": "2024-01-15T10:30:00Z",
    "url": "https://jota.info/tributos/stf-imposto-renda",
    "author": "Jota Newsroom"
  }'
```

**Response:**
```json
{"status": "accepted"}
```

### REST API Endpoints

**News Articles:**
```bash
# List all news
curl http://localhost:8000/api/news/

# Filter by category
curl http://localhost:8000/api/news/?category=tributos

# Filter urgent news
curl http://localhost:8000/api/news/?is_urgent=true

# Search by keyword
curl "http://localhost:8000/api/news/?search=imposto"

# Filter by tags
curl "http://localhost:8000/api/news/?tags=stf,imposto"

# Filter by date range
curl "http://localhost:8000/api/news/?published_after=2024-01-01&published_before=2024-12-31"

# Mark as urgent
curl -X PATCH http://localhost:8000/api/news/1/mark-urgent/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Categories:**
```bash
# List categories
curl http://localhost:8000/api/categories/

# Get category details
curl http://localhost:8000/api/categories/1/

# News in category
curl http://localhost:8000/api/categories/1/news/
```

**Tags:**
```bash
# List tags
curl http://localhost:8000/api/tags/

# News with tag
curl http://localhost:8000/api/tags/1/news/
```

**Statistics:**
```bash
# System stats
curl http://localhost:8000/api/stats/
```

### API Response Format

```json
{
  "links": {
    "next": "http://localhost:8000/api/news/?page=2",
    "previous": null
  },
  "count": 1450,
  "total_pages": 73,
  "results": [
    {
      "id": 1,
      "title": "News article title",
      "content": "Article content...",
      "source": "News Source",
      "published_at": "2024-01-15T10:30:00Z",
      "category": {
        "id": 2,
        "name": "Tributos",
        "slug": "tributos"
      },
      "tags": [
        {"id": 1, "name": "imposto", "slug": "imposto"}
      ],
      "is_urgent": false,
      "urgency_score": 45,
      "created_at": "2024-01-15T10:31:00Z"
    }
  ]
}
```

## Architecture

### System Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Webhook   │───▶│  SQS Queue  │───▶│   Lambda    │───▶│ PostgreSQL  │
│  Endpoint   │    │ (AWS/Local) │    │ Processor   │    │  Database   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                             │                    │
                                             ▼                    ▼
                                      ┌─────────────┐    ┌─────────────┐
                                      │ Classifier  │    │  REST API   │
                                      │ + Tagger +  │    │  + Filters  │
                                      │ Urgency     │    │ + Cache     │
                                      └─────────────┘    └─────────────┘
```

### Classification System

**Categories:**
- **Tributos** - Tax and fiscal matters
- **Poder** - Government powers (Executive, Legislative, Judicial)  
- **Saúde** - Health and medical topics
- **Trabalhista** - Labor and employment law
- **Outros** - Uncategorized articles

**Keywords Examples:**
```python
CATEGORY_KEYWORDS = {
    'Tributos': ['imposto', 'tributacao', 'receita federal', 'ir', 'icms'],
    'Poder': ['supremo', 'stf', 'congresso', 'senado', 'presidente'],
    'Saude': ['saude', 'sus', 'medicamento', 'anvisa'],
    'Trabalhista': ['clt', 'trabalhador', 'emprego', 'tst']
}
```

**Urgency Scoring:**
- Urgent keywords: +30 points
- Night/weekend timing: +20 points  
- Authority mentions: +20 points
- Score ≥ 70 = Urgent article

**Performance Metrics:**
- Throughput: 200+ articles/second
- Classification: 100% automatic
- Response Time: <100ms API responses

## Configuration

### Settings Structure

```
jota_news/settings/
├── base.py          # Common settings
├── development.py   # Development overrides
├── production.py    # Production configuration
└── test.py         # Test environment
```

### Key Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | `your-secret-key` |
| `DJANGO_DEBUG` | Debug mode | `True`/`False` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection | `redis://localhost:6379/0` |
| `WEBHOOK_API_KEY` | Webhook authentication | `your-api-key` |

## Production Deployment

### AWS Infrastructure

Complete Terraform configuration included:

```bash
cd infrastructure/terraform
terraform init
terraform plan -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars
```

**AWS Services:**
- ECS Fargate (containers)
- RDS PostgreSQL (database)
- ElastiCache Redis (cache)
- Lambda (processing)
- SQS (queuing)
- ALB (load balancing)
- CloudWatch (monitoring)

### Deployment Scripts

```bash
# Deploy application
./infrastructure/scripts/deploy.sh

# Run migrations
./infrastructure/scripts/migrate.sh

# Health check
./infrastructure/scripts/health_check.sh
```

## Security

### Features

- **JWT Authentication** - Secure API access
- **API Key Authentication** - Webhook security
- **Rate Limiting** - 1000 requests/hour
- **Input Validation** - XSS and injection prevention
- **Security Headers** - HSTS, CSP, etc.

### Security Headers

```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
```

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health/live/

# Database connectivity  
curl http://localhost:8000/health/ready/

# Deep system check
curl http://localhost:8000/health/deep/
```

### Metrics

- Request latency and throughput
- Database query performance
- Cache hit rates
- Error rates by endpoint

### Logging

Structured JSON logging with:
- Request/response tracking
- Error monitoring
- Performance metrics
- Business events

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific categories
pytest tests/unit/
pytest tests/integration/
pytest apps/webhook/tests/

# Coverage report
pytest --cov=apps --cov-report=html
```

### Test Categories

- **Unit Tests** - Component testing
- **Integration Tests** - API testing  
- **Performance Tests** - Load testing
- **End-to-End Tests** - Workflow validation

## Project Structure

```
jota_news/
├── apps/                    # Django applications
│   ├── api/                # REST API implementation
│   ├── categories/         # Category models
│   ├── core/              # Common utilities
│   ├── monitoring/        # Health checks & metrics
│   ├── news/              # News article models
│   ├── security/          # Authentication & validation
│   └── webhook/           # Webhook receiver
├── docs/                  # Documentation
├── fixtures/              # Initial data
├── infrastructure/        # Deployment configurations
│   ├── docker/           # Docker configurations
│   ├── scripts/          # Deployment scripts
│   └── terraform/        # AWS infrastructure
├── lambda_processor/      # News processing logic
├── monitoring/           # Monitoring configurations
├── scripts/              # Utility scripts
└── tests/               # Test suites
```

## URLs Reference

### Application URLs

- **Local Development**: `http://127.0.0.1:8000`
- **Docker**: `http://localhost:8000`
- **Admin Panel**: `/admin/`
- **API Documentation**: `/api/swagger/`

### Key Endpoints

- **Webhook**: `POST /api/webhook/news/`
- **News API**: `GET /api/news/`
- **Categories**: `GET /api/categories/`
- **Health Check**: `GET /health/live/`

## Contributing

### Setup

```bash
git clone https://github.com/wilsonricardopereirasilveira/jota_news.git
cd jota_news
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
pre-commit install
```

### Standards

- Follow PEP 8 style guide
- Use Django best practices
- Maintain >90% test coverage
- Document all public APIs
- Use type annotations

### Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Run full test suite
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: Open GitHub issue
- **Documentation**: Check `/docs` directory  
- **Architecture**: Review system design docs

---

*Built for high-performance news processing*