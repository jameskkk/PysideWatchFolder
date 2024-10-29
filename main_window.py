import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QIcon, QCloseEvent
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main_window_ui import Ui_MainWindow
import resources_rc

# 監控事件處理
class DirectoryEventHandler(QObject, FileSystemEventHandler):
    file_changed = Signal(str)

    def __init__(self):
        super().__init__()

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"檔案已修改: {event.src_path}")
        self.file_changed.emit(f"File modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"檔案已創建: {event.src_path}")
        self.file_changed.emit(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"檔案已刪除: {event.src_path}")
        self.file_changed.emit(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        print(f"檔案已移動: {event.src_path} 到 {event.dest_path}")
        self.file_changed.emit(f"File moved: {event.src_path} to {event.dest_path}")

# 背景線程進行目錄監控
class DirectoryWatcher(QThread):
    file_changed = Signal(str)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.observer = Observer()
        self.event_handler = DirectoryEventHandler()
        self.event_handler.file_changed.connect(self.handle_file_change)

    def handle_file_change(self, message: str):
        self.file_changed.emit(message)

    def run(self):
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        self.exec()  # 保持執行直到線程終止

    def stop(self):
        self.observer.stop()
        self.observer.join()

# GUI 主視窗
class FileWatcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(320, 200) # Base Windows size
        # self.setFixedSize(320, 200) # Fixed Windows size
        resources_rc.qInitResources()
        self.setWindowIcon(QIcon(":/nkg.ico"))  # Set icon from resource

        # self.init_layout()
        self.ui.select_button.clicked.connect(self.select_directory)

        self.directory_watcher = None

    def init_layout(self):
        self.setWindowTitle("Directory Watcher")

        self.layout = QVBoxLayout()
        self.select_folder_label = QLabel("Select a directory to monitor: ")
        self.layout.addWidget(self.select_folder_label)

        self.select_button = QPushButton("Select Directory")
        self.select_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_button)

        self.folder_label = QLabel("No directory selected.")
        self.folder_label.setWordWrap(True)  # 啟用自動換行
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # 設定文字對齊
        self.layout.addWidget(self.folder_label)

        self.status_label = QLabel("Not monitoring.")
        self.status_label.setWordWrap(True)  # 啟用自動換行
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # 設定文字對齊
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            # self.status_label.setText(f"Monitoring: {directory}")
            self.ui.folder_label.setText(f"Monitoring: {directory}")
            if self.directory_watcher:
                self.directory_watcher.stop()
                self.ui.status_label.setText(f"Not Monitoring...")

            # 啟動監控線程
            self.directory_watcher = DirectoryWatcher(directory)
            self.directory_watcher.file_changed.connect(self.update_status)
            self.directory_watcher.start()
            self.ui.status_label.setText(f"Start Monitoring...")

    def update_status(self, message: str):
        # self.status_label.setText(message)
        self.ui.status_label.setText(message)

    def closeEvent(self, event: QCloseEvent):
        if self.directory_watcher:
            self.directory_watcher.stop()
        event.accept()

        # Make sure Application exit
        QApplication.instance().quit()

if __name__=="__main__":
    # 執行應用
    app = QApplication(sys.argv)
    window = FileWatcherApp()
    window.show()
    sys.exit(app.exec())
