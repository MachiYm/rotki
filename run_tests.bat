@echo off
REM Jednoduchy skript na spustenie testov
REM Pouzitie: run_tests.bat

echo ================================
echo   ROTKI AUTO-LOGIN TESTS
echo ================================
echo.

python -m pytest rotkehlchen\tests\db\test_auto_login_unit.py -v

echo.
echo ================================
echo   TESTY DOKONCENE
echo ================================
