import sys
import hashlib
import zlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, 
    QMessageBox, QMainWindow, QAction
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication, QUrl
from PyQt5.QtGui import QDesktopServices
import json
import urllib.request

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

class HashCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.file_path_label = QLabel('Selected File:')
        self.file_path_line_edit = QLabel()
        self.file_path_line_edit.setWordWrap(True)

        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_file)

        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_line_edit)
        layout.addWidget(self.browse_button)

        self.hash_algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512', 'CRC32']
        self.hash_labels = [QLabel(f'{algorithm}:') for algorithm in self.hash_algorithms]
        self.hash_results = [QLabel() for _ in self.hash_algorithms]
        for label, result_label in zip(self.hash_labels, self.hash_results):
            layout.addWidget(label)
            layout.addWidget(result_label)

        self.central_widget.setLayout(layout)
        self.setWindowTitle('Hash Calculator - Waiting for user action')
        self.setGeometry(300, 300, 700, 300)
        self.setAcceptDrops(True)

        self.hash_thread = HashThread(self)
        self.hash_thread.hash_results_ready.connect(self.update_hash_results)

        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        file_action = QAction('Select file', self)
        file_action.setShortcut('Ctrl+I')
        file_action.triggered.connect(self.browse_file)
        file_menu.addAction(file_action)
        
        export_action = QAction('Export', self)
        export_action.setShortcut('Ctrl+S')
        export_action.triggered.connect(self.export_hashes)
        file_menu.addAction(export_action)

        compare_action = QAction('Compare', self)
        compare_action.setShortcut('Ctrl+H')
        compare_action.triggered.connect(self.compare_hashes)
        file_menu.addAction(compare_action)
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Esc')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        about_menu = menubar.addMenu('About')
        
        about_action = QAction('About', self)
        about_action.setShortcut('Alt+A')
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)
        
        changelog_action = QAction('Changelog', self)
        changelog_action.setShortcut('Alt+C')
        changelog_action.triggered.connect(self.show_changelog_dialog)
        about_menu.addAction(changelog_action)
        
        sponsor_action = QAction('Sponsor', self)
        sponsor_action.setShortcut('Alt+S')
        sponsor_action.triggered.connect(self.show_sponsor_dialog)
        about_menu.addAction(sponsor_action)
        
        cfu_action = QAction('Check for update', self)
        cfu_action.setShortcut('Ctrl+U')
        cfu_action.triggered.connect(self.check_for_update)
        about_menu.addAction(cfu_action)

    def check_for_update(self):
        try:
            url = "https://raw.githubusercontent.com/ElliotCHEN37/Hash-Calculator/main/cfu.json"
            with urllib.request.urlopen(url) as response:
                data = response.read()
                version_info = json.loads(data)

            latest_version = version_info["latest_version"]
            current_version = '1.5'
            if latest_version > current_version:
                download_url = version_info["download_url"]
                reply = QMessageBox.question(self, 'New Version Available',
                                             f'A new version ({latest_version}) is available. '
                                             'Do you want to download it?',
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    QDesktopServices.openUrl(QUrl(download_url))
                    pass
            elif latest_version == current_version:
                QMessageBox.information(self, "No Update Available", "You are using the latest version")
            elif latest_version <= current_version:
                QMessageBox.information(self, "No Update Available", "You are using higher version than the latest version")
        except Exception as e:
            QMessageBox.critical(self, 'Error while checking for update', f'Error while checking for update: {str(e)}')

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select file', '', 'All Files (*)', options=options)

        if file_path:
            self.file_path_line_edit.setText(file_path)
            self.hash_thread.set_file_path(file_path)
            self.setWindowTitle('Hash Calculator - Calculating')
            self.hash_thread.start()
            messagebox_shown = False

    def update_hash_results(self, results):
        self.hash_results_data = results
        for result_label, result in zip(self.hash_results, results):
            result_label.setText(result)
        self.setWindowTitle('Hash Calculator - Done')

        try:
            with open('hash_values.json', 'r') as json_file:
                expected_values = json.load(json_file)

            for algo, expected_value, result_label in zip(self.hash_algorithms, expected_values.values(),
                                                          self.hash_results):
                if result_label.text() == expected_value:
                    result_label.setStyleSheet('color: green;')
                else:
                    result_label.setStyleSheet('color: red;')

        except Exception as e:
            print(f"Error while comparing hash values: {e}")

    def export_hashes(self):
        if hasattr(self, 'hash_results_data'):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'Text Files (*.txt)', options=options)

            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(f"File Path: {self.file_path_line_edit.text()}\n")
                        for algo, result in zip(self.hash_algorithms, self.hash_results_data):
                            file.write(f"{algo}: {result}\n")
                    QMessageBox.information(self, "Export Successful", "Hash values exported successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", f"An error occurred while exporting:\n{str(e)}")
        else:
            QMessageBox.warning(self, "No Data", "No hash values to export. Calculate hash values first.")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        messagebox_shown = False
        self.file_path_line_edit.setText(file_path)
        self.hash_thread.set_file_path(file_path)
        self.setWindowTitle('Hash Calculator - Calculating')
        self.hash_thread.start()

    def show_about_dialog(self):
        about_text = "Hash Calculator Version 1.5 (02/01/24) By ElliotCHEN\n\nA simple hash value calculation program written in PyQt5\n\nhttps://github.com/ElliotCHEN37/Hash-Calculator\n\nThis work is licensed under MIT License"
        QMessageBox.about(self, "About", about_text)

    def show_changelog_dialog(self):
        QDesktopServices.openUrl(QUrl('https://github.com/ElliotCHEN37/Hash-Calculator?tab=readme-ov-file#changelog'))

    def show_sponsor_dialog(self):
        sponsor_text = "李涵博 $0.42 CNY"
        QMessageBox.about(self, "Sponsor", sponsor_text)

    def compare_hashes(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                self, 'Select JSON file', '', 'JSON Files (*.json)', options=options)

            if file_path:
                with open(file_path, 'r') as json_file:
                    expected_values = json.load(json_file)

                mismatched_items = []

                for algo, expected_value, result_label in zip(self.hash_algorithms, expected_values.values(),
                                                              self.hash_results):
                    if result_label.text() != expected_value:
                        mismatched_items.append((algo, expected_value, result_label.text()))

                if mismatched_items:
                    message = "The following hash values didn't match:\n\n"
                    for algo, expected_value, computed_value in mismatched_items:
                        message += f"{algo}:\n  JSON: {expected_value}\n  Computed: {computed_value}\n\n"
                    result_label.setStyleSheet('color: red;')
                    QMessageBox.critical(self, "Compare - Didn't match", message)
                else:
                    result_label.setStyleSheet('color: green;')
                    QMessageBox.information(self, "Compare - Matched", "All hash values matched")

        except Exception as e:
            QMessageBox.critical(self, "Compare - Error", f'Error while comparing hashes values: {str(e)}')

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
                print(str(e))
                self.hash_results_ready.emit(['Error: ' + str(e)])
        else:
            self.hash_results_ready.emit(['Please select file'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCalculator()
    window.show()
    sys.exit(app.exec_())
