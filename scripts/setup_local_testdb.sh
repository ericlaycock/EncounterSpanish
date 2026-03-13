#!/usr/bin/env bash
# Creates the local test database for pytest.
# Run once: bash scripts/setup_local_testdb.sh

set -euo pipefail

DB_USER="test"
DB_PASS="test"
DB_NAME="test_db"

echo "Creating PostgreSQL user '$DB_USER' and database '$DB_NAME'..."

sudo -u postgres psql <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
    CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';
  END IF;
END
\$\$;

SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
SQL

echo "Done. Verify with: PGPASSWORD=test psql -U test -h localhost -d test_db -c 'SELECT 1'"
