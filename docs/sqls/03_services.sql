-- Services offered (home page "Services" cards and the enquiry form's event types).
-- Source today: SERVICES in homepage/content.py.

CREATE TABLE IF NOT EXISTS services (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    title        VARCHAR(120)      NOT NULL,
    slug         VARCHAR(120)      NOT NULL,
    description  TEXT              NOT NULL,
    icon         VARCHAR(30)       NULL COMMENT 'Icon name used by the frontend, e.g. mic, globe',
    image        VARCHAR(255)      NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    is_active    BOOLEAN           NOT NULL DEFAULT TRUE,
    created_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_services_slug (slug),
    KEY ix_services_active_order (is_active, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
