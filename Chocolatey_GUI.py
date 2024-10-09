import PySimpleGUI as sg
import subprocess, sys, webbrowser, os, time
from pathlib import Path
import threading

def main():
    predefined_choco_package = [
"choco install amd-ryzen-chipset --version 2023.8.17 -y",
"choco install 7zip --version 23.1.0 -y",
"choco install bitwarden --version 2023.8.4 -y",
"choco install cheatengine --version 7.5 -y",
"choco install icue --version 4.33.138 -y",
"choco install discord --version 1.0.9005 -y",
"choco install ea-app --version 13.23.0.5536 -y",
"choco install steam --version 2.10.91.91221129 -y",
"choco install epicgameslauncher --version 1.3.51.0 -y",
"choco install git --version 2.42.0 -y",
"choco install github-desktop --version 3.3.1 -y",
"choco install handbrake --version 1.6.1 -y",
"choco install hwinfo --version 7.62 -y",
"choco install lghub --version 2023.7.8769 -y",
"choco install firefox --version 117.0.1 -y",
"choco install nilesoft-shell --version 1.8.1 -y",
"choco install nodejs-lts --version 18.17.1 -y",
"choco install notepadplusplus --version 8.5.7 -y",
"choco install obsidian --version 1.4.13 -y",
"choco install sharex --version 15.0.0 -y",
"choco install treesize --version 9.0.2 -y",
"choco install treesizefree --version 4.7 -y",
"choco install ubisoft-connect --version 142.1.0.10881 -y",
"choco install vlc --version 3.0.18 -y",
"choco install vortex --version 1.9.4 -y",
"choco install vscode --version 1.82.2 -y",
"choco install goggalaxy --version 2.0.67.2 -y"
]

    # Install function for Chocolatey, in case you don't have it
    def install_choco():
        try:
            window["-PBAR-"].update(0,max=1)
            window["-PBAR-"].update(current_count= 0 + 1)

            window["-STATUSBAR-"].update(value = "Running Installer", text_color = "#6fb97e")
            process = subprocess.run(["powershell.exe","Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol    =  [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community. chocolatey.org/   install.ps1'))"], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            window["-OUTPUT-"].print(f">>> {process.stdout}\n")
            window["-OUTPUT_POWERSHELL-"].print(process)
            time.sleep(1)

            window["-PBAR-"].update(0)
            window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
            window.refresh()
        except Exception as e:
            window["-OUTPUT-"].print(e)
            
    # My personal predefined Software Package that I use on a Fresh Windows Install
    def install_predefined_choco_packages(package_list):
        count = 0

        for element in package_list:
            count += 1

            window["-STATUSBAR-"].update(value = f"Running Script: {count}/{len(package_list)}", text_color = "#6fb97e")
            process = subprocess.run(["powershell.exe", element], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) 
            window["-PBAR-"].update(0,max=len(package_list)) # Sets the max_value of pg.Progressbar to the length of the predefined package list
            window["-PBAR-"].update(current_count= 0 + count) # Updates the progress bar step by step with the length of the predefined package list

            window.refresh()
            window["-OUTPUT-"].print(f">>> {process.stdout}\n")
            window["-OUTPUT_POWERSHELL-"].print(process)
            window.refresh()
            time.sleep(0.5)

        window["-PBAR-"].update(0)
        window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
        window.refresh()

    # Option to add your own Software Package as a .txt file which will be read and set as an Variable. #
    def read_user_added_package(file_to_read):
        try:
            file_to_read = Path(file_to_read).read_text()
            window["-OUTPUT-"].print(f">>> Your Package contains:\n{file_to_read}")
        except FileNotFoundError:
            window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")

    # Reads the .txt file that is found in the Input Field and executes every single LINE one by one and returns a returncode 1 = ERROR and returncode 0 =  SUCCESSFULL
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
                process = subprocess.run(["powershell.exe", element], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                window.refresh()
                window["-OUTPUT-"].print(f">>> {process.stdout}\n")
                window["-OUTPUT_POWERSHELL-"].print(process)
                window.refresh()
                time.sleep(0.5)

            window["-PBAR-"].update(0)
            window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")

        except FileNotFoundError:
            window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")
        if process.returncode == 1:
            window["-OUTPUT-"].print(">>> Ran on Errors. Reason: Command Wrong most likely.")
            
            
    def check_if_choco_is_installed():
        
        window["-STATUSBAR-"].update(value = "Checking...", text_color = "#778eca")
        process = subprocess.run(["powershell.exe","choco --version"], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        window["-OUTPUT_POWERSHELL-"].print(process)
        if process.returncode == 0:
            window["-CHOCO_STATUSBAR-"].update("Chocolatey is Installed")
            #subprocess.run(["powershell.exe","choco feature enable -n=allowGlobalConfirmation"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            window["-OUTPUT-"].print(f"Chocolatey is installed | Version: {process.stdout}")
            window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
            window.refresh()
        else:
            window["-INSTALL_CHOCOLATEY-"].update(disabled=False)
            window["-CHOCO_STATUSBAR-"].update("Chocolatey is not Installed")
            window["-STATUSBAR-"].update(value = "Waiting for an Event", text_color = "#778eca")
            window["-OUTPUT-"].print(process.stderr)
        
    # Add your new theme colors and settings
    my_new_theme = {"BACKGROUND": "#1c1e23",
                    "TEXT": "#d2d2d3",
                    "INPUT": "#3d3f46",
                    "TEXT_INPUT": "#d2d2d3",
                    "SCROLL": "#3d3f46",
                    "BUTTON": ("#6fb97e", "#313641"),
                    "PROGRESS": ("#6fb97e", "#4a6ab3"),
                    "BORDER": 1,
                    "SLIDER_DEPTH": 0,
                    "PROGRESS_DEPTH": 0}

    # Add your dictionary to the PySimpleGUI themes
    sg.theme_add_new("MyGreen", my_new_theme)

    # Switch your theme to use the newly added one. You can add spaces to make it more readable
    sg.theme("MyGreen")
    font = ("Roboto", 16)

    MENU_RIGHT_CLICK = ["",["Clear Output", "Version", "Exit"]]

    layout_description = [[sg.Text("Chocolatey-GUI", font="Arial 24 bold underline", text_color="#6fb97e")],
              [sg.Text()],
              [sg.Text("A Package Manager with a GUI that uses the Windows Subprocess to executing commands in PowerShell.")],
              [sg.Text("This Program uses"),sg.Text("Chocolatey",font="Arial 14 underline",text_color="#6fb97e",enable_events=True,tooltip="Redirect Link to    Chocolatey's Website.", key="-URL_REDIRECT-"),sg.Text("and it's Script automation to install the desired Software.")],
              [sg.Text("Hint: There are tooltips on mouse hover and underlined text are Web Links.")],
              [sg.Text()],
              [sg.Text("If you don't have Chocolatey, you can install it bellow. You can install a Predefined Package as well.")],
              [sg.Text("The 'Install Package' button will be disabled, to enable it press the 'List Package' button.")],
              [sg.Text("Lastly you can go to"),sg.Text("Chocolatey Packages",font="Arial 14 underline",text_color="#6fb97e",enable_events=True, tooltip="Redirect Link to Chocolatey's Package Page.", key="-URL_REDIRECT_PACKAGES-"),sg.Text("and bundle your own Packages as a Text File.")]]

    layout_buttons = [[sg.Text("Install Choco:",font="Arial 16 bold"),sg.Push(),sg.Button("Install Chocolatey",size=(15,1),disabled=True,key="-INSTALL_CHOCOLATEY-")],
                      [sg.Text("List Packages:",font="Arial 16 bold"),sg.Push(),sg.Button("List Package",size=(15,1),key="-LIST_PACKAGE-")],
                      [sg.Text("Install Packages",font="Arial 16 bold"),sg.Push(),sg.Button("Install Package",size=(15,1),key="-INSTALL_PACKAGE-",disabled=True)]]

    layout_addown_n_output = [[sg.Text("Add own package File:"),sg.Input(key="-CONF_INPUT-",default_text="Search for a .txt File"),sg.FileBrowse(file_types=(("Text File", "*.txt"),("Config File","*.config"))),sg.Button("Read", tooltip="Adds and prints the file content into the Output.", key="-READ-"),sg.Button("Install",tooltip="Starts intalling the Package as a PowerShell script. BE CAREFUL!", key="-INSTALL-")],
                              [sg.Text()],
                              [sg.Text("Program Output:",font="Arial 16 bold"),sg.Push(),sg.Text("PowerShell Output:",font="Arial 16 bold")],
                              [sg.Multiline(size=(40,10),key="-OUTPUT-",reroute_stdout=True,reroute_stderr=True),sg.Multiline(size=(45,10),key="-OUTPUT_POWERSHELL-",reroute_stdout=True,reroute_stderr=True)]]

    frame_layout_end = [[sg.Text("Status:"),sg.StatusBar(f"Waiting for an Event",key="-STATUSBAR-",text_color="#778eca",size=(16,1)),sg.Text("Progress:"),sg.ProgressBar(10, orientation= "h",size=(50,25), key="-PBAR-"),sg.Button("Exit",size=(10,1),tooltip="Exit the Program.", expand_x=True)]]

    layout_buttons_2 = [[sg.Text("Work in Progress:")],
                        [sg.Text("Choco Status:"),sg.StatusBar("",key="-CHOCO_STATUSBAR-",size=(5,1)),sg.Button("Check",key="-CHOCO_CHECK_BUTTON-")],
                        [sg.Text("Custom Package URL:"),sg.Input(size=(15,2),key="-REPO_URL-"),sg.Button("Load", key="-LOAD_BUTTON-")]]

    layout = [[sg.Column(layout_description)],
              [sg.HSeparator()],
              [sg.Text()],
              [sg.Column(layout_buttons),sg.VSeparator(),sg.Column(layout_buttons_2)],
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
            threading.Thread(target=install_predefined_choco_packages, args=(predefined_choco_package,), daemon=True).start()
            #window.perform_long_operation(lambda: install_predefined_choco_packages(predefined_choco_package),"-OUTPUT-")

        elif event == "-LIST_PACKAGE-":
            window["-OUTPUT-"].print(">>> The predefined Package contains: ")
            for x in predefined_choco_package:
                window["-OUTPUT-"].print(x)
            window["-OUTPUT-"].print(f"\nTotal Packages: {len(predefined_choco_package)}")
            window["-INSTALL_PACKAGE-"].update(disabled=False)

        elif event == "-READ-" and len(values["-CONF_INPUT-"]) > 0:
            window.perform_long_operation(lambda: read_user_added_package(add_own_package),"-OUTPUT-")

        elif event == "-INSTALL-" and len(values["-CONF_INPUT-"]) > 0 and "Search for a .txt File" not in values["-CONF_INPUT-"]:
            window["-OUTPUT-"].print(">>> Installing Package from Input...")
            threading.Thread(target=install_user_added_package, args=(add_own_package,), daemon=True).start()
            #window.perform_long_operation(lambda: install_user_added_package(add_own_package),"-OUTPUT-")

        elif event == "-LOAD_BUTTON-" and values["-REPO_URL-"]:
            custom_repo_url = values["-REPO_URL-"]
            install_command = f"choco install --source={custom_repo_url} <package_name>"
            process = subprocess.run([install_command], text=True)
            window["-OUTPUT-"].print(process)

        elif event == "-INSTALL-" and values["-CONF_INPUT-"] == "Search for a .txt File" or values["-CONF_INPUT-"] == "":
            window["-OUTPUT-"].print(">>> FileNotFoundError: No file found, check Input.")
        
        elif event == "-CHOCO_CHECK_BUTTON-":
            threading.Thread(target=check_if_choco_is_installed, daemon=True).start()

        elif event == "Clear Output":
            window["-OUTPUT-"].update("")

        elif event == "Version":
            sg.popup_scrolled(sg.get_versions())

    window.close()

if __name__ == '__main__':
    main()
