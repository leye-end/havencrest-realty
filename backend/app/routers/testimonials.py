from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.core.database import get_db
from backend.app.models.models import Testimonial
from backend.app.schemas.schemas import TestimonialCreate, TestimonialResponse

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])

@router.get("", response_model=list[TestimonialResponse])
async def list_testimonials(db: AsyncSession = Depends(get_db)):
    query = select(Testimonial).where(Testimonial.is_active == True).order_by(Testimonial.id.asc())
    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def create_testimonial(test_in: TestimonialCreate, db: AsyncSession = Depends(get_db)):
    testimonial = Testimonial(**test_in.model_dump())
    db.add(testimonial)
    await db.commit()
    await db.refresh(testimonial)
    return testimonial
