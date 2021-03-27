#!/usr/bin/python

from __future__ import division
from collections import defaultdict
import sys
import itertools 

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np



class SelItem:
    def __init__(self, min, max):
        self.selmin = min
        self.selmax = max
        self.selnow = 0

    def next(self):
        n = self.selnow
        n = n + 1
        if n > self.selmax:
           n = self.selmin
        self.selnow = n
        return self.selnow
        

def factorial(N):
    """Factorial of N."""
    if N == 0: return 1.0
    r = 1.0
    # Perform the multiplications 1 * 2 * 3 * 4 * ... * N
    for i in range(2, N+1):
        r *= i
    return r

def C(n,r):
    """Number of ways to choose r out of n items."""
    nCr = 1
    # Because C(n,r) == C(n,n-r), and loop is over r, so we want r to be small
    if (r*2) > n:
        r = n-r
    for i in range(r-1, -1, -1): # r-1 ... 0
        nCr = (nCr*(n-i)) // (r-i)
    return nCr

def weighted_sum_of_multivariate_hypergeometric(w, f, n):
    """Construct the the sum-of-multivariate-hypergeometrics distribution
    @param w: Weights w=(w_1,w_2,...w_s) for observations in each
    component of the random variable X=(X_1,X_2,...,X_s).  The
    weighted sum random variable Y is the dot product Y = w*X.
    @param f: Population size of the components (f_1,f_2,...,f_s). The
    total population size is m=f_1+f_2+...+f_s
    @param n: Make n observations without replacement.
    @return: (values,mass) corresponding to the values and probability masses
    of the discrete distribution Y=d*X, being the weighted sum of X.
    """
    s = len(w)
    assert len(f) == s
    # m is the size of the population (f_1+f_2+...+f_s)
    m = sum(f)

    # Y[y] is P[Y=y], the probability of observing Y=y
    Y = defaultdict(float)

    # maxfree[i] is the maximum number of balls that can
    # be drawn in total from components >= i
    maxfree = list(f)
    for i in range(s-2, -1, -1): # s-2 ... 0
        maxfree[i] += maxfree[i+1]
    maxfree += [0]

    def enumerate_probabilities(i, free, y, g):
        """Recursively enumerate all of the possible outcomes.  Add each outcomes
	probability to its weighted sum.
        @param i: Component of population to enumerate.
	@param free: Observations (out of original n) remaining to be made.
	@param y: Weighted sum of the observations.
	@param g: Probability of the observed outcome.
        """
        if free == 0:
	    # Add the probability of this outcome to total probability of
	    # observing the weighted sum y
            Y[y] += g
        else:
            # Constraints should ensure that we use up all the observations in time.
            assert i < s
	    # k = number of balls drawn from this component
	    # free-maxfree[i+1] = minimum number of balls that could be drawn from this component.
	    # min(f[i],free) = maximum number of balls that could be drawn from this component.
	    # w[i]*k = weighted contribution of balls drawn from this component
	    # C(f[i],k) = number of ways to choose k balls from f[i] in the component.
            for k in range(max(0, free-maxfree[i+1]), min(f[i], free)+1):
                enumerate_probabilities(i+1, free-k, y+(w[i]*k), g*C(f[i],k))

    enumerate_probabilities(i=0, free=n, y=0, g=1)
    values = sorted(Y.keys())
    # Finish the probability using the shared C(m,n) denominator
    # http://www.math.uah.edu/stat/urn/MultiHypergeometric.xhtml
    mass = [Y[k]/C(m,n) for k in values]
    return (values, mass)


def discrete_pvalue(values, mass, t):
    """Calculate the p-value of a test value t in a discrete
    distribution.  That is, the sum of the probability mass that
    corresponds to values at least as extreme as t.
    @param values: Values of the discrete distribution.
    @param mass: Distribution mass associated with each value.
    @param t: Value to test for significance.
    """
    print("The discrete distribution is: ")
    for (v,d) in zip(values,mass):
    	print(v, d)
    print ("Sum of probability mass (should be 1.0): %f" % sum(mass))
    print ("Mean (expected value): %f" %
            sum(v*d for (v,d) in zip(values,mass)))
    print ("Calculating the p-value of %s" % str(t))
    '''
    try:
	i = values.index(t)
        pval_left = sum(mass[j] for j in range(0, i+1))
        pval_right = sum(mass[j] for j in range(i, len(values)))
        pval = min(pval_right, pval_left)
	print ("1-tailed p-value: ", pval)
    except ValueError, e:
    '''
	#print ("Test value %d is not one of the values in the distribution." % t)

