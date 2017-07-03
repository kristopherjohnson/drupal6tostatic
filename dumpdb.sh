#!/bin/bash

# Before running this script, substitute your database password for SECRET below.

dbname=drupal6_undefinedvalue
dbuser=drupal6
dbpass=SECRET

echo Dumping table definitions to "$dbname-defs.sql..."
mysqldump --user=$dbuser --password=$dbpass --no-data --routines --events  --databases "$dbname" > "$dbname-defs.sql"

echo Dumping everything to "$dbname.sql..." >&2
mysqldump --user=$dbuser --password=$dbpass --tz-utc --databases "$dbname" > "$dbname.sql"

echo Archiving to "$dbname.zip..." >&2
zip "$dbname.zip" "$dbname-defs.sql" "$dbname.sql"

