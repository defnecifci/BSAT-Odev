import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# İzleme olaylarını ele alacak sınıf
class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def on_any_event(self, event):
        change = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(self.log_file, "a") as f:
            json.dump(change, f)
            f.write("\n")

def main():
    # İzlenecek ve log kaydedilecek dizinler
    watch_dir = "/home/kali/bsm/test"
    log_file = "/home/kali/bsm/logs/changes.json"

    # Log dosyasını oluşturun
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")

    # Watchdog kurulum
    event_handler = DirectoryChangeHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, path=watch_dir, recursive=True)

    # İzlemeye başlama
    observer.start()
    print(f"İzleme başlatıldı: {watch_dir}")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
