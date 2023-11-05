
class DispenserCriteria(object):
    '''Greedy algorithm to find minimum number of coins'''

    __COIN_DENO, __COIN_HANDLER = range(2)

    def __init__(self, *denominations):
        self._denominations = dict([])
        self._coins = list([])
        for deno in denominations:
            if type(deno) is not tuple:
                raise Exception("The expectation is an array of tuples as denominations")
            self._coins.append(deno[self.__COIN_DENO])
            self._denominations[deno[self.__COIN_DENO]] = deno[self.__COIN_HANDLER]
        self._coins = sorted(self._coins)

    def __call__(self, amount):
        '''Devise the minimum number of denominations'''
        n = len(self._coins)
        # Traverse through all denomination
        offset = n - 1
        while(offset >= 0):
            # Find denominations
            while (amount >= self._coins[offset]):
                amount -= self._coins[offset]
                self._denominations[self._coins[offset]]()
            offset -= 1
