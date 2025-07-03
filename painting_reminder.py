import sys
import os
import time
import random
import threading
import subprocess
import urllib.request
import tempfile
import shutil
from datetime import datetime
import pygame
from pygame.locals import *
import win32api
import win32con
import win32gui
from PIL import Image, ImageDraw
import pystray

# 程序版本号
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/yourusername/hell_painting_reminder/main/version.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/yourusername/hell_painting_reminder/main/painting_reminder.py"

# 地狱笑话风格语句库 (50句)
HELL_PHRASES = [
    "画布在哭泣，宁的小目标完成了吗？颜料都干啦！",
    "宁的手是装饰品吗？15分钟就画了这点？",
    "艺术之神在注视，宁在摸鱼对吧？",
    "颜料怪兽饿了，快喂它新作品！别饿死它！",
    "调色盘想知道：宁今天画了个寂寞？",
    "毕加索托梦说：宁这速度，棺材板都盖上了还没画完？",
    "达芬奇点赞：宁确定这是艺术不是行为艺术？",
    "梵高耳朵痛：宁画得比割耳朵还痛苦？",
    "莫奈的睡莲都开了，宁画完没？睡莲都谢了！",
    "蒙娜丽莎微笑：宁的任务完成？她笑宁天真！",
    "画笔成精了：主人真棒！棒槌的棒！",
    "颜料在沸腾：继续战斗吗？还是继续摸鱼？",
    "画架快散架了，成果如何？散架的速度比宁画画快！",
    "艺术之魂燃烧：突破极限了？宁的极限是躺平吧！",
    "调色刀威胁：不画就削宁！说到做到！",
    "素描本抗议：页页都要满！不是让宁写满'我不会画'！",
    "水彩说：别让我干涸啊！宁倒是加点水啊！",
    "油画棒打滚：还要玩多久？宁当这是游乐场？",
    "马克笔尖叫：画满这张纸！不是让宁画满请假条！",
    "橡皮擦抱怨：别老用我！宁倒是画对一次啊！",
    "透视原理问：结构准吗？宁确定不是抽象派？",
    "色彩理论喊：搭配美吗？宁确定不是车祸现场？",
    "构图法则催：平衡了吗？宁确定不是故意歪的？",
    "光影精灵问：立体感够吗？宁确定不是纸片人？",
    "速写本撒娇：再画一页嘛~宁忍心拒绝我吗？",
    "创意枯竭？不存在的！宁根本没创意吧！",
    "手速爆表了吗？宁的手速只适合刷短视频吧！",
    "灵感喷泉爆发没？宁的灵感是枯井吧！",
    "艺术之魂附体了？附体的是咸鱼魂吧！",
    "变成绘画机器了吗？宁是生锈的机器吧！",
    "突破舒适圈没？宁的舒适圈是床吧！",
    "超越昨天的自己？昨天的自己也在摸鱼吧！",
    "让作品说话了吗？它说'放我出去'！",
    "惊艳到自己没？被自己的菜惊艳到了吧！",
    "画到忘我境界了？忘我到忘记画画了吧！",
    "触摸到艺术本质了？本质是宁不会画画吧！",
    "感受到创作的快乐了？宁的快乐是收工吧！",
    "榨干所有创意了？宁的创意是真空包装吧！",
    "突破技术瓶颈了？宁的瓶颈是瓶盖吧！",
    "找到个人风格了？宁的风格是'不会画画'吧！",
    "画出灵魂之作了？宁的灵魂在睡觉吧！",
    "让作品有呼吸了？宁确定不是断气了？",
    "注入情感能量了？宁的情感是'想下班'吧！",
    "达到心流状态了？宁的心流流向沙发了吧！",
    "成为更好的艺术家了？更好的躺平艺术家吧！",
    "让世界更美好了？宁确定不是更抽象了？",
    "您的肝还好吗？已连续创作3小时，建议去ICU预约床位",
    "颜料干成撒哈拉了！目标完成没？没完成就继续跪着画！",
    "手不酸吗？该检查进度啦！宁确定不是手残？",
    "创意精灵问：宁超神了吗？超鬼还差不多！",
    "艺术细胞在抗议：还要画多久？宁的细胞想罢工！"
]

