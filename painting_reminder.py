# -*- coding: utf-8 -*-
import sys
import os
import time
import random
import threading
import subprocess
import urllib.request
import tempfile
import shutil
import pygame
from pygame.locals import *
import win32api
import win32con
import win32gui
from PIL import Image, ImageDraw
import pystray

# 防止乱码处理
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

# 程序版本号
CURRENT_VERSION = "1.1.0"
UPDATE_URL = "https://raw.githubusercontent.com/wang1145/hell_painting_reminder/main/version.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/wang1145/hell_painting_reminder/main/painting_reminder.py"

# 地狱式吐槽语录
HELL_PHRASES = [
    "宁就是带艺术家？画得跟屎一样！",
    "就这？我奶奶闭着眼都画得比你好！",
    "宁这水平也敢自称画师？笑死！",
    "15分钟画了个寂寞？宁在摸鱼吧！",
    "画成这样也好意思发出来？",
    "宁这画技是胎教水平吧？",
    "我上我也行，不行我倒立吃屎！",
    "宁这画的是毕加索的棺材板？",
    "建议宁转行，别侮辱艺术了！",
    "宁的画让我的眼睛流产了！",
    "这画值5毛，不能再多了！",
    "宁的画技和宁的颜值一样感人！",
    "宁是抽象派？不，是抽风派！",
    "宁的画让我想起了我家的马桶圈！",
    "宁这水平也好意思接稿？",
    "建议宁去工地，那里需要宁的抽象！",
    "宁的画让蒙娜丽莎笑成了蒙娜丽哭！",
    "宁的画技和宁的人生一样失败！",
    "宁的画是视觉污染！建议销毁！",
    "宁的画让我想自戳双目！",
    "宁就是传说中的灵魂画手？灵魂出窍那种！",
    "宁的画让梵高想把自己的耳朵再割一次！",
    "宁的画技和宁的智商一样令人捉急！",
    "宁的画是当代艺术？当代垃圾吧！",
    "宁的画让我想起了我家的狗抓板！",
    "建议宁把画笔吃了，别祸害艺术了！",
    "宁的画是精神污染！建议隔离！",
    "宁的画让达芬奇在棺材里仰卧起坐！",
    "宁的画技和宁的发际线一样后退！",
    "宁的画是行为艺术？不，是自残艺术！"
]

# 全局变量
is_active = True
start_time = time.time()
pause_time = 0
timer_thread = None
update_available = False
clock_window = None  # 电子钟窗口


def create_cat_clock():
    """创建猫形电子钟窗口并置顶"""
    global clock_window

    # 创建电子钟窗口
    pygame.init()
    clock = pygame.display.set_mode((200, 250))
    pygame.display.set_caption(f"地狱猫钟 v{CURRENT_VERSION}")

    # 设置窗口位置（右上角）
    hwnd = pygame.display.get_wm_info()["window"]
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          screen_width - 220, 50, 200, 250, 0)

    # 设置窗口样式
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                           win32con.WS_EX_LAYERED)

    clock_window = clock
    return clock, hwnd


