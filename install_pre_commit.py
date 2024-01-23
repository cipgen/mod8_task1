# -*- coding: utf-8 -*-
import platform
import subprocess
import sys

def get_os():
    # Detect the operating system
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
    # Check if a command is available in the system
    try:
        process = subprocess.Popen([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode == 0
    except:
        return False

def install_package(os_name, package_name):
    # Install a package based on the operating system
    try:
        if os_name == 'darwin':
            subprocess.call(["brew", "install", package_name])
        elif os_name == 'windows':
            subprocess.call(["pip", "install", package_name])
        elif os_name == 'linux':
            # Use pip to install pre-commit on Linux
            if package_name == "pre-commit":
                subprocess.call(["pip", "install", package_name])
            elif is_command_available("apt-get"):
                subprocess.call(["sudo", "apt-get", "install", package_name])
            elif is_command_available("yum"):
                subprocess.call(["sudo", "yum", "install", package_name])
            else:
                print("Package manager for {} not found.".format(os_name))
                return False
        print("{} successfully installed for {}.".format(package_name, os_name))
        return True
    except:
        print("Error installing {} for {}.".format(package_name, os_name))
        return False

def setup_pre_commit_config():
    # Set up the configuration for pre-commit
    config_content = """repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.16.1
    hooks:
      - id: gitleaks
        args: ['--verbose']  # Add the --verbose option for more detailed results
        name: Gitleaks with verbose output"""
    with open('.pre-commit-config.yaml', 'w') as config_file:
        config_file.write(config_content)

def install_pre_commit_tools(os_name, enable_gitleaks):
    # Install pre-commit tools and optionally enable gitleaks
    if enable_gitleaks:
        if install_package(os_name, "pre-commit"):
            setup_pre_commit_config()
            subprocess.call(["pre-commit", "install"])
            subprocess.call(["pre-commit", "autoupdate"])
    else:
        print("Gitleaks is disabled.")

def main():
    # Main function
    os_name = get_os()
    print("Operating system: {}".format(os_name))
    
    # Read the enable option from git config
    enable_gitleaks = False
    try:
        enable_gitleaks_str = subprocess.check_output(["git", "config", "--local", "--get", "gitleaks.enable"]).strip().decode()
        if enable_gitleaks_str.lower() == "true":
            enable_gitleaks = True
    except subprocess.CalledProcessError:
        pass  # Option is not set
    
    print("Gitleaks enabled: {}".format(enable_gitleaks))
    
    if os_name != 'unknown':
        install_pre_commit_tools(os_name, enable_gitleaks)
    else:
        print("Unknown OS, unable to install tools.")

if __name__ == "__main__":
    main()
