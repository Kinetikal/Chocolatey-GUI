import PySimpleGUI as sg
import subprocess, sys, webbrowser, os, time
from pathlib import Path

predefined_choco_package = ["choco install firefox --version 111.0.1 -y",
                                    "choco install 7zip.install --version 22.1 -y",
                                    "choco install vlc --version 3.0.18 -y"]

# Install function for Chocolatey, in case you don't have it
def install_choco():
    result = subprocess.run(["powershell.exe", "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"], capture_output=True, text=True)
    window["-OUTPUT-"].print(result.stdout)
    
# My personal predefined Software Package that I use on a Fresh Windows Install
def install_predefined_choco_packages(package_list):
    count = 0
    
    for element in package_list:
        count += 1
        
        window["-PBAR-"].update(0,max=len(package_list)) # Sets the max_value of pg.Progressbar to the length of the predefined package list
        window["-PBAR-"].update(current_count= 0 + count) # Updates the progress bar step by step with the length of the predefined package list

        window["-STATUSBAR-"].update(value = f"Running Script: {count}/{len(package_list)}", text_color = "#6fb97e")
        result = subprocess.run(["powershell.exe", element], text = True) 
        window["-OUTPUT-"].print(result)
        time.sleep(0.5)
        
    window["-PBAR-"].update(0)
    window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
        
# Option to add your own Software Package as a .txt file which will be read and set as an Variable. #
def read_user_added_package(file_to_read):
    try:
        file_to_read = Path(file_to_read).read_text()
        window["-OUTPUT-"].print(f">>> Your Package contains:\n{file_to_read}")
    except FileNotFoundError:
        window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")

# Reads the .txt file that is found in the Input Field and executes every single LINE one by one and returns a returncode 1 = ERROR and returncode 0 = SUCCESSFULL
def install_user_added_package(install_own_package):
    try:
        with open(install_own_package) as file:
            lines = [line.rstrip() for line in file]
            
        count = 0
        for element in lines:
            count += 1
            
            window["-PBAR-"].update(0,max=len(lines)) # Sets the max_value of pg.Progressbar to the length of the predefined package list
            window["-PBAR-"].update(current_count= 0 + count) # Updates the progress bar step by step with the length of the predefined package list

            window["-STATUSBAR-"].update(value = f"Running Script: {count}/{len(lines)}", text_color = "#6fb97e")
            result = subprocess.run(["powershell.exe", element], text=True)
            window["-OUTPUT-"].print(result)
            time.sleep(0.5)

        window["-PBAR-"].update(0)
        window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
            
    except FileNotFoundError:
        window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")

