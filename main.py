import numpy as np
from collections import OrderedDict
from collections import Counter
import matplotlib.pyplot as plt

from brv_gen_inverse_transformation import RandomBinomialsIT
from brv_gen_n_bernoulli import RandomBinomialsNB
from brv_gen_1_uniform import RandomBinomials1U
from IQ_agent import IncrementalQuantilesEstimator

n = 24
m = 25
p = 0.5

# inverse transformation
print('-----INVERSE TRANSFORMATION-----')
rng = RandomBinomialsIT()
print('---p =', p,'---')
ITB = rng.random(n, m, p)
print(ITB)
# plot results
count = Counter(ITB)
scount = {}
for key in sorted(count.keys()):
    scount[key] = count[key]
print(count)
print(scount)
x = list(scount.keys())
y = list(scount.values())
plt.plot(x, y, 'bo')
plt.vlines(x, 0, y, colors='b', lw=5, alpha=0.5)
plt.title('inversion method')
plt.xlabel('number of defectives')
plt.ylabel('occurrences')
plt.show()

# n bernoulli
print('-----N BERNOULLI-----')
rng = RandomBinomialsNB()
print('---p =', p,'---')
NBB = rng.random(n, m, p)
print(NBB)
# plot results
count = Counter(NBB)
scount = {}
for key in sorted(count.keys()):
    scount[key] = count[key]
print(count)
print(scount)
x = list(scount.keys())
y = list(scount.values())
plt.plot(x, y, 'bo')
plt.vlines(x, 0, y, colors='b', lw=5, alpha=0.5)
plt.title('n Bernoulli')
plt.xlabel('number of defectives')
plt.ylabel('occurrences')
plt.show()

# one uniform
print('-----ONE UNIFORM-----')
rng = RandomBinomials1U()
print('---p =', p,'---')
OUB = rng.random(n, m, p)
print(OUB)
# plot results
count = Counter(OUB)
scount = {}
for key in sorted(count.keys()):
    scount[key] = count[key]
print(count)
print(scount)
x = list(scount.keys())
y = list(scount.values())
plt.plot(x, y, 'bo')
plt.vlines(x, 0, y, colors='b', lw=5, alpha=0.5)
plt.title('one uniform')
plt.xlabel('number of defectives')
plt.ylabel('occurrences')
plt.show()

# reference
print('-----REFERENCE RANDOM NUMBERS-----')
print('---p =', p,'---')
RB = [np.random.binomial(m, p) for _ in range(n)]
print(RB)
# plot results
count = Counter(RB)
scount = {}
for key in sorted(count.keys()):
    scount[key] = count[key]
print(count)
print(scount)
x = list(scount.keys())
y = list(scount.values())
plt.plot(x, y, 'bo')
plt.vlines(x, 0, y, colors='b', lw=5, alpha=0.5)
plt.title('reference')
plt.xlabel('number of defectives')
plt.ylabel('occurrences')
plt.show()


# check implementation
# check if quantiles are the same for all generators for high number of samples
s = OrderedDict([(0.0, 0), (0.25, 25), (0.5, 50), (0.75, 75), (1.0, 100)])
t = 0

print('---check inverse transformation---')
IQagentIT = IncrementalQuantilesEstimator(s, t, False)
IQagentIT.update(ITB)
print(IQagentIT.state)
print(IQagentIT.t)

print('---check n bernoulli---')
IQagentNB = IncrementalQuantilesEstimator(s, t, False)
IQagentNB.update(NBB)
print(IQagentNB.state)
print(IQagentNB.t)


print('---check one uniform---')
IQagentON = IncrementalQuantilesEstimator(s, t, False)
IQagentON.update(OUB)
print(IQagentON.state)
print(IQagentON.t)

# used to compare other generators with a correct implementation
print('---check reference---')
IQagentR = IncrementalQuantilesEstimator(s, t, False)
IQagentR.update(RB)
print(IQagentR.state)
print(IQagentR.t)
