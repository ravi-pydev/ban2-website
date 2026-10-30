-- Enquiries submitted through the website form (POST /api/enquiries/).
-- Every enquiry is saved here (then emailed), so this table keeps a permanent
-- record and tracks each lead through the sales pipeline.

CREATE TABLE IF NOT EXISTS enquiries (
    id              BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100)      NOT NULL,
    email           VARCHAR(254)      NOT NULL,
    phone           VARCHAR(20)       NULL,
    company         VARCHAR(120)      NULL,
    service_id      INT UNSIGNED      NULL COMMENT 'Matching service, if event_type is one',
    event_type      VARCHAR(120)      NOT NULL COMMENT 'As chosen on the form, kept even if the service is renamed',
    guests          INT UNSIGNED      NULL,
    preferred_date  DATE              NULL,
    event_location  VARCHAR(150)      NOT NULL DEFAULT '' COMMENT 'City or venue where the event will be held',
    message         TEXT              NULL,
    status          ENUM('new', 'contacted', 'proposal_sent', 'won', 'lost', 'spam')
                                      NOT NULL DEFAULT 'new',
    source          VARCHAR(30)       NOT NULL DEFAULT 'website',
    email_sent      BOOLEAN           NOT NULL DEFAULT FALSE COMMENT 'Notification email delivered',
    ip_address      VARCHAR(45)       NULL COMMENT 'IPv4 or IPv6',
    user_agent      VARCHAR(255)      NULL,
    created_at      DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_enquiries_status_created (status, created_at),
    KEY ix_enquiries_email (email),
    KEY ix_enquiries_preferred_date (preferred_date),
    CONSTRAINT chk_enquiries_guests CHECK (guests IS NULL OR guests BETWEEN 1 AND 100000),
    CONSTRAINT fk_enquiries_service
        FOREIGN KEY (service_id) REFERENCES services (id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Follow-up notes on an enquiry: calls, proposals sent, quoted amounts.
CREATE TABLE IF NOT EXISTS enquiry_followups (
    id              BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT,
    enquiry_id      BIGINT UNSIGNED   NOT NULL,
    contact_method  ENUM('call', 'email', 'whatsapp', 'meeting', 'other') NOT NULL,
    note            TEXT              NOT NULL,
    quoted_amount   DECIMAL(12, 2)    NULL COMMENT 'In INR',
    next_action_on  DATE              NULL,
    created_at      DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_enquiry_followups_enquiry (enquiry_id, created_at),
    KEY ix_enquiry_followups_next_action (next_action_on),
    CONSTRAINT chk_enquiry_followups_amount CHECK (quoted_amount IS NULL OR quoted_amount >= 0),
    CONSTRAINT fk_enquiry_followups_enquiry
        FOREIGN KEY (enquiry_id) REFERENCES enquiries (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
