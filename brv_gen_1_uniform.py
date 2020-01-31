import random

class RandomBinomials1U(object):

    def __init__(self, seed=None):
        self.seed = seed
        if self.seed != None:
            self.uniform = random.Random(seed)
        else:
            self.uniform = random.Random()

    def _singleNumber(self, x):
        # generate uniform
        u = self.uniform.random()
        X = [x for i in range(self.m)]
        for k in range(self.m):
            if u <= self.p:
                X[k] = 1
                u = u / self.p
            else:
                X[k] = 0
                u = (u - self.p) / (1.0 - self.p)
        return (sum(X))

    def random(self, n, m, p):
        """
        n = sample size
        m = number of trials
        p = success probability
        """
        self.m = m
        self.p = p
        res = [0 for i in range(n)]
        return list(map(self._singleNumber, res))


# ---- test
if __name__ == '__main__':
    ranbin3 = RandomBinomials1U()
    #ranbin3.random(n=24, m=25, p=0.15, Debug=True)
    print(ranbin3.random(n=24, m=25, p=0.15))
