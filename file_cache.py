from datetime import timedelta, datetime
import os

class FileCache:

    def __init__(self, refresh_delay):
        self._cache = {}
        self._delay = refresh_delay

    def _load(self, filepath, binary):
        entry = None
        print("Info: Loading file " + filepath)
        with open(filepath, 'r' + binary) as stream:
            entry = (datetime.now(), os.stat(filepath).st_mtime, stream.read())
        return entry

    def _cache_file(self, filepath, binary):
        entry = self._load(filepath, binary)
        self._cache[filepath] = entry
        return entry

    def fetch(self, filepath):
        return self._fetch(filepath, '')

    def fetch_bytes(self, filepath):
        return self._fetch(filepath, 'b')

    def _fetch(self, filepath, binary):
        entry = self._pick_and_check(filepath)
        if entry is None:
            entry = self._cache_file(filepath, binary)
        if entry is None:
            raise Exception("Cannot load file: " + filepath)
        _, _, f = entry
        return f

    def _pick_and_check(self, filepath):
        entry = self._cache.get(filepath)
        if entry is None:
            return None
        time, last_modified, f = entry
        now = datetime.now()
        print(time + self._delay, now, time + self._delay >= now)
        if now - self._delay >= time:
            print("File expired " + filepath)
            if os.stat(filepath).st_mtime != last_modified:
                print("File changed " + filepath)
                del self._cache[filepath]
                return None
            self._cache[filepath] = (datetime.now(), last_modified, f)
        return entry
