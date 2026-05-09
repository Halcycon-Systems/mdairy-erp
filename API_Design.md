# Detailed API Design for Milk Processing Cooperative System

Based on your final system design (PDF), here is a **production-ready API design** using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. The design is modular, team-collaboration friendly, and includes Swagger documentation.

---

## 1. Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Apps                              │
│  React Web Dashboard | React Native Mobile | React POS Terminal  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTPS/JSON
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx (Reverse Proxy)                       │
│                    SSL Termination / Load Balancing              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Routers     │  │  Services    │  │  Models      │           │
│  │ (Endpoints)  │──│ (Business    │──│ (SQLAlchemy) │           │
│  └──────────────┘  │   Logic)     │  └──────────────┘           │
│                    └──────────────┘                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Schemas     │  │  Core        │  │  Utils       │           │
│  │ (Pydantic)   │  │ (Auth, DB)   │  │ (Helpers)    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────┬──────────────┬──────────────┬─────────────────────┘
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐   ┌────────────┐   ┌────────────┐
     │ PostgreSQL │   │   Redis    │   │   Odoo     │
     │  (primary) │   │ (cache/    │   │  (external │
     │            │   │  queue)    │   │   API)     │
     └────────────┘   └────────────┘   └────────────┘
              │
              ▼
     ┌────────────────────────────────────────────┐
     │         External Services                  │
     │  Daraja (M-Pesa) | SMTP | SMS Gateway      │
     └────────────────────────────────────────────┘
```

---

## 2. Project Folder Structure (Modular for Team Collaboration)

```
milk-coop-backend/
├── docker-compose.yml
├── .env.example
├── Dockerfile
├── requirements.txt
├── .gitignore
├── README.md
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app creation, lifespan, router inclusion
│   │
│   ├── core/                   # Core configurations & utilities
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic settings (DB, Redis, Daraja, Odoo)
│   │   ├── database.py         # SQLAlchemy engine, session local
│   │   ├── redis_client.py     # Redis connection pool
│   │   ├── security.py         # JWT functions, password hashing, RBAC dependency
│   │   ├── deps.py             # Common dependencies (get_current_user, etc.)
│   │   └── logging.py          # Structured logging setup
│   │
│   ├── models/                 # SQLAlchemy ORM models (one file per module)
│   │   ├── __init__.py
│   │   ├── base.py             # Declarative base
│   │   ├── user.py             # User, Role, Permission, UserSession
│   │   ├── farmer.py           # Farmer, Society, CollectionCenter
│   │   ├── milk.py             # MilkCollection, QualityTest, RejectionLog
│   │   ├── wallet.py           # FarmerWallet, WalletTransaction, SocietyLiability
│   │   ├── pricing.py          # PricingRule
│   │   ├── loan.py             # LoanApplication, LoanProduct, LoanRepaymentSchedule
│   │   ├── pos.py              # Product, SaleOrder, CreditSale
│   │   ├── payment.py          # PaymentSchedule, MpesaTransaction, DeductionRule
│   │   └── audit.py            # AuditLog
│   │
│   ├── schemas/                # Pydantic models (request/response validation)
│   │   ├── __init__.py
│   │   ├── common.py           # Pagination, standard responses
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── farmer.py
│   │   ├── milk.py
│   │   ├── wallet.py
│   │   ├── pricing.py
│   │   ├── loan.py
│   │   ├── pos.py
│   │   ├── payment.py
│   │   └── report.py
│   │
│   ├── services/               # Business logic (one per module)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── farmer_service.py
│   │   ├── milk_service.py
│   │   ├── pricing_service.py
│   │   ├── wallet_service.py
│   │   ├── loan_service.py
│   │   ├── pos_service.py
│   │   ├── payment_service.py
│   │   ├── odoo_service.py     # Odoo API calls
│   │   ├── daraja_service.py   # M-Pesa API calls
│   │   └── notification_service.py  # SMS/Email/Push
│   │
│   ├── api/                    # Route handlers (routers)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── farmers.py
│   │   │   ├── societies.py
│   │   │   ├── milk.py
│   │   │   ├── wallet.py
│   │   │   ├── loans.py
│   │   │   ├── pos.py
│   │   │   ├── payments.py
│   │   │   ├── reports.py
│   │   │   ├── webhooks.py     # Daraja C2B callbacks
│   │   │   └── odoo_sync.py
│   │   │
│   │   └── deps.py             # Router-level dependencies
│   │
│   ├── tasks/                  # Background tasks (Celery / Redis Queue)
│   │   ├── __init__.py
│   │   ├── worker.py
│   │   ├── payment_tasks.py    # Batch B2C, wallet deductions
│   │   ├── loan_tasks.py       # Amortization schedule generation, penalty calculation
│   │   └── notification_tasks.py
│   │
│   ├── utils/                  # Helper functions
│   │   ├── __init__.py
│   │   ├── idempotency.py
│   │   ├── validators.py       # Phone, email, ID number validation
│   │   ├── date_helpers.py
│   │   └── excel_generator.py
│   │
│   └── migrations/             # Alembic database migrations
│       ├── env.py
│       ├── versions/
│       └── alembic.ini
│
├── tests/                      # Pytest tests (mirrors app structure)
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
│
└── scripts/                    # Utility scripts
    ├── seed_data.py
    └── init_db.py
