from unittest import TestCase
from .lfc import LiquidFlowCycle
import time


class TestLiquidFlowCycle(TestCase):

    def test_happy_path(self):
        '''The cycle is never interrupted'''
        start_time, stop_time = 0, 0
        def open_handler():
            pass
        def close_handler():
            pass

        # During three seconds the liquid shall flow
        interval = 3
        with LiquidFlowCycle(interval, open_handler, close_handler) as rflow:
            start_time = time.time()
        stop_time = time.time()
        # It shall truncate decimal part
        gap = int(interval - (stop_time - start_time))
        self.assertTrue(gap == 0)
