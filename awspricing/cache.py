import os
import json
import logging
import re
import time


_USE_CACHE = None
_CACHE_PATH = None
_CACHE_MINUTES = None
_WRITE_TO_CACHE = False

DEFAULT_USE_CACHE = '1'  # False
DEFAULT_CACHE_PATH = os.path.join('/tmp', 'awspricing')
DEFAULT_CACHE_MINUTES = '1440'  # 1 day


logger = logging.getLogger(__name__)

class Cache:

    def __init__(self, cache_key):
        self.cache_key = cache_key
        self._CACHE_PATH = None
        self._CACHE_MINUTES = None
        self._WRITE_TO_CACHE = False
        self._USE_CACHE = None
        self.use_cache()
        self.path = self._build_path()

    def use_cache(self):
        if self._USE_CACHE is None:
            setting = os.getenv('AWSPRICING_USE_CACHE', DEFAULT_USE_CACHE)
            if setting not in ['0', '1']:
                raise ValueError("Unknown value '{}' for AWSPRICING_USE_CACHE."
                                 .format(setting))
            self._USE_CACHE = bool(int(setting))
        return self._USE_CACHE


    def cache_path(self):
        if self._CACHE_PATH is None:
            setting = os.getenv('AWSPRICING_CACHE_PATH', DEFAULT_CACHE_PATH)
            if not os.path.isdir(setting):
                try:
                    os.makedirs(setting)
                except OSError:
                    logger.exception("Unable to create cache directory: %s",
                                     setting)
                    raise
            self._CACHE_PATH = setting
        return self._CACHE_PATH


    def cache_minutes(self):
        if self._CACHE_MINUTES is None:
            setting = os.getenv('AWSPRICING_CACHE_MINUTES', DEFAULT_CACHE_MINUTES)
            try:
                self._CACHE_MINUTES = int(setting)
            except ValueError:
                raise ValueError("Unknown value '{}' for AWSPRICING_CACHE_MINUTES. "
                                 "Expected an integer.".format(setting))
        return self._CACHE_MINUTES

    def _is_cache_expired(self):
        try:
            mod_time = os.path.getmtime(self.path)
        except (OSError, IOError):
            return True
        cache_lifetime_seconds = time.time() - mod_time
        result = cache_lifetime_seconds > self.cache_minutes() * 60
        return result


    def _build_path(self):
        if not re.match(r'^[A-Za-z0-9_\-\.]*$', self.cache_key):
            raise ValueError("Cache key '{}' contains invalid characters."
                             .format(self.cache_key))
        return os.path.join(self.cache_path(), self.cache_key)

    def maybe_read_from_cache(self):
        if not self.use_cache():
            return None

        if not os.path.exists(self.path):
            self._WRITE_TO_CACHE = True
            return None  # not in cache
        elif self._is_cache_expired():
            os.remove(self.path)
            self._WRITE_TO_CACHE = True
            return None
        with open(self.path) as f:
            return json.load(f)


    def maybe_write_to_cache(self, data):
        if not self.use_cache():
            return
        if not self._WRITE_TO_CACHE:
            return

        if self._is_cache_expired():
            with open(self.path, 'w') as f:
                f.write(json.dumps(data, indent=0))
