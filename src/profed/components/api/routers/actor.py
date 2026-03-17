# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import JSONResponse
from profed.components.api.services.actor import resolve_actor
from profed.components.api.models.actor import Actor


router = APIRouter()


class ActivityPubJSONResponse(JSONResponse):
    media_type = "application/activity+json"


@router.get("/actors/{username}",
            response_model=Actor,
            response_class=ActivityPubJSONResponse)
async def actor(username: str = Path(pattern=r"^[a-zA-Z0-9_.-]+$")):
    try:
        actor = await resolve_actor(username)
        if actor is None:
            raise HTTPException(status_code=404)

        return actor
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)

