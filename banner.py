#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Banner Module
"""
# =====================================================================
#                           Import Dependencies
# =====================================================================

import os
import psutil
import platform

# =====================================================================
#                           ANSI Color Codes
# =====================================================================

class colors:
    reset = '\033[0m'
    bright = '\033[1m'
    dim = '\033[2m'
    
    # Foreground colors
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    
    # Background colors
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'
    bg_blue = '\033[44m'
    bg_magenta = '\033[45m'
    bg_cyan = '\033[46m'
    bg_white = '\033[47m'
    
    # RGB colors - gradient (from #005faf to #00ff00)
    # Adjusted middle colors for better visibility
    rgb1 = '\033[38;2;0;95;175m'    # #005faf - deep blue
    rgb2 = '\033[38;2;0;150;150m'   # #009696 - cyan (more visible)
    rgb3 = '\033[38;2;0;200;80m'    # #00c850 - cyan-green (more visible)
    rgb4 = '\033[38;2;0;255;0m'     # #00ff00 - bright green

# =====================================================================
#                           Utility Functions
# =====================================================================

def format_bytes(bytes_value):
    """Format byte size"""
    if bytes_value == 0:
        return '0 B'
    
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    temp = bytes_value
    
    while temp >= k and i < len(sizes) - 1:
        temp /= k
        i += 1
    
    return f"{temp:.2f} {sizes[i]}"

def create_progress_bar(percentage, length=50):
    """Create progress bar"""
    filled = round((percentage / 100) * length)
    empty = length - filled
    
    # Use dark gray as background color, visible on dark backgrounds
    bg_color = '\033[38;2;80;80;80m'  # #505050 - more visible gray
    
    # Use ━ character instead of = to avoid ligatures
    return colors.rgb4 + '━' * filled + bg_color + '━' * empty + colors.reset

def apply_horizontal_gradient(lines):
    """Apply horizontal gradient - each vertical column uses same color"""
    # Find maximum line length
    max_len = max(len(line) for line in lines)
    
    # Define color thresholds and corresponding colors
    color_map = [
        (0.25, colors.rgb1),
        (0.50, colors.rgb2),
        (0.75, colors.rgb3),
        (1.00, colors.rgb4)
    ]
    
    # Build output line by line
    result = []
    for line in lines:
        colored_line = ''
        for i in range(len(line)):
            # Calculate which color this column should use
            progress = i / max_len
            
            # Find appropriate color based on progress
            color = next(c for threshold, c in color_map if progress < threshold)
            colored_line += color + line[i]
        
        result.append(colored_line + colors.reset)
    
    return result

# =====================================================================
#                           Banner Display Functions
# =====================================================================

def show_banner(bot_info=None):
    """Display startup banner"""
    if bot_info is None:
        bot_info = {}
    
    # Discord Bot ASCII art - standard font (most concise)
    ascii_lines = [
        '  ____  _                       _   ____        _   ',
        ' |  _ \\(_)___  ___ ___  _ __ __| | | __ )  ___ | |_ ',
        ' | | | | / __|/ __/ _ \\| \'__/ _` | |  _ \\ / _ \\| __|',
        ' | |_| | \\__ \\ (_| (_) | | | (_| | | |_) | (_) | |_ ',
        ' |____/|_|___/\\___\\___/|_|  \\__,_| |____/ \\___/ \\__|'
    ]
    
    # Apply horizontal gradient
    gradient_lines = apply_horizontal_gradient(ascii_lines)
    
    print()
    for line in gradient_lines:
        print(line)
    print(f"  {colors.white}Revolutionary Free Hosting      {colors.yellow}POWERED BY{colors.reset} {colors.rgb4}Python{colors.reset}")
    print()
    
    # Bot basic information
    print(f"{colors.cyan}{colors.bright}=[ Basic account info ]={colors.reset}")
    if bot_info.get('username'):
        print(f"      Username: {colors.green}{bot_info['username']}{colors.reset}")
        print(f"        Bot ID: {colors.green}{bot_info['id']}{colors.reset}")
        print(f"       Servers: {colors.green}{bot_info.get('servers', 0)}{colors.reset}")
        print(f"        Prefix: {colors.green}{bot_info.get('prefix', '!')}{colors.reset}")
    print()
    
    # Resource usage
    mem = psutil.virtual_memory()
    total_mem = mem.total
    free_mem = mem.free
    used_mem = total_mem - free_mem
    mem_percentage = ((used_mem / total_mem) * 100)
    mem_used = format_bytes(used_mem)
    mem_total = format_bytes(total_mem)
    
    print(f"{colors.cyan}{colors.bright}=[ Limits ]={colors.reset}")
    print(f"        Memory: [{create_progress_bar(mem_percentage)}] {mem_percentage:.2f}% ({mem_used}/{mem_total})")
    
    # CPU progress bar - use same gray background as memory
    cpu_cores = psutil.cpu_count()
    cpu_bar_length = 50
    cpu_filled = min(cpu_cores, cpu_bar_length)
    cpu_empty = max(cpu_bar_length - cpu_cores, 0)
    bg_color = '\033[38;2;80;80;80m'  # #505050 - more visible gray
    cpu_bar = colors.rgb4 + '━' * cpu_filled + bg_color + '━' * cpu_empty + colors.reset
    
    print(f"     CPU Cores: [{cpu_bar}] {cpu_cores} cores")
    print(f"        Python: {colors.green}{platform.python_version()}{colors.reset}")
    print(f"      Platform: {colors.green}{platform.system()} {platform.machine()}{colors.reset}")
    print()
    
    # Status
    print(f"{colors.cyan}{colors.bright}=[ Status ]={colors.reset}")
    print(f"    Bot is {colors.green}{colors.bright}ONLINE{colors.reset} and ready to serve!")
    print(f"    Type {colors.cyan}{bot_info.get('prefix', '!')}help{colors.reset} in Discord to see available commands.")
    print()
    
    # Support information
    print(f"{colors.cyan}{colors.bright}=[ Support ]={colors.reset}")
    print(f"    Looking for help? Documentation is available.")
    print(f"    Still have questions? Fast free support available on Discord.")
    print()

# =====================================================================
#                           Message Display Functions
# =====================================================================

def show_simple_banner(message):
    """Display simple startup message"""
    print(f"{colors.cyan}{colors.bright}[INFO]{colors.reset} {message}")

def show_success(message):
    """Display success message"""
    print(f"{colors.rgb4}{colors.bright}[SUCCESS]{colors.reset} {message}")

def show_error(message):
    """Display error message"""
    print(f"{colors.red}{colors.bright}[ERROR]{colors.reset} {message}")

def show_warning(message):
    """Display warning message"""
    print(f"{colors.yellow}{colors.bright}[WARNING]{colors.reset} {message}")

# =====================================================================
#                           Test Code
# =====================================================================

if __name__ == '__main__':
    # Test banner display
    test_bot_info = {
        'username': 'TestBot#1234',
        'id': '123456789012345678',
        'servers': 5,
        'prefix': '!'
    }
    show_banner(test_bot_info)
    
    # Test other messages
    show_simple_banner("This is an info message")
    show_success("Operation completed successfully")
    show_warning("This is a warning")
    show_error("This is an error message")
