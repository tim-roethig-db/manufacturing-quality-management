import numpy as np

class RandomBinomialsNB(object):

    def __init__(self):
        pass

    def bernoulli_random(self):
        #generate bernoulli random variable
        return np.random.binomial(1, self.p)

    def _single_number(self):
        #add bernoulli random variables
        X = []
        for i in range(self.m):
            X.append(self.bernoulli_random())
        return sum(X)

    def random(self, n, m, p):
        """
        n = sample size
        m = number of trials
        p = success probability
        """
        self.m = m
        self.p = p
        rnum = []
        for i in range(n):
            rnum.append(self._single_number())
        return rnum

# test
if __name__ == '__main__':
    ranbin3 = RandomBinomialsNB()
    #ranbin3.random(n=24, m=25, p=0.15, Debug=True)
    print(ranbin3.random(n=24, m=25, p=0.15))