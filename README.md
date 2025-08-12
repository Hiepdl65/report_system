# Report System Backend API

A FastAPI-based backend for the FlexiReport system, providing RESTful APIs for report generation, data source management, and template management.

## Features

- 🚀 **FastAPI**: High-performance web framework for building APIs
- 🔐 **Authentication**: JWT-based authentication system
- 📊 **Data Sources**: Support for multiple database types (MySQL, PostgreSQL, CSV, Excel, API)
- 📋 **Templates**: Report template management and sharing
- 🔐 **Permissions**: Role-based access control for templates
- 📤 **Reports**: Dynamic report generation and export
- 🗄️ **Database**: SQLAlchemy ORM with MySQL support

## Prerequisites

- Python 3.8+
- MySQL 5.7+ or PostgreSQL 12+
- Redis (optional, for caching)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd report_system
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database and configuration settings
```

## Configuration

Update the `.env` file with your settings:

```env
# Database
MYSQL_SERVER=localhost
MYSQL_PORT=3306
MYSQL_USER=report_user
MYSQL_PASSWORD=secure_password
MYSQL_DB=report_system

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Running the Application

### Development Mode

```bash
# Start the development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Using the start script
./start_app.sh

# Or manually
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Health Check
- `GET /api/v1/health` - Health status

### Data Sources
- `GET /api/v1/data-sources/` - Get all data sources
- `POST /api/v1/data-sources/` - Create new data source
- `POST /api/v1/data-sources/test-connection` - Test connection
- `GET /api/v1/data-sources/{id}/tables` - Get tables from data source
- `GET /api/v1/data-sources/{id}/tables/{table}/columns` - Get columns from table

### Templates
- `GET /api/v1/templates/` - Get all templates
- `POST /api/v1/templates/` - Create new template
- `GET /api/v1/templates/{id}` - Get specific template
- `PUT /api/v1/templates/{id}` - Update template
- `DELETE /api/v1/templates/{id}` - Delete template
- `POST /api/v1/templates/{id}/duplicate` - Duplicate template

### Reports
- `POST /api/v1/reports/run` - Execute report
- `POST /api/v1/reports/preview` - Preview report
- `GET /api/v1/reports/history` - Get report history

### Permissions
- `POST /api/v1/permissions/grant` - Grant template permissions
- `GET /api/v1/permissions/template/{id}` - Get template permissions
- `DELETE /api/v1/permissions/template/{id}/user/{user_id}` - Revoke permission
- `GET /api/v1/permissions/check/{id}` - Check user permission

## Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/
│       ├── endpoints/      # Route handlers
│       └── api.py         # Main router
├── core/                   # Core configuration
│   └── config.py          # Settings and configuration
├── models/                 # Database models
├── schemas/                # Pydantic schemas
├── services/               # Business logic
├── utils/                  # Utility functions
└── main.py                 # Application entry point
```

## Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE report_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'report_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON report_system.* TO 'report_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Run migrations (when available):
```bash
# Future: alembic upgrade head
```

## Development

### Code Style

- Use Black for code formatting
- Follow PEP 8 guidelines
- Use type hints throughout the codebase

### Testing

```bash
# Run tests (when available)
pytest

# Run with coverage
pytest --cov=app
```

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Add router to `app/api/v1/api.py`
3. Create corresponding schema in `app/schemas/`
4. Create service in `app/services/`
5. Add tests

## Docker Support

Build and run with Docker:

```bash
# Build image
docker build -t report-system .

# Run container
docker run -p 8000:8000 report-system
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 