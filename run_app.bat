@echo off
title ResumeIQ - AI Resume Analyzer
cd /d "%~dp0"
echo ========================================================
echo Starting ResumeIQ...
echo Your browser will automatically open at http://localhost:8501
echo To stop the server anytime, close this window.
echo ========================================================
echo.
python -m streamlit run app.py
pause
