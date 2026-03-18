# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later


from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from .activity_streams import ActivityStreamsObject

class Resume(BaseModel):

    model_config = ConfigDict(extra="allow")

    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    skills: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []


class Actor(ActivityStreamsObject):
    @classmethod
    def default_context(cls) -> list[str | dict[str, str]]:
        return super().default_context() + [
            {
                "profed": "https://profed.social/ns#",
                "resume": "profed:resume",
            }
        ]

    context: list[str | dict[str, str]] = Field(
        default_factory=lambda: Actor.default_context(),
        alias="@context",
    )

    type: str = "Person"
    preferredUsername: str

    name: Optional[str] = None
    summary: Optional[str] = None

    resume: Optional[Resume] = None

