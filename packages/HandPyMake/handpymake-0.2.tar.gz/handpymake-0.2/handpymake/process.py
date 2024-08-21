import os
import subprocess
import shutil
import sys
from pathlib import Path
import venv
import platform
import mpremote
import keyboard
import time
import requests

def process_project(config: dict, port: str):
    # 获取当前操作系统平台
    current_platform = platform.system()

    # Step 1: Handle AutoClone
    if config.get('AutoClone', {}).get('enable', False):
        repo_uri = config['AutoClone']['repoUri']
        repo_dir = Path('./runtime/gitProject/')
        
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True)
        
        if repo_uri.endswith('.git'):
            project_name = repo_uri.split('/')[-1].replace('.git', '')
        else:
            project_name = repo_uri.split('/')[-1]
        
        local_repo_path = repo_dir / project_name
        
        # Clone repository if not already cloned
        if not local_repo_path.exists():
            clone_cmd = f'git clone https://{config["AutoClone"]["repoPlatform"]}.com/{repo_uri} {local_repo_path}'
            subprocess.run(clone_cmd, shell=True, check=True)

        # Copy cloned repository to the current working directory
        for item in local_repo_path.iterdir():
            if item.is_dir():
                shutil.copytree(item, item.name, dirs_exist_ok=True)
            else:
                shutil.copy(item, item.name)

    # Step 2: Create and activate virtual environment
    venv_dir = Path('./venv')
    if not venv_dir.exists():
        venv.create(venv_dir, with_pip=True)
    
    # 根据平台设置激活脚本路径
    if current_platform == "Windows":
        activate_script = venv_dir / 'Scripts' / 'activate'
        activate_cmd = f'{activate_script} && '
    else:
        activate_script = venv_dir / 'bin' / 'activate'
        activate_cmd = f'source {activate_script} && '

    # Step 3: Install requirements
    requirements_file = config['EntryPoint']['requirements']
    if Path(requirements_file).exists():
        subprocess.run(f'{activate_cmd}{sys.executable} -m pip install -r {requirements_file}', 
                       shell=True, check=True, executable='/bin/bash' if current_platform != "Windows" else None)

    # Step 4: Run build script
    build_script = config['EntryPoint']['build']
    subprocess.run(f'{activate_cmd}{sys.executable} {build_script}', 
                   shell=True, check=True, executable='/bin/bash' if current_platform != "Windows" else None)

    # Step 5: Handle AutoFlash (before AutoInstall)
    if config.get('AutoFlash', {}).get('enable', False):
        # 如果需要先擦除
        if config['AutoFlash'].get('eraseBeforeFlash', False):
            erase_cmd = f"esptool.py --chip esp32 --port {port} erase_flash"
            subprocess.run(erase_cmd, shell=True, check=True)
        
        # 下载固件文件
        flash_file_url = f"{config['AutoFlash']['flashFileServerEndpoint']}{config['AutoFlash']['flashFileServerFilename']}"
        flash_file_path = Path('./firmware.bin')
        response = requests.get(flash_file_url)
        flash_file_path.write_bytes(response.content)
        
        # 替换 flashCommands 里面的占位符并执行命令
        for cmd in config['AutoFlash']['flashCommands']:
            cmd = cmd.replace("{{ port }}", port)
            cmd = cmd.replace("{{ flashFile }}", str(flash_file_path))
            subprocess.run(cmd, shell=True, check=True)

    # Step 6: Handle AutoInstall
    if config.get('AutoInstall', {}).get('enable', False):
        build_output = config['EntryPoint']['buildOouput']
        install_method = config['AutoInstall']['installMethod']

        if install_method == 'mount':
            # 使用 mpremote 挂载 buildOutput 目录
            mount_cmd = f'mpremote mount {build_output}'
            subprocess.run(mount_cmd, shell=True, check=True)
        
        # Step 7: Handle afterMount
        after_mount = config['AutoInstall'].get('afterMount')
        if after_mount:
            time.sleep(0.5)
            # 使用 keyboard 模拟键盘输入
            keyboard.write(after_mount)
            keyboard.press_and_release('enter')

