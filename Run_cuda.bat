@echo off
setlocal

echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python -m pip install ultralytics opencv-python numpy pillow imageio

echo.
echo Script loading...
python CreateErinEyeTexture.py

echo.
echo Done
pause
