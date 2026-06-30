@echo off
chcp 65001 >nul
echo ========================================
echo  下载 Hermes 桌面端安装包
echo ========================================
echo.

set "DOWNLOAD_URL=https://mirror.ghproxy.com/https://github.com/NVIDIA/hermes-agent/releases/download/v0.16.0/Hermes-Setup.exe"
set "OUTPUT_FILE=%USERPROFILE%\Downloads\Hermes-Setup.exe"

echo 正在从 GitHub 镜像下载 Hermes...
echo 下载地址: %DOWNLOAD_URL%
echo 保存位置: %OUTPUT_FILE%
echo.

curl -L "%DOWNLOAD_URL%" -o "%OUTPUT_FILE%" --progress-bar

if exist "%OUTPUT_FILE%" (
    echo.
    echo ========================================
    echo 下载成功！正在启动安装程序...
    echo ========================================
    start "" "%OUTPUT_FILE%"
) else (
    echo.
    echo ========================================
    echo 下载失败，尝试其他镜像...
    echo ========================================
    set "DOWNLOAD_URL2=https://gh.api.99988866.xyz/https://github.com/NVIDIA/hermes-agent/releases/download/v0.16.0/Hermes-Setup.exe"
    curl -L "%DOWNLOAD_URL2%" -o "%OUTPUT_FILE%" --progress-bar
    
    if exist "%OUTPUT_FILE%" (
        echo.
        echo ========================================
        echo 下载成功！正在启动安装程序...
        echo ========================================
        start "" "%OUTPUT_FILE%"
    ) else (
        echo.
        echo ========================================
        echo 所有镜像都失败了，请手动下载：
        echo https://github.com/NVIDIA/hermes-agent/releases
        echo ========================================
        pause
    )
)
