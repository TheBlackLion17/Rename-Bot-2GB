# Rename-Bot-2GB: MySQL VPS migration

This is an **in-progress migration**, not yet a production-ready replacement.
The original MongoDB handlers must be inventoried and rewritten before switching the runtime.

## Ubuntu 24.04 setup
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server ffmpeg git
sudo systemctl enable --now mysql
git clone -b development/mysql-vps https://github.com/TheBlackLion17/Rename-Bot-2GB.git
cd Rename-Bot-2GB
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install aiomysql==0.2.0
```

## Database initialization
```bash
sudo mysql < sql/schema.sql
sudo mysql
```
Inside MySQL (replace password with a unique strong value):
```sql
CREATE USER 'renamer_app'@'localhost' IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE ON renamer_bot.* TO 'renamer_app'@'localhost';
```

## Credentials
Do not reuse the API hash, bot token, or MongoDB credentials committed to the original config.py.
Rotate them before deploying. Use environment variables and protect the environment file
with chmod 600. Avoid publishing logs containing credentials.

## Current implementation status
- MySQL schema: added
- Async MySQL connection module: added
- Existing MongoDB plugin handlers: NOT YET migrated
- Runtime switched to MySQL: NO
- File renaming regression tests: NOT YET run
- Production systemd service: NOT YET enabled

Do not run the original bot with old hardcoded secrets. Do not remove MongoDB or delete
existing user records until data migration and feature parity are verified.
