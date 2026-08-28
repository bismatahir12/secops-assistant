from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.system import System
from app.models.user import User
from app.schemas.system import SystemCreate, SystemRead

router = APIRouter(prefix="/systems", tags=["systems"])


@router.post("", response_model=SystemRead, status_code=201)
async def connect_system(
    payload: SystemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> System:
    system = System(
        owner_id=current_user.id,
        name=payload.name,
        system_type=payload.system_type,
    )
    db.add(system)
    await db.commit()
    await db.refresh(system)
    return system


@router.get("", response_model=list[SystemRead])
async def list_systems(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[System]:
    result = await db.execute(select(System).where(System.owner_id == current_user.id))
    return list(result.scalars().all())
