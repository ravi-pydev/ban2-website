-- Smaller home page content blocks.
-- Source today: STATS, WHY_ME, PROCESS and CLIENT_TYPES in homepage/content.py.

-- Key numbers strip, e.g. "50+ MNC events executed".
CREATE TABLE IF NOT EXISTS stats (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    value        VARCHAR(20)       NOT NULL COMMENT 'Display text, e.g. 50+',
    label        VARCHAR(100)      NOT NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    is_active    BOOLEAN           NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- "Why work with me" reasons.
CREATE TABLE IF NOT EXISTS selling_points (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    title        VARCHAR(100)      NOT NULL,
    description  VARCHAR(500)      NOT NULL,
    icon         VARCHAR(30)       NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    is_active    BOOLEAN           NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- "How it works" steps. step_number gives the order shown (01, 02, …).
CREATE TABLE IF NOT EXISTS process_steps (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    step_number  TINYINT UNSIGNED  NOT NULL,
    title        VARCHAR(100)      NOT NULL,
    description  VARCHAR(500)      NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_process_steps_number (step_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Types of clients served (scrolling ribbon and "Trusted by" tags).
CREATE TABLE IF NOT EXISTS client_types (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    name         VARCHAR(100)      NOT NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_client_types_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
