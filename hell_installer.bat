@echo off
chcp 65001 > nul
title 地狱绘画时间提醒器安装程序
color 0F
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     汪氏屎山代码工作室 - 地狱绘画时间提醒器安装       ║
echo ║                                                  ║
echo ║  本程序每15分钟提醒绘画时间                       ║
echo ║  包含高强度地狱式吐槽                             ║
echo ╚══════════════════════════════════════════════════╝
echo.
echo [地狱提示] 正在安装灵魂暴击监督程序...

:: 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【地狱警告】连Python都没装？宁是用脚画画的吗？      ║
    echo ║ 2023年了还有人电脑不装Python？山顶洞人？         ║
    echo ║ >>> 立即安装：https://www.python.org/downloads/  ║
    echo ╚══════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set python_version=%%a
echo [系统检测] Python %python_version% 已就绪（算你识相）

:: 下载主程序
echo [地狱下载] 正在获取灵魂暴击核心...
curl -O "https://raw.githubusercontent.com/wang1145/hell_painting_reminder/main/painting_reminder.py" --silent
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【网络嘲讽】下载失败！宁的网线被拔了？             ║
    echo ║ 尝试用祖传备用线路...                            ║
    echo ╚══════════════════════════════════════════════════╝
    curl -O "http://backup.wangstudio.com/hell_painting_reminder/painting_reminder.py"
)

:: 下载版本文件
curl -O "https://raw.githubusercontent.com/wang1145/hell_painting_reminder/main/version.txt" --silent

:: 创建卸载脚本
echo @echo off > hell_uninstaller.bat
echo chcp 65001 > nul >> hell_uninstaller.bat
echo title 地狱提醒器卸载程序 >> hell_uninstaller.bat
echo color 0C >> hell_uninstaller.bat
echo. >> hell_uninstaller.bat
echo echo ╔══════════════════════════════════════════════════╗ >> hell_uninstaller.bat
echo echo ║      汪氏屎山代码工作室 - 地狱提醒器卸载           ║ >> hell_uninstaller.bat
echo echo ║                                                  ║ >> hell_uninstaller.bat
echo echo ║ 【地狱告别】终于受不了了？玻璃心！               ║ >> hell_uninstaller.bat
echo echo ╚══════════════════════════════════════════════════╝ >> hell_uninstaller.bat
echo echo. >> hell_uninstaller.bat
echo echo 正在删除地狱监督程序... >> hell_uninstaller.bat
echo del painting_reminder.py >> hell_uninstaller.bat
echo del version.txt >> hell_uninstaller.bat
echo del hell_installer.bat >> hell_uninstaller.bat
echo echo. >> hell_uninstaller.bat
echo echo 程序已卸载！宁的电脑清净了！ >> hell_uninstaller.bat
echo echo 温馨提示：你的抗压能力已提升100%... >> hell_uninstaller.bat
echo echo. >> hell_uninstaller.bat
echo pause >> hell_uninstaller.bat

:: 安装依赖
echo.
echo [地狱提示] 正在安装灵魂暴击引擎...
echo [毒舌提示] 如果卡住可能是宁的破网该换了...
echo.
python -m pip install pygame pystray pillow pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple/

if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【终极侮辱】依赖安装失败！宁的电脑是土豆发电的？   ║
    echo ║ 手动执行：pip install pygame pystray pillow pywin32 ║
    echo ╚══════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: 启动程序
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║      地狱绘画时间提醒器安装完成！                  ║
echo ║                                                  ║
echo ║  每15分钟收获灵魂暴击                             ║
echo ║  坚持使用可获得成就【脸皮比城墙厚】               ║
echo ╚══════════════════════════════════════════════════╝
echo.
timeout /t 3 /nobreak >nul
start python painting_reminder.py