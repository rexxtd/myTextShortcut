# Working with text more easily for Windows 10

## Getting Started

#### Clone repository

> Python 3.8 or higher is required.

> Python library that must be installed correctly into the system environment path:

        pip install -r requirements.txt
        pip install --upgrade git+https://github.com/rexxtd/mywinocr.git

> List of packages:

        customtkinter==5.2.0
        Pillow==10.0.0
        pyautogui==0.9.54
        opencv-python==4.8.0.76
        numpy==1.24.4
        pywinauto==0.6.8
        psutil==5.9.5
        configparser==6.0.0
        diff-match-patch==20230430
        pywin32
        winocr
        googletrans==3.1.0a0

All of the dependencies are located inside “requirements.txt”. We highly recommend installing it using pip as the following guide: https://intellipaat.com/community/31672/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project.

## Known Issue

<b>Scan Text Error:</b>

1. Language is not installed

- In case of error 0x800f0954 (not able to install language packages), please follow guideline from this website: https://thesysadminchannel.com/solved-add-windowscapability-failed-error-code-0x800f0954-rsat-fix/
