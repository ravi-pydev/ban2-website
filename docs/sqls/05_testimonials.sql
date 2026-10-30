-- Happy clients / testimonials (home page "Happy Clients").
-- Source today: TESTIMONIALS in homepage/content.py.
-- Only rows with is_published = TRUE should be shown on the site.
-- Feedback submitted on the website arrives with is_published = FALSE
-- (source = 'website') and is shown only after the owner approves it.

CREATE TABLE IF NOT EXISTS testimonials (
    id               INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    event_session_id INT UNSIGNED      NULL,
    client_name      VARCHAR(100)      NOT NULL,
    client_email     VARCHAR(254)      NOT NULL DEFAULT '' COMMENT 'Reviewer contact, never shown on the site',
    source           VARCHAR(20)       NOT NULL DEFAULT 'admin' COMMENT 'admin = added by the owner, website = submitted through the feedback form',
    client_role      VARCHAR(100)      NULL COMMENT 'Designation',
    company          VARCHAR(150)      NULL,
    quote            TEXT              NOT NULL,
    rating           TINYINT UNSIGNED  NOT NULL DEFAULT 5,
    photo            VARCHAR(255)      NULL,
    consent_given    BOOLEAN           NOT NULL DEFAULT FALSE COMMENT 'Client agreed to be quoted publicly',
    is_published     BOOLEAN           NOT NULL DEFAULT FALSE,
    sort_order       SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    received_on      DATE              NULL,
    created_at       DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_testimonials_published_order (is_published, sort_order),
    KEY ix_testimonials_pub_rating (is_published, rating DESC),
    CONSTRAINT chk_testimonials_rating CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT fk_testimonials_event_session
        FOREIGN KEY (event_session_id) REFERENCES event_sessions (id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
