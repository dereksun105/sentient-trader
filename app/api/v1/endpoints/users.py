"""
Sentient Trader - 使用者管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.database_models import User
from app.models.schemas import UserResponse, UserPreferencesUpdate


router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me/preferences", response_model=UserResponse)
def update_preferences(payload: UserPreferencesUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.preferences = payload.preferences
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


