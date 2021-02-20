#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
import uvicorn

from app.server import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8080, log_level="info", reload=True)
