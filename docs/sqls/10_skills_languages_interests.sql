-- About Me page: highlights, skills, languages and interests.
-- Source today: HIGHLIGHTS, SKILLS, LANGUAGES and INTERESTS in homepage/content.py.

-- Awards and achievements.
CREATE TABLE IF NOT EXISTS highlights (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id   INT UNSIGNED      NOT NULL,
    title        VARCHAR(150)      NOT NULL,
    description  VARCHAR(500)      NULL,
    icon         VARCHAR(30)       NULL,
    achieved_on  DATE              NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    KEY ix_highlights_profile (profile_id, sort_order),
    CONSTRAINT fk_highlights_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS skills (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id   INT UNSIGNED      NOT NULL,
    name         VARCHAR(60)       NOT NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_skills_profile_name (profile_id, name),
    CONSTRAINT fk_skills_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS languages (
    id            INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id    INT UNSIGNED      NOT NULL,
    name          VARCHAR(50)       NOT NULL,
    proficiency   VARCHAR(60)       NOT NULL COMMENT 'e.g. Full professional proficiency',
    level_percent TINYINT UNSIGNED  NOT NULL DEFAULT 100 COMMENT 'Width of the level bar',
    sort_order    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_languages_profile_name (profile_id, name),
    CONSTRAINT chk_languages_level CHECK (level_percent BETWEEN 0 AND 100),
    CONSTRAINT fk_languages_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS interests (
    id           INT UNSIGNED      NOT NULL AUTO_INCREMENT,
    profile_id   INT UNSIGNED      NOT NULL,
    name         VARCHAR(60)       NOT NULL,
    sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_interests_profile_name (profile_id, name),
    CONSTRAINT fk_interests_profile
        FOREIGN KEY (profile_id) REFERENCES profile (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
