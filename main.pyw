import sys
import hashlib
import zlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, 
    QMessageBox, QMainWindow, QAction, QMenu
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

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
        file_action.triggered.connect(self.browse_file)
        file_menu.addAction(file_action)
        export_action = QAction('Export', self)
        export_action.triggered.connect(self.export_hashes)
        file_menu.addAction(export_action)
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        about_menu = menubar.addMenu('About')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)
        changelog_action = QAction('Changelog', self)
        changelog_action.triggered.connect(self.show_changelog_dialog)
        about_menu.addAction(changelog_action)
        sponsor_action = QAction('Sponsor', self)
        sponsor_action.triggered.connect(self.show_sponsor_dialog)
        about_menu.addAction(sponsor_action)

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
        self.file_path_line_edit.setText(file_path)
        self.hash_thread.set_file_path(file_path)
        self.setWindowTitle('Hash Calculator - Calculating')
        self.hash_thread.start()

    def show_about_dialog(self):
        about_text = "Hash Calculator Version 1.4 (01/29/24) By ElliotCHEN\n\nA simple hash value calculation program written in PyQt5\n\nhttps://github.com/ElliotCHEN37/Hash-Calculator\n\nThis work is licensed under MIT License"
        QMessageBox.about(self, "About", about_text)

    def show_changelog_dialog(self):
        changelog_text = "v1.4 (01/29/24)\nNew\n-Export Feature"
        QMessageBox.about(self, "Changelog", changelog_text)

    def show_sponsor_dialog(self):
        sponsor_text = "李涵博 $0.42 CNY"
        QMessageBox.about(self, "Sponsor", sponsor_text)

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