def draw_cat_clock(screen, current_time):
    """绘制猫形电子钟"""
    # 清屏
    screen.fill((255, 240, 240))  # 浅粉色背景

    # 绘制猫脸
    pygame.draw.circle(screen, (240, 200, 180), (100, 100), 80)  # 猫脸

    # 绘制猫耳朵
    pygame.draw.polygon(screen, (240, 200, 180), [(60, 40), (40, 20), (80, 30)])  # 左耳
    pygame.draw.polygon(screen, (240, 200, 180), [(140, 40), (160, 20), (120, 30)])  # 右耳

    # 绘制猫眼睛
    pygame.draw.circle(screen, (80, 80, 160), (70, 90), 15)  # 左眼
    pygame.draw.circle(screen, (80, 80, 160), (130, 90), 15)  # 右眼
    pygame.draw.circle(screen, (0, 0, 0), (70, 90), 7)  # 左眼珠
    pygame.draw.circle(screen, (0, 0, 0), (130, 90), 7)  # 右眼珠

    # 绘制猫鼻子
    pygame.draw.polygon(screen, (255, 150, 150), [(100, 110), (90, 120), (110, 120)])  # 鼻子

    # 绘制猫嘴
    pygame.draw.arc(screen, (0, 0, 0), (85, 120, 30, 30), 0, 3.14, 2)  # 微笑

    # 绘制猫胡须
    pygame.draw.line(screen, (0, 0, 0), (60, 110), (30, 100), 1)  # 左上
    pygame.draw.line(screen, (0, 0, 0), (60, 120), (30, 120), 1)  # 左中
    pygame.draw.line(screen, (0, 0, 0), (60, 130), (30, 140), 1)  # 左下
    pygame.draw.line(screen, (0, 0, 0), (140, 110), (170, 100), 1)  # 右上
    pygame.draw.line(screen, (0, 0, 0), (140, 120), (170, 120), 1)  # 右中
    pygame.draw.line(screen, (0, 0, 0), (140, 130), (170, 140), 1)  # 右下

    # 绘制猫身体
    pygame.draw.ellipse(screen, (240, 200, 180), (50, 150, 100, 80))  # 身体

    # 绘制时间显示
    font_large = pygame.font.SysFont('simhei', 24)
    time_text = font_large.render(current_time, True, (80, 30, 30))
    screen.blit(time_text, (100 - time_text.get_width() // 2, 180))

    # 绘制日期
    current_date = time.strftime("%Y-%m-%d")
    font_small = pygame.font.SysFont('simhei', 16)
    date_text = font_small.render(current_date, True, (100, 100, 100))
    screen.blit(date_text, (100 - date_text.get_width() // 2, 210))

    pygame.display.flip()


def create_window():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption(f"地狱绘画提醒器 v{CURRENT_VERSION}")

    # 设置窗口图标
    pygame.display.set_icon(pygame.Surface((1, 1)))

    # 创建透明背景
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # 设置窗口样式为无边框
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                           win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)

    # 设置窗口透明
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    return screen, hwnd


def show_hell_reminder():
    global is_active

    # 计算绘画时间
    elapsed = time.time() - start_time - pause_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)

    # 随机选择地狱语录
    hell_phrase = random.choice(HELL_PHRASES)

    # 创建弹窗
    pygame.init()
    reminder = pygame.display.set_mode((550, 300))
    pygame.display.set_caption(f"地狱提醒 v{CURRENT_VERSION}")

    # 设置弹窗位置（右上角）
    hwnd = pygame.display.get_wm_info()["window"]
    screen_width = win32api.GetSystemMetrics(0)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          screen_width - 570, 20, 550, 300, 0)

    # 加载字体
    try:
        font_large = pygame.font.SysFont('simhei', 28)
        font_medium = pygame.font.SysFont('simhei', 24)
        font_small = pygame.font.SysFont('simhei', 20)
    except:
        # 如果字体加载失败使用默认字体
        font_large = pygame.font.Font(None, 28)
        font_medium = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)

    # 渲染文本
    title = font_large.render("地狱绘画时间提醒", True, (200, 30, 30))
    time_text = font_medium.render(f"当前时间: {time.strftime('%H:%M')}", True, (50, 50, 50))
    duration_text = font_medium.render(f"已绘画: {hours}小时{minutes}分钟", True, (50, 50, 50))
    phrase_text = font_medium.render(hell_phrase, True, (180, 30, 30))
    continue_text = font_small.render("继续创作吧！带艺术家！", True, (30, 100, 30))

    # 绘制界面
    reminder.fill((255, 240, 240))  # 浅红色背景
    pygame.draw.rect(reminder, (220, 180, 180), (0, 0, 550, 60))  # 标题栏

    # 添加文本到界面
    reminder.blit(title, (160, 15))
    reminder.blit(time_text, (50, 90))
    reminder.blit(duration_text, (50, 130))
    reminder.blit(phrase_text, (50, 170))
    reminder.blit(continue_text, (50, 250))

    # 添加地狱图标
    pygame.draw.circle(reminder, (200, 30, 30), (470, 180), 30)  # 红色圆圈
    pygame.draw.line(reminder, (100, 30, 30), (470, 150), (470, 210), 4)  # 恶魔叉
    pygame.draw.line(reminder, (100, 30, 30), (460, 160), (480, 200), 4)
    pygame.draw.line(reminder, (100, 30, 30), (480, 160), (460, 200), 4)

    pygame.display.flip()

    # 显示弹窗10秒
    start = time.time()
    while time.time() - start < 10 and is_active:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        time.sleep(0.1)

    pygame.quit()


def check_for_updates():
    """检查地狱级更新"""
    global update_available

    try:
        with urllib.request.urlopen(UPDATE_URL) as response:
            latest_version = response.read().decode('utf-8').strip()

            if latest_version != CURRENT_VERSION:
                print(f"[地狱通知] 发现新版本: {latest_version} (宁还在用老掉牙的 {CURRENT_VERSION})")
                update_available = True
                return True
    except Exception as e:
        print(f"[地狱嘲讽] 检查更新失败: {e} 宁的网络是被狗吃了吗？")

    return False


