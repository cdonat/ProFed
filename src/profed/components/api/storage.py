# Copyright (C) 2026 Christof Donat
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Dict
import asyncpg


class _webfinger_storage:
    def __init__(self, pool: asyncpg.Pool, schema_name: str):
        self._pool = pool
        self._schema_name = schema_name

    async def ensure_table(self) -> None:
        await (await self._pool.acquire()).execute(f"""
                                                   CREATE TABLE IF NOT EXISTS {self._schema_name}.webfinger_users (
                                                       acct TEXT PRIMARY KEY,
                                                       actor_url TEXT NOT NULL
                                                   )
                                                   """)

    async def fetch_actor_url(self, acct: str) -> str | None:
        row = await (await self._pool.acquire()).fetchrow(f"""
                                                          SELECT actor_url
                                                          FROM {self._schema_name}.webfinbger_users
                                                          WHERE ACCT = $1
                                                          """,
                                                          acct)
        return row["actor_url"] if row else None


    async def add(self, acct: str, actor_url: str) -> None:
        await (await self._pool.acquire()).execute(f"""
                                                   INSERT INTO {self._schema_name}.webfinger_users (acct, actor_url)
                                                   VALUES ($1, $2)
                                                   ON CONFLICT (acct) DO NOTHING
                                                   """,
                                                   acct,
                                                   actor_url)

    async def update(self, acct: str, actor_url: str) -> None:
        await (await self._pool.acquire()).execute(f"""
                                                   UPDATE {self._schema_name}.webfinger_users
                                                   SET actor_url = $2
                                                   WHERE acct = $1
                                                   """,
                                                   acct,
                                                   actor_url)

    async def delete(self, acct: str, _) -> None:
        await (await self._pool.acquire()).execute(f"""
                                                   DELETE FROM {self._schema_name}.webfinger_users
                                                   WHERE acct = $1
                                                   """,
                                                   acct)


_instance: _webfinger_storage | None = None


async def init_webfinger_storage(component_name: str, config: Dict[str, str]) -> None:
    global _instance
    pool = await asyncpg.create_pool(host=config["host"],
                                     port=int(config["port"]),
                                     database=config["database"],
                                     user=config["user"],
                                     password=config["password"],)
    _instance = _webfinger_storage(pool, component_name)


async def webfinger_storage() -> _webfinger_storage:
    if _instance is None:
        raise RuntimeError("Webfinger Storage is not initialized.")
    return _instance
