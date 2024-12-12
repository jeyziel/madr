from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Romancist
from madr.schemas import RomancistResponse, RomancistSchema, RomancistListResponse, Message

router = APIRouter(prefix='/romancists', tags=['romancists'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=RomancistResponse
)
def create_romancist(
    romancist: RomancistSchema, session: Session = Depends(get_session)
):
    db_romancist = session.scalar(
        select(Romancist).where((Romancist.nome == romancist.nome))
    )

    if db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Romancist with name {romancist.nome} already exists.',
        )

    romancist = Romancist(**romancist.model_dump())

    session.add(romancist)
    session.commit()
    session.refresh(romancist)

    return romancist


@router.get('/', response_model=RomancistListResponse)
def read_romancists(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    romancists = session.scalars(
        select(Romancist).offset(skip).limit(limit)
    ).all()

    return {'romancists': romancists}


@router.get('/{romancist_id}', response_model=RomancistResponse)
def find_romancist(romancist_id: int, session: Session = Depends(get_session)):
    db_romancist = session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Romancist with id {romancist_id} not found',
        )

    return db_romancist


@router.patch('/{romancist_id}', response_model=RomancistResponse)
def update_romancist(
    romancist_id: int,
    romancist: RomancistSchema,
    session: Session = Depends(get_session),
):
    db_romancist = session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Romancist with id {romancist_id} not found',
        )

    for key, value in romancist.model_dump(exclude_unset=True).items():
        setattr(db_romancist, key, value)

    session.add(db_romancist)
    session.commit()
    session.refresh(db_romancist)

    return db_romancist


@router.delete('/{romancist_id}', response_model=Message)
def delete_romancist(
    romancist_id: int, session: Session = Depends(get_session)
):
    db_romancist = session.scalar(
        select(Romancist).where(Romancist.id == romancist_id)
    )

    if not db_romancist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Romancist with id {romancist_id} not found',
        )

    session.delete(db_romancist)
    session.commit()

    return {'message': 'Romancist has been deleted successfully.'}
