import time
import queue
import logging
import multiprocessing as mp


class FlowGateCycle(object):
    '''Perform the flow gate cycle'''

    __SENTINEL_INTERVAL = 0

    def __init__(self, stop_queue, interval, open_handler, close_handler):
        self._logger = logging.getLogger()
        if interval <= self.__SENTINEL_INTERVAL:
            emsg = "Interval can not be zero or elapse less than {}".format(self.__SENTINEL_INTERVAL)
            raise Exception(emsg)
        self._qstop = stop_queue
        self._interval = interval
        self._open_handler, self._close_handler = open_handler, close_handler

    def __enter__(self):
        self._open_handler()

    def __exit__(self, exc_type, exc_value, traceback):
        self._hold_on()
        self._close_handler()

    def _hold_on(self):
        try:
            msg = self._qstop.get(True, self._interval)
            if msg is None: # We send this as a sentinel to stop
                self._logger.info("It was summoned a stop")
            else:
                raise Exception("We can not summon a stop by passing any value")
        except queue.Empty:
            self._logger.info("Lapse to summon a stop is over")
        except:
            raise Exception("Perhaps the queue is closed")

    @classmethod
    def _cycle_process(cls, queue, interval, og_callback, cg_callback, delta):
        start_time = 0
        with cls(queue, interval, og_callback, cg_callback) as flow:
            start_time = time.time()
        delta.value = time.time() - start_time

    @classmethod
    def sluice(cls, stop_queue, interval, og_callback, cg_callback):
        delta = mp.Value('f', 0.0)
        proc = mp.Process(
                target=cls._cycle_process,
                args=(stop_queue, interval, og_callback, cg_callback, delta))
        proc.start()
        proc.join()
        return delta.value
