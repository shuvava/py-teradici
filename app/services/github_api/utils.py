# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Vladimir Shurygin.  All rights reserved.
#
from datetime import datetime
from typing import Optional, Dict

ISO8601 = '%Y-%m-%dT%H:%M:%S%z'


def parse_dt(dt: Optional[str], dt_format: Optional[str] = None) -> Optional[datetime]:
    if not dt:
        return None
    try:
        return datetime.strptime(dt, dt_format or ISO8601)
    except:
        return None


def dt_to_str(dt: datetime) -> str:
    return dt.strftime(ISO8601)


def get_dict(item: Dict, name: str) -> Dict:
    if item is None:
        return {}
    _prop = item.get(name, {})
    if _prop is None:
        return {}
    return _prop

