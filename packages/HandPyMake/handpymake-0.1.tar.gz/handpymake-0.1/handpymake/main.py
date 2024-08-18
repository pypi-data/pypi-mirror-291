import toml
import os.path

from .process import process_project

def checkMakeFile():
    if os.path.isfile('hpymake.toml'):
        print('Checking hpymake.toml exists... Success')
    else:
        raise RuntimeError('Cannot find hpymake.toml')

def loadMakeFile():
    checkMakeFile()
    
    with open('hpymake.toml') as f:
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
        }
    }

    if not isinstance(data, dict):
        return False

    for section, keys in required_structure.items():
        if section not in data or not isinstance(data[section], dict):
            return False
        for key, value_type in keys.items():
            if key == "enable":
                # enable 是必选项
                if key not in data[section] or not isinstance(data[section][key], bool):
                    return False
            else:
                # 其他键为可选项
                if key in data[section] and not isinstance(data[section][key], value_type):
                    return False

    return True

def validateMakeInfo():
    makeFile = loadMakeFile()
    if not validateStructure(makeFile):
        raise RuntimeError('Invalid hpymake.toml format')
    
    return makeFile

def make():
    process_project(validateMakeInfo())

def main():
    make()

if __name__ == "__main__":
    main()