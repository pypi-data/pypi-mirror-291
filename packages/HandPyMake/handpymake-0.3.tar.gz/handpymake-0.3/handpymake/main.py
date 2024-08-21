import toml
import os.path
import serial.tools.list_ports  # 用于检测串口
import logging  # 用于记录日志

from .process import process_project

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def checkMakeFile():
    if os.path.isfile('hpymake.toml'):
        logging.info('Checking hpymake.toml exists... Success')
    else:
        logging.error('Cannot find hpymake.toml')
        raise RuntimeError('Cannot find hpymake.toml')

def loadMakeFile():
    checkMakeFile()
    
    with open('hpymake.toml') as f:
        logging.info('Loading hpymake.toml')
        return toml.load(f)

def validateStructure(data):
    required_structure = {
        "EntryPoint": {
            "requirements": str,
            "build": str,
            "buildOouputType": str,
            "buildOouput": str,
            "projectName": str
        },
        "AutoInstall": {
            "enable": bool,
            "installMethod": (str, type(None)),  # 可选项允许为 None 或不存在
            "afterMount": (str, type(None))
        },
        "AutoClone": {
            "enable": bool,
            "repoPlatform": (str, type(None)),
            "repoUri": (str, type(None))
        },
        "AutoFlash": {
            "enable": bool,
            "eraseBeforeFlash": bool,
            "flashCommands": list,
            "flashFileServerEndpoint": str,
            "flashFileServerFilename": str,
            "flashFileGetMethod": str
        }
    }

    if not isinstance(data, dict):
        logging.error('Invalid hpymake.toml structure: Root should be a dictionary')
        return False

    for section, keys in required_structure.items():
        if section not in data or not isinstance(data[section], dict):
            logging.error(f'Invalid hpymake.toml structure: Missing or invalid section [{section}]')
            return False
        for key, value_type in keys.items():
            if key == "enable":
                # enable 是必选项
                if key not in data[section] or not isinstance(data[section][key], bool):
                    logging.error(f'Invalid hpymake.toml structure: Missing or invalid key [{key}] in section [{section}]')
                    return False
            else:
                # 其他键为可选项
                if key in data[section] and not isinstance(data[section][key], value_type):
                    logging.error(f'Invalid hpymake.toml structure: Invalid type for key [{key}] in section [{section}]')
                    return False

    logging.info('hpymake.toml structure validation passed')
    return True

def detect_micropython_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            logging.info(f'Detected MicroPython board on port: {port.device}')
            return port.device
    logging.error('No MicroPython board detected')
    raise RuntimeError("No MicroPython board detected")

def validateMakeInfo():
    makeFile = loadMakeFile()
    if not validateStructure(makeFile):
        logging.error('Invalid hpymake.toml format')
        raise RuntimeError('Invalid hpymake.toml format')
    
    return makeFile

def make():
    make_info = validateMakeInfo()
    micropython_port = detect_micropython_port()
    process_project(make_info, micropython_port)

def main():
    make()

if __name__ == "__main__":
    main()
