from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from backend.app.core.config import settings
from backend.app.core.database import engine, Base, AsyncSessionLocal
from backend.app.models.models import Property, Testimonial
from backend.app.routers import properties, inquiries, testimonials

# Initial seed data matching the frontend templates
INITIAL_PROPERTIES = [
    {
        "slug": "serene-haven-villa",
        "title": "Serene Haven Villa",
        "price": 850000.0,
        "currency": "USD",
        "status": "for-sale",
        "property_type": "Villa",
        "bedrooms": 4,
        "bathrooms": 3.5,
        "sqft": 3800,
        "address": "12 Banana Island Road",
        "city": "Ikoyi, Lagos",
        "state": "Lagos",
        "country": "Nigeria",
        "description": "Nestled in an exclusive neighborhood, Serene Haven Villa offers an exquisite blend of contemporary luxury and tranquil living.",
        "image_url": "/assets/image/hero-house.png",
        "features": "Private Swimming Pool, Landscaped Garden, Smart Home Automation, 24/7 Security, 2-Car Garage",
        "is_featured": True
    },
    {
        "slug": "crestview-residence",
        "title": "Crestview Residence",
        "price": 420000.0,
        "currency": "USD",
        "status": "for-sale",
        "property_type": "Contemporary Home",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "sqft": 2600,
        "address": "45 Lekki Phase 1",
        "city": "Lekki, Lagos",
        "state": "Lagos",
        "country": "Nigeria",
        "description": "A stunning contemporary home designed with light-filled spaces, high ceilings, and premium European finishes throughout.",
        "image_url": "/assets/image/house card 2.jpg",
        "features": "Gourmet Kitchen, Rooftop Terrace, Backup Solar Power, High Ceilings, CCTV System",
        "is_featured": True
    },
    {
        "slug": "aurora-heights-estate",
        "title": "Aurora Heights Estate",
        "price": 1200000.0,
        "currency": "USD",
        "status": "for-rent",
        "property_type": "Penthouse / Estate",
        "bedrooms": 5,
        "bathrooms": 5.0,
        "sqft": 5200,
        "address": "8 Diplomatic Zone, Maitama",
        "city": "Abuja",
        "state": "FCT",
        "country": "Nigeria",
        "description": "The pinnacle of grand living, Aurora Heights Estate features expansive entertaining grounds and panoramic skyline views.",
        "image_url": "/assets/image/house card 3.jpg",
        "features": "Infinity Pool, Private Cinema, Elevator Access, Wine Cellar, Staff Quarters",
        "is_featured": True
    }
]

INITIAL_TESTIMONIALS = [
    {
        "name": "Oyinlola Israel",
        "location": "Lagos State",
        "quote": "Havencrest Realty truly cares about its clients. They took the time to understand my needs and guided me toward finding the perfect home in Lagos.",
        "image_url": "/assets/image/israel.jpg",
        "is_active": True
    },
    {
        "name": "Ayinde Fawaz",
        "location": "Ogun State",
        "quote": "I had an exceptional experience working with Havencrest Realty. Their expertise and personalized service exceeded my expectations.",
        "image_url": "/assets/image/fawaz.png",
        "is_active": True
    },
    {
        "name": "Adesanya Hubert",
        "location": "Abuja",
        "quote": "Havencrest Realty turned my dream of homeownership into reality. Their dedicated team guided me through every step.",
        "image_url": "/assets/image/hubert.png",
        "is_active": True
    }
]

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Check if properties exist
        prop_count = await session.execute(select(Property))
        if not prop_count.scalars().first():
            for p in INITIAL_PROPERTIES:
                session.add(Property(**p))
            await session.commit()

        # Check if testimonials exist
        test_count = await session.execute(select(Testimonial))
        if not test_count.scalars().first():
            for t in INITIAL_TESTIMONIALS:
                session.add(Testimonial(**t))
            await session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()
    yield
    # Teardown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(properties.router, prefix=settings.API_V1_PREFIX)
app.include_router(inquiries.router, prefix=settings.API_V1_PREFIX)
app.include_router(testimonials.router, prefix=settings.API_V1_PREFIX)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Mount static files from havencrest-realty frontend
frontend_dir = Path(__file__).resolve().parent.parent.parent / "havencrest-realty"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
