import hashlib
import json
import sys
import time
import urllib.request
import zlib

from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QMainWindow, QAction, QInputDialog, QTextEdit
)

current_time = time.ctime()
print("[INFO]", current_time, "| Start")


class HashCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.text_or_file_label = QLabel('Text or File Path:')
        layout.addWidget(self.text_or_file_label)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate_text_or_file)
        layout.addWidget(self.calculate_button)

        self.result_label = QLabel('Hash Results:')
        layout.addWidget(self.result_label)

        self.hash_algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']
        self.hash_labels = [QLabel(f'{algorithm}:') for algorithm in self.hash_algorithms]
        self.hash_results = [QLabel() for _ in self.hash_algorithms]
        for label, result_label in zip(self.hash_labels, self.hash_results):
            layout.addWidget(label)
            layout.addWidget(result_label)

        self.central_widget.setLayout(layout)
        self.setWindowTitle('Hash Calculator - Waiting for user action')
        self.setGeometry(300, 300, 700, 300)

        self.hash_thread = HashThread(self)
        self.hash_thread.hash_results_ready.connect(self.update_hash_results)

        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        about_menu = menubar.addMenu('About')

        file_actions = [
            ('Select file', 'Ctrl+I', self.browse_file),
            ('Insert text', 'Ctrl+T', self.insert_text),
            ('Export', 'Ctrl+S', self.export_hashes),
            ('Compare', 'Ctrl+H', self.compare_hashes),
            ('Online Compare', 'Ctrl+Alt+H', self.online_compare),
            ('Exit', 'Esc', self.close)
        ]

        about_actions = [
            ('About', 'Alt+A', self.show_about_dialog),
            ('Changelog', 'Alt+C', self.show_changelog_dialog),
            ('Check for update', 'Ctrl+U', self.check_for_update)
        ]

        self.add_actions_to_menu(file_menu, file_actions)
        self.add_actions_to_menu(about_menu, about_actions)

    def add_actions_to_menu(self, menu, actions):
        for action_name, shortcut, method in actions:
            action = QAction(action_name, self)
            action.setShortcut(shortcut)
            action.triggered.connect(method)
            menu.addAction(action)

    def insert_text(self):
        text, ok = QInputDialog.getText(self, 'Insert Text', 'Enter the text:')
        if ok:
            self.text_input.setPlainText(text)

    def calculate_text_or_file(self):
        text = self.text_input.toPlainText()
        if text:
            self.calculate_text_hash(text)
        else:
            self.browse_file()

    def calculate_text_hash(self, text):
        results = []
        try:
            text_bytes = text.encode()

            for algorithm in ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']:
                if algorithm == 'MD5':
                    hash_value = hashlib.md5(text_bytes).hexdigest()
                elif algorithm == 'SHA1':
                    hash_value = hashlib.sha1(text_bytes).hexdigest()
                elif algorithm == 'SHA256':
                    hash_value = hashlib.sha256(text_bytes).hexdigest()
                elif algorithm == 'SHA512':
                    hash_value = hashlib.sha512(text_bytes).hexdigest()
                elif algorithm == 'CRC32':
                    hash_value = format(zlib.crc32(text_bytes) & 0xFFFFFFFF, '08x')

                results.append(hash_value)

            self.update_hash_results(results)
        except Exception as e:
            self.show_hash_error(str(e))

    def check_for_update(self):
        print("[INFO]", current_time, "| Checking for update")
        try:
            url = "https://raw.githubusercontent.com/ElliotCHEN37/Hash-Calculator/main/cfu.json"
            with urllib.request.urlopen(url) as response:
                data = response.read()
                version_info = json.loads(data)

            latest_version = version_info["latest_version"]
            current_version = '1.7'
            if latest_version > current_version:
                self.prompt_update(latest_version, version_info["download_url"])
            elif latest_version == current_version:
                QMessageBox.information(self, "No Update Available", "You are using the latest version")
            elif latest_version <= current_version:
                QMessageBox.information(self, "No Update Available",
                                        "You are using a higher version than the latest version")
        except Exception as e:
            self.show_update_error(str(e))

    def prompt_update(self, latest_version, download_url):
        print("[INFO]", current_time, "| Update available", latest_version)
        reply = QMessageBox.question(self, 'New Version Available',
                                     f'A new version ({latest_version}) is available. '
                                     'Do you want to download it?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("[INFO]", current_time, "| Redirecting to download url")
            QDesktopServices.openUrl(QUrl(download_url))
        else:
            print("[INFO]", current_time, "| Update cancelled")

    def show_update_error(self, error_msg):
        print("[ERROR]", current_time, f"| Error: {error_msg}")
        QMessageBox.critical(self, 'Error while checking for update', f'Error while checking for update: {error_msg}')

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select file', '', 'All Files (*)', options=options)

        if file_path:
            self.text_input.setPlainText(file_path)
            self.hash_thread.set_file_path(file_path)
            print("[INFO]", current_time, f"| Selected file: {file_path}")
            self.setWindowTitle('Hash Calculator - Calculating')
            print("[INFO]", current_time, f"| Start calculating")
            self.hash_thread.start()

    def update_hash_results(self, results):
        for result_label, result in zip(self.hash_results, results):
            result_label.setText(result)
        self.setWindowTitle('Hash Calculator - Done')
        print("[INFO]", current_time, "| Done")

    def show_hash_error(self, error_msg):
        print("[ERROR]", current_time, f"| Error: {error_msg}")
        QMessageBox.critical(self, 'Hash Calculation Error', f'Error while calculating hash: {error_msg}')

    def export_hashes(self):
        if hasattr(self, 'hash_results_data'):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'Text Files (*.txt);;JSON Files (*.json)', options=options)

            if file_path:
                try:
                    if file_path.endswith('.json'):
                        hash_data = {algo: hash_value for algo, hash_value in
                                     zip(self.hash_algorithms, self.hash_results_data)}

                        with open(file_path, 'w') as file:
                            json.dump(hash_data, file, indent=4)
                    elif file_path.endswith('.txt'):
                        with open(file_path, 'w') as file:
                            file.write(f"File Path: {self.text_input.toPlainText()}\n")
                            for algo, hash_value in zip(self.hash_algorithms, self.hash_results_data):
                                file.write(f"{algo}: {hash_value}\n")

                    print("[INFO]", current_time, f"| Export to {file_path}")
                    QMessageBox.information(self, "Export Successful", "Hash values exported successfully!")
                except Exception as e:
                    self.show_export_error(str(e))
        else:
            print("[INFO]", current_time, f"| No data to export")
            QMessageBox.warning(self, "No Data", "No hash values to export. Calculate hash values first.")

    def show_export_error(self, error_msg):
        print("[ERROR]", current_time, f"| Error: {error_msg}")
        QMessageBox.critical(self, "Export Error", f"An error occurred while exporting:\n{error_msg}")

    def show_about_dialog(self):
        about_text = ("Hash Calculator Version 1.7 (02/18/24) By ElliotCHEN\n\nA simple hash value calculation "
                      "program written in PyQt5\n\nhttps://github.com/ElliotCHEN37/Hash-Calculator\n\nThis work is "
                      "licensed under MIT License\nApp icon is from Google Fonts (Material Icons)")
        print("[INFO]", current_time, "| Show about text")
        QMessageBox.about(self, "About", about_text)

    def show_changelog_dialog(self):
        print("[INFO]", current_time, "| Redirecting to changelog")
        QDesktopServices.openUrl(QUrl(
            'https://github.com/ElliotCHEN37/Hash-Calculator?tab=readme-ov-file#pyqt5-edition-pyqt5%E7%89%88%E6%9C%AC'))

    def load_json_from_url(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                json_data = json.loads(data)
            return json_data
        except Exception as e:
            self.show_load_hash_values_error(str(e))
            return None

    def online_compare(self):
        print("[INFO]", current_time, "| Online compare start")
        try:
            url, ok = QInputDialog.getText(self, 'Enter JSON URL', 'Enter the URL of the JSON file:')
            if ok:
                print("[INFO]", current_time, "| Online JSON file loaded")
                json_data = self.load_json_from_url(url)
                if json_data:
                    mismatched_items = []
                    for algo, expected_value, result_label in zip(self.hash_algorithms, json_data.values(),
                                                                  self.hash_results):
                        computed_value = result_label.text()
                        if computed_value == json_data.get(algo, ""):
                            result_label.setStyleSheet('color: green;')
                        else:
                            result_label.setStyleSheet('color: red;')
                            mismatched_items.append((algo, json_data.get(algo, ""), computed_value))
                        print("[INFO]", current_time, "| Compare finished")

                    if mismatched_items:
                        message = "The following hash values didn't match:\n\n"
                        for algo, expected_value, computed_value in mismatched_items:
                            message += f"{algo}:\n  JSON: {expected_value}\n  Computed: {computed_value}\n\n"
                        QMessageBox.critical(self, "Compare - Didn't match", message)
                    else:
                        QMessageBox.information(self, "Compare - Matched", "All hash values matched")
        except Exception as e:
            print("[ERROR]", current_time, f"| Error: {str(e)}")
            self.show_compare_error(str(e))

    def compare_hashes(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                self, 'Select JSON file', '', 'JSON Files (*.json)', options=options)

            if file_path:
                with open(file_path, 'r') as json_file:
                    expected_values = json.load(json_file)
                    print("[INFO]", current_time, f"| JSON file loaded: {file_path}")

                mismatched_items = []

                for algo, expected_value, result_label in zip(self.hash_algorithms, expected_values.values(),
                                                              self.hash_results):
                    computed_value = result_label.text()
                    if computed_value == expected_values.get(algo, ""):
                        result_label.setStyleSheet('color: green;')
                    else:
                        result_label.setStyleSheet('color: red;')
                        mismatched_items.append((algo, expected_values.get(algo, ""), computed_value))
                    print("[INFO]", current_time, f'| "hash_values.json" loaded')

                if mismatched_items:
                    message = "The following hash values didn't match:\n\n"
                    for algo, expected_value, computed_value in mismatched_items:
                        message += f"{algo}:\n  JSON: {expected_value}\n  Computed: {computed_value}\n\n"
                    print("[WARN]", current_time, "| Values didn't match")
                    QMessageBox.critical(self, "Compare - Didn't match", message)
                else:
                    print("[INFO]", current_time, "| All values matched")
                    QMessageBox.information(self, "Compare - Matched", "All hash values matched")

        except Exception as e:
            self.show_compare_error(str(e))

    def show_compare_error(self, error_msg):
        print("[ERROR]", current_time, f"| Error: {error_msg}")
        QMessageBox.critical(self, "Compare - Error", f'Error while comparing hashes values: {error_msg}')


class HashThread(QThread):
    hash_results_ready = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None

    def set_file_path(self, file_path):
        self.file_path = file_path

    def run(self):
        if self.file_path:
            results = []
            try:
                with open(self.file_path, 'rb') as file:
                    content = file.read()
                    for algorithm in ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']:
                        if algorithm == 'MD5':
                            hash_value = hashlib.md5(content).hexdigest()
                        elif algorithm == 'SHA1':
                            hash_value = hashlib.sha1(content).hexdigest()
                        elif algorithm == 'SHA256':
                            hash_value = hashlib.sha256(content).hexdigest()
                        elif algorithm == 'SHA512':
                            hash_value = hashlib.sha512(content).hexdigest()
                        elif algorithm == 'CRC32':
                            hash_value = format(zlib.crc32(content) & 0xFFFFFFFF, '08x')

                        results.append(hash_value)

                self.hash_results_ready.emit(results)
            except Exception as e:
                print("[ERROR]", current_time, f"| Error: {str(e)}")
                self.hash_results_ready.emit(['Error: ' + str(e)])
        else:
            print("[WARN]", current_time, f"| Please select a file first")
            self.hash_results_ready.emit(['Please select a file first'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCalculator()
    window.show()
    sys.exit(app.exec_())
