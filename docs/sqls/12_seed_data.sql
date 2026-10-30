-- =============================================================
-- Event & Experience by Ban2 – seed data: the site's current content.
-- Works on SQLite and MySQL.
--
-- Safe to re-run: it clears and refills the content tables.
-- It never touches enquiries or enquiry_followups.
--
-- Load it with:   python manage.py load_seed
-- (MySQL only:    mysql -u root -p ban2plans < docs/sqls/12_seed_data.sql)
-- =============================================================

-- Clear content tables (children before parents)
DELETE FROM page_sections;
DELETE FROM testimonials;
DELETE FROM event_sessions;
DELETE FROM experience_points;
DELETE FROM experience;
DELETE FROM education;
DELETE FROM highlights;
DELETE FROM skills;
DELETE FROM languages;
DELETE FROM interests;
DELETE FROM faqs;
DELETE FROM stats;
DELETE FROM selling_points;
DELETE FROM process_steps;
DELETE FROM client_types;
DELETE FROM site_settings;
UPDATE enquiries SET service_id = NULL;
DELETE FROM services;
DELETE FROM profile;

-- Site settings (single row)
INSERT INTO site_settings (id, site_name, tagline, whatsapp_number, enquiry_email, service_area, created_at, updated_at) VALUES
    (1, 'Event & Experience by Ban2', 'Hospitality sales & event management', '919050824511', 'ravidarshan95@gmail.com', 'Delhi NCR & across India', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Profile
INSERT INTO profile (id, full_name, job_title, current_company, summary, email, phone, location, date_of_birth, photo, show_dob, show_phone, created_at, updated_at) VALUES
    (1, 'Shashi Darshan', 'Assistant Sales Manager', 'Welcomhotel by ITC Hotels', 'Ability to work under pressure, time management and being target focused are some of the key qualities I have. I believe in smart working and want to keep learning to enhance my knowledge and polish my skills.', 'shashidarshan.999@gmail.com', '', 'Rohtak, India', '1999-05-08', 'profile.jpg', 1, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Services
INSERT INTO services (id, title, slug, description, icon, image, sort_order, is_active, created_at, updated_at) VALUES
    (1, 'Corporate Events & Conferences', 'corporate-events-and-conferences', 'Annual meets, conferences, town halls and product launches — planned end to end, from agenda and seating to AV and catering.', 'mic', 'conference.jpg', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'MICE Planning', 'mice-planning', 'Meetings, incentives, conferences and exhibitions for corporate, government and travel trade groups of any size.', 'globe', 'seminar.jpg', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'Venue Sourcing & Negotiation', 'venue-sourcing-and-negotiation', 'Shortlisting the right hotel or banquet, comparing proposals and negotiating rates, inclusions and contract terms for you.', 'building', 'banquet-hall.jpg', 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (4, 'Gala Dinners & Award Nights', 'gala-dinners-and-award-nights', 'Theme, décor, menu, stage and run-of-show for dinners and recognition evenings your team will remember.', 'glass', 'dinner-setup.jpg', 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (5, 'Offsites & Retreats', 'offsites-and-retreats', 'Leadership offsites and team retreats with room blocks, activities and transfers organised in one plan.', 'sun', 'resort.jpg', 5, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (6, 'Social Celebrations', 'social-celebrations', 'Birthdays, anniversaries and family functions with the same attention to detail as a corporate event.', 'heart', 'celebration.jpg', 6, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Organised sessions (portfolio)
INSERT INTO event_sessions (id, service_id, title, description, image, client_name, venue, city, event_date, guest_count, is_featured, is_published, sort_order, created_at, updated_at) VALUES
    (1, 1, 'Corporate conferences', 'Multi-session conferences for MNC clients with stage, AV and breakout planning.', 'conference.jpg', '', '', '', NULL, NULL, 0, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 4, 'Gala dinners', 'Seated dinners with custom menus, table layouts and décor.', 'dinner-setup.jpg', '', '', '', NULL, NULL, 0, 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 1, 'Workshops & trainings', 'Interactive sessions with the right room set-up and refreshments.', 'workshop.jpg', '', '', '', NULL, NULL, 0, 1, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (4, 2, 'Seminars & keynotes', 'Theatre-style sessions with registration, stage and speaker support.', 'seminar.jpg', '', '', '', NULL, NULL, 0, 1, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (5, 5, 'Team offsites', 'Retreats combining work sessions, leisure and accommodation.', 'retreat.jpg', '', '', '', NULL, NULL, 0, 1, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (6, 1, 'Launches & celebrations', 'High-energy launches and parties with entertainment and stage cues.', 'stage.jpg', '', '', '', NULL, NULL, 0, 1, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Testimonials: PLACEHOLDERS. consent_given = 0 makes the site show a "Sample" badge.
-- Replace with real client feedback and set consent_given = 1.
INSERT INTO testimonials (id, event_session_id, client_name, client_role, company, quote, rating, photo, consent_given, is_published, sort_order, received_on, created_at, updated_at) VALUES
    (1, NULL, 'Client name', 'Designation', 'Company', 'Add a short quote from a happy client here — what the event was and what they valued most about working with Shashi.', 5, '', 0, 1, 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, NULL, 'Client name', 'Designation', 'Company', 'Add a second testimonial here, ideally from a corporate or MICE client, mentioning the size or type of event.', 5, '', 0, 1, 2, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, NULL, 'Client name', 'Designation', 'Company', 'Add a third testimonial here, for example from a social event or offsite, to show the range of events handled.', 5, '', 0, 1, 3, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- FAQs
INSERT INTO faqs (id, question, answer, sort_order, is_active, created_at, updated_at) VALUES
    (1, 'What size of events do you handle?', 'Anything from a 10-person board meeting to large conferences and gala dinners. The planning approach scales with the guest count.', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Which cities do you work in?', 'Mainly Delhi NCR, and I can coordinate events with hotels across India.', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'How early should I get in touch?', 'Four to eight weeks ahead is ideal for corporate events, and earlier for peak wedding and conference season. Shorter timelines are possible.', 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (4, 'Do you only work with one hotel brand?', 'Tell me your requirements and I will recommend the venue options that fit them best.', 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Key numbers
INSERT INTO stats (id, value, label, sort_order, is_active) VALUES
    (1, '4+', 'Years in hospitality', 1, 1),
    (2, '50+', 'MNC events executed', 2, 1),
    (3, '5', 'Events handled in a day', 3, 1),
    (4, '2', 'Associate awards', 4, 1);

-- Why work with me
INSERT INTO selling_points (id, title, description, icon, sort_order, is_active) VALUES
    (1, 'Hotel insider knowledge', 'I have sold and run events from the hotel side, so I know what to ask for.', 'key', 1, 1),
    (2, 'Better rates & terms', 'Proposals, quotations and contract negotiation are my everyday work.', 'rupee', 2, 1),
    (3, 'Calm under pressure', 'Used to handling up to five events in a single day without missing a detail.', 'clock', 3, 1),
    (4, 'Award-winning service', 'Recognised as Associate of the Month and Associate of the Quarter.', 'award', 4, 1);

-- How it works
INSERT INTO process_steps (id, step_number, title, description) VALUES
    (1, 1, 'Consultation', 'We talk through your goals, guest count, dates and budget.'),
    (2, 2, 'Proposal', 'You get venue options, a plan and a transparent cost estimate.'),
    (3, 3, 'Negotiation', 'I secure rates, inclusions and contract terms on your behalf.'),
    (4, 4, 'Execution', 'On the day I coordinate every team so the event runs to plan.'),
    (5, 5, 'Follow-up', 'Final bills are checked and feedback reviewed for next time.');

-- Client types
INSERT INTO client_types (id, name, sort_order) VALUES
    (1, 'Multinational corporates', 1),
    (2, 'Government bodies', 2),
    (3, 'Travel trade partners', 3),
    (4, 'MICE agencies', 4),
    (5, 'Startups & SMEs', 5),
    (6, 'Families & private hosts', 6);

-- Work experience (end_date NULL = current role)
INSERT INTO experience (id, profile_id, job_title, company, location, start_date, end_date, sort_order, created_at, updated_at) VALUES
    (1, 1, 'Assistant Sales Manager', 'Welcomhotel by ITC Hotels', 'Delhi', '2026-04-01', NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 1, 'Sales Executive', 'Welcomhotel by ITC Hotels', 'Delhi', '2025-02-01', '2026-04-01', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 1, 'Event Coordinator', 'Le Méridien Gurgaon', 'Gurugram', '2022-10-01', '2024-12-01', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Experience bullet points
INSERT INTO experience_points (id, experience_id, point, sort_order) VALUES
    (1, 1, 'Identify and develop new corporate, government, travel trade, and MICE accounts', 1),
    (2, 1, 'Prepare proposals, contracts, quotations, and negotiate commercial terms', 2),
    (3, 1, 'Conduct daily sales calls, client meetings, and hotel presentations', 3),
    (4, 1, 'Follow up on enquiries and convert leads into confirmed business', 4),
    (5, 1, 'Coordinate with internal departments for seamless event planning and guest service delivery', 5),
    (6, 1, 'Monitor competitor activities, market trends, and pricing strategies', 6),
    (7, 2, 'Property show rounds and understanding guest requirements', 1),
    (8, 2, 'Venue selling and blocking', 2),
    (9, 2, 'Event documentation', 3),
    (10, 3, 'Executed events for more than 50 MNCs', 1),
    (11, 3, 'Handled more than 5 events in a day', 2),
    (12, 3, 'Understood the requirements of each event', 3),
    (13, 3, 'Awarded "Associate of the Month"', 4),
    (14, 3, 'Awarded "Associate of the Quarter"', 5);

-- Education
INSERT INTO education (id, profile_id, qualification, institution, note, completed_on, sort_order) VALUES
    (1, 1, 'Masters of Hotel Management', 'IHTM, MDU', '', '2022-10-01', 1),
    (2, 1, 'Bachelor of Arts', 'Sh. Lal Nath Hindu College, Rohtak', 'Indian Red Cross Society', '2020-11-01', 2),
    (3, 1, 'Basics of Tally', '', '', '2020-07-01', 3),
    (4, 1, '12th', 'Sh. Baba Mast Nath Public School, Rohtak', 'Merit certificate', '2017-03-01', 4);

-- Highlights / awards
INSERT INTO highlights (id, profile_id, title, description, icon, achieved_on, sort_order) VALUES
    (1, 1, 'Associate of the Month', 'Recognised at Le Méridien Gurgaon for outstanding event delivery.', 'award', NULL, 1),
    (2, 1, 'Associate of the Quarter', 'Awarded for consistent performance across a full quarter.', 'star', NULL, 2),
    (3, 1, '50+ MNC events', 'Planned and executed corporate events for leading multinationals.', 'calendar', NULL, 3),
    (4, 1, 'Corporate & MICE sales', 'Building corporate, government, travel trade and MICE accounts at ITC Hotels.', 'trend', NULL, 4);

-- Skills
INSERT INTO skills (id, profile_id, name, sort_order) VALUES
    (1, 1, 'Leadership', 1),
    (2, 1, 'Public Speaking', 2),
    (3, 1, 'MS Office', 3),
    (4, 1, 'Problem Solving', 4),
    (5, 1, 'Time Management', 5),
    (6, 1, 'Adaptability', 6);

-- Languages
INSERT INTO languages (id, profile_id, name, proficiency, level_percent, sort_order) VALUES
    (1, 1, 'English', 'Full professional proficiency', 85, 1),
    (2, 1, 'Hindi', 'Native or bilingual proficiency', 100, 2);

-- Interests
INSERT INTO interests (id, profile_id, name, sort_order) VALUES
    (1, 1, 'Cooking', 1),
    (2, 1, 'Social work', 2),
    (3, 1, 'Music', 3),
    (4, 1, 'Playing guitar', 4);

-- Home page wording: hero, intro and call-to-action band.
-- body: paragraphs separated by a blank line. items: one per line.
INSERT INTO page_sections (id, page, `key`, kicker, heading, body, items, image, button_label, is_active, created_at, updated_at) VALUES
    (1, 'home', 'hero', '', 'Events that run on time, on budget and on brand.', 'From boardroom meetings to large conferences, I plan, negotiate and deliver corporate and social events with the eye of a hotel insider — so you can focus on your guests while every detail is handled.', '', 'banquet-hall.jpg', 'Plan my event', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'home', 'intro', 'Why hire a hospitality professional', 'A hotel insider on your side of the table', 'I have spent my career inside luxury hotels — first coordinating events at Le Méridien Gurgaon, then selling venues and building corporate accounts at Welcomhotel by ITC Hotels. I know how hotels price, plan and run events, and where the hidden costs and common mistakes are.

That experience means I can find the right venue faster, negotiate fairer terms, and coordinate every department — banquets, kitchen, AV, front office — so your event feels effortless for you and your guests.', 'Venue, menu and AV in one plan
Transparent quotations
One point of contact, start to finish
On-site coordination on the day', 'conference-hall.jpg', 'Read my full story', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'home', 'cta', '', 'Have an event coming up?', 'Share your date and guest count — I will come back with venue options and a clear plan.', '', 'stage.jpg', 'Get a free consultation', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);