-- Page wording blocks: home page hero, intro and call-to-action band.
-- One row per (page, key). Seeded by 12_seed_data.sql.

CREATE TABLE IF NOT EXISTS page_sections (
    id            INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    page          VARCHAR(30)   NOT NULL DEFAULT 'home',
    `key`         VARCHAR(30)   NOT NULL COMMENT 'Which block: hero, intro, cta',
    kicker        VARCHAR(100)  NOT NULL DEFAULT '' COMMENT 'Small label above the heading',
    heading       VARCHAR(200)  NOT NULL,
    body          TEXT          NOT NULL COMMENT 'Paragraphs separated by a blank line',
    items         TEXT          NOT NULL COMMENT 'List items, one per line',
    image         VARCHAR(255)  NOT NULL DEFAULT '',
    button_label  VARCHAR(60)   NOT NULL DEFAULT '',
    is_active     BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_page_sections_page_key (page, `key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
