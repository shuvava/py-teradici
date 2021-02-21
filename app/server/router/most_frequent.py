# -*- coding: utf-8 -*-
from sys import exc_info
from datetime import timezone, datetime, date
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.logger import logger

from app.services import get_commit_frequency, parse_dt, CommitFrequency

router = APIRouter()

BASE_URL = 'most-frequent'


@router.get(f'/{BASE_URL}')
async def get_all_users(start: Optional[date] = None, end: Optional[date] = None) -> List[CommitFrequency]:
    try:
        db = router.db

        if start is not None:
            start_dt = datetime.combine(start, datetime.min.time()).replace(tzinfo=timezone.utc)
        else:
            start_dt = parse_dt('2019-06-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)
        if end is not None:
            end_dt = datetime.combine(end, datetime.min.time()).replace(tzinfo=timezone.utc)
        else:
            end_dt = parse_dt('2020-05-01', '%Y-%m-%d').replace(tzinfo=timezone.utc)

        return get_commit_frequency(5, start_dt, end_dt, db=db)
    except:
        logger.error("Unexpected error:", exc_info()[0])
        raise HTTPException(status_code=500, detail='Unexpected error')
