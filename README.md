# Chocolatey-GUI
The Chocolatey Windows Package Manager, built as a GUI with Python's PySimpleGUI Module.

## Usage

This program is fairly simple. It reads events and stores them in Variables which get executed in Functions.
These functions open a subprocces in PowerShell and run the commands in the PowerShell window, just as you would manually type stuff in there.
This makes the proccess quicker and somewhat automated.

There is a predefined package that I use but it can be skipped/deleted.
Also there is an Option to add your own Package as a .txt File and install that.

Python will read the .txt file and save it's content which would look like this ``` choco install firefox --version 111.0.1 -y ``` which will install Firefox with Chocolatey.

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

## Use the .exe to run it as a Program

If you would like to use the Program as a standalone executable for Windows I would recommend to use ```auto-py-to-exe``` to make a .exe out of the Script.

## Screenshots
![ChocoGUI](https://github.com/Kinetikal/ChocolateyGUI/assets/93329694/0c7cf9c4-62d0-45e2-903b-8acb897f9d6b)
