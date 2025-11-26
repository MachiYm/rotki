# PowerShell skript na spustenie testov s coverage# PowerShell skript na spustenie testov s coverage# Jednoduchý PowerShell skript na spustenie testov s coverage

# Pouzitie: .\run_tests.ps1

# Pouzitie: .\run_tests.ps1# Použitie: .\run_tests.ps1

Write-Host "================================" -ForegroundColor Cyan

Write-Host "  ROTKI AUTO-LOGIN TESTS" -ForegroundColor Cyan

Write-Host "================================" -ForegroundColor Cyan

Write-Host ""Write-Host "================================" -ForegroundColor CyanWrite-Host "=== Spúšťam testy s coverage meraním ===" -ForegroundColor Green



# Spusti len auto_login testy s coverageWrite-Host "  ROTKI AUTO-LOGIN TESTS" -ForegroundColor CyanWrite-Host ""

python -m pytest -k "auto_login" --cov=rotkehlchen.db.settings --cov=rotkehlchen.db.dbhandler --cov=rotkehlchen.api.rest --cov=rotkehlchen.data_migrations.migrations.migration_22 --cov-report=term-missing --cov-report=html -v

Write-Host "================================" -ForegroundColor Cyan

Write-Host ""

Write-Host "================================" -ForegroundColor GreenWrite-Host ""# Spustenie len auto_login testov s coverage

Write-Host "  HTML Report: htmlcov\index.html" -ForegroundColor Green

Write-Host "================================" -ForegroundColor Greenpython -m pytest `


# Spusti len auto_login testy s coverage    -k "auto_login" `

python -m pytest -k "auto_login" `    --cov=rotkehlchen.db.settings `

    --cov=rotkehlchen.db.settings `    --cov=rotkehlchen.db.dbhandler `

    --cov=rotkehlchen.db.dbhandler `    --cov=rotkehlchen.api.rest `

    --cov=rotkehlchen.api.rest `    --cov=rotkehlchen.data_migrations.migrations.migration_22 `

    --cov=rotkehlchen.data_migrations.migrations.migration_22 `    --cov-report=term `

    --cov-report=term-missing `    -v

    --cov-report=html `

    -vWrite-Host ""

Write-Host "=== Testy dokončené ===" -ForegroundColor Green

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  HTML Report: htmlcov\index.html" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
