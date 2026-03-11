# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.core.message_bus import message_bus
from profed.components.api.storage import webfinger_storage


last_seen = 0

async def webfinger_handle_user_events() -> None:
    global last_seen

    wf_storage = await webfinger_storage() 

    async for event in message_bus().topic("users").subscribe():
        event_type = event.get("type")
        data = event["payload"]

        await {"Created": wf_storage.add,
               "Deleted": wf_storage.delete,
               "Update":  wf_storage.update}[event_type](data["acct"],
                                                         data.get("actor_url", None))


async def rebuild_webfinger_projection() -> None:
    global last_seen

    wf_storage = await webfinger_storage()
    wf_storage.ensure_table()
    
    last_seen, users = message_bus().topic("users").last_snapshot()
    for u in users:
        wf_storage.add(u["acct"], u["actor_url"])

