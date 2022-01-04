
from fastapi import APIRouter
from typing import List

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from .. import database, models,schemas, hashing

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=hashing.Hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      details=f'No user found with id {id}')
    return user