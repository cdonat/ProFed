# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.components.api.storage.actor import storage


async def resolve_actor(username: str):
    act_storage = await storage()
    return await act_storage.fetch(username)
