import sys
import subprocess
import webbrowser
import os
import time
from pathlib import Path
import threading

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar,
                               QFileDialog, QStatusBar)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QDesktopServices

class InstallWorker(QThread):
    progress = Signal(int, int)
    output = Signal(str)
    finished = Signal()

    def __init__(self, package_list):
        super().__init__()
        self.package_list = package_list

    def run(self):
        count = 0
        for element in self.package_list:
            count += 1
            self.progress.emit(count, len(self.package_list))
            process = subprocess.run(["powershell.exe", element], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.output.emit(f">>> {process.stdout}\n")
            self.output.emit(str(process))
            time.sleep(0.5)
        self.finished.emit()

class ChocolateyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chocolatey Package Manager")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()

        self.predefined_choco_package = [
            "choco install amd-ryzen-chipset --version 2023.8.17 -y",
            "choco install 7zip --version 23.1.0 -y",
            # ... (rest of the package list)
        ]

    def setup_ui(self):
        # Description
        description_layout = QVBoxLayout()
        title_label = QLabel("Chocolatey-GUI")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        description_layout.addWidget(title_label)

        description_text = QLabel("A Package Manager with a GUI that uses the Windows Subprocess to execute commands in PowerShell.")
        description_layout.addWidget(description_text)

        choco_link = QLabel('This Program uses <a href="https://chocolatey.org/">Chocolatey</a> and its Script automation to install the desired Software.')
        choco_link.setOpenExternalLinks(True)
        description_layout.addWidget(choco_link)

        self.layout.addLayout(description_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.install_choco_button = QPushButton("Install Chocolatey")
        self.install_choco_button.setEnabled(False)
        self.install_choco_button.clicked.connect(self.install_choco)
        button_layout.addWidget(self.install_choco_button)

        self.list_package_button = QPushButton("List Package")
        self.list_package_button.clicked.connect(self.list_package)
        button_layout.addWidget(self.list_package_button)

        self.install_package_button = QPushButton("Install Package")
        self.install_package_button.setEnabled(False)
        self.install_package_button.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_package_button)

        self.layout.addLayout(button_layout)

        # Add own package
        package_layout = QHBoxLayout()
        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("Search for a .txt File")
        package_layout.addWidget(self.package_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        package_layout.addWidget(self.browse_button)

        self.read_button = QPushButton("Read")
        self.read_button.clicked.connect(self.read_package)
        package_layout.addWidget(self.read_button)

        self.install_custom_button = QPushButton("Install")
        self.install_custom_button.clicked.connect(self.install_custom_package)
        package_layout.addWidget(self.install_custom_button)

        self.layout.addLayout(package_layout)

        # Output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Progress bar and status
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.layout.addLayout(progress_layout)

    def install_choco(self):
        self.output_text.append("Installing Chocolatey...")
        self.status_bar.showMessage("Running Installer")
        
        def run_install():
            process = subprocess.run(["powershell.exe", "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.output_text.append(f">>> {process.stdout}\n")
            self.output_text.append(str(process))
            self.status_bar.showMessage("Waiting for an Event")

        threading.Thread(target=run_install, daemon=True).start()

    def list_package(self):
        self.output_text.append(">>> The predefined Package contains: ")
        for package in self.predefined_choco_package:
            self.output_text.append(package)
        self.output_text.append(f"\nTotal Packages: {len(self.predefined_choco_package)}")
        self.install_package_button.setEnabled(True)

    def install_package(self):
        self.worker = InstallWorker(self.predefined_choco_package)
        self.worker.progress.connect(self.update_progress)
        self.worker.output.connect(self.update_output)
        self.worker.finished.connect(self.installation_finished)
        self.worker.start()

    def update_progress(self, current, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_bar.showMessage(f"Running Script: {current}/{total}")

    def update_output(self, text):
        self.output_text.append(text)

    def installation_finished(self):
        self.progress_bar.setValue(0)
        self.status_bar.showMessage("Waiting for an Event")

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Package File", "", "Text Files (*.txt);;Config Files (*.config)")
        if file_name:
            self.package_input.setText(file_name)

    def read_package(self):
        file_to_read = self.package_input.text()
        try:
            content = Path(file_to_read).read_text()
            self.output_text.append(f">>> Your Package contains:\n{content}")
        except FileNotFoundError:
            self.output_text.append(">>> FileNotFoundError: No file found, check Input.")

    def install_custom_package(self):
        file_to_install = self.package_input.text()
        if not file_to_install or file_to_install == "Search for a .txt File":
            self.output_text.append(">>> FileNotFoundError: No file found, check Input.")
            return

        try:
            with open(file_to_install) as file:
                lines = [line.rstrip() for line in file]
            
            self.worker = InstallWorker(lines)
            self.worker.progress.connect(self.update_progress)
            self.worker.output.connect(self.update_output)
            self.worker.finished.connect(self.installation_finished)
            self.worker.start()
        except FileNotFoundError:
            self.output_text.append(">>> FileNotFoundError: No file found, check Input.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChocolateyGUI()
    window.show()
    sys.exit(app.exec())
