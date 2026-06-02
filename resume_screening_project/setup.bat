@echo off
echo ============================================
echo   AI Resume Screening System - Setup
echo ============================================
echo.

echo [1/4] Creating conda environment (Python 3.10)...
call conda create -n resume_screen python=3.10 -y

echo.
echo [2/4] Activating environment...
call conda activate resume_screen

echo.
echo [3/4] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [4/4] Downloading language models...
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo To generate sample resumes for testing, run:
echo   python create_sample_data.py
echo.
echo To launch the Streamlit app, run:
echo   streamlit run app/app.py
echo.
pause
