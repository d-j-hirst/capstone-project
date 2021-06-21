@ECHO Running full sequence for automated tests
:: replace "postgres" with user name and "a" with required password
:: if no password, then remove the following line ("set PGPASSWORD=a")
@set PGPASSWORD=a
:: turn off authorization checks for this run-through
@set CAPSTONE_RBAC_SKIP=1
:: drop and recreate the database ready for the standard dump file to be added
dropdb -U postgres capstone_test_db
createdb -U postgres capstone_test_db
:: restore the database from the local dump file
::  -U flag sets the user
::  --set ON_ERROR_STOP=on ensures that the database creation stops encountering an error
::  --quiet suppresses display of SQL commands
::  -o NUL suppresses
::  -d capstone_test_db < test_db.sql gives the database name and the dump file
psql -U postgres --set ON_ERROR_STOP=on --quiet -o NUL -d capstone_test_db < test_db.sql
:: if any above commands produced an error, don't bother to run tests, instead give a message and exit
:: also, don't echo the if block itself, only the actual commands
@echo off
if %errorlevel% neq 0 (
  @echo on
  ECHO Error in creating and restoring test database, abandoning testing
  exit /b %errorlevel%
)
@echo on
:: If all is successful, actually run the tests
python tests.py
:: turn on authorization checks when subsequently running
@set CAPSTONE_RBAC_SKIP=0