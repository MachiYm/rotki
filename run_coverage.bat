@echo off
REM Skript na spustenie testov s coverage
REM Pouzitie: run_coverage.bat

echo ================================
echo   COVERAGE MEASUREMENT  
echo ================================
echo.

python -m pytest -k "auto_login" --cov=rotkehlchen.db.settings --cov=rotkehlchen.db.dbhandler --cov-report=term-missing --cov-report=html -q

echo.
echo ================================
echo   HTML Report: htmlcov\index.html
echo ================================
