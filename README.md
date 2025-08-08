# ERP Query Application

Ứng dụng ERP Query đã được tái cấu trúc theo mô hình modular với cấu trúc thư mục rõ ràng.

## Cấu trúc dự án

```
App_query/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config/
│   │   └── __init__.py          # Configuration settings
│   ├── extensions/
│   │   └── __init__.py          # Flask extensions
│   ├── models/
│   │   ├── __init__.py
│   │   └── database_models.py   # Database models
│   ├── services/
│   │   ├── __init__.py
│   │   └── database_service.py  # Business logic
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── health.py            # Health check endpoints
│   │   └── database.py          # Database operation endpoints
│   └── utils/
│       ├── __init__.py
│       ├── logging_utils.py     # Logging utilities
│       └── validation_utils.py  # Validation utilities
├── run.py                       # Application entry point
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Các thành phần chính

### 1. Configuration (`app/config/`)
- Quản lý cấu hình ứng dụng
- Hỗ trợ nhiều môi trường (development, production, testing)
- Cấu hình CORS, database, security settings

### 2. Models (`app/models/`)
- `database_models.py`: Database connection và connection pooling
- Quản lý kết nối database an toàn và hiệu quả

### 3. Services (`app/services/`)
- `database_service.py`: Business logic cho database operations
- Tách biệt logic nghiệp vụ khỏi controllers

### 4. Blueprints (`app/blueprints/`)
- `health.py`: Health check và monitoring endpoints
- `database.py`: Database operation endpoints
- Tổ chức routes theo chức năng

### 5. Utils (`app/utils/`)
- `logging_utils.py`: Cấu hình và quản lý logging
- `validation_utils.py`: Validation và security utilities

### 6. Extensions (`app/extensions/`)
- Khởi tạo Flask extensions (CORS, etc.)

## Cách sử dụng

### 1. Cài đặt dependencies
```bash
# Tạo virtual environment (nếu chưa có)
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cài đặt ODBC Driver (nếu chưa có)
```bash
# Cài đặt Microsoft ODBC Driver 18 cho SQL Server
sudo apt-get update
sudo apt-get install -y curl apt-transport-https gnupg

# Thêm Microsoft repository
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Cài đặt driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev
```

### 3. Chạy ứng dụng
```bash
# Sử dụng script tự động
./start_app.sh

# Hoặc chạy thủ công
source venv/bin/activate
python3 run.py
```

### 3. Cấu hình môi trường
```bash
export DEBUG=True
export PORT=3000
```

## API Endpoints

### Health Check
- `GET /api/health` - Health check
- `GET /api/stats` - Application statistics

### Database Operations
- `POST /api/test-connection` - Test database connection
- `POST /api/list-databases` - List databases
- `POST /api/tables` - Get tables
- `POST /api/columns` - Get columns
- `POST /api/select` - Select data
- `POST /api/query` - Execute custom query
- `POST /api/export-excel` - Export to Excel

## Lợi ích của cấu trúc mới

1. **Modular**: Mỗi thành phần có trách nhiệm riêng biệt
2. **Maintainable**: Dễ bảo trì và mở rộng
3. **Testable**: Có thể test từng thành phần riêng biệt
4. **Scalable**: Dễ dàng thêm tính năng mới
5. **Clean Architecture**: Tuân thủ nguyên tắc clean architecture

## Migration từ app.py cũ

File `app.py` cũ đã được tách thành các thành phần:
- Configuration → `app/config/__init__.py`
- Database models → `app/models/database_models.py`
- Business logic → `app/services/database_service.py`
- Routes → `app/blueprints/`
- Utilities → `app/utils/`
- Application factory → `app/__init__.py`

## Monitoring

Ứng dụng có tích hợp monitoring:
- Health check endpoint
- Application statistics
- Request/query/error counters
- Connection pool monitoring

## Troubleshooting

### Lỗi ODBC Driver
Nếu gặp lỗi `Can't open lib 'ODBC Driver 18 for SQL Server'`, hãy:

1. **Kiểm tra driver đã cài:**
```bash
odbcinst -q -d
```

2. **Kiểm tra trong Python:**
```bash
python3 -c "import pyodbc; print(pyodbc.drivers())"
```

3. **Test kết nối:**
```bash
python3 test_connection.py
```

### Lỗi Virtual Environment
Đảm bảo kích hoạt virtual environment trước khi chạy:
```bash
source venv/bin/activate
```

### Lỗi Permission
Nếu script không chạy được:
```bash
chmod +x start_app.sh
``` 