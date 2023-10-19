
class DispenserCriteria(object):
    '''Greedy algorithm to find minimum number of coins'''

    def __init__(self, **denominations):
        self._denominations = denominations
        self._coins = sorted([int(deno) for deno, handler in denominations.items()])

    def min_coin_ex(self, amount):
        '''Devise the minimum number of denominations'''
        n = len(self._coins)
        # Traverse through all denomination
        offset = n - 1
        while(offset >= 0):
            # Find denominations
            while (amount >= self._coins[offset]):
                amount -= self._coins[offset]
                self._denominations[str(self._coins[offset])]()
            offset -= 1
