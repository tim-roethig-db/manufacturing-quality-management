import random
from scipy.stats import binom

class RandomBinomialsIT(object):
    def __init__(self, seed=None):
        """
        constructor of the ranbin3 generator
        parameters:
        """
        self.seed = seed
        if self.seed != None:
            self.uniform = random.Random(seed)
        else:
            self.uniform = random.Random()

    def _singleNumber(self):
        # sample from a binomial distribution
        u = self.uniform.random()
        b = 0
        pr = binom.pmf(b, self.m, self.p)
        while(pr <= u):
            b = b+1
            u = u-pr
            pr = binom.pmf(b, self.m, self.p)
        return b

    def random(self, n, m, p):
        """
        n = sample size
        m = number of trials
        p = success probability
        """
        self.m = m
        self.p = p
        res = [self._singleNumber() for i in range(n)]

        return res


# ---- test
if __name__ == '__main__':
    ranbin3 = RandomBinomialsIT()
    #ranbin3.random(n=24, m=25, p=0.15, Debug=True)
    print(ranbin3.random(n=24, m=25, p=0.15))
