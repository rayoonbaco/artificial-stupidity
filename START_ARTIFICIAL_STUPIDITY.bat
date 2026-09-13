@echo off
setlocal
cd /d "%~dp0"
title Artificial Stupidity Gate

where py >nul 2>&1
if not errorlevel 1 (
    set "AS_PYTHON=py -3"
) else (
    where python >nul 2>&1
    if not errorlevel 1 (
        set "AS_PYTHON=python"
    ) else (
        echo.
        echo Python 3 was not found on this computer.
        echo Install Python 3, then run this file again.
        echo https://www.python.org/downloads/windows/
        echo.
        pause
        exit /b 1
    )
)

:menu
cls
echo ============================================================
echo                ARTIFICIAL STUPIDITY GATE
echo ============================================================
echo.
echo This is the independent decision gate for autoresearch.
echo It does not run GPU model training.
echo.
echo   1. Run the complete smoke test
echo   2. Demonstrate KEEP
echo   3. Demonstrate REJECT
echo   4. Demonstrate ESCALATE
echo   5. Compare original rule versus our gate
echo   6. Show the protected-holdout H100 decision
echo   7. Check this computer for GPU benchmark readiness
echo   8. Show the protected H100 rerun command
echo   9. Exit
echo.
choice /c 123456789 /n /m "Choose 1, 2, 3, 4, 5, 6, 7, 8, or 9: "

if errorlevel 9 exit /b 0
if errorlevel 8 goto h100rerun
if errorlevel 7 goto gpucheck
if errorlevel 6 goto realbenchmark
if errorlevel 5 goto compare
if errorlevel 4 goto escalate
if errorlevel 3 goto reject
if errorlevel 2 goto keep
if errorlevel 1 goto tests

:tests
cls
echo Running all gate tests...
echo.
%AS_PYTHON% -m unittest discover -s tests -v
echo.
if errorlevel 1 (
    echo RESULT: TEST FAILURE
) else (
    echo RESULT: ALL TESTS PASSED
)
goto done

:keep
cls
echo Demonstrating a supported improvement...
echo.
%AS_PYTHON% gate\as_gate.py --baseline gate\examples\baseline.json --candidate gate\examples\candidate_keep.json
goto done

:reject
cls
echo Demonstrating a rejected improvement...
echo.
%AS_PYTHON% gate\as_gate.py --baseline gate\examples\baseline.json --candidate gate\examples\candidate_reject.json
goto done

:escalate
cls
echo Demonstrating an improvement that requires human review...
echo.
%AS_PYTHON% gate\as_gate.py --baseline gate\examples\baseline.json --candidate gate\examples\candidate_escalate.json
goto done

:compare
cls
echo Comparing the original acceptance rule with our evidence gate...
echo.
%AS_PYTHON% benchmark\compare_loops.py --manifest benchmark\example_experiments.json --output benchmark\example_report.json
echo.
echo The full report was also saved as benchmark\example_report.json
goto done

:realbenchmark
cls
echo Replaying the protected-holdout H100 evidence through the gate...
echo.
%AS_PYTHON% gate\as_gate.py --baseline benchmark\evidence\h100_sxm_20260913\repaired_decision\baseline_gate_record.json --candidate benchmark\evidence\h100_sxm_20260913\repaired_decision\candidate_gate_record.json
echo.
echo Expected result: ESCALATE only because a named human must authorize KEEP.
echo The empirical validation and protected-holdout boundaries both passed.
echo Final governed decision: KEEP, authorized by Raymond Anthony Gomez on September 13, 2026.
echo Read benchmark\evidence\h100_sxm_20260913\repaired_decision\VERIFIED_RESULT.md.
goto done

:gpucheck
cls
echo Checking this computer for the real autoresearch benchmark...
echo.
where nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo NVIDIA GPU: NOT DETECTED
    echo RESULT: This computer cannot run the original GPU experiment as packaged.
    echo We will need rented NVIDIA hardware or a deliberately adapted fork.
) else (
    echo NVIDIA GPU detected:
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
    echo.
    where git >nul 2>&1
    if errorlevel 1 (echo Git: NOT FOUND) else (echo Git: FOUND)
    where uv >nul 2>&1
    if errorlevel 1 (echo uv: NOT FOUND) else (echo uv: FOUND)
    echo.
    echo Copy or photograph this result and send it to ChatGPT before training.
)
goto done

:h100rerun
cls
echo Protected H100 rerun
echo.
echo On a fresh single-H100 RunPod, upload and extract this complete project.
echo Open its Jupyter terminal, enter the project folder, and run:
echo.
echo     bash RUN_H100_EVIDENCE.sh
echo.
echo When it finishes, download this unmistakably named file before stopping:
echo.
echo     /workspace/ARTIFICIAL_STUPIDITY_H100_EVIDENCE_DOWNLOAD_ME.zip
echo.
echo Full preregistration: benchmark\H100_RERUN_PROTOCOL.md
goto done

:done
echo.
pause
goto menu
