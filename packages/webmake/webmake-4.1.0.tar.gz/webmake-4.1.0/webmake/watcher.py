import itertools
import os
import signal
import time
import threading

from watchdog import events
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from . import compiler, settings
from .modules.utils import log


DEBOUNCE_DELAY = 0.3


class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, signal_exit):
        self.signal_exit = signal_exit
        self.timer = None

    def on_any_event(self, event):
        if (event.is_directory or event.src_path.endswith('.depscache') or
                event.event_type in (events.EVENT_TYPE_OPENED, events.EVENT_TYPE_CLOSED)):
            return

        if os.path.abspath(event.src_path) == os.path.abspath(settings.MAKEFILEPATH):
            log('Detected change to makefile {}, please restart the watcher.\n'.format(settings.MAKEFILEPATH))
            self.signal_exit()
            return

        what = 'directory' if event.is_directory else 'file'
        log('{} {} {}'.format(event.event_type.title(), what, event.src_path))

        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(DEBOUNCE_DELAY, self.on_timer)
        self.timer.start()

    def on_timer(self):
        compiler.compile_if_modified(settings.MAKEFILE, settings.MAKEFILEPATH, settings.RELEASE)
        log('')


def start_watching(polling_watcher_prefix=None):
    log('\nWatching for filesystem changes, Ctrl-C to exit...\n')
    settings.VERBOSE = True

    paths = itertools.chain.from_iterable(d['dependencies'] for d in settings.MAKEFILE)
    paths = set(os.path.abspath(os.path.dirname(p)) for p in paths)

    # import pprint
    # pprint.pprint(paths, indent=4)

    # Use the polling observer instead of inotify if poll was specified and
    # any dependency path prefix matches
    if polling_watcher_prefix and (
            polling_watcher_prefix == '*' or
            any(p for p in paths if p.startswith(polling_watcher_prefix))):
        observer = PollingObserver(timeout=3)
    else:
        observer = Observer()

    def signal_exit(sig=None, frame=None):
        log('Shutting down...')
        observer.stop()
        raise KeyboardInterrupt()

    for path in paths:
        observer.schedule(WatchdogEventHandler(signal_exit), path, recursive=False)
    observer.start()

    signal.signal(signal.SIGINT, signal_exit)
    signal.signal(signal.SIGTERM, signal_exit)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    observer.join()
