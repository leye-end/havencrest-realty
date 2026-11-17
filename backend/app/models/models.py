from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from backend.app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(String(50), nullable=False, index=True)  # for-sale, for-rent, sold
    property_type = Column(String(50), default="Residential") # Villa, Apartment, Penthouse, etc.
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Float, default=0.0)
    sqft = Column(Integer, default=0)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="Nigeria")
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    features = Column(Text, nullable=True)  # JSON or comma-separated list of amenities
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)


class ContactInquiry(Base):
    __tablename__ = "contact_inquiries"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    property_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=True)
    inquiry_type = Column(String(50), default="general")  # newsletter, tour, general
    created_at = Column(DateTime, default=utc_now)


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    quote = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
