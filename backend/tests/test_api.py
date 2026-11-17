import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.main import app
from backend.app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.anyio
async def test_create_and_get_property():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create property
        prop_payload = {
            "slug": "test-villa",
            "title": "Test Luxury Villa",
            "price": 500000.0,
            "currency": "USD",
            "status": "for-sale",
            "property_type": "Villa",
            "bedrooms": 4,
            "bathrooms": 3.0,
            "sqft": 3200,
            "address": "10 Ocean View St",
            "city": "Lagos",
            "state": "Lagos",
            "country": "Nigeria",
            "description": "Lovely villa with sea view",
            "image_url": "/assets/image/hero-house.png",
            "features": "Pool, Garden",
            "is_featured": True
        }
        res = await ac.post("/api/properties", json=prop_payload)
        assert res.status_code == 201
        created = res.json()
        assert created["id"] is not None
        assert created["title"] == "Test Luxury Villa"

        # List properties with filter
        list_res = await ac.get("/api/properties?status=for-sale")
        assert list_res.status_code == 200
        props = list_res.json()
        assert len(props) >= 1

        # Fetch by slug
        get_res = await ac.get("/api/properties/test-villa")
        assert get_res.status_code == 200
        assert get_res.json()["slug"] == "test-villa"

@pytest.mark.anyio
async def test_submit_contact_inquiry():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        inquiry_payload = {
            "email": "visitor@example.com",
            "full_name": "Jane Doe",
            "phone": "+2348012345678",
            "message": "I am interested in scheduling an inspection.",
            "inquiry_type": "general"
        }
        res = await ac.post("/api/inquiries", json=inquiry_payload)
        assert res.status_code == 201
        data = res.json()
        assert data["email"] == "visitor@example.com"
        assert data["id"] is not None

        # Invalid email validation check
        bad_payload = {"email": "not-an-email"}
        bad_res = await ac.post("/api/inquiries", json=bad_payload)
        assert bad_res.status_code == 422
