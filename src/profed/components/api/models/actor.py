# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later


from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any


class Resume(BaseModel):

    model_config = ConfigDict(extra="allow")

    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    skills: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []


class Actor(BaseModel):

    model_config = ConfigDict(extra="allow")

    context: list = Field(
        default=[
            "https://www.w3.org/ns/activitystreams",
            {
                "profed": "https://profed.social/ns#",
                "resume": "profed:resume"
            }
        ],
        alias="@context"
    )

    id: str
    type: str = "Person"
    preferredUsername: str

    name: Optional[str] = None
    summary: Optional[str] = None

    resume: Optional[Resume] = None

