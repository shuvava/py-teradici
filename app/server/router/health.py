# -*- coding: utf-8 -*-
import sys

from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from sqlalchemy import text

router = APIRouter()

BASE_URL = 'health'


@router.get(f'/{BASE_URL}/isAlive')
async def get_version():
    ver = router.version
    title = router.title
    return {'title': title, 'version': ver}


@router.get(f'/{BASE_URL}/isReady')
async def check_health():
    db = router.db.get_session()
    try:
        db.execute(text("SELECT 1"))
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        raise HTTPException(status_code=503, detail='db connection error')
    return 'OK'
