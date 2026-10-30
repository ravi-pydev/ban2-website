-- Work history (About Me page timeline) and its bullet points.
-- Source today: EXPERIENCE in homepage/content.py.

CREATE TABLE IF NOT EXISTS experience (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id   INT UNSIGNED      NOT NULL,
    job_title    VARCHAR(100)      NOT NULL,
    company      VARCHAR(150)      NOT NULL,
    location     VARCHAR(100)      NULL,
    start_date   DATE              NOT NULL,
    end_date     DATE              NULL COMMENT 'NULL = current role',
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    created_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_experience_profile_start (profile_id, start_date),
    CONSTRAINT chk_experience_dates CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT fk_experience_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS experience_points (
    id             INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    experience_id  INT UNSIGNED      NOT NULL,
    point          VARCHAR(500)      NOT NULL,
    sort_order     SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    KEY ix_experience_points_experience (experience_id, sort_order),
    CONSTRAINT fk_experience_points_experience
        FOREIGN KEY (experience_id) REFERENCES experience (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
