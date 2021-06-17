:: Convenience batch file for creating a dump file from a postgres database
:: the standard syntax doesn't work because it creates a file with the incorrect encoding
:: The flags used here ensure that the file has the correct encoding
@echo off
set PGPASSWORD=a
set /p db_name="Enter database name (example: capstone_test_db): "
set /p dest_filename="Enter file name to dump to (example: test_db.sql): "
@echo on
pg_dump -U postgres -E UTF8 -f %dest_filename% %db_name%