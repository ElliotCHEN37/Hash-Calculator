import sys
import hashlib
import zlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class HashCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.file_path_label = QLabel('選擇文件:')
        self.file_path_line_edit = QLabel()
        self.file_path_line_edit.setWordWrap(True)

        self.browse_button = QPushButton('瀏覽')
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

        self.setLayout(layout)
        self.setWindowTitle('Hash Calculator')
        self.setGeometry(300, 300, 400, 300)

        self.setAcceptDrops(True)

        # 創建哈希計算的執行緒
        self.hash_thread = HashThread(self)
        # 連接信號
        self.hash_thread.hash_results_ready.connect(self.update_hash_results)

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, '選擇文件', '', 'All Files (*)', options=options)

        if file_path:
            self.file_path_line_edit.setText(file_path)
            # 在選擇文件後啟動計算哈希值的執行緒
            self.hash_thread.set_file_path(file_path)
            self.hash_thread.start()

    def update_hash_results(self, results):
        # 更新哈希值結果
        for result_label, result in zip(self.hash_results, results):
            result_label.setText(result)
        self.setWindowTitle('Hash Calculator - 完成')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_path_line_edit.setText(file_path)
        # 在拖放文件後啟動計算哈希值的執行緒
        self.hash_thread.set_file_path(file_path)
        self.hash_thread.start()
        self.setWindowTitle('Hash Calculator - 計算中')

class HashThread(QThread):
    # 定義信號
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

                # 發送信號通知主執行緒更新界面
                self.hash_results_ready.emit(results)
            except Exception as e:
                print(str(e))
                self.hash_results_ready.emit(['錯誤: ' + str(e)])
        else:
            self.hash_results_ready.emit(['請選擇文件'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCalculator()
    window.show()
    sys.exit(app.exec_())
