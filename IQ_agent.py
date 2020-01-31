#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MICS Computational Statistics
# RB November 2017
###########################################

class IncrementalQuantilesEstimator(object):
    """
    Testing the updating of a given cumulative probability density with
    a set of new observations.
    Input: OrderedDict with percentage keys and quantiles &
    the size of the set of past observations.
    """

    def __init__(self, state, t, Debug=False):
        from collections import OrderedDict
        self.state = state
        self.p = [x for x in state]
        q = [state[x] for x in state]
        q.sort()
        self.q = q
        cdf = OrderedDict()
        for p in state:
            cdf[state[p]] = p
        self.cdf = cdf
        self.np = len(self.p)
        self.t = t
        self.Debug = Debug
        if Debug:
            print('state =', self.state)
            print('cdf =', self.cdf)
            print('history =', self.t)

    def _interpolateQuantile(self, x, newq, newp):
        if self.Debug:
            print(x, newq, newp)
        np = len(newp)
        i = 0
        while i < np:
            if x < newp[i]:
                ix = i
                if self.Debug:
                    print(ix, newp[ix - 1], newq[ix - 1], newp[ix], newq[ix])
                    # nsq[0]
                diffq = newp[ix] - newp[ix - 1]
                if diffq > 0.0:
                    return newq[ix - 1] + (x - newp[ix - 1]) / diffq * (newq[ix] - newq[ix - 1])
                else:  # avoid dividing by 0
                    return newq[ix - 1]
                i = np
            elif x == newp[i]:
                ix = i
                if self.Debug:
                    print(ix, newp[ix], newq[ix])
                return newq[ix]
            else:  # x > newp[i]
                ix = i
                i += 1

    def update(self, newData):
        from collections import OrderedDict
        # get present state of the estimator
        s = self.state
        cdf = self.cdf
        p = self.p
        q = self.q
        t = self.t
        np = self.np
        oldfrq = [p[i] * t for i in range(np)]
        if self.Debug:
            print(q)
            print(p)
            print(oldfrq)
            print(t)
        # new observations
        nv = sorted(newData)
        nt = len(nv)
        if self.Debug:
            print(nv, nt)

        # Init results newq and newp
        # Init indexes: i in q & p & oldfrq, j in nv, ins = # insertions
        if nv[0] < q[0] or t == 0:
            newq = [nv[0]]
            ins = 1
            j = 1
            i = 0
        elif nv[0] > q[0]:
            newq = [q[0]]
            j = 0
            ins = 0
            i = 1
        else:
            newq = [q[0]]
            j = 1
            ins = 1
            i = 1

        newp = [0.0]

        # compute new cumulative densities
        while i < np:
            while j < nt and i < np:
                # print(i,j)
                if nv[j] > q[i]:
                    newq.append(q[i])
                    # ins += 0
                    newp.append(cdf[q[i]] + ins)
                    i += 1
                elif nv[j] < q[i]:
                    newq.append(nv[j])
                    # ins += 1
                    # interpolate cdf of nv[j]
                    cdfnv = cdf[q[i - 1]] + (nv[j] - q[i - 1]) / (q[i] - q[i - 1]) * cdf[q[i]] + ins
                    newp.append(cdfnv)
                    ins += 1
                    j += 1
                else:  # nv[j] = q[i]
                    newp[-1] += 1
                    ins += 1
                    j += 1
            if j == nt:
                if t > 0:
                    for ni in range(i, np):
                        newq.append(q[ni])
                        newp.append(cdf[q[ni]] + ins)
                        # ins += 0
                i = np
        for nj in range(j, nt):
            ins += 1
            if newq[-1] < nv[nj]:
                newq.append(nv[nj])
                newp.append(newp[-1] + 1)
            else:
                newp[-1] += 1
        if self.Debug:
            self.newp = newp
            self.newq = newq

        # renormalising frequencies
        if self.Debug:
            print('#inserts = %d' % ins)
        t += len(nv)
        for i in range(len(newq)):
            newp[i] /= newp[-1]
        if self.Debug:
            print('q \t x(q) \t t*q')
            for i in range(len(newq)):
                print('%.3f \t %.2f \t %.2f' % (newp[i], newq[i], newp[i] * t))
            print('t = %d' % t)

        # compute new state by interpolation
        ns = OrderedDict([(newp[0], newq[0])])
        if self.Debug:
            print('quantiles', p)
        np = len(p)
        for i in range(1, np):
            x = p[i]
            if self.Debug:
                print(x)
            ns[x] = self._interpolateQuantile(x, newq, newp)
            if self.Debug:
                print('new state p(i)', i, x, ns[x])

        # store new state
        state = ns
        self.state = state
        q = [state[x] for x in state]
        q.sort()
        self.q = q
        for p in state:
            cdf[state[p]] = p
        self.cdf = cdf
        self.t = t

    def random(self):
        p = self.p
        q = self.q
        u = random.random()
        return self._interpolateQuantile(u, q, p)


# ------- for testing purposes --------
if __name__ == "__main__":
    from collections import OrderedDict
    import random



    ## lecture example data series
    s = OrderedDict([(0.0, 0), (0.25, 25), (0.5, 50), (0.75, 75), (1.0, 100)])
    t = 0
    qest = IncrementalQuantilesEstimator(s, t, False)
    '''
    X = [21, 24, 24, 30, 30, 30, 30, 31, 31, 31, 31, 32,
         32, 33, 33, 34, 34, 34, 34, 34, 36, 36, 36, 36, 37,
         37, 38, 39, 40, 40, 41, 41, 41, 42, 42, 43, 43, 45,
         46, 46, 46, 47, 48, 50, 51, 51, 55, 56, 56, 62, 62]
    '''

    ##  debugging
    # s = OrderedDict([(0.0,0),(0.25,25),(0.5,50),(0.75,75),(1.0,100)])
    # t = 1000
    # qest = QuantilesEstimator(s,t,True)
    # X = [random.uniform(0,100) for i in range(1000)]

    ## simultaing a Gaussian data series
    # s = OrderedDict([(0.0,-2),(0.1,-1),(0.2,-0.9),(0.3,-0.5),(0.4,-0.1),                   (0.5,0.0 ),(0.6,0.1 ),(0.7,0.5 ),(0.8,0.8 ),(0.9,0.9 ),(1.0,2 )])
    # t = 100
    # qest = QuantilesEstimator(s,t,False)
    # X = [random.gauss(0,1) for i in range(1000)]

    qest.update(X)
    print(qest.state)
    print(qest.t)

    nSim = 10 ** 4
    fo = open('simulData.csv', 'w')
    fo.write('"X"\n')
    for s in range(nSim):
        fo.write('%.3f\n' % qest.random())
    fo.close






