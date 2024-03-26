import subprocess


def is_ocr_language_installed(language_code):
    # Construct the PowerShell command to check if the OCR language is installed
    powershell_get_cmd = f"Get-WindowsCapability -Online -Name 'Language.OCR~~~{language_code}~0.0.1.0'"

    # Execute the PowerShell command
    try:
        result = subprocess.run(["powershell", "-Command", powershell_get_cmd], capture_output=True, text=True, check=True)
        output = result.stdout
        # Check if the output contains the language information
        if "NotPresent" in output:
            return False, output
        else:
            return True, output
    except subprocess.CalledProcessError as e:
        # If the PowerShell command failed, return False
        return False, e
    
def ocr_lang_installer(language_code):
    state, string = is_ocr_language_installed(language_code)
    if (state):
        return True, string
    else:
        # Construct the PowerShell command to check if the OCR language is installed
        powershell_add_cmd = f"Add-WindowsCapability -Online -Name 'Language.OCR~~~{language_code}~0.0.1.0'"

        # Execute the PowerShell command
        try:
            subprocess.run(["powershell", "-Command", powershell_add_cmd], capture_output=True, text=True, check=True)
            state, output = is_ocr_language_installed(language_code)
            # Check if the output contains the language information
            if "NotPresent" in output:
                return False, output
            else:
                return True, output
        except subprocess.CalledProcessError as e:
        # If the PowerShell command failed, raise a custom exception
            return False, f"Failed to execute PowerShell command: {e}"
