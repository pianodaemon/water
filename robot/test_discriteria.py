from unittest import TestCase
from .discriteria import DispenserCriteria

class TestDispenserCriteria(TestCase):

    _ONE_WOOLONG = 1
    _TWO_WOOLONG = 2
    _FIVE_WOOLONG = 5
    _TEN_WOOLONG = 10
    _TWENTY_WOOLONG = 20
    _FITHTY_WOOLONG = 50

    def test_two_deno(self):
        '''Test for an implementation featuring two coin hoppers'''
        exchange_collected = []
        # Each handler mocks an enabled coin hopper
        def one():
            exchange_collected.append(TestDispenserCriteria._ONE_WOOLONG)
        def two():
            exchange_collected.append(TestDispenserCriteria._TWO_WOOLONG)

        # The exchange's distribution that shall be received by the client
        exchange_expected = [
            TestDispenserCriteria._TWO_WOOLONG,
            TestDispenserCriteria._TWO_WOOLONG,
            TestDispenserCriteria._ONE_WOOLONG
        ]

        dispenser = DispenserCriteria(
            (TestDispenserCriteria._ONE_WOOLONG, one),
            (TestDispenserCriteria._TWO_WOOLONG, two))

        # It'll dispense 5 woolongs as exchange
        dispenser(sum(exchange_expected))
        self.assertTrue(exchange_expected == exchange_collected)

    def test_six_deno(self):
        '''Test for an implementation featuring six coin hoppers'''
        exchange_collected = []
        # Each handler mocks an enabled coin hopper
        def one():
            exchange_collected.append(TestDispenserCriteria._ONE_WOOLONG)
        def two():
            exchange_collected.append(TestDispenserCriteria._TWO_WOOLONG)
        def five():
            exchange_collected.append(TestDispenserCriteria._FIVE_WOOLONG)
        def ten():
            exchange_collected.append(TestDispenserCriteria._TEN_WOOLONG)
        def twenty():
            exchange_collected.append(TestDispenserCriteria._TWENTY_WOOLONG)
        def fithy():
            exchange_collected.append(TestDispenserCriteria._FITHTY_WOOLONG)

        # The exchange's distribution that shall be received by the client
        exchange_expected = [
                TestDispenserCriteria._FITHTY_WOOLONG,
                TestDispenserCriteria._TWENTY_WOOLONG,
                TestDispenserCriteria._TWENTY_WOOLONG,
                TestDispenserCriteria._TWO_WOOLONG,
                TestDispenserCriteria._ONE_WOOLONG
        ]

        dispenser = DispenserCriteria(
            (TestDispenserCriteria._ONE_WOOLONG, one),
            (TestDispenserCriteria._TWO_WOOLONG, two),
            (TestDispenserCriteria._FIVE_WOOLONG, five),
            (TestDispenserCriteria._TEN_WOOLONG, ten),
            (TestDispenserCriteria._TWENTY_WOOLONG, twenty),
            (TestDispenserCriteria._FITHTY_WOOLONG, fithy))

        # It'll dispense 93 woolongs as exchange
        dispenser(sum(exchange_expected))
        self.assertTrue(exchange_expected == exchange_collected)
