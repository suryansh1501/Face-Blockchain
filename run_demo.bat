@echo off
call .venv\Scripts\activate
python -m src.pipeline --image data\input.jpg
pause
