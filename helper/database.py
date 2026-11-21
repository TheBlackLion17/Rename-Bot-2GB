"""MySQL-only replacement for the legacy MongoDB user settings API."""
from mysql_store import execute, fetch_one, fetch_all
from .utils import send_log

class Database:
    async def _ensure(self, user_id):
        uid = int(user_id)
        await execute("INSERT IGNORE INTO users (telegram_id) VALUES (%s)", (uid,))
        await execute("INSERT IGNORE INTO user_settings (telegram_id) VALUES (%s)", (uid,))

    async def add_user(self, bot, message):
        user = message.from_user
        exists = await self.is_user_exist(user.id)
        await self._ensure(user.id)
        await execute("UPDATE users SET username=%s, first_name=%s WHERE telegram_id=%s",
                      (user.username, user.first_name, user.id))
        if not exists:
            await send_log(bot, user)

    async def is_user_exist(self, user_id):
        return bool(await fetch_one("SELECT telegram_id FROM users WHERE telegram_id=%s", (int(user_id),)))

    async def total_users_count(self):
        row = await fetch_one("SELECT COUNT(*) AS count FROM users")
        return row["count"]

    async def get_all_users(self):
        # Preserve the legacy async-iterator interface used by broadcast handlers.
        rows = await fetch_all("SELECT telegram_id AS _id FROM users")
        async def iterator():
            for row in rows:
                yield row
        return iterator()

    async def delete_user(self, user_id):
        await execute("DELETE FROM users WHERE telegram_id=%s", (int(user_id),))

    async def _set(self, user_id, column, value):
        allowed = {"thumbnail_file_id", "caption", "prefix", "suffix", "metadata", "metadata_code"}
        if column not in allowed:
            raise ValueError("Unsupported settings field")
        await self._ensure(user_id)
        await execute(f"UPDATE user_settings SET {column}=%s WHERE telegram_id=%s", (value, int(user_id)))

    async def _get(self, user_id, column):
        allowed = {"thumbnail_file_id", "caption", "prefix", "suffix", "metadata", "metadata_code"}
        if column not in allowed:
            raise ValueError("Unsupported settings field")
        row = await fetch_one(f"SELECT {column} FROM user_settings WHERE telegram_id=%s", (int(user_id),))
        return row[column] if row else None

    async def set_thumbnail(self, id, file_id): await self._set(id, "thumbnail_file_id", file_id)
    async def get_thumbnail(self, id): return await self._get(id, "thumbnail_file_id")
    async def set_caption(self, id, caption): await self._set(id, "caption", caption)
    async def get_caption(self, id): return await self._get(id, "caption")
    async def set_prefix(self, id, prefix): await self._set(id, "prefix", prefix)
    async def get_prefix(self, id): return await self._get(id, "prefix")
    async def set_suffix(self, id, suffix): await self._set(id, "suffix", suffix)
    async def get_suffix(self, id): return await self._get(id, "suffix")
    async def set_metadata(self, id, bool_meta): await self._set(id, "metadata", bool(bool_meta))
    async def get_metadata(self, id): return await self._get(id, "metadata")
    async def set_metadata_code(self, id, metadata_code): await self._set(id, "metadata_code", metadata_code)
    async def get_metadata_code(self, id): return await self._get(id, "metadata_code")

    async def ban_user(self, user_id):
        if await self.is_banned(user_id): return False
        await execute("INSERT INTO banned_users (telegram_id) VALUES (%s)", (int(user_id),))
        return True

    async def is_banned(self, user_id):
        return bool(await fetch_one("SELECT telegram_id FROM banned_users WHERE telegram_id=%s", (int(user_id),)))

    async def is_unbanned(self, user_id):
        if not await self.is_banned(user_id): return False
        await execute("DELETE FROM banned_users WHERE telegram_id=%s", (int(user_id),))
        return True

jishubotz = Database()
