-- =============================================================
-- DUMMY testimonials for the home page "Happy Clients" section.
-- For development and design previews only. The names and companies are invented.
--
-- consent_given = 0 makes the site show a "Sample" badge on each card.
-- Replace these with real client feedback (consent_given = 1) before going live.
--
-- Safe to re-run: it only replaces testimonials without consent
-- (placeholders and samples) and never touches real ones.
--
-- Load it with:  python manage.py load_seed --file docs/sqls/14_dummy_testimonials.sql
-- =============================================================

DELETE FROM testimonials WHERE consent_given = 0;

INSERT INTO testimonials (event_session_id, client_name, client_role, company, quote, rating, photo, consent_given, is_published, sort_order, received_on, created_at, updated_at) VALUES
    ((SELECT id FROM event_sessions WHERE title = 'Corporate conferences'), 'Ananya Mehra', 'HR Manager', 'Northwind Technologies', 'Our annual conference for 300 employees ran without a single hiccup. Shashi handled the venue, AV and catering so smoothly that our team could focus entirely on the agenda.', 5, '', 0, 1, 1, '2026-08-14', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ((SELECT id FROM event_sessions WHERE title = 'Gala dinners'), 'Rohit Malhotra', 'Head of Sales', 'Bluepeak Pharma', 'The awards night was the best we have hosted. From the menu to the stage cues, every detail was planned, and he negotiated a much better package than we expected.', 5, '', 0, 1, 2, '2026-07-02', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ((SELECT id FROM event_sessions WHERE title = 'Team offsites'), 'Priyanka Sethi', 'Founder', 'Craftleaf Studio', 'Planning a two-day offsite for a small team felt overwhelming until Shashi stepped in. Rooms, transfers and activities were sorted in one clear plan.', 5, '', 0, 1, 3, '2026-05-21', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ((SELECT id FROM event_sessions WHERE title = 'Seminars & keynotes'), 'Vikram Choudhary', 'Event Lead', 'Horizon MICE Partners', 'Reliable, quick to respond and calm under pressure. When our keynote speaker arrived late, the schedule was re-arranged in minutes without guests noticing.', 4, '', 0, 1, 4, '2026-04-09', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ((SELECT id FROM event_sessions WHERE title = 'Launches & celebrations'), 'Neha Kapoor', 'Marketing Director', 'Zestora Foods', 'Our product launch looked premium and stayed within budget. The hotel insider knowledge really shows in how he works with banquet and kitchen teams.', 5, '', 0, 1, 5, '2026-02-17', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (NULL, 'Sanjay & Meera Arora', 'Private hosts', '', 'We booked Shashi for our 25th anniversary dinner. Thoughtful, organised and genuinely warm. Our family still talks about how relaxed we were on the day.', 5, '', 0, 1, 6, '2025-12-28', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
