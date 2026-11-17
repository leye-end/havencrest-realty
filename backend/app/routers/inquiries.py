from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.core.database import get_db
from backend.app.models.models import ContactInquiry
from backend.app.schemas.schemas import ContactInquiryCreate, ContactInquiryResponse

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

@router.post("", response_model=ContactInquiryResponse, status_code=status.HTTP_201_CREATED)
async def submit_inquiry(inquiry_in: ContactInquiryCreate, db: AsyncSession = Depends(get_db)):
    inquiry = ContactInquiry(**inquiry_in.model_dump())
    db.add(inquiry)
    await db.commit()
    await db.refresh(inquiry)
    return inquiry

@router.get("", response_model=list[ContactInquiryResponse])
async def list_inquiries(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    query = select(ContactInquiry).offset(skip).limit(limit).order_by(ContactInquiry.id.desc())
    result = await db.execute(query)
    return result.scalars().all()
