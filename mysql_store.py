"""Async MySQL persistence for the VPS migration branch.

Requires aiomysql. Use init_pool() at startup and close_pool() at shutdown.
No database credentials are stored in source code.
"""
import os
import aiomysql

_pool = None

async def init_pool():
    global _pool
    if _pool is None:
        _pool = await aiomysql.create_pool(
            host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
            port=int(os.environ.get("MYSQL_PORT", "3306")),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            db=os.environ.get("MYSQL_DATABASE", "renamer_bot"),
            autocommit=True,
            minsize=1,
            maxsize=10,
            charset="utf8mb4",
        )
    return _pool

async def close_pool():
    global _pool
    if _pool is not None:
        _pool.close()
        await _pool.wait_closed()
        _pool = None

async def execute(sql, args=()):
    if _pool is None:
        raise RuntimeError("MySQL pool is not initialized")
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, args)
            return cur.lastrowid

async def fetch_one(sql, args=()):
    if _pool is None:
        raise RuntimeError("MySQL pool is not initialized")
    async with _pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql, args)
            return await cur.fetchone()

async def fetch_all(sql, args=()):
    if _pool is None:
        raise RuntimeError("MySQL pool is not initialized")
    async with _pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql, args)
            return await cur.fetchall()
