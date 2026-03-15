# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.core.config import config
from profed.components.api.storage import webfinger_storage


def domain() -> str:
    return config().get("api", {}).get("domain", "example.com")


def acct_from_username(username: str) -> str:
    return f"{username}@{domain()}"


def actor_url_from_username(username: str) -> str:
    return f"https://{domain()}/actors/{username}"


def username_from_acct(acct: str) -> str:
    return acct.split("@", 1)[0]


async def resolve_actor_url(acct: str):
    username = username_from_acct(acct)
    wfs = await webfinger_storage()
    if await wfs.user_exists(username):
        return actor_url_from_username(username)
    return None