```

---

## 3. Docker Configuration

### 3.1 Dockerfile (FastAPI)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2 and cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations on startup (optional, can be done via entrypoint)
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 3.2 entrypoint.sh

```bash
#!/bin/bash
set -e

# Run Alembic migrations
alembic upgrade head

# Seed initial data if needed
python scripts/seed_data.py

# Start the app
exec "$@"
```

### 3.3 docker-compose.yml (Full Stack)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: milk_coop_postgres
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - milk_coop_network

  redis:
    image: redis:7-alpine
    container_name: milk_coop_redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - milk_coop_network

  api:
    build: .
    container_name: milk_coop_api
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
    volumes:
      - ./app:/app/app
      - ./tests:/app/tests
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - milk_coop_network
    develop:  # for hot reload during development
      watch:
        - action: sync
          path: ./app
          target: /app/app
        - action: rebuild
          path: requirements.txt

  nginx:
    image: nginx:alpine
    container_name: milk_coop_nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl  # optional
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - api
    networks:
      - milk_coop_network

networks:
  milk_coop_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 3.4 .env.example

```env
# Database
DB_USER=coop_user
DB_PASSWORD=strong_password
DB_NAME=milk_coop
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_PASSWORD=redis_secure

# JWT
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Daraja API (Sandbox)
DARAJAK_CONSUMER_KEY=your_consumer_key
DARAJAK_CONSUMER_SECRET=your_consumer_secret
DARAJAK_PASSKEY=your_passkey
DARAJAK_SHORTCODE=174379
DARAJAK_ENVIRONMENT=sandbox  # or production

# Odoo
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=odoo_db
ODOO_USERNAME=api_user
ODOO_PASSWORD=api_password
ODOO_API_KEY=your_api_key

# SMS/Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=notification@coop.com
SMTP_PASSWORD=email_password
SMS_API_KEY=africastalking_key
```

---

## 4. Core Code Implementation

### 4.1 app/core/config.py (Pydantic Settings)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://coop_user:password@postgres:5432/milk_coop"
    
    # Redis
    REDIS_URL: str = "redis://:password@redis:6379"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Daraja
    DARAJAK_CONSUMER_KEY: str
    DARAJAK_CONSUMER_SECRET: str
    DARAJAK_PASSKEY: str
    DARAJAK_SHORTCODE: str = "174379"
    DARAJAK_ENVIRONMENT: str = "sandbox"  # sandbox or production
    
    # Odoo
    ODOO_URL: str
    ODOO_DB: str
    ODOO_USERNAME: str
    ODOO_PASSWORD: str
    ODOO_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 4.2 app/core/database.py (SQLAlchemy Setup)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.3 app/core/security.py (JWT & Password)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### 4.4 app/core/deps.py (Common Dependencies)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.services.auth_service import get_user_by_id

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

def role_required(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.name != required_role and current_user.role.name != "company_admin":
            raise HTTPException(status_code=403, detail=f"Role {required_role} required")
        return current_user
    return role_checker

def permission_required(permission: str):
    def perm_checker(current_user: User = Depends(get_current_user)):
        if not current_user.has_permission(permission):
            raise HTTPException(status_code=403, detail=f"Permission {permission} required")
        return current_user
    return perm_checker
```

### 4.5 app/main.py (FastAPI Application)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1 import auth, farmers, milk, wallet, loans, pos, payments, reports, webhooks
from app.core.database import engine, Base
from app.core.config import settings

# Create tables (in production use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Milk Processing Cooperative API",
    description="API for managing farmers, milk collection, wallets, loans, POS, and M-Pesa payments",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefix /api/v1
