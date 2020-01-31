from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)
n, p = 25, 0.15
x = np.arange(binom.ppf(0, n, p), binom.ppf(1, n, p))
ax.plot(x, binom.pmf(x, n, p), 'bo', label='binom pmf')
ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)
ax.legend(loc='best', frameon=False)
plt.show()

