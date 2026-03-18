# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any
from .activity_streams import ActivityStreamsObject


class OrderedCollectionBase(ActivityStreamsObject):
    orderedItems: list[dict[str, Any]] = []


class OrderedCollection(OrderedCollectionBase):
    type: str = "OrderedCollection"
    totalItems: int


class OrderedCollectionPage(OrderedCollectionBase):
    type: str = "OrderedCollectionPage"
    partOf: str
    next: str | None = None
    prev: str | None = None