def plot_density(values, mass):
    """For a discrete distribtion, plut probability mass on Y axis against
    values of the distribution on the X axis."""
    from matplotlib import pylab
    pylab.plot(values, mass)
    print ("Press any key to exit the program.")
    pylab.show()
    #raw_input()

def main(args):
    """Calculate p-values under the null hypothesis of a weighted sum
    of a multivariate hypergeometric random variable.
    """
    '''
    try:
	
    args = [int(v) for v in args[1:]]
	f = args[0:3]
	n = args[3]
	t = args[4]
    
    f = [1,2,3]
    n = 12
    t = 5
    except Exception:
	print __doc__
    # Weights for occurences in each component
    '''
    f = [1,2,3]
    n = 12
    t = 5
    w = [0.1, 0.5, 0.4]
    (values,mass) = weighted_sum_of_multivariate_hypergeometric(w, f, n)
    #discrete_pvalue(values, mass, t)
    plot_density(values, mass)

def getcombination(lsel, n):
    ltotal = []
    for i in range(0, len(lsel)):
        onelst = []
        for i in range(0, lsel[i] + 1):
            onelst.append(i)
        ltotal.append(onelst)

    res = list(itertools.product(*ltotal)) 
    #sum filter 
    lastres = []
    for comb in res:
        if sum(comb) == n:
            lastres.append(comb)

    return lastres

def sequenceproduct(w, lc, ls):
    res = 1.0
    for i in range(0, len(lc)):
       p =  C(lc[i], ls[i]) * pow(w[i],ls[i])
       res = res * p

    return res

def calcP0(w,lcount,lsel):
    prob = 0.0
    for item in lsel:        
        p = sequenceproduct(w,lcount, item)
        prob = prob + p

    return prob

def calcPk(w, n, k,lh,ld):

    prob = 0.0

    uhk = getcombination(lh, k)
    udk = getcombination(ld, n-k)

    for h in uhk:
        p = sequenceproduct(w,lh, h)
        for d in udk:
            p1 = p * sequenceproduct(w,ld, d)
            prob = prob + p1        

    return prob

def calcProb(w, n, total, hpercent):
    hcount = int(total * hpercent)
    dcount = total - hcount
    c = len(w)
    haverage = int(hcount / c)
    daverage = int(dcount / c)
    lH = []
    lD = []
    for i in range(0, c-1):
        lH.append(haverage)
        lD.append(daverage)

    lH.append(hcount - haverage*(c-1))
    lD.append(dcount - daverage*(c-1))

    lM = []
    for i in range(0, len(lH)):
        lM.append(lH[i] + lD[i])

    ltotal = getcombination(lM, n)
    P0 = calcP0(w,lM,ltotal)
    #print(0, P0)

    sumprob = 0.0

    for k in range(int(n/2) + 1, n+1):
        pk = calcPk(w, n, k, lH, lD)
        #print(k, pk)
        sumprob += pk

    prob =  sumprob / P0   

    return prob     

if __name__ == "__main__":
    #main(sys.argv)

    #Let’s c = 4, W= {0.1, 0.2, 0.3, 0.4}, H = { 3,4,5,6}, D = { 2,3,4,5}, M = {5, 7, 9, 11} N = 24, n=6, k=3  

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    lW = [0.1, 0.2, 0.3, 0.4]

    lx = []
    ly = []

    for total in range(5, 50):
        lx.append(total)
    for i in range(50, 100, 5):
        hpercent = float(i / 100)
        ly.append(hpercent)


    for total in lx:
        lprob = []
        for hpercent in ly:
            prob = calcProb(lW, 3, total, hpercent)
            lprob.append(prob)
        ax.scatter(total, ly, lprob, marker='o')

    ax.set_xlabel('X(# of total nodes)')
    ax.set_ylabel('Y(percent of honest nodes)')
    ax.set_zlabel('Z(Probability(K>n/2)')

    plt.show()    

 
   


