import os
import sys
import subprocess
import time
import shutil
import threading
import logging
import subprocess
import glob
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from _utils.config_operations import read_config, initialize_logging


class Watcher:
    def __init__(self, watch_directory, build_directory):
        self.watch_directory = watch_directory
        self.build_directory = build_directory
        self.event_handler = WatchHandler()
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                pass
        except:
            self.observer.stop()
            logging.info("Observer stopped")


class WatchHandler(FileSystemEventHandler):
    debounce_delay = 3  # prevent multiple rapid triggers
    cooldown_time = 35  # refractory period after first build
    last_build_time = 0
    timer = None
    pending_trigger = False

    @staticmethod
    def find_python_executable(build_root):
        # Search for python.exe in .venv* directories recursively
        venv_paths = glob.glob(os.path.join(build_root, ".venv*"), recursive=True)
        for venv_path in venv_paths:
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
            if os.path.isfile(python_path):
                return python_path

        # If .venv python not found, log a warning and try global python
        logging.warning(
            "No .venv Python executable found. Searching for global Python..."
        )
        global_python_path = shutil.which("python")
        if global_python_path:
            return global_python_path
        else:
            logging.error("No global Python executable found. Exiting.")
            sys.exit(1)

    @staticmethod
    def trigger():
        current_time = time.time()
        if current_time - WatchHandler.last_build_time < WatchHandler.cooldown_time:
            logging.info("Build request ignored due to cooldown.")
            return
        logging.info("Triggering build...")
        try:
            subprocess.run(["revealpack", "build"])
            WatchHandler.last_build_time = time.time()
            logging.info("Successfully ran build.py")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to run build.py: {e}")

    @staticmethod
    def process(event):
        logging.info(f"Event type: {event.event_type} at {event.src_path}")

        if WatchHandler.pending_trigger:
            if WatchHandler.timer:
                WatchHandler.timer.cancel()
        else:
            WatchHandler.pending_trigger = True

        WatchHandler.timer = threading.Timer(
            WatchHandler.debounce_delay, WatchHandler.execute_trigger
        )
        WatchHandler.timer.start()

    @staticmethod
    def execute_trigger():
        WatchHandler.trigger()
        WatchHandler.pending_trigger = False
        WatchHandler.timer = None

    def on_modified(self, event):
        self.process(event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serve the presentation with watcher.')
    parser.add_argument('--root', type=str, default=os.getcwd(), help='Target directory for setup')
    args = parser.parse_args()

    config = read_config(args.root)
    initialize_logging(config)

    watch_directory = os.path.join(
        config["directories"]["source"]["root"],
        config["directories"]["source"]["presentation_root"],
    )
    build_directory = config["directories"]["build"]
    # py_path = config.get("python_path", None)

    # Start the watcher in a separate thread
    logging.info(f"Starting build watch on {watch_directory}")
    watcher = Watcher(watch_directory, build_directory)
    # watcher.event_handler = WatchHandler()
    watcher_thread = threading.Thread(target=watcher.run)
    watcher_thread.daemon = True
    watcher_thread.start()
    # Start the http-server from npm (not sure how to make this a requirement)
    http_service = subprocess.Popen(f"http-server {build_directory} -o", shell=True)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Shutting down server.")
        watcher.observer.stop()
        watcher.observer.join()
        http_service.kill()
