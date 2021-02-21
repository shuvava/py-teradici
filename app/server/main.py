# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.openapi.utils import get_openapi

from app.config import load_config, DefaultSectionKeys, ConfigSections
from app.database import DbEngine
from .router import health, users, most_frequent


def custom_openapi(server):
    if server.openapi_schema:
        return server.openapi_schema
    openapi_schema = get_openapi(
        title="GitHubAPI Client App",
        version="0.1.0",
        description="This is GitHubAPI Client App OpenAPI schema",
        routes=server.routes,
    )
    server.openapi_schema = openapi_schema
    return server.openapi_schema


def get_app() -> FastAPI:
    app_settings = load_config()
    title = app_settings[ConfigSections.DEFAULT][DefaultSectionKeys.NAME]
    version = app_settings[ConfigSections.DEFAULT][DefaultSectionKeys.VERSION]
    api_prefix = app_settings[ConfigSections.DEFAULT][DefaultSectionKeys.API_PREFIX]
    conn_string = app_settings[ConfigSections.DEFAULT][DefaultSectionKeys.CACHE_CONNECTION_STRING]
    db = DbEngine(conn_string)

    server = FastAPI(
        title=title,
        version=version,
    )

    server.db = db

    health.router.version = server.version
    health.router.title = server.title
    health.router.db = db
    server.include_router(
        health.router,
    )

    users.router.db = db
    server.include_router(
        users.router,
        #prefix=api_prefix,
    )

    most_frequent.router.db = db
    server.include_router(
        most_frequent.router,
        #prefix=api_prefix,
    )

    logger.info('****************** Starting Server *****************')
    return server


def get_db(server):
    return server.db
