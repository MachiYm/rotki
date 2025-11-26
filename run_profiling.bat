@echo off
REM Profiling runner - spusti vsetky profiling benchmarky
REM Pouzitie: run_profiling.bat

echo ========================================
echo   ROTKI PROFILING SUITE
echo ========================================
echo.

echo [1/4] Running cProfile on tests...
python -m cProfile -o profile_output.prof -m pytest rotkehlchen\tests\db\test_auto_login_unit.py -q
echo.

echo [2/4] Analyzing profile results...
python analyze_profile.py > profile_analysis.txt
echo   Results saved to: profile_analysis.txt
echo.

echo [3/4] Running Mock vs Fake comparison...
python compare_mock_vs_fake.py
echo.

echo [4/4] Measuring test execution times...
echo.
echo   Original tests (with Mock):
powershell -Command "Measure-Command { python -m pytest rotkehlchen\tests\db\test_auto_login_unit.py -q } | Select-Object -ExpandProperty TotalMilliseconds"
echo.
echo   Optimized tests (with Fake):
powershell -Command "Measure-Command { python -m pytest rotkehlchen\tests\db\test_auto_login_optimized.py -q } | Select-Object -ExpandProperty TotalMilliseconds"
echo.

echo ========================================
echo   PROFILING COMPLETE
echo ========================================
echo.
echo Reports generated:
echo   - PROFILING_REPORT.md (main report)
echo   - profiling_comparison.txt
echo   - profile_analysis.txt
echo.
