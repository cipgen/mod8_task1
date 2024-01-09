# -*- coding: utf-8 -*-
import platform
import subprocess

def get_os():
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'darwin'
    elif os_name == 'Windows':
        return 'windows'
    elif os_name == 'Linux':
        return 'linux'
    else:
        return 'unknown'

def is_command_available(command):
    try:
        process = subprocess.Popen([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode == 0
    except:
        return False

def install_package(os_name, package_name):
    try:
        if os_name == 'darwin':
            subprocess.call(["brew", "install", package_name])
        elif os_name == 'windows':
            subprocess.call(["pip", "install", package_name])
        elif os_name == 'linux':
            if is_command_available("apt-get"):
                subprocess.call(["sudo", "apt-get", "install", package_name])
            elif is_command_available("yum"):
                subprocess.call(["sudo", "yum", "install", package_name])
            else:
                print("Пакетный менеджер для {} не найден.".format(os_name))
                return False
        print("{} успешно установлен для {}.".format(package_name, os_name))
        return True
    except:
        print("Ошибка установки {} для {}.".format(package_name, os_name))
        return False

def setup_pre_commit_config():
    config_content = """repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.16.1
    hooks:
      - id: gitleaks"""
    with open('.pre-commit-config.yaml', 'w') as config_file:
        config_file.write(config_content)

def install_pre_commit_tools(os_name):
    if install_package(os_name, "pre-commit"):
        setup_pre_commit_config()
        subprocess.call(["pre-commit", "install"])
        subprocess.call(["pre-commit", "autoupdate"])

def main():
    os_name = get_os()
    print("Операционная система: {}".format(os_name))
    if os_name != 'unknown':
        install_pre_commit_tools(os_name)
    else:
        print("Неизвестная ОС, установка инструментов невозможна.")

if __name__ == "__main__":
    main()
