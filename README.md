# textCompare and more

## Getting Started

#### Installation

> All stable versions of the application can be found here: https://github.com/rexxtd/textCompare/releases.

> To download to your machine, click on the Assets dropdown menu, then click on the zip file, it will automatically download to your machine.

> If there is a pop-up window appears on your browser, simply choose the location you want to save it, and click Save to download the file.

> After finishing the download, you want to navigate to the folder/location where you save the zip file. Extract the file by Right-click on the zip file and selecting “Extract Here” if you have WinRar installed, or select “7-Zip”, and choose “Extract Here”.

> Note: Depending on your machine, the program must be run as administrator in order to work correctly. If you want to set up the application to run as an administrator everytime, you might want to follow this guide: https://www.windowscentral.com/how-set-apps-always-run-administrator-windows-10

#### Clone repository

> Python 3.8 or higher is required.

> Python library that must be installed correctly into system environment path:

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

All of the dependencies is located inside “requirements.txt”. We highly recommend installing it using pip as the following guide: https://intellipaat.com/community/31672/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project.

## Known Issue

<b>Scan Text Error:</b>

1. Language is not installed

- Open Windows Powershell as Administrator
- Search for installed languages

        Get-WindowsCapability -Online -Name "Language.OCR\*"

- Install language packages

        Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0" (replace en-US with different language)

- In case of error 0x800f0954 (not able to install language packages): https://thesysadminchannel.com/solved-add-windowscapability-failed-error-code-0x800f0954-rsat-fix/
