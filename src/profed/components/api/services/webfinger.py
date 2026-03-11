# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.components.api.storage import webfinger_storage


async def resolve_webfinger(acct: str):
    actor_url = (await webfinger_storage()).fetch_actor_url(acct)

    return ({"subject": f"acct:{acct}",
             "links": [{"rel": "self",
                        "type": "application/activity+json",
                        "href": actor_url}]}
            if actor_url is not None else None)

