import sys
import time
import requests
import logging
from logging.handlers import RotatingFileHandler
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
        self.created_files = {}  # 用來記錄剛剛被創建的檔案

    def on_modified(self, event):
        if event.is_directory:
            return
        # 檢查檔案是否剛被創建過，若是則忽略此事件
        if event.src_path in self.created_files:
            # 若創建在1秒內，視為重複事件，不處理
            if time.time() - self.created_files[event.src_path] < 1:
                return
        print(f"檔案已修改: {event.src_path}")
        logging.info(f"檔案已修改: {event.src_path}")
        self.file_changed.emit(f"File modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            return
        # 記錄創建時間
        self.created_files[event.src_path] = time.time()
        print(f"檔案已創建: {event.src_path}")
        logging.info(f"檔案已創建: {event.src_path}")
        self.file_changed.emit(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"檔案已刪除: {event.src_path}")
        logging.info(f"檔案已刪除: {event.src_path}")
        self.file_changed.emit(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        print(f"檔案已移動: {event.src_path} 到 {event.dest_path}")
        logging.info(f"檔案已移動: {event.src_path} 到 {event.dest_path}")
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
        self.init_log()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(320, 200) # Base Windows size
        # self.setFixedSize(320, 200) # Fixed Windows size
        resources_rc.qInitResources()
        self.setWindowIcon(QIcon(":/nkg.ico"))  # Set icon from resource

        # self.init_layout()
        self.ui.select_button.clicked.connect(self.select_directory_event)
        self.ui.fetch_button.clicked.connect(self.fetch_data_event)

        self.directory_watcher = None
        logging.warning(f"Initializer App finished!")
        
    def init_layout(self):
        self.setWindowTitle("Directory Watcher")

        self.layout = QVBoxLayout()
        self.select_folder_label = QLabel("Select a directory to monitor: ")
        self.layout.addWidget(self.select_folder_label)

        self.select_button = QPushButton("Select Directory")
        self.select_button.clicked.connect(self.select_directory_event)
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

    def init_log(self):
        # 配置Logging，將日誌輸出到檔案
        # log_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
        # log 達到5MB後會自動Rollback
        log_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)-7s - %(message)s"))
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.DEBUG)

        # Log test
        # for i in range(1000):
        #         logging.info(f"Log entry {i}")

    def select_directory_event(self):
        # self.fetch_data()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            # self.status_label.setText(f"Monitoring: {directory}")
            self.ui.folder_label.setText(f"Monitoring: {directory}")
            logging.info(f"Monitoring: {directory}")
            if self.directory_watcher:
                self.directory_watcher.stop()
                self.ui.status_label.setText(f"Not Monitoring...")

            # 啟動監控線程
            self.directory_watcher = DirectoryWatcher(directory)
            self.directory_watcher.file_changed.connect(self.update_status_event)
            self.directory_watcher.start()
            self.ui.status_label.setText(f"Start Monitoring...")
            logging.info(f"Start Monitoring...")

    def update_status_event(self, message: str):
        # self.status_label.setText(message)
        self.ui.status_label.setText(message)

    def fetch_data_event(self):
        self.fetch_data()

    def fetch_data(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        try:
            # 發送GET請求
            response = requests.get(url)
            response.raise_for_status()  # 確保請求成功
            if response.status_code == 200:
                data = response.json()  # 解析回傳的 JSON 資料
                # 顯示結果
                self.ui.status_label.setText(str(data))
                logging.info(f"response code: {response.status_code}")
            else:
                self.ui.status_label.setText(f"Error fetching data: {response.status_code}")
                logging.error(f"Error fetching data: {response.status_code}")
        except requests.RequestException as e:
            self.ui.status_label.setText(f"Error fetching data: {e}")
            logging.error(f"Error fetching data: {e}")

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
