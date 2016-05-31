#!/usr/bin/env python3

import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

UNITEST_DIR = "tests/unit/" # ending with /
# This file for ending with '_test'

# nosetests --rednose --with-coverage --cover-erase --cover-package=opentsdb_importer.flush_data -v ./opentsdb_importer/tests/flush_data_test.py

def when_file_changed(filename):

    def projectname():
        """
            Projectname from name of current directory ('.')
            if there are dash '-' in its name replace to underscore '_'
        """
        return os.path.abspath(".").rsplit("/", 1)[1].replace("-", "_")

    def package(filename):
        basename = os.path.basename(filename)

        if not basename.endswith("_test.py"):
            package = filename.replace("./", "").replace(".py", "")
        else:
            package = filename.replace( UNITEST_DIR, "").replace(".py", "")
            package = package.replace("_test", "")

        package = package.replace("./", "").replace("/", ".")
        return package

    def test_file(filename):
        basename = os.path.basename(filename)
        if not basename.endswith("_test.py"):
            filename = filename.replace(basename, "")
            filename += UNITEST_DIR + basename.replace(".py","") + "_test.py"
        return filename

    cls()
    print(os.path.abspath(filename))
    args = {"package": package(filename), "testfile": test_file(filename)}
    cmd = "nosetests --rednose --with-coverage --cover-erase --cover-package={package}" \
          " -v {testfile}".format(**args)
    print(cmd)
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
