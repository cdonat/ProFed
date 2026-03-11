# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, HTTPException, Query
from profed.components.api.services.webfinger import resolve_webfinger


router = APIRouter()

@router.get("/.well-known/webfinger")
async def webfinger(resource: str = Query(pattern=r"^acct:[^@]+@[^@]+$")):
    result = await resolve_webfinger(resource.split(":")[1])

    if result is None:
        raise HTTPException(status_code=404)

    return result