api_v1 = FastAPI()
api_v1.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1.include_router(farmers.router, prefix="/farmers", tags=["Farmers"])
api_v1.include_router(milk.router, prefix="/milk", tags=["Milk Collection"])
api_v1.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
api_v1.include_router(loans.router, prefix="/loans", tags=["Loans"])
api_v1.include_router(pos.router, prefix="/pos", tags=["POS"])
api_v1.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_v1.include_router(reports.router, prefix="/reports", tags=["Reports"])

app.mount("/api/v1", api_v1)

# Webhooks (no versioning)
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

# Custom OpenAPI to include bearer auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 5. Example Router, Schema, Service

### 5.1 Schema (app/schemas/farmer.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class FarmerBase(BaseModel):
    name: str
    national_id: str
    phone: str
    email: Optional[EmailStr] = None
    society_id: int
    rfid_card_number: Optional[str] = None

class FarmerCreate(FarmerBase):
    pass

class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class FarmerResponse(FarmerBase):
    id: int
    wallet_balance: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FarmerWithWallet(FarmerResponse):
    wallet_id: int
```

### 5.2 Model (app/models/farmer.py)

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Society(Base):
    __tablename__ = "societies"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True)
    address = Column(Text)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    farmers = relationship("Farmer", back_populates="society")
    collection_centers = relationship("CollectionCenter", back_populates="society")

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True)
    society_id = Column(Integer, ForeignKey("societies.id"))
    name = Column(String(200), nullable=False)
    national_id = Column(String(20), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    rfid_card_number = Column(String(50), unique=True)
    wallet_balance = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    society = relationship("Society", back_populates="farmers")
    wallet = relationship("FarmerWallet", uselist=False, back_populates="farmer")
    milk_collections = relationship("MilkCollection", back_populates="farmer")
    loan_applications = relationship("LoanApplication", back_populates="farmer")
```

### 5.3 Service (app/services/farmer_service.py)

```python
from sqlalchemy.orm import Session
from app.models.farmer import Farmer, Society
from app.schemas.farmer import FarmerCreate, FarmerUpdate
from app.services.wallet_service import create_wallet_for_farmer

def get_farmer(db: Session, farmer_id: int):
    return db.query(Farmer).filter(Farmer.id == farmer_id, Farmer.is_active == True).first()

def get_farmer_by_national_id(db: Session, national_id: str):
    return db.query(Farmer).filter(Farmer.national_id == national_id).first()

def get_farmers_by_society(db: Session, society_id: int, skip: int = 0, limit: int = 100):
    return db.query(Farmer).filter(Farmer.society_id == society_id).offset(skip).limit(limit).all()

def create_farmer(db: Session, farmer_data: FarmerCreate):
    # Check if society exists
    society = db.query(Society).filter(Society.id == farmer_data.society_id).first()
    if not society:
        raise ValueError("Society not found")
    
    db_farmer = Farmer(**farmer_data.model_dump())
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    
    # Create wallet for farmer
    create_wallet_for_farmer(db, db_farmer.id)
    
    return db_farmer

def update_farmer(db: Session, farmer_id: int, farmer_update: FarmerUpdate):
    db_farmer = get_farmer(db, farmer_id)
    if not db_farmer:
        return None
    update_data = farmer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_farmer, field, value)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

def delete_farmer(db: Session, farmer_id: int):
    db_farmer = get_farmer(db, farmer_id)
    if db_farmer:
        db_farmer.is_active = False
        db.commit()
        return True
    return False
```

### 5.4 Router (app/api/v1/farmers.py)

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user, role_required, permission_required
from app.models.user import User
from app.schemas.farmer import FarmerCreate, FarmerUpdate, FarmerResponse
from app.services import farmer_service

router = APIRouter()

@router.get("/", response_model=List[FarmerResponse])
def list_farmers(
    society_id: int = Query(None, description="Filter by society"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required("society_manager"))
):
    if society_id:
        # Ensure manager belongs to that society (implement check)
        farmers = farmer_service.get_farmers_by_society(db, society_id, skip, limit)
    else:
        farmers = farmer_service.get_farmers_by_society(db, current_user.society_id, skip, limit)
    return farmers