# Add your new theme colors and settings
my_new_theme = {'BACKGROUND': '#1c1e23',
                'TEXT': '#d2d2d3',
                'INPUT': '#3d3f46',
                'TEXT_INPUT': '#d2d2d3',
                'SCROLL': '#c7e78b',
                'BUTTON': ('#6fb97e', '#313641'),
                'PROGRESS': ('#778eca', '#6fb97e'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new('MyGreen', my_new_theme)

# Switch your theme to use the newly added one. You can add spaces to make it more readable
sg.theme("MyGreen")
font=("Arial", 16)

MENU_RIGHT_CLICK = ["",["Clear Output", "Version", "Exit"]]

layout_description = [[sg.Text("Chocolatey-GUI", font="Arial 24 bold underline", text_color="#6fb97e")],
          [sg.Text()],
          [sg.Text("A Package Manager with a GUI that uses the Windows Subprocess to executing commands in PowerShell.")],
          [sg.Text("This Program uses"),sg.Text("Chocolatey",font="Arial 14 underline",text_color="#6fb97e",enable_events=True,tooltip="Redirect Link to Chocolatey's Website.", key="-URL_REDIRECT-"),sg.Text("and it's Script automation to install the desired Software.")],
          [sg.Text("Built using Python and the amazing PySimpleGUI Module.")],
          [sg.Text()],
          [sg.Text("If you don't have Chocolatey, please install it with the 'Install Chocolatey' button.")],
          [sg.Text("You can install a Predefined Package with the 'Install Packages' button.")],
          [sg.Text("Lastly you can go to"),sg.Text("Chocolatey Packages",font="Arial 14 underline",text_color="#6fb97e",enable_events=True,tooltip="Redirect Link to Chocolatey's Package Page.", key="-URL_REDIRECT_PACKAGES-"),sg.Text("and bundle your own Packages and add it as a .txt File to this Program.")]]

layout_buttons = [[sg.Text()],
                  [sg.Text("If you want to List the Predefined Package",font="Arial 16 bold"),sg.Push(),sg.Button("List Package",size=(15,1),key="-LIST_PACKAGE-")],
                  [sg.Text("Install Chocolatey with Windows PowerShell",font="Arial 16 bold"),sg.Push(),sg.Button("Install Chocolatey",size=(15,1),key="-INSTALL_CHOCOLATEY-")],
                  [sg.Text("Install Predefined Chocolatey Package",font="Arial 16 bold"),sg.Push(),sg.Button("Install Package",size=(15,1),key="-INSTALL_PACKAGE-")]]

layout_addown_n_output = [[sg.Text("Add own package File:"),sg.Input(key="-CONF_INPUT-",default_text="Search for a .txt File"),sg.FileBrowse(file_types=(("Text File", "*.txt"),)),sg.Button("Add", tooltip="Adds and prints the file content into the Output.", key="-ADD-"),sg.Button("Install",tooltip="Starts intalling the Package as a PowerShell script. BE CAREFUL!", key="-INSTALL-")],
                          [sg.HSeparator()],
                          [sg.Multiline(size=(90,10),key="-OUTPUT-")]]

frame_layout_end = [[sg.Text("Status:"),sg.StatusBar(f"Waiting for an Event",key="-STATUSBAR-",text_color="#778eca",size=(16,1)),sg.Text("Progress:"),sg.ProgressBar(10, orientation= "h",size=(50,25), key="-PBAR-"),sg.Button("Exit",size=(10,1),tooltip="Exit the Program.", expand_x=True)]]

layout = [[sg.Column(layout_description)],
          [sg.HSeparator()],
          [sg.Column(layout_buttons)],
          [sg.Text()],
          [sg.Column(layout_addown_n_output)],
          [sg.Column(frame_layout_end, justification="center")]]

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
       
    elif event == "-INSTALL_CHOCOLATEY-":
        window.perform_long_operation(install_choco,"-OUTPUT-")
        
    elif event == "-INSTALL_PACKAGE-":
        window.refresh()
        window.perform_long_operation(lambda: install_predefined_choco_packages(predefined_choco_package),"-OUTPUT-")
    
    elif event == "-LIST_PACKAGE-":
        window["-OUTPUT-"].print(">>> The user defined Package contains: ")
        for x in predefined_choco_package:
            window["-OUTPUT-"].print(x)
        
    elif event == "-ADD-" and len(values["-CONF_INPUT-"]) > 0:
        window.perform_long_operation(lambda: read_user_added_package(add_own_package),"-OUTPUT-")
        
    elif event == "-INSTALL-" and len(values["-CONF_INPUT-"]) > 0 and "Search for a .txt File" not in values["-CONF_INPUT-"]:
        window["-OUTPUT-"].print(">>> Installing Package from Input...")
        window.perform_long_operation(lambda: install_user_added_package(add_own_package),"-OUTPUT-")
        
    elif event == "-INSTALL-" and values["-CONF_INPUT-"] == "Search for a .txt File" or values["-CONF_INPUT-"] == "":
        window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")
        
    elif event == "Clear Output":
        window["-OUTPUT-"].update("")
        
    elif event == "Version":
        sg.popup_scrolled(sg.get_versions())
            
window.close()
