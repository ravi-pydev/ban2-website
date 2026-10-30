# Database schema (MySQL)

The SQL files in `sqls/` create the Ban2Plans database for MySQL 8.0.16+ and fill it with the site's content. The API (`/api/site/`, `/api/home/`, `/api/about/`) reads all its content from these tables.

## Files (`docs/sqls/`)

| File | Tables | Holds |
|---|---|---|
| `00_create_database.sql` | – | Creates the `ban2plans` database (utf8mb4) |
| `01_site_settings.sql` | `site_settings` | Site name, WhatsApp number, enquiry inbox (single row) |
| `02_profile.sql` | `profile` | Shashi's details for the About page and contact info |
| `03_services.sql` | `services` | Services offered (also the form's event types) |
| `04_event_sessions.sql` | `event_sessions` | Organised events / portfolio gallery |
| `05_testimonials.sql` | `testimonials` | Happy-client quotes (with consent and publish flags) |
| `06_faqs.sql` | `faqs` | FAQ questions and answers |
| `07_business_content.sql` | `stats`, `selling_points`, `process_steps`, `client_types` | Smaller home page blocks |
| `08_experience.sql` | `experience`, `experience_points` | Work history and bullet points |
| `09_education.sql` | `education` | Qualifications |
| `10_skills_languages_interests.sql` | `highlights`, `skills`, `languages`, `interests` | About page lists |
| `11_enquiries.sql` | `enquiries`, `enquiry_followups` | Form submissions and sales follow-up notes |
| `13_page_sections.sql` | `page_sections` | Home page wording: hero, intro (paragraphs and checklist), call-to-action band |
| `12_seed_data.sql` | all content tables | **INSERTs of the current site content.** Clears and refills the content tables, never touches enquiries. Works on SQLite and MySQL |
| `14_dummy_testimonials.sql` | `testimonials` | **Dummy** Happy Clients quotes for previews (shown with a "Sample" badge). Replaces only testimonials without consent. Load with `python manage.py load_seed --file docs/sqls/14_dummy_testimonials.sql` |
| `99_create_all.sql` | – | Runs 00–11 and 13 in order (creates the tables only) |

## How the tables relate

```
services ──< event_sessions ──< testimonials
services ──< enquiries ──< enquiry_followups
profile  ──< experience ──< experience_points
profile  ──< education / highlights / skills / languages / interests
```

`──<` means "one to many". Deleting a service or event keeps the linked rows and sets the link to NULL. Deleting a profile or enquiry also deletes its child rows.

## Usage

From the project root:

```bash
mysql -u root -p < docs/sqls/99_create_all.sql
```

Every statement uses `CREATE … IF NOT EXISTS`, so re-running is safe.

### Loading the content

Load the site content into whichever database Django is using (SQLite or MySQL):

```bash
python manage.py load_seed
```

This runs `docs/sqls/12_seed_data.sql`. Re-running it resets the content to these defaults, overwriting any edits made in admin, so run it once and then edit in `/admin/`. If the content tables are empty, the API returns `503` with a message saying to run this command.

## Relationship to Django

The same tables are defined as Django models in `homepage/models.py` (same table names, columns, foreign keys, indexes and checks). **Normally you create them with:**

```bash
make migrate
```

This works on both SQLite and MySQL, and the tables can be managed in Django admin at `/admin/`.

Use these `.sql` files as readable reference, or to create the schema in MySQL without Django. If you change a table, update `homepage/models.py`, run `makemigrations`, and then update the matching `.sql` file here.

Small differences from the models: Django uses `BIGINT` ids everywhere, and `ENUM` columns are `VARCHAR` with the allowed values enforced by Django.
