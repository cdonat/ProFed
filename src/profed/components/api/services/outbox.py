# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.components.api.models.ordered_collection import OrderedCollection
from profed.components.api.identity import actor_url_from_username


async def resolve_outbox(username: str) -> OrderedCollection:
    return OrderedCollection(
        id=f"{actor_url_from_username(username)}/outbox",
        totalItems=0,
        orderedItems=[],
    )