def perform_hell_update():
    """执行地狱级更新"""
    print("[地狱提示] 开始更新程序...新增骂人词库！")

    try:
        # 下载最新版脚本
        with urllib.request.urlopen(SCRIPT_URL) as response:
            script_content = response.read().decode('utf-8')

            # 保存到临时文件
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, "hell_reminder_temp.py")

            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 替换当前文件
            current_path = os.path.abspath(__file__)
            shutil.move(temp_path, current_path)

            print("[地狱欢呼] 更新成功！骂人词汇量+50%！")
            return True
    except Exception as e:
        print(f"[地狱暴怒] 更新失败: {e} 宁的电脑是废铁吗？")
        return False


def hell_reminder_loop():
    global is_active, pause_time, start_time

    last_pause_time = 0
    while True:
        if is_active:
            if last_pause_time > 0:
                pause_time += time.time() - last_pause_time
                last_pause_time = 0

            # 每15分钟提醒一次
            time.sleep(900)
            if is_active:
                show_hell_reminder()
        else:
            if last_pause_time == 0:
                last_pause_time = time.time()
            time.sleep(1)


def create_hell_tray_icon():
    def tray_thread():
        # 创建地狱图标
        image = Image.new('RGB', (64, 64), (200, 30, 30))  # 地狱红
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill=(150, 30, 30))
        dc.line([32, 20, 32, 46], fill=(100, 30, 30), width=3)
        dc.line([20, 33, 44, 33], fill=(100, 30, 30), width=3)

        def on_clicked(icon, item):
            global is_active, update_available

            if str(item) == "暂停吐槽(让宁喘口气)":
                is_active = False
                icon.notify("吐槽已暂停", "珍惜这段宁静时光吧菜鸟！")
            elif str(item) == "继续吐槽(找喷模式)":
                is_active = True
                icon.notify("吐槽继续", "准备好接受下一轮暴击吧！")
            elif str(item) == "检查更新(看看宁多落后)":
                if check_for_updates():
                    icon.notify("发现新版本！", "本次更新：\n- 骂人词汇量+50%\n- 新增祖安词库")
                else:
                    icon.notify("宁已是最新版", "继续享受毒舌待遇吧！")
            elif str(item) == "执行更新(跟上时代)":
                if perform_hell_update():
                    icon.stop()
                    pygame.quit()
                    os.execv(sys.executable, ['python'] + sys.argv)
            elif str(item) == "地狱卸载(彻底跑路)":
                icon.stop()
                pygame.quit()
                subprocess.Popen("hell_uninstaller.bat", shell=True)
                sys.exit()

        # 创建地狱菜单
        menu_items = [
            pystray.MenuItem("继续吐槽(找喷模式)" if not is_active else "暂停吐槽(让宁喘口气)", on_clicked),
            pystray.MenuItem("检查更新(看看宁多落后)", on_clicked),
            pystray.MenuItem("执行更新(跟上时代)", on_clicked) if update_available else None,
            pystray.MenuItem("地狱卸载(彻底跑路)", on_clicked)
        ]

        # 过滤掉None值
        menu_items = [item for item in menu_items if item is not None]

        menu = pystray.Menu(*menu_items)

        icon = pystray.Icon("hell_painting_reminder", image, f"地狱提醒器 v{CURRENT_VERSION}", menu)
        icon.run()

    threading.Thread(target=tray_thread, daemon=True).start()


def clock_update_loop():
    """电子钟更新线程"""
    clock_screen, clock_hwnd = create_cat_clock()

    while True:
        # 获取当前北京时间
        beijing_time = time.strftime("%H:%M:%S")

        # 绘制猫形电子钟
        draw_cat_clock(clock_screen, beijing_time)

        # 每秒更新一次
        time.sleep(1)


def main():
    global timer_thread

    # 启动时检查更新
    check_for_updates()

    # 创建隐藏主窗口
    screen, hwnd = create_window()

    # 创建系统托盘图标
    create_hell_tray_icon()

    # 启动提醒线程
    timer_thread = threading.Thread(target=hell_reminder_loop, daemon=True)
    timer_thread.start()

    # 启动电子钟线程
    clock_thread = threading.Thread(target=clock_update_loop, daemon=True)
    clock_thread.start()

    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        time.sleep(0.1)


if __name__ == "__main__":
    # 首次启动显示地狱欢迎语
    print("╔══════════════════════════════════════════════════╗")
    print("║          地狱绘画时间提醒器 v1.1.0 已启动         ║")
    print("║  新增功能：猫形电子钟（置顶显示）               ║")
    print("║  温馨提示：本程序包含高强度地狱式吐槽             ║")
    print("║  坚持使用可获得成就【脸皮比城墙厚】               ║")
    print("╚══════════════════════════════════════════════════╝")
    main()