# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict
import asyncpg


class _storage:
    def __init__(self, pool: asyncpg.Pool, schema_name: str):
        self._pool = pool
        self._schema_name = schema_name

    async def ensure_table(self) -> None:
        raise NotImplementedError()

    async def fetch(self, username: str):
        raise NotImplementedError()

    async def add(self, username: str, payload: dict):
        raise NotImplementedError()

    async def update(self, username: str, payload: dict):
        raise NotImplementedError()

    async def delete(self, username: str, _):
        raise NotImplementedError()


_instance: _storage | None = None


async def init(component_name: str, config: Dict[str, str]) -> None:
    global _instance
    pool = await asyncpg.create_pool(host=config["host"],
                                     port=int(config["port"]),
                                     database=config["database"],
                                     user=config["user"],
                                     password=config["password"],)
    _instance = _storage(pool, component_name)


async def storage() -> _storage:
    if _instance is None:
        raise RuntimeError("Webfinger Storage is not initialized.")
    return _instance
