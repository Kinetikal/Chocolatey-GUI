# ChocolateyGUI
The Chocolatey Windows Package Manager, built as a GUI with Python's PySimpleGUI Module.

## Usage

This program is fairly simple. It reads events and stores them in Variables which get executed in Functions.
These functions open a subprocces in PowerShell and run the commands in the PowerShell window, just as you would manually type stuff in there.
This makes the proccess quicker and somewhat automated.

There is a predefined package that I use but it can be skipped/deleted.
Also there is an Option to add your own Package as a text File and install that.

## How the package text File should be formatted

The text File which contains multiple packages should be formated like this:
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

A Script File that if formated like this can be grabbed from [Chocolatey Packages](https://community.chocolatey.org/packages) by building your own package of apps and copying the Script and saving it as a text File.

## Setting your own Predefine Package in the code

If you don't want to read a Package from a text File (For example: Set a hardcoded package in the Python code and run that when you have a fresh Install of Windows), you can change the variable code (Line 5) to your own Predefined Package and with a press of a button install it. The Variable is a list.

Code to change:
```python
    chocolatey_packages = [ "Enter the Package Script Here" ]
```

## Use the .exe to run it as a Program

I converted the Script into a .exe File in the ```Chocolatey_GUI``` folder.
Download the whole Folder and save it to anywhere you like. Open the Chocolatey_GUI.exe and start using the Program as normal.

Also, if you would like to use your own predefined which you changed in the code I would recommend to use the [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) module. 

You can install it with```pip install auto-py-to-exe```.

With it you can make your own executable File of the Python script.

## Screenshots
![python_5y7BB9zbdQ](https://user-images.githubusercontent.com/93329694/233802814-521c5576-b52e-4874-ab85-9c9c68b811fb.png)


