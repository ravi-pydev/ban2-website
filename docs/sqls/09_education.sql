-- Education and certifications (About Me page).
-- Source today: EDUCATION in homepage/content.py.

CREATE TABLE IF NOT EXISTS education (
    id              INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id      INT UNSIGNED      NOT NULL,
    qualification   VARCHAR(150)      NOT NULL COMMENT 'e.g. Masters of Hotel Management, 12th',
    institution     VARCHAR(200)      NULL,
    note            VARCHAR(200)      NULL COMMENT 'e.g. Merit certificate',
    completed_on    DATE              NULL COMMENT 'Day is not significant; month and year are shown',
    sort_order      SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    KEY ix_education_profile (profile_id, completed_on),
    CONSTRAINT fk_education_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
