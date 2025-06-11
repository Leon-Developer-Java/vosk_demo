@echo off
chcp 65001 >nul
echo ====================================
echo    Vosk 实时语音识别演示程序
echo ====================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

:: 检查是否存在模型文件夹
if not exist "model" (
    echo 未找到模型文件夹，正在启动模型下载程序...
    echo.
    python download_model.py
    echo.
)

:: 检查模型是否下载成功
if not exist "model" (
    echo 模型下载失败或被取消，程序退出
    pause
    exit /b 1
)

:: 运行语音识别程序
echo 启动实时语音识别程序...
echo 按 Ctrl+C 可以停止程序
echo.
python real_time_speech_recognition.py

echo.
echo 程序已结束
pause