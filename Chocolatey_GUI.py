import PySimpleGUI as sg
import subprocess, sys, webbrowser, os
from pathlib import Path

user_defined_choco_packages = """choco install firefox --version 111.0.1 -y
choco install vcredist140 --version 14.34.31938 -y
choco install python3 --version 3.11.3 -y
choco install 7zip.install --version 22.1 -y
choco install vlc --version 3.0.18 -y
choco install git.install --version 2.40.0 -y
choco install vscode --version 1.77.3 -y
choco install treesizefree --version 4.6.3 -y
choco install amd-ryzen-chipset --version 2023.2.28 -y
choco install nvidia-display-driver --version 531.41 -y
choco install sharex --version 15.0.0 -y
choco install discord --version 1.0.9005 -y
choco install handbrake --version 1.6.1 -y
choco install steam --version 2.10.91.91221129 -y
choco install epicgameslauncher --version 1.3.51.0 -y
choco install ea-app --version 12.158.0.5415 -y
choco install ubisoft-connect --version 140.0.0.10857 -y
choco install notepadplusplus --version 8.5.2 -y
choco install msiafterburner --version 4.6.5.230316 -y"""

# Custom theme inputs, changed by desire.
my_new_theme = {'BACKGROUND': '#401955',
                'TEXT': 'white',
                'INPUT': '#deb887',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#c7e78b',
                'BUTTON': ('white', '#7541ba'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes.
sg.theme_add_new('MyNewTheme', my_new_theme)

# Install proccess for Chocolatey, in case you don't have it. #
def install_choco():
    result = subprocess.run(["powershell.exe", "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"], shell=True, capture_output=True, text=True)
    window["-OUTPUT-"].print(result.stdout)
    
# My personal predefined Software Package that I use on a Fresh Windows Install. #
def predefined_choco_packages():

    subprocess.run(["powershell.exe", user_defined_choco_packages])

    
# Option to add your own Software Package as a .txt file which will be read and executed. #
def read_package_content(add_own_package):
    try:
        add_own_package = Path(add_own_package).read_text()
        window["-OUTPUT-"].print(f">>> Your Package contains:\n{add_own_package}")
    except PermissionError:
        window["-OUTPUT-"].print(">>> PermissionError: File not found!")

def install_useradded_package(add_own_package):
    content = Path(add_own_package).read_text()
    result = subprocess.run(["powershell.exe", content], shell=True, capture_output=True, text=True)
    window["-OUTPUT-"].print(result.stdout)

sg.theme("DarkGrey13")
font=("Arial", 16)

MENU_RIGHT_CLICK = ["",["Clear Output", "Version", "Exit"]]

layout_description = [[sg.Text("Chocolatey-GUI", font="Arial 20 bold underline")],
          [sg.Text()],
          [sg.Text("A WPM with a GUI that uses the Windows Subprocess for executing commands in the PowerShell/Command Prompt.")],
          [sg.Text("This Program uses"),sg.Text("Chocolatey",font="Arial 14 underline",text_color="#42b3f5",enable_events=True,tooltip="Redirect Link to Chocolatey's Website.", key="-URL_REDIRECT-"),sg.Text("a solid WPM which executes commands and installs Software.")],
          [sg.Text("Built using Python and the PySimpleGUI Module.")],
          [sg.Text()],
          [sg.Text("If you don't have Chocolatey, please install it with the 'Install Chocolatey' button.")],
          [sg.Text("You can install a Predefined Package with the 'Install Packages' button.")],
          [sg.Text("Lastly you can go to"),sg.Text("Chocolatey Packages",font="Arial 14 underline",text_color="#42b3f5",enable_events=True,tooltip="Redirect Link to Chocolatey's Package Page.", key="-URL_REDIRECT_PACKAGES-"),sg.Text("and bundle your own Packages and add it as a .txt File to this Program.")]]

layout_buttons = [[sg.Text()],
                  [sg.Text("If you want to list the predefined Packages",font="Arial 16 bold"),sg.Push(),sg.Button("List Packages",size=(15,1))],
                  [sg.Text("Install Chocolatey with Windows PowerShell",font="Arial 16 bold"),sg.Push(),sg.Button("Install Chocolatey",size=(15,1))],
                  [sg.Text("Install Predefined Chocolatey Packages",font="Arial 16 bold"),sg.Push(),sg.Button("Install Packages",size=(15,1))]]

layout_addown_n_output = [[sg.Text("Add own package File:"),sg.Input(key="-CONF_INPUT-",default_text="Search for a .txt File"),sg.FileBrowse(file_types=(("Text Files", "*.txt"),)),sg.Button("Add"),sg.Button("Install")],
                          [sg.HSeparator()],
                          [sg.Multiline(size=(90,10),key="-OUTPUT-")]]

frame_layout_end = [[sg.Text("Credit: Jovan", font= "Arial 10 bold underline"),sg.Button("Exit",size=(10,1),tooltip="Exit the Program.", expand_x=True)]]

layout = [[sg.Column(layout_description)],
          [sg.HSeparator()],
          [sg.Column(layout_buttons)],
          [sg.Text()],
          [sg.Column(layout_addown_n_output)],
          [sg.Column(frame_layout_end, justification="right")]]

window = sg.Window("Chocolatey Package Manager",layout,font=font, finalize=True,right_click_menu=MENU_RIGHT_CLICK)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    # Variable #
    add_own_package = values["-CONF_INPUT-"]
    
    # Redirection URL to Chocolatey #
    if event == "-URL_REDIRECT-":
       url = "https://chocolatey.org/"
       webbrowser.open(url)

    elif event == "-URL_REDIRECT_PACKAGES-":
        url_pckg = "https://community.chocolatey.org/packages"
        webbrowser.open(url_pckg)
       
    elif event == "Install Chocolatey":
        window.perform_long_operation(install_choco,"-OUTPUT-")
        
    elif event == "Install Packages":
        window.perform_long_operation(predefined_choco_packages,"-OUTPUT-")
    
    elif event == "List Packages":
        window["-OUTPUT-"].print(user_defined_choco_packages)
        
    elif event == "Add" and len(values["-CONF_INPUT-"]) > 0:
        window.perform_long_operation(lambda: read_package_content(add_own_package),"-OUTPUT-")
 
    elif event == "Add" and len(values["-CONF_INPUT-"]) == 0:
        window["-OUTPUT-"].print(">>> Error: No file found, check Input.")
        
    elif event == "Install" and len(values["-CONF_INPUT-"]) > 0:
        window.perform_long_operation(lambda: install_useradded_package(add_own_package),"-OUTPUT-")
        
    elif event == "Install" and len(values["-CONF_INPUT-"]) == 0:
        window["-OUTPUT-"].print(">>> Error: No file found, check Input.")
        
    elif event == "Clear Output":
        window["-OUTPUT-"].update("")
        #sg.execute_editor(__file__)
        
    elif event == "Version":
        sg.popup_scrolled(sg.get_versions())
            
window.close()
