import os
from threading import Timer
import time

# Need an object so we get a reference inside our thread when we pass-by-ref
# If this is just a boolean, we pass by value, so updating it does nothing
is_running = { "run": True }

###
# Watch a file. The callback must accept a single argument, which is
# the contents of the file once it's updated. 
###
def watch(filename_to_watch, callback):
    if (not os.path.isfile(filename_to_watch)):
        raise(Exception("{0} doesn't exist".format(filename_to_watch)))

    w = Watch(filename_to_watch, callback)
    t = Timer(1, check_and_notify, [w]) # trigger in 1s
    w.notify(w.get_modified_time()) # trigger immediately
    t.start()

def stop():
    is_running["run"] = False

def check_and_notify(watch):
    while(is_running["run"] == True):
        now = watch.get_modified_time()
        if watch.is_updated(now):
            watch.notify(now)
        time.sleep(1)

class Watch:
    def __init__(self, filename, callback):
        self.filename = filename
        self._callback = callback
        self._last_updated = None
    
    def get_modified_time(self):
        return os.path.getmtime(self.filename)

    def is_updated(self, now):
        return self._last_updated == None or self._last_updated != now

    def notify(self, now):
        self._last_updated = now
        if self._callback != None:
            with open(self.filename) as f:
                contents = f.read()
            self._callback(contents)
            print("{0} updated".format(self.filename, now))