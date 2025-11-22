from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Boat
from auth_routes import get_current_user

router = APIRouter()


class BoatCreate(BaseModel):
    name: str
    registration: str | None = None
    type: str | None = None
    length_m: int | None = None
    home_port: str | None = None


class BoatOut(BaseModel):
    id: int
    name: str
    registration: str | None
    type: str | None
    length_m: int | None
    home_port: str | None

    class Config:
        from_attributes = True


@router.post("/", response_model=BoatOut)
def create_boat(
    boat_in: BoatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Only captains/owners can create boats (you can tighten this later)
    if current_user.role not in ("captain", "owner"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only captains or owners can register boats",
        )

    boat = Boat(
        name=boat_in.name,
        registration=boat_in.registration,
        type=boat_in.type,
        length_m=boat_in.length_m,
        home_port=boat_in.home_port,
        owner_id=current_user.id,
    )
    db.add(boat)
    db.commit()
    db.refresh(boat)
    return boat


@router.get("/my", response_model=list[BoatOut])
def list_my_boats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    boats = (
        db.query(Boat)
        .filter(Boat.owner_id == current_user.id)
        .order_by(Boat.created_at.desc())
        .all()
    )
    return boats
