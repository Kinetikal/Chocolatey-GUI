# Chocolatey-GUI
The Chocolatey Windows Package Manager, built as a GUI with Python's PySimpleGUI Module.


## Usage

This program is fairly simple. It reads events and stores them in Variables which get executed in Functions.
These functions open a subprocces in PowerShell and run the commands in the PowerShell window, just as you would manually type stuff in there.
This makes the proccess quicker and somewhat automated.

There is a predefined package that I use but it can be skipped/deleted.
Also there is an Option to add your own Package as a .txt File and install that.

Python will read the .txt file and save it's content which would look like this ``` choco install firefox --version 111.0.1 -y ``` which will install Firefox with Chocolatey.

## Use the .exe to run it as a Program

I converted the Script into a .exe File in the ```Chocolatey_GUI``` folder.
Download the whole Folder and save it to anywhere you like. Open the Chocolatey_GUI.exe and start using the Program as normal.


## How the package .txt File should be formatted

The .txt File which contains multiple packages should be formated like this:
```
choco install python3 --version 3.11.3 -y
choco install 7zip.install --version 22.1 -y
choco install vlc --version 3.0.18 -y
choco install git.install --version 2.40.0 -y
choco install vscode --version 1.77.3 -y
choco install treesizefree --version 4.6.3 -y
choco install handbrake --version 1.6.1 -y
```
with new lines where the installer will iterate through the lines and execute the commands one by one.

## Setting your own Predefine Package

If you don't want to read a Package from a .txt File, you can change the variable at the top of the code (Line 5) to your own Predefined Package and with a press of a button install it. The Variable is a list.

Code to change:
```python
    chocolatey_packages = [ "Enter the Package Build Content Here" ]
    # Docstring as String Variable is used isntead of making multiple Variables where each would start with choco install APPNAME 
```

## Screenshots
![Chocolatey-GUI](https://user-images.githubusercontent.com/93329694/233053660-4e73ea42-0752-4b3b-b99b-21c8d8ad433a.png)


