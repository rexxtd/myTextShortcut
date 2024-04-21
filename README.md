# MyShortcut - Text

## Working with text more easily for Windows
This is my application that is made using Python.

The application's purpose is to help reduce the text workload I have to do in my daily work in <b> the most secure way </b> and <b> the fastest way </b> as possible.

There are 2 main functions:

### 1. Text Comparison
- The most secure way to compare the differences between text/paragraph/code.
- It is built to only run the function on your local computer, therefore the data will never leave your computer.
- It is very useful when you need to working with some internal information that cannot use any online tools on the websites.

### 2. Scan Text
- The fastest way to extract the text from an image on your computer.
- It uses the WinOCR modules, thanks to this [repo](https://github.com/GitHub30/winocr).
- The feature uses the OCR detecting engine provided directly from Windows, which has an incredibly fast processing time but can still maintain a decent accuracy rate.
- For the simplification of the application, there are only several languages that are supported, including: <b>English (Global), English (US), Korean, Japanese, Chinese (Simplified), Chinese (Traditional), Russian, German, Spanish, Portuguese, and French</b>.
- However, in order to use it, it is required to install the language package first. The installation is only required once. You can install the language package in 2 ways:

  #### <b>Method 1: </b>
  On the MyShortcut application, go to <b>Setting</b>, then scroll down to the <i>Add OCR Language</i>, click on the dropdown button next to the <i>OCR Language</i> and select the language you want to install. Then click <b>Add</b> to install the language package.

  #### <b>Method 2: </b>
  Open the Start Menu, type Windows PowerShell, then select <i>Run as administrator</i>. Then type in: <b>Add-WindowsCapability -Online -name Language.OCR~~~en-US~0.0.1.0</b>. Replace the "en-US" with your language tag that represents the language you want to install. For the language tag, please refer to the table included in this [link](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/available-language-packs-for-windows?view=windows-11).
<br>

# Download and usage
1. Go to this [link](https://github.com/rexxtd/myTextShortcut/releases) and select the version you want to download. The latest version should be always on top.

2. Download the <b>myShortcut-Text.zip</b> file and extract it with any extractor tool such as 7-Zip or WinRAR

3. Run the <b>MyShortcut.exe</b>. 

4. In case the application is not running, right-click it and select <b>Run as administrator</b>

# Getting Started for development

### Requirement
> Python 3.8 or higher is required.

> All of the dependencies located inside “requirements.txt” must be installed.

I highly recommend installing it using pip as the following guide: https://intellipaat.com/community/31672/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project.

### Step 1. Clone repository
> First, clone the repository
        
        https://github.com/rexxtd/myTextShortcut.git
        

### Step 2. Install dependencies
> Python library that must be installed correctly into the system environment path:

        pip install -r requirements.txt
        pip install --upgrade git+https://github.com/rexxtd/mywinocr.git

### Step 3. Run the code
> a. Change the working directory to <b>./myTextShortcut/src</b>

> b. Run the <b>main.py</b>

# Known Issue

### 1. Virus detected when extracting/running the program
- The problem occurs due to the application being compiled using pyinstaller, which make the Windows Security system mark it as a virus since the program is made from an undetected source. 
- The application is written purely in Python, and you can review the source code yourself. There is no single harmful line of code that was included, therefore it is safe to use.
- To whitelist apps in Windows Defender, open the Windows Security app, navigate to “Virus & threat protection,” then select “Manage settings” under “Virus & threat protection settings.” Next, scroll down to “Exclusions” and choose “Add or remove exclusions” to add the desired apps to the whitelist.

### 2. Language is not installed
- When you try to install the language package for Scan Text, you might encounter an error below: 0x800f0954
![language package error](https://thesysadminchannel.com/wp-content/uploads/2020/08/Add-WindowsCapability-Name-RSAT-Error.png)
- The issue was caused due to Windows not allowing you to download directly from Windows Updates, but instead through the Windows Server Updates Services (WSUS).
- To fix the issue, please follow the guidelines from this [website](https://thesysadminchannel.com/solved-add-windowscapability-failed-error-code-0x800f0954-rsat-fix/).

# Future Direction
- I plan to implement more features to support more languages.
- More OCR methods will be implemented to increase the accuracy. This can be achieved with enough datasets and a precise machine-learning model.
