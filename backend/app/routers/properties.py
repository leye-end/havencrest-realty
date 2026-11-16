from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.core.database import get_db
from backend.app.models.models import Property
from backend.app.schemas.schemas import PropertyCreate, PropertyUpdate, PropertyResponse

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("", response_model=list[PropertyResponse])
async def list_properties(
    status: Optional[str] = Query(None, description="Filter by status: for-sale, for-rent, sold"),
    city: Optional[str] = Query(None, description="Filter by city"),
    is_featured: Optional[bool] = Query(None, description="Filter featured properties"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_bedrooms: Optional[int] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(Property)
    if status:
        query = query.where(Property.status == status)
    if city:
        query = query.where(func.lower(Property.city) == city.lower())
    if is_featured is not None:
        query = query.where(Property.is_featured == is_featured)
    if min_price is not None:
        query = query.where(Property.price >= min_price)
    if max_price is not None:
        query = query.where(Property.price <= max_price)
    if min_bedrooms is not None:
        query = query.where(Property.bedrooms >= min_bedrooms)

    query = query.offset(skip).limit(limit).order_by(Property.id.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{property_id_or_slug}", response_model=PropertyResponse)
async def get_property(property_id_or_slug: str, db: AsyncSession = Depends(get_db)):
    if property_id_or_slug.isdigit():
        query = select(Property).where(Property.id == int(property_id_or_slug))
    else:
        query = select(Property).where(Property.slug == property_id_or_slug)

    result = await db.execute(query)
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return prop


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(prop_in: PropertyCreate, db: AsyncSession = Depends(get_db)):
    # Check slug uniqueness
    existing = await db.execute(select(Property).where(Property.slug == prop_in.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Property with slug '{prop_in.slug}' already exists."
        )

    new_prop = Property(**prop_in.model_dump())
    db.add(new_prop)
    await db.commit()
    await db.refresh(new_prop)
    return new_prop


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: int, prop_update: PropertyUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Property).where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    update_data = prop_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(prop, field, val)

    await db.commit()
    await db.refresh(prop)
    return prop


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(property_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Property).where(Property.id == property_id))
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")

    await db.delete(prop)
    await db.commit()
    return None
