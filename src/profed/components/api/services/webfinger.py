# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from profed.components.api.storage import webfinger_storage


async def resolve_actor_url(acct: str):
    wfs = await webfinger_storage()
    return await wfs.fetch_actor_url(acct)

