CREATE DATABASE IF NOT EXISTS renamer_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE renamer_bot;
CREATE TABLE IF NOT EXISTS users (
 telegram_id BIGINT PRIMARY KEY,
 username VARCHAR(255),
 first_name VARCHAR(255),
 joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS user_settings (
 telegram_id BIGINT PRIMARY KEY,
 caption TEXT,
 prefix VARCHAR(255),
 suffix VARCHAR(255),
 thumbnail_file_id TEXT,
 metadata BOOLEAN NOT NULL DEFAULT FALSE,
 metadata_code TEXT,
 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS rename_jobs (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 telegram_id BIGINT NOT NULL,
 source_file_id TEXT,
 original_name VARCHAR(1024),
 output_name VARCHAR(1024),
 status ENUM('queued','processing','completed','failed') NOT NULL DEFAULT 'queued',
 error_message TEXT,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 completed_at TIMESTAMP NULL,
 INDEX idx_user_status (telegram_id, status),
 FOREIGN KEY (telegram_id) REFERENCES users(telegram_id) ON DELETE CASCADE
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS bot_settings (
 setting_key VARCHAR(100) PRIMARY KEY,
 setting_value TEXT
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS broadcasts (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 admin_id BIGINT NOT NULL,
 status VARCHAR(30) NOT NULL DEFAULT 'queued',
 sent_count INT NOT NULL DEFAULT 0,
 failed_count INT NOT NULL DEFAULT 0,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS banned_users (telegram_id BIGINT PRIMARY KEY, banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB;
