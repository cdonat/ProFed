# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
from profed.core.message_bus import message_bus
from profed.components.api.storage.webfinger import storage


logger = logging.getLogger(__name__)
last_seen = 0

def _ignore_msg(msg):
    return f"Ignoring malformed users event: {msg}"


def _event_type(event):
    if not isinstance(event, dict):
        logger.warning(_ignore_msg(f"event is not a JSON object: {event!r}"))
        return None 

    if "type" not in event:
        logger.warning(_ignore_msg(f"missing event type: {event!r}"))
        return None

    event_type = event["type"]
    if not isinstance(event_type, str):
        logger.warning(_ignore_msg(f"event type is not a string: {event_type!r}"))
        return None
    return event_type


def _payload(event):
    if "payload" not in event:
        logger.warning(_ignore_msg(f"missing payload: {event!r}"))
        return None

    data = event["payload"]

    if not isinstance(data, dict):
        logger.warning(_ignore_msg(f"payload is not a JSON object: {data!r}"))
        return None

    if "username" not in data:
        logger.warning(_ignore_msg(f"username not found in payload: {data!r}"))
        return None

    return data


async def handle_user_events() -> None:
    global last_seen

    wf_storage = await storage() 

    async for event in message_bus().topic("users").subscribe(last_seen):
        event_type = _event_type(event)
        if event_type is None or event_type not in ("created", "deleted"):
            continue

        data = _payload(event)
        if data is None:
            continue

        await {"created": wf_storage.add,
               "deleted": wf_storage.delete}[event_type](data["username"])


async def rebuild() -> None:
    global last_seen

    wf_storage = await storage()
    await wf_storage.ensure_table()
    
    last_seen, users = await message_bus().topic("users").last_snapshot()
    for u in users:
        if "username" in u:
            await wf_storage.add(u["username"])

