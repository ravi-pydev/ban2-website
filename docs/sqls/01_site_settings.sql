-- Site-wide settings. Holds a single row (id = 1).
-- Source today: SITE_NAME and WHATSAPP_NUMBER in homepage/content.py,
-- ENQUIRY_EMAIL_TO in .env.

CREATE TABLE IF NOT EXISTS site_settings (
    id                TINYINT UNSIGNED NOT NULL DEFAULT 1,
    site_name         VARCHAR(100)     NOT NULL,
    tagline           VARCHAR(200)     NULL,
    whatsapp_number   VARCHAR(20)      NOT NULL COMMENT 'Country code + number, digits only, e.g. 919412833444',
    enquiry_email     VARCHAR(254)     NOT NULL COMMENT 'Inbox that receives enquiry emails',
    service_area      VARCHAR(150)     NULL,
    created_at        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT chk_site_settings_single_row CHECK (id = 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
