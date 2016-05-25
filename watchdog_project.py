#!/usr/bin/env python3

import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def when_file_changed(filename):
    cls()
    nose = "nosetests"
    options = "--rednose --with-coverage --cover-erase " \
        "--cover-package=opentsdb_importer opentsdb_importer".format(**locals())
    # -v verbose show a list of tests
    cmd = nose + " " + options
    os.system(cmd)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class ModifiedHandler(PatternMatchingEventHandler):
    patterns = ["*.py"]

    def on_created(self, event):
        when_file_changed(event.src_path)

    def on_any_event(self, event):
        pass

    def on_modified(self, event):
        when_file_changed(event.src_path)

if __name__ == '__main__':
    args = sys.argv[1:]
    event_handler = ModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler,
                      path=args[1] if args else '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
