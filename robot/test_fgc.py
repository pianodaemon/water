from unittest import TestCase
from .fgc import FlowGateCycle
import time
import multiprocessing as mp


class TestFlowGateCycle(TestCase):

    @staticmethod
    def _stop_process(q, delay):
        time.sleep(delay)
        q.put(None)

    def test_stop_cycle(self):
        '''The cycle is never interrupted'''
        stop_queue = mp.Queue(1)
        def og_callback():
            pass
        def cg_callback():
            pass

        # It will trigger stop in 3 seconds away
        proc = mp.Process(target=self._stop_process, args=(stop_queue, 3))
        proc.start()

        # During six seconds the liquid shall flow
        interval = 6
        gap = FlowGateCycle.sluice(stop_queue, interval, og_callback, cg_callback)
        # More than 2 seconds should have been left as time non-used
        self.assertTrue((interval - int(gap)) >= 2)

    def test_happy_path(self):
        '''The cycle is never interrupted'''
        stop_queue = mp.Queue(1)
        def og_callback():
            pass
        def cg_callback():
            pass

        # During three seconds the liquid shall flow
        interval = 3
        gap = FlowGateCycle.sluice(stop_queue, interval, og_callback, cg_callback)
        self.assertTrue((interval - int(gap)) == 0)
