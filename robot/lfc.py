import time

class FlowGateCycle(object):
    '''Perform the flow gate cycle'''

    __SENTINEL_INTERVAL_MS = 0.05

    def __init__(self, interval, open_handler, close_handler):
        if interval <= self.__SENTINEL_INTERVAL_MS:
            emsg = "Interval can not elapse less than {}".format(self.__SENTINEL_INTERVAL_MS)
            raise Exception(emsg)
        self._interval = interval
        self._open_handler, self._close_handler = open_handler, close_handler
        self._getoff = False

    def __enter__(self):
        self._open_handler()

    def __exit__(self, exc_type, exc_value, traceback):
        self._hold_on()
        self._close_handler()

    def _time_gap(self):
        t = time.time()
        return t, t + self._interval

    def _hold_on(self):
        tbegin, tend = self._time_gap()
        while not self._getoff:
            time.sleep(self.__SENTINEL_INTERVAL_MS)
            if time.time() >= tend:
                self._getoff = True
