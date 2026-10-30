-- Frequently asked questions (home page FAQ).
-- Source today: FAQS in homepage/content.py.

CREATE TABLE IF NOT EXISTS faqs (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    question     VARCHAR(255)      NOT NULL,
    answer       TEXT              NOT NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    is_active    BOOLEAN           NOT NULL DEFAULT TRUE,
    created_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_faqs_active_order (is_active, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
