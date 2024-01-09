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

def install_pre_commit(os_name):
    try:
        if os_name == 'darwin':
            if is_command_available("brew"):
                subprocess.call(["brew", "install", "pre-commit"])
            else:
                print("Brew не найден. Попробуйте установить 'pre-commit' вручную.")
                return
        elif os_name == 'windows':
            if is_command_available("pip"):
                subprocess.call(["pip", "install", "pre-commit"])
            else:
                print("Pip не найден. Попробуйте установить 'pre-commit' вручную.")
                return
        elif os_name == 'linux':
            if is_command_available("apt-get"):
                subprocess.call(["sudo", "apt-get", "install", "pre-commit"])
            elif is_command_available("yum"):
                subprocess.call(["sudo", "yum", "install", "pre-commit"])
            else:
                print("Ни apt-get, ни yum не найдены. Попробуйте установить 'pre-commit' вручную.")
                return
        print("Pre-commit успешно установлен для {}.".format(os_name))
    except:
        print("Ошибка установки pre-commit для {}.".format(os_name))

def main():
    os_name = get_os()
    print("Операционная система: {}".format(os_name))
    if os_name != 'unknown':
        install_pre_commit(os_name)
    else:
        print("Неизвестная ОС, установка pre-commit невозможна.")

if __name__ == "__main__":
    main()