# 全局变量
is_active = True
start_time = time.time()
pause_time = 0
timer_thread = None
update_available = False


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

    # 随机选择地狱语句
    hell_phrase = random.choice(HELL_PHRASES)

    # 创建弹窗
    pygame.init()
    reminder = pygame.display.set_mode((500, 300))
    pygame.display.set_caption(f"地狱时间提醒 v{CURRENT_VERSION}")

    # 设置弹窗位置（右上角）
    hwnd = pygame.display.get_wm_info()["window"]
    screen_width = win32api.GetSystemMetrics(0)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          screen_width - 520, 20, 500, 300, 0)

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
    title = font_large.render("地狱绘画时间提醒", True, (150, 30, 30))
    time_text = font_medium.render(f"当前时间: {time.strftime('%H:%M')}", True, (50, 50, 50))
    duration_text = font_medium.render(f"已绘画: {hours}小时{minutes}分钟", True, (50, 50, 50))
    phrase_text = font_medium.render(hell_phrase, True, (180, 30, 30))
    question = font_small.render("宁完成这个小目标了吗？说实话！", True, (100, 30, 30))
    continue_text = font_small.render("继续创作吧！菜鸟艺术家！", True, (30, 100, 30))

    # 绘制界面
    reminder.fill((255, 240, 240))  # 浅红色背景
    pygame.draw.rect(reminder, (220, 180, 180), (0, 0, 500, 60))  # 标题栏

    # 添加文本到界面
    reminder.blit(title, (130, 15))
    reminder.blit(time_text, (50, 90))
    reminder.blit(duration_text, (50, 130))
    reminder.blit(phrase_text, (50, 170))
    reminder.blit(question, (50, 210))
    reminder.blit(continue_text, (50, 250))

    # 添加地狱图标
    pygame.draw.circle(reminder, (200, 30, 30), (420, 180), 30)  # 红色圆圈
    pygame.draw.line(reminder, (100, 30, 30), (420, 150), (420, 210), 4)  # 恶魔叉
    pygame.draw.line(reminder, (100, 30, 30), (410, 160), (430, 200), 4)
    pygame.draw.line(reminder, (100, 30, 30), (430, 160), (410, 200), 4)

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
    print("[地狱提示] 开始更新程序...甲方改需求了！")

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

            print("[地狱欢呼] 更新成功！宁终于跟上时代了！")
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
        image = Image.new('RGB', (64, 64), (150, 30, 30))
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill=(200, 30, 30))
        dc.line([32, 20, 32, 46], fill=(100, 30, 30), width=3)
        dc.line([20, 30, 44, 30], fill=(100, 30, 30), width=3)

        def on_clicked(icon, item):
            global is_active, update_available

            if str(item) == "暂停提醒(让宁喘口气)":
                is_active = False
                icon.notify("提醒已暂停", "珍惜这段宁静时光吧菜鸟！")
            elif str(item) == "继续提醒(找骂模式)":
                is_active = True
                icon.notify("提醒继续", "准备好接受下一轮暴击吧！")
            elif str(item) == "检查更新(看看宁多落后)":
                if check_for_updates():
                    icon.notify("发现新版本！", "本次更新：\n- 骂人词汇量+50%\n- 新增猝死预警功能")
                else:
                    icon.notify("宁已是最新版", "继续享受地狱级待遇吧！")
            elif str(item) == "执行更新(跟上时代)":
                if perform_hell_update():
                    icon.stop()
                    pygame.quit()
                    os.execv(sys.executable, ['python'] + sys.argv)
            elif str(item) == "自爆卸载(彻底跑路)":
                icon.stop()
                pygame.quit()
                subprocess.Popen("uninstall.bat", shell=True)
                sys.exit()

        # 创建地狱菜单
        menu_items = [
            pystray.MenuItem("继续提醒(找骂模式)" if not is_active else "暂停提醒(让宁喘口气)", on_clicked),
            pystray.MenuItem("检查更新(看看宁多落后)", on_clicked),
            pystray.MenuItem("执行更新(跟上时代)", on_clicked) if update_available else None,
            pystray.MenuItem("自爆卸载(彻底跑路)", on_clicked)
        ]

        # 过滤掉None值
        menu_items = [item for item in menu_items if item is not None]

        menu = pystray.Menu(*menu_items)

        icon = pystray.Icon("hell_painting_reminder", image, f"地狱提醒器 v{CURRENT_VERSION}", menu)
        icon.run()

    threading.Thread(target=tray_thread, daemon=True).start()


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
    print("║          地狱级绘画时间提醒器 v1.0.0 已启动        ║")
    print("║  温馨提示：本程序可能对玻璃心造成成吨伤害！        ║")
    print("║  坚持使用可获得成就【脸皮比城墙厚】               ║")
    print("╚══════════════════════════════════════════════════╝")
    main()