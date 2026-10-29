from pathlib import Path

from django.conf import settings
from django.db import connection, transaction

SEED_FILE = Path(settings.BASE_DIR) / 'docs' / 'sqls' / '12_seed_data.sql'


def split_statements(sql):
    """Split a .sql file into statements. Statements must end with ';' at the end of a line."""
    lines = [line for line in sql.splitlines() if not line.lstrip().startswith('--')]
    statements = '\n'.join(lines).split(';\n')
    return [s.strip().rstrip(';') for s in statements if s.strip()]


def load_sql_file(path=SEED_FILE):
    """Run every statement in the file inside one transaction. Returns the statement count."""
    statements = split_statements(Path(path).read_text(encoding='utf-8') + '\n')
    with transaction.atomic(), connection.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)
    return len(statements)
