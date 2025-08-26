# POS Backend API

A FastAPI-based backend service for Point of Sale operations that provides RESTful APIs for fare media operations.

## Features

- **RESTful API Endpoints** for all POS operations
- **Standard Response Format** with metadata (status, timestamp, transactionId, robotRunId)
- **CRM Integration** - Proxies requests to CRM backend
- **API Key Authentication** for security
- **CORS Support** for frontend integration
- **Health Check** endpoints
- **Database Support** - SQLite for local development, PostgreSQL for production

## API Endpoints

### Core POS Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cards/issue` | POST | Issue a new card |
| `/api/cards/{id}/reload` | POST | Reload card with amount |
| `/api/cards/{id}/products` | POST | Add product to card |
| `/api/cards/{id}/balance` | GET | Get card balance |
| `/api/payment/simulate` | POST | Simulate payment |
| `/api/customers/{id}` | GET | Get customer information |
| `/api/cards/{id}/transactions` | GET | Get card transaction history |
| `/api/reports/summary` | GET | Get reports summary |
| `/api/simulate/cardTap` | POST | Simulate card tap |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/` | GET | API information |

## Standard Response Format

All API endpoints return a standardized response format:

```json
{
  "status": "success|error",
  "timestamp": "2025-01-14T18:45:32.957936",
  "transactionId": "uuid-string",
  "robotRunId": "optional-robot-id",
  "message": "Operation description",
  "data": {
    // Response data from CRM backend
  }
}
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL (for both local and production)

### Installation

1. **Install PostgreSQL:**
   - Download from: https://www.postgresql.org/download/
   - Set password as `password` during installation
   - Keep default port as `5432`

2. **Set up database:**
   ```bash
   python setup_postgresql.py
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://postgres:password@localhost:5432/pos_db` |
| `POS_API_KEY` | API key for POS authentication | `pos_secret_key` |
| `CRM_API_KEY` | API key for CRM backend | `mysecretkey` |
| `CRM_BASE_URL` | CRM backend URL | `https://crm-n577.onrender.com` |

## Database Configuration

### Local Development (PostgreSQL)
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/pos_db
```

### Production (PostgreSQL on Render)
```bash
DATABASE_URL=postgresql://render_postgres_url
```

## API Authentication

All API endpoints require the `x-api-key` header:

```bash
curl -H "x-api-key: pos_secret_key" http://localhost:8001/api/cards/123/balance
```

## Example Usage

### Issue a Card

```bash
curl -X POST "http://localhost:8001/api/cards/issue" \
  -H "x-api-key: pos_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "4716000000000001",
    "card_type": "Closed Loop Card",
    "customer_id": "CUST000001",
    "issue_date": "2025-01-14"
  }'
```

### Reload a Card

```bash
curl -X POST "http://localhost:8001/api/cards/4716000000000001/reload" \
  -H "x-api-key: pos_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00
  }'
```

### Get Card Balance

```bash
curl -X GET "http://localhost:8001/api/cards/4716000000000001/balance" \
  -H "x-api-key: pos_secret_key"
```

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

## Deployment

### Local Development

```bash
python main.py
```

### Production (Render)

1. Create a new Web Service on Render
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. **For Database:** Create a PostgreSQL database on Render and use the provided DATABASE_URL
7. **Local Setup:** Install PostgreSQL locally and create a database named `pos_db`

## Integration with Frontend

Update the POS frontend to use the new backend:

```javascript
// In POS frontend api.js
const BASE_URL = "http://localhost:8001"; // Local development
// const BASE_URL = "https://your-pos-backend.onrender.com"; // Production
```

## Health Check

```bash
curl http://localhost:8001/health
```

Response:
```json
{
  "status": "healthy",
  "service": "POS Backend",
  "timestamp": "2025-01-14T18:45:32.957936"
}
```

## Architecture

The POS backend acts as an API gateway that:

1. **Receives requests** from POS frontend, Robot, or CRM
2. **Authenticates** requests using API keys
3. **Forwards requests** to CRM backend
4. **Formats responses** with standard metadata
5. **Logs operations** to local database
6. **Returns standardized responses** to clients

## Database Schema

### POSLog Table
- `id`: Primary key
- `operation`: Type of operation performed
- `card_id`: Card identifier
- `customer_id`: Customer identifier
- `amount`: Transaction amount
- `status`: Operation status
- `transaction_id`: Unique transaction ID
- `robot_run_id`: Optional robot run identifier
- `timestamp`: Operation timestamp
- `details`: Additional operation details 