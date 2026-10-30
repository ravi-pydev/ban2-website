-- Successfully organised sessions / events (home page portfolio gallery).
-- Source today: SESSIONS in homepage/content.py (event types only).
-- Extra columns let you record real past events as the portfolio grows.

CREATE TABLE IF NOT EXISTS event_sessions (
    id            INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    service_id    INT UNSIGNED      NULL,
    title         VARCHAR(150)      NOT NULL,
    description   TEXT              NULL,
    image         VARCHAR(255)      NULL,
    client_name   VARCHAR(150)      NULL COMMENT 'Shown only if the client agreed',
    venue         VARCHAR(150)      NULL,
    city          VARCHAR(100)      NULL,
    event_date    DATE              NULL,
    guest_count   INT UNSIGNED      NULL,
    is_featured   BOOLEAN           NOT NULL DEFAULT FALSE,
    is_published  BOOLEAN           NOT NULL DEFAULT TRUE,
    sort_order    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    created_at    DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_event_sessions_published_order (is_published, sort_order),
    KEY ix_event_sessions_event_date (event_date),
    CONSTRAINT fk_event_sessions_service
        FOREIGN KEY (service_id) REFERENCES services (id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
