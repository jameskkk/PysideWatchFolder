import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.event_handler = Handler()
        self.observer = Observer()

    def run(self):
        print(f"監控中: {self.directory_to_watch}")
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"檔案已創建: {event.src_path}")

    def on_deleted(self, event):
        print(f"檔案已刪除: {event.src_path}")

    def on_modified(self, event):
        print(f"檔案已修改: {event.src_path}")

    def on_moved(self, event):
        print(f"檔案已移動: {event.src_path} 到 {event.dest_path}")

if __name__ == "__main__":
    # 指定需要監控的目錄
    directory_to_watch = "D:/CA_Project/CP/CPSourceCode/PySide/SerialTool/TestFolder"
    watcher = Watcher(directory_to_watch)
    watcher.run()

    # t = ['x', 'A', 'k', 'y', 's', 'u', 'm', 'd', 'c', 'e', 'i', 'l', ' ', ',']
    # indices = [1, 11, 9, 0, 13, 4, 5, 8, 2, 12, 6, 3, 12, 7, 10, 8, 2]
    # result = "".join([t[i] for i in indices])
    # print(result)


