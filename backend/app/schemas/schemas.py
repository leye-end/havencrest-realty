from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ----------------- PROPERTY SCHEMAS -----------------
class PropertyBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    slug: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    currency: str = "USD"
    status: str = Field(..., pattern="^(for-sale|for-rent|sold)$")
    property_type: Optional[str] = "Residential"
    bedrooms: int = Field(0, ge=0)
    bathrooms: float = Field(0.0, ge=0)
    sqft: int = Field(0, ge=0)
    address: str = Field(..., min_length=3)
    city: str = Field(..., min_length=2)
    state: Optional[str] = None
    country: str = "Nigeria"
    description: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[str] = None
    is_featured: bool = False

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    sqft: Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[str] = None
    is_featured: Optional[bool] = None

class PropertyResponse(PropertyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ----------------- CONTACT INQUIRY SCHEMAS -----------------
class ContactInquiryCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=50)
    property_id: Optional[int] = None
    message: Optional[str] = Field(None, max_length=2000)
    inquiry_type: Optional[str] = Field("general", pattern="^(general|newsletter|tour)$")

class ContactInquiryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    property_id: Optional[int]
    message: Optional[str]
    inquiry_type: str
    created_at: datetime


# ----------------- TESTIMONIAL SCHEMAS -----------------
class TestimonialBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    location: str = Field(..., min_length=2, max_length=150)
    quote: str = Field(..., min_length=5)
    image_url: Optional[str] = None
    is_active: bool = True

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialResponse(TestimonialBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
