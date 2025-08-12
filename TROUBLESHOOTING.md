# Troubleshooting Guide

## Lỗi 404 Not Found cho API endpoints

### Vấn đề:
```
Failed to import API router: No module named 'app.models.datasource'
```

### Nguyên nhân:
1. Import sai trong các file
2. Thiếu file `__init__.py`
3. Conflict với tên field trong Pydantic models
4. Dependencies chưa được cài đặt

### Giải pháp đã áp dụng:

#### 1. Sửa import trong DataSourceService:
```python
# Trước (sai):
from app.models.data_source import DataSource

# Sau (đã sửa):
# Loại bỏ import không cần thiết
```

#### 2. Tạo các file `__init__.py`:
- `app/models/__init__.py`
- `app/schemas/__init__.py`
- `app/services/__init__.py`
- `app/api/v1/endpoints/__init__.py`

#### 3. Sửa conflict với Pydantic BaseModel:
```python
# Trước (có conflict):
schema: Optional[str] = Field(None, description="Table schema")

# Sau (đã sửa):
table_schema: Optional[str] = Field(None, description="Table schema")
```

#### 4. Cài đặt dependencies:
```bash
source venv/bin/activate
pip install PyJWT==2.8.0
```

### Cách test:

#### 1. Khởi động backend:
```bash
cd project_root/report_system
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Test API endpoints:
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test data sources endpoint
curl http://localhost:8000/api/v1/data-sources/test

# Test data sources main endpoint
curl http://localhost:8000/api/v1/data-sources/
```

#### 3. Sử dụng script test:
```bash
python test_api.py
```

### Kiểm tra logs:
- Xem logs của backend để tìm lỗi import
- Kiểm tra console của frontend để tìm lỗi API calls
- Đảm bảo backend đang chạy trên port 8000

### Nếu vẫn còn lỗi:
1. Kiểm tra tất cả imports trong các file
2. Đảm bảo tất cả dependencies đã được cài đặt
3. Restart backend sau khi sửa
4. Kiểm tra file permissions và cấu trúc thư mục
