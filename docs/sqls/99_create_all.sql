-- Creates the database and every table, in dependency order.
-- Run from the project root with the MySQL command-line client:
--   mysql -u root -p < docs/sqls/99_create_all.sql
-- (SOURCE paths are relative to the directory mysql is started from.)

SOURCE docs/sqls/00_create_database.sql;
SOURCE docs/sqls/01_site_settings.sql;
SOURCE docs/sqls/02_profile.sql;
SOURCE docs/sqls/03_services.sql;
SOURCE docs/sqls/04_event_sessions.sql;
SOURCE docs/sqls/05_testimonials.sql;
SOURCE docs/sqls/06_faqs.sql;
SOURCE docs/sqls/07_business_content.sql;
SOURCE docs/sqls/08_experience.sql;
SOURCE docs/sqls/09_education.sql;
SOURCE docs/sqls/10_skills_languages_interests.sql;
SOURCE docs/sqls/11_enquiries.sql;
SOURCE docs/sqls/13_page_sections.sql;