@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farmer = farmer_service.get_farmer(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    # Authorization: company_admin or manager of same society
    if current_user.role.name not in ["company_admin", "super_admin"]:
        if farmer.society_id != current_user.society_id:
            raise HTTPException(status_code=403, detail="Not authorized")
    return farmer

@router.post("/", response_model=FarmerResponse, status_code=status.HTTP_201_CREATED)
def create_farmer(
    farmer_data: FarmerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(permission_required("create_farmer"))
):
    try:
        farmer = farmer_service.create_farmer(db, farmer_data)
        return farmer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{farmer_id}", response_model=FarmerResponse)
def update_farmer(
    farmer_id: int,
    farmer_update: FarmerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(permission_required("edit_farmer"))
):
    farmer = farmer_service.update_farmer(db, farmer_id, farmer_update)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer

@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(
    farmer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(permission_required("delete_farmer"))
):
    if not farmer_service.delete_farmer(db, farmer_id):
        raise HTTPException(status_code=404, detail="Farmer not found")
```

---

## 6. Swagger Documentation

FastAPI automatically generates OpenAPI JSON at `/api/openapi.json` and Swagger UI at `/api/docs`. The custom openapi function in `main.py` adds Bearer authentication to all endpoints.

To view: Run the API and visit `http://localhost:8000/api/docs`

---

## 7. Team Collaboration Guidelines

### 7.1 Branch Strategy

```
main (production)
│
├── develop (integration)
│   ├── feature/auth-module
│   ├── feature/farmer-mgmt
│   ├── feature/milk-collection
│   ├── feature/wallet-pricing
│   ├── feature/loan-mgmt
│   ├── feature/pos
│   ├── feature/payment-engine
│   ├── feature/odoo-integration
│   └── feature/daraja-integration
```

### 7.2 Code Ownership (Team A vs Team B)

| Team | Folders |
|------|---------|
| **Team A** | `app/api/v1/auth.py`, `users.py`, `wallet.py`, `loans.py`, `payments.py`, `webhooks.py`<br>`app/services/auth_service.py`, `wallet_service.py`, `loan_service.py`, `payment_service.py`, `odoo_service.py`, `daraja_service.py`<br>`app/models/user.py`, `wallet.py`, `loan.py`, `payment.py`<br>`app/schemas/auth.py`, `wallet.py`, `loan.py`, `payment.py` |
| **Team B** | `app/api/v1/farmers.py`, `societies.py`, `milk.py`, `pos.py`, `reports.py`<br>`app/services/farmer_service.py`, `milk_service.py`, `pricing_service.py`, `pos_service.py`, `notification_service.py`<br>`app/models/farmer.py`, `milk.py`, `pricing.py`, `pos.py`<br>`app/schemas/farmer.py`, `milk.py`, `pricing.py`, `pos.py`, `report.py` |

### 7.3 Development Workflow

1. Each developer works on a feature branch from `develop`
2. Use `pre-commit` hooks (black, isort, flake8)
3. Write unit tests for services (pytest)
4. Run `docker-compose up --build` to test locally
5. Submit PR to `develop`; CI runs tests and linters
6. Weekly integration: merge `develop` to `main` after QA approval

---

## 8. Running the Project

### 8.1 First Time Setup

```bash
# Clone repo
git clone https://github.com/your-org/milk-coop-backend.git
cd milk-coop-backend

# Copy environment variables
cp .env.example .env
# Edit .env with real credentials

# Build and run
docker-compose up -d --build

# Check logs
docker-compose logs -f api

# Run migrations manually (if needed)
docker-compose exec api alembic upgrade head

# Seed initial data (roles, admin user)
docker-compose exec api python scripts/seed_data.py
```

### 8.2 Access Services

| Service | URL |
|---------|-----|
| API Swagger UI | http://localhost:8000/api/docs |
| API Redoc | http://localhost:8000/api/redoc |
| PostgreSQL | localhost:5432 |
| Redis Insight | localhost:6379 |

---

## 9. Testing (Pytest)

```python
# tests/test_api/test_farmers.py
def test_create_farmer(client, db_session, auth_header):
    response = client.post(
        "/api/v1/farmers/",
        json={
            "name": "John Mwangi",
            "national_id": "12345678",
            "phone": "0712345678",
            "society_id": 1
        },
        headers=auth_header
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John Mwangi"
```

Run tests:

```bash
docker-compose exec api pytest -v
```

---

## 10. Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | REST endpoints with OpenAPI |
| ORM | SQLAlchemy | Database models & queries |
| Validation | Pydantic V2 | Request/response schemas |
| Auth | JWT + bcrypt | Stateless authentication, RBAC |
| Caching/Queue | Redis | Session storage, rate limiting, task queue |
| Database | PostgreSQL | Primary data store |
| Containerization | Docker + Compose | Development & production isolation |
| Testing | Pytest | Unit & integration tests |

This design enables **parallel development** by two teams, with clear separation of concerns, automatic API documentation, and easy deployment via Docker. All code is modular, testable, and ready for scaling.