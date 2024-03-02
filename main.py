import hashlib
import json
import os
import sys
import urllib.request
import zlib

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QMainWindow, QAction, QLineEdit, QDialog, QHBoxLayout, QComboBox
)

try:
    from ctypes import windll

    appid = 'ElliotCHEN.Hash Calculator.Hash Calculator.v1.9'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
except ImportError:
    pass


class HashCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.compare_dialog = None

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.file_path_label = QLabel('Selected File:')
        self.file_path_line_edit = QLabel()
        self.file_path_line_edit.setWordWrap(True)

        self.text_input_label = QLabel('Input Text:')
        self.text_input_line_edit = QLineEdit()
        layout.addWidget(self.text_input_label)
        layout.addWidget(self.text_input_line_edit)

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate_hash_text)

        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_line_edit)
        layout.addWidget(self.calculate_button)

        self.hash_algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']
        self.hash_labels = [QLabel(f'{algorithm}:') for algorithm in self.hash_algorithms]
        self.hash_results = [QLabel() for _ in self.hash_algorithms]
        for label, result_label in zip(self.hash_labels, self.hash_results):
            layout.addWidget(label)
            layout.addWidget(result_label)

        self.central_widget.setLayout(layout)
        basedir = os.path.dirname(__file__)
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'icon.ico')))
        self.setWindowTitle('Hash Calculator - Waiting for user action')
        self.setGeometry(300, 300, 700, 300)
        self.setAcceptDrops(True)

        self.hash_thread = HashThread(self)
        self.hash_thread.hash_results_ready.connect(self.update_hash_results)

        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        about_menu = menubar.addMenu('About')

        file_actions = [
            ('Select file', 'Ctrl+I', self.browse_file),
            ('Calculate Text', 'Ctrl+T', self.calculate_hash_text),
            ('Compare Hash', 'Ctrl+H', self.compare_hash),
            ('Export', 'Ctrl+S', self.export_hashes),
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

    def calculate_hash_text(self):
        input_text = self.text_input_line_edit.text()
        if input_text:
            results = []
            try:
                input_bytes = input_text.encode('utf-8')
                for algorithm in ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']:
                    if algorithm == 'MD5':
                        hash_value = hashlib.md5(input_bytes).hexdigest()
                    elif algorithm == 'SHA1':
                        hash_value = hashlib.sha1(input_bytes).hexdigest()
                    elif algorithm == 'SHA256':
                        hash_value = hashlib.sha256(input_bytes).hexdigest()
                    elif algorithm == 'SHA512':
                        hash_value = hashlib.sha512(input_bytes).hexdigest()
                    elif algorithm == 'CRC32':
                        hash_value = format(zlib.crc32(input_bytes) & 0xFFFFFFFF, '08x')

                    results.append(hash_value)

                self.update_hash_results(results)
            except Exception as e:
                self.show_hash_text_error(str(e))
        else:
            QMessageBox.warning(self, "No Text", "Please input text to calculate hash.")

    def compare_hash(self):
        if not self.compare_dialog:
            self.compare_dialog = CompareHashDialog(self)
        if self.compare_dialog.exec_() == QDialog.Accepted:
            algorithm = self.compare_dialog.algorithm_combo.currentText()
            user_hash = self.compare_dialog.hash_input_line_edit.text()

            if not user_hash:
                QMessageBox.warning(self, "No Text", "Please enter hash value to compare.")
                return

            if hasattr(self, 'hash_results_data'):
                try:
                    index = self.hash_algorithms.index(algorithm)
                    calculated_hash = self.hash_results_data[index]

                    if calculated_hash == user_hash:
                        QMessageBox.information(self, "Hash Comparison", "Hash values match!")
                    else:
                        QMessageBox.warning(self, "Hash Comparison", "Hash values do not match!")
                except ValueError:
                    QMessageBox.warning(self, "Invalid Algorithm", "Selected algorithm is not valid.")
            else:
                QMessageBox.warning(self, "No Data", "No hash values available for comparison.")

    def check_for_update(self):
        try:
            url = "https://raw.githubusercontent.com/ElliotCHEN37/Hash-Calculator/main/cfu.json"
            with urllib.request.urlopen(url) as response:
                data = response.read()
                version_info = json.loads(data)

            latest_version = version_info["latest_version"]
            current_version = '1.9'
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
        reply = QMessageBox.question(self, 'New Version Available',
                                     f'A new version ({latest_version}) is available. '
                                     'Do you want to download it?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl(download_url))
        else:
            pass

    def show_update_error(self, error_msg):
        QMessageBox.critical(self, 'Error while checking for update', f'Error while checking for update: {error_msg}')

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select file', '', 'All Files (*)', options=options)

        if file_path:
            self.file_path_line_edit.setText(file_path)
            self.hash_thread.set_file_path(file_path)
            self.setWindowTitle('Hash Calculator - Calculating')
            self.hash_thread.start()

    def update_hash_results(self, results):
        self.hash_results_data = results
        for result_label, result in zip(self.hash_results, results):
            result_label.setText(result)
        self.setWindowTitle('Hash Calculator - Done')

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
                            file.write(f"File Path: {self.file_path_line_edit.text()}\n")
                            for algo, hash_value in zip(self.hash_algorithms, self.hash_results_data):
                                file.write(f"{algo}: {hash_value}\n")

                    QMessageBox.information(self, "Export Successful", "Hash values exported successfully!")
                except Exception as e:
                    self.show_export_error(str(e))
        else:
            QMessageBox.warning(self, "No Data", "No hash values to export. Calculate hash values first.")

    def show_export_error(self, error_msg):
        QMessageBox.critical(self, "Export Error", f"An error occurred while exporting:\n{error_msg}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_path_line_edit.setText(file_path)
        self.hash_thread.set_file_path(file_path)
        self.setWindowTitle('Hash Calculator - Calculating')
        self.hash_thread.start()

    def show_about_dialog(self):
        about_text = ("Hash Calculator Version 1.9 (03/02/24) By ElliotCHEN\n\nA simple hash value calculation "
                      "program written in PyQt5\n\nhttps://github.com/ElliotCHEN37/Hash-Calculator\n\nThis work is "
                      "licensed under MIT License\nApp icon is from Google Fonts (Material Icons)")
        QMessageBox.about(self, "About", about_text)

    def show_changelog_dialog(self):
        QDesktopServices.openUrl(QUrl(
            'https://github.com/ElliotCHEN37/Hash-Calculator?tab=readme-ov-file#pyqt5-edition-pyqt5%E7%89%88%E6%9C%AC'))


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
                self.hash_results_ready.emit(['Error: ' + str(e)])
        else:
            self.hash_results_ready.emit(['Please select a file first'])


class CompareHashDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Compare Hash')
        layout = QHBoxLayout()

        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32'])

        self.hash_input_line_edit = QLineEdit()
        self.hash_input_line_edit.setPlaceholderText('Enter Hash Value')

        self.compare_button = QPushButton('Compare')
        self.compare_button.clicked.connect(self.compare_hashes)

        layout.addWidget(self.algorithm_combo)
        layout.addWidget(self.hash_input_line_edit)
        layout.addWidget(self.compare_button)

        self.setLayout(layout)

    def compare_hashes(self):
        algorithm = self.algorithm_combo.currentText()
        user_hash = self.hash_input_line_edit.text()

        if not user_hash:
            QMessageBox.warning(self, "No Text", "Please enter hash value to compare.")
            return

        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCalculator()
    window.show()
    sys.exit(app.exec_())
