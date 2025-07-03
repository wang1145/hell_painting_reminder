@echo off
title 绘画时间提醒器-地狱安装版
color 0A
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║            地狱级绘画时间提醒器安装程序            ║
echo ║        警告：本程序包含高强度嘴臭提示！           ║
echo ║  玻璃心创作者请自备钛合金脸皮或联系心理医生！    ║
echo ╚══════════════════════════════════════════════════╝
echo.

:: 检查Python是否安装
echo [地狱检测] 正在检查宁的电脑有没有装Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【致命警告】连Python都没装？宁是在用脚画画吗？      ║
    echo ║ 2023年了还有人电脑不装Python？宁是山顶洞人吗？    ║
    echo ║ >>> 拯救传送门：https://www.python.org/downloads/ ║
    echo ╚══════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set python_version=%%a
echo [阴阳怪气] 哟~ Python %python_version% 居然装好了？太阳从西边出来了？
echo.

:: 下载主程序
echo [地狱下载] 正在从阴间服务器拖程序...
curl -O "https://raw.githubusercontent.com/yourusername/hell_painting_reminder/main/painting_reminder.py" --silent
if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【灵魂拷问】下载失败！宁的网络是被甲方拔线了吗？   ║
    echo ║ 尝试用备胎镜像...                                ║
    echo ╚══════════════════════════════════════════════════╝
    curl -O "http://backup.hellserver.com/hell_painting_reminder/painting_reminder.py"
)

:: 下载版本文件
curl -O "https://raw.githubusercontent.com/yourusername/hell_painting_reminder/main/version.txt" --silent

:: 创建卸载脚本
echo @echo off > uninstall.bat
echo echo 正在自爆卸载地狱提醒器... >> uninstall.bat
echo del painting_reminder.py >> uninstall.bat
echo del version.txt >> uninstall.bat
echo del hell_installer.bat >> uninstall.bat
echo echo 程序已卸载！宁的电脑终于清净了！ >> uninstall.bat
echo pause >> uninstall.bat

:: 安装依赖
echo.
echo [地狱提示] 准备安装依赖库，宁的电脑是土豆发电的吗？
echo 如果卡住建议给宁的破网烧柱香...
echo.
python -m pip install pygame pystray pillow pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple/

if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════╗
    echo ║ 【终极侮辱】依赖安装失败！宁的电脑是废铁吗？       ║
    echo ║ 手动执行：pip install pygame pystray pillow pywin32 ║
    echo ╚══════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

:: 启动程序
echo.
echo [地狱通知] 安装完成！准备接受灵魂暴击吧！
echo 温馨提示：本程序对玻璃心创作者具有致死量伤害
echo 坚持使用30天可获得成就【脸皮比画布还厚】
echo.
timeout /t 3 /nobreak >nul
start python painting_reminder.py