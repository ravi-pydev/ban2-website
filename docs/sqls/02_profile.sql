-- The person behind the business (About Me page, profile card, contact details).
-- Source today: PROFILE in homepage/content.py.

CREATE TABLE IF NOT EXISTS profile (
    id              INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    full_name       VARCHAR(100)  NOT NULL,
    job_title       VARCHAR(100)  NOT NULL,
    current_company VARCHAR(150)  NULL,
    summary         TEXT          NULL,
    email           VARCHAR(254)  NOT NULL,
    phone           VARCHAR(20)   NULL,
    location        VARCHAR(100)  NULL,
    date_of_birth   DATE          NULL,
    photo           VARCHAR(255)  NULL COMMENT 'Image file name or URL',
    show_dob        BOOLEAN       NOT NULL DEFAULT TRUE,
    show_phone      BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_profile_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
