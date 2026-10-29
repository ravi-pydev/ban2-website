from django.core.management.base import BaseCommand

from homepage.seed import SEED_FILE, load_sql_file


class Command(BaseCommand):
    help = 'Load the site content from docs/sqls/12_seed_data.sql (clears and refills content tables).'

    def add_arguments(self, parser):
        parser.add_argument('--file', default=str(SEED_FILE), help='SQL file to run')

    def handle(self, *args, **options):
        count = load_sql_file(options['file'])
        self.stdout.write(self.style.SUCCESS(f"Ran {count} statements from {options['file']}"))
