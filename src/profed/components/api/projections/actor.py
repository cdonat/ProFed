# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.core.message_bus import message_bus
from profed.components.api.storage.actor import storage


last_seen = 0


async def _unknown_message_type(_1, _2):
    pass


async def handle_user_events() -> None:
    global last_seen

    act_storage = await storage()

    async for event in message_bus().topic("users").subscribe(last_seen):
        event_type = event.get("type")
        data = event["payload"]

        await {"created": act_storage.add,
               "updated": act_storage.update,
               "deleted": act_storage.delete}.get(
                       event_type,
                       _unknown_message_type)(
                               data["username"],
                               data)


async def rebuild() -> None:
    global last_seen

    act_storage = await storage()
    await act_storage.ensure_table()
    
    last_seen, users = message_bus().topic("users").last_snapshot()
    for u in users:
        await act_storage.add(u["username"], u)


