# Havencrest Realty - Backend & Frontend Integration

This repository hosts the **Havencrest Realty** web platform. It pairs the responsive HTML5/CSS3/Vanilla JS frontend with an asynchronous **FastAPI + SQLAlchemy + SQLite** backend.

---

## Architecture & Project Structure

```text
leye project/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic Settings & Environment configs
│   │   │   └── database.py     # Async SQLAlchemy engine & session factory
│   │   ├── models/
│   │   │   └── models.py       # Property, ContactInquiry, Testimonial models
│   │   ├── schemas/
│   │   │   └── schemas.py      # Request & Response Pydantic v2 validation models
│   │   ├── routers/
│   │   │   ├── properties.py   # CRUD, filtering by status/city/price
│   │   │   ├── inquiries.py    # Contact / inspection lead capture
│   │   │   └── testimonials.py # Testimonial feed
│   │   └── main.py             # FastAPI app, seed data, static mount
│   ├── tests/
│   │   └── test_api.py         # Pytest test suite with in-memory DB
│   └── requirements.txt        # Production & test dependencies
├── havencrest-realty/          # Web frontend assets (HTML, CSS, JS, Images)
└── venv/                       # Python virtual environment
```

---

## Quickstart

### 1. Activate Environment & Install Dependencies
```powershell
.\venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Run the Server
```powershell
uvicorn backend.app.main:app --reload --port 8000
```

- **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Frontend Web Pages**: [http://localhost:8000/index.html](http://localhost:8000/index.html)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status check |
| `GET` | `/api/properties` | List properties with query filters (`status`, `city`, `is_featured`, `min_price`, etc.) |
| `GET` | `/api/properties/{id_or_slug}` | Fetch single property by numerical ID or slug |
| `POST` | `/api/properties` | Create new property listing |
| `PUT` | `/api/properties/{id}` | Update existing property |
| `DELETE` | `/api/properties/{id}` | Remove property |
| `POST` | `/api/inquiries` | Submit client contact / newsletter / tour inquiry |
| `GET` | `/api/inquiries` | View captured inquiries (Admin) |
| `GET` | `/api/testimonials` | Fetch active client testimonials |
| `POST` | `/api/testimonials` | Add a client testimonial |

---

## Running Verification Tests
```powershell
$env:PYTHONPATH="."
.\venv\Scripts\pytest backend\tests
```
